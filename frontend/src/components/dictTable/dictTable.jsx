import React, { useState, useEffect } from 'react';
import DataTable from 'react-data-table-component';

async function fetchData(setTableData, setIsLoading, setError) {
  try {
    const response = await fetch('http://127.0.0.1:5000/get_json');
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json();
    setTableData(data);
  } catch (error) {
    console.error(error);
    setError(error);
  } finally {
    setIsLoading(false);
  }
}

function DictTable({ data: initialData, file }) {
  const [tableData, setTableData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData(setTableData, setIsLoading, setError);
  }, []);

  const data = tableData.length > 0 ? tableData : initialData;
  const headers = tableData.length > 0 ? Object.keys(tableData[0]) : [];
  const columns = headers.map((header) => ({
    name: header,
    selector: header,
    sortable: true,
  }));

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  return (
    <>
      <div className="table-name" style={{
        background: "white",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}>
        <b>{file.name}</b>
      </div>
      <DataTable
        title="Data Table"
        columns={columns}
        data={data}
        pagination
        highlightOnHover
        responsive
        noHeader
      />
    </>
  );
}

export default DictTable;
