import FileUpload from '../components/fileUpload/fileUpload';
import CssBaseline from '@mui/material/CssBaseline';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import { createTheme, ThemeProvider } from '@mui/material/styles';

const theme = createTheme();

function Home() {

    return (
        <ThemeProvider theme={theme}>
            <Grid container component="main" sx={{ height: '100vh', width: '100vw', position: 'relative' }}>
                <CssBaseline />
                <Grid
                    item
                    md={12}
                    sx={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    width: '100%',
                    height: '100%',
                    backgroundImage: 'url(https://images.unsplash.com/photo-1615716175455-9a098e2388be?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80)',
                    backgroundRepeat: 'no-repeat',
                    backgroundColor: (t) =>
                        t.palette.mode === 'light' ? t.palette.grey[50] : t.palette.grey[900],
                    backgroundSize: 'cover',
                    backgroundPosition: 'center',
                    }}
                />
                <Grid item xs={12} sm={8} md={5} component={Paper} elevation={6} square sx={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', justifyContent: 'center', alignItems: 'center' }}>
                    <Box
                        sx={{
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center',
                        }}
                    >
                        <FileUpload />
                    </Box>
                </Grid>
            </Grid>
        </ThemeProvider>
    );
}

export default Home;
