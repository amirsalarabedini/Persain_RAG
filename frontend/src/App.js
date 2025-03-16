import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

// Components
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import DocumentsPage from './pages/DocumentsPage';
import QueryPage from './pages/QueryPage';
import QueryHistoryPage from './pages/QueryHistoryPage';

// Create a theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/documents" element={<DocumentsPage />} />
          <Route path="/query" element={<QueryPage />} />
          <Route path="/history" element={<QueryHistoryPage />} />
        </Routes>
      </Layout>
    </ThemeProvider>
  );
}

export default App;