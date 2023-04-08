from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader
from llama_index.output_parsers import GuardrailsOutputParser
from llama_index.llm_predictor import StructuredLLMPredictor
from llama_index.prompts.prompts import QuestionAnswerPrompt, RefinePrompt
from llama_index.prompts.default_prompts import DEFAULT_TEXT_QA_PROMPT_TMPL, DEFAULT_REFINE_PROMPT_TMPL
import json
import dotenv


# take environment variable from .env
try:
    dotenv.load_dotenv()
except Exception as e:
    print(f"Error loading the .env file: {e}")

def create_llm_predictor():
    return StructuredLLMPredictor()

def load_documents(input_dir='./output_files'):
    return SimpleDirectoryReader(input_dir=input_dir).load_data()

def create_index(documents):
    return GPTSimpleVectorIndex.from_documents(documents)

def create_output_parser(rail_spec, llm):
    return GuardrailsOutputParser.from_rail_string(rail_spec, llm=llm)

def create_qa_prompt(fmt_qa_tmpl, output_parser):
    return QuestionAnswerPrompt(fmt_qa_tmpl, output_parser=output_parser)

def create_refine_prompt(fmt_refine_tmpl, output_parser):
    return RefinePrompt(fmt_refine_tmpl, output_parser=output_parser)

def llm_index_generator(prompt="What are the values in column 'Pay Scale Area'?", llm_predictor=None, documents=None, index=None):
    if not llm_predictor:
        llm_predictor = create_llm_predictor()
    if not documents:
        documents = load_documents()
    if not index:
        index = create_index(documents)

    rail_spec = ("""
    <rail version="0.1">
    <output>
        <string name="step_names" format="list" on-fail-list="reask" description="the values in column 'Pay Scale Area'" />
    </output>
    <prompt>
        Return your response as a string.

        @xml_prefix_prompt

        {output_schema}

        @json_suffix_prompt_v2_wo_none
    </prompt>
    </rail>
    """)

    output_parser = create_output_parser(rail_spec, llm_predictor.llm)

    fmt_qa_tmpl = output_parser.format(DEFAULT_TEXT_QA_PROMPT_TMPL)
    fmt_refine_tmpl = output_parser.format(DEFAULT_REFINE_PROMPT_TMPL)

    qa_prompt = create_qa_prompt(fmt_qa_tmpl, output_parser)
    refine_prompt = create_refine_prompt(fmt_refine_tmpl, output_parser)

    response = index.query(
        prompt,
        text_qa_template=qa_prompt,
        refine_template=refine_prompt,
    )

    print(response.response)

    return json.loads(response.response)['step_names']


def llm_json_generator(prompt="What is the salary schedule in this document?", llm_predictor=None, documents=None, index=None):
    if not llm_predictor:
        llm_predictor = create_llm_predictor()
    if not documents:
        documents = load_documents()
    if not index:
        index = create_index(documents)

    print(documents)

    output_list = []

    rail_spec = ("""
    <rail version="0.1">
    <output>
        <object name="salary_schedule" description="salary schedule for pay scale area {area}" >
            <string name="pay_scale_area" format="max-len: 1" on-fail-max-len="reask" description="pay scale area {area} returned as float" />
            <float name="base_salary"  format="float" on-fail-float="reask" description="base salary for Pay Scale Area {area} returned as float" />
            <float name="qtea_addon" format="float" on-fail-float="reask" description="qtea add-on for Pay Scale Area {area} returned as
            float" />
            <float name="fwea_addon" format="float" on-fail-float="reask" description="fwea add-on for Pay Scale Area {area} returned as float" />
            <float name="total_annual_salary" format="float" on-fail-float="reask" description="total annual salary for Pay Scale Area {area} returned as float" />
            <float name="per_diem" format="float" on-fail-float="reask" description="per diem for Pay Scale Area {area} returned as float" />
        </object>
    </output>
    <prompt>
        Return all numbers in your response in the Float format. Remove the commas from the numeric values since commas are not allowed in JSON numbers.
        @xml_prefix_prompt

        {output_schema}

        @json_suffix_prompt_v2_wo_none
    </prompt>
    </rail>
    """)

    step_names = llm_index_generator(llm_predictor=llm_predictor, documents=documents, index=index)

    for area in step_names:
        formatted_spec = rail_spec.format(area=area, output_schema="{output_schema}")
        output_parser = create_output_parser(formatted_spec, llm_predictor.llm)

        fmt_qa_tmpl = output_parser.format(DEFAULT_TEXT_QA_PROMPT_TMPL)
        fmt_refine_tmpl = output_parser.format(DEFAULT_REFINE_PROMPT_TMPL)

        qa_prompt = create_qa_prompt(fmt_qa_tmpl, output_parser)
        refine_prompt = create_refine_prompt(fmt_refine_tmpl, output_parser)

        response = index.query(
            prompt,
            text_qa_template=qa_prompt,
            refine_template=refine_prompt,
        )

        try:
            output_list.append(
                json.loads(response.response)['salary_schedule']
            )

        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")
            output_list.append(response.response)
    
    
    return output_list
