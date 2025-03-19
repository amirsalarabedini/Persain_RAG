import React, { useState, useEffect } from 'react';
import { 
  Typography, 
  Paper, 
  Table, 
  TableBody, 
  TableCell, 
  TableContainer, 
  TableHead, 
  TableRow,
  CircularProgress,
  Card,
  CardContent,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Chip,
  Box
} from '@mui/material';
import { ExpandMore as ExpandMoreIcon } from '@mui/icons-material';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

const QueryHistoryPage = () => {
  const [queryHistory, setQueryHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchQueryHistory = async () => {
      try {
        const response = await axios.get('/api/query/history/');
        setQueryHistory(response.data);
        setLoading(false);
      } catch (err) {
        setError('Failed to load query history');
        setLoading(false);
        console.error(err);
      }
    };

    fetchQueryHistory();
  }, []);

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', marginTop: '2rem' }}>
        <CircularProgress />
      </div>
    );
  }

  if (error) {
    return (
      <Paper elevation={2} sx={{ p: 3, mt: 2 }}>
        <Typography color="error">{error}</Typography>
      </Paper>
    );
  }

  return (
    <div>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom fontWeight="600">
          Query History
        </Typography>
        <Typography variant="subtitle1" paragraph sx={{ opacity: 0.8 }}>
          View the history of queries made to the RAG system.
        </Typography>
      </Box>

      {queryHistory.length === 0 ? (
        <Paper 
          elevation={0} 
          sx={{ 
            p: 4, 
            textAlign: 'center',
            border: '1px solid',
            borderColor: 'rgba(0, 0, 0, 0.06)',
            borderRadius: 3
          }}
        >
          <Typography variant="body1" color="text.secondary">
            No query history found. Try making some queries first.
          </Typography>
        </Paper>
      ) : (
        <TableContainer 
          component={Paper}
          elevation={0}
          sx={{ 
            border: '1px solid',
            borderColor: 'rgba(0, 0, 0, 0.06)',
            borderRadius: 3,
            overflow: 'hidden'
          }}
        >
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Query</TableCell>
                <TableCell>Timestamp</TableCell>
                <TableCell>Response</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {queryHistory.map((item) => (
                <TableRow key={item.id}>
                  <TableCell>{item.query}</TableCell>
                  <TableCell>{new Date(item.timestamp).toLocaleString()}</TableCell>
                  <TableCell>
                    <Accordion>
                      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                        <Typography>View Response</Typography>
                      </AccordionSummary>
                      <AccordionDetails>
                        <ReactMarkdown>{item.response}</ReactMarkdown>
                      </AccordionDetails>
                    </Accordion>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </div>
  );
};

export default QueryHistoryPage;