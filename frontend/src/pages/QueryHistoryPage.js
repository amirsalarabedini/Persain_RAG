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
  Chip
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
      <Typography variant="h4" gutterBottom>
        Query History
      </Typography>
      <Typography variant="subtitle1" paragraph>
        View the history of queries made to the RAG system.
      </Typography>

      {queryHistory.length === 0 ? (
        <Paper elevation={2} sx={{ p: 3, textAlign: 'center' }}>
          <Typography variant="body1">
            No query history found. Try making some queries first.
          </Typography>
        </Paper>
      ) : (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Query</TableCell>
                <TableCell>Timestamp</TableCell>
                <TableCell>Documents Retrieved</TableCell>
                <TableCell>Details</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {queryHistory.map((item) => (
                <TableRow key={item.id}>
                  <TableCell>{item.query_text.length > 50 ? `${item.query_text.substring(0, 50)}...` : item.query_text}</TableCell>
                  <TableCell>{new Date(item.timestamp).toLocaleString()}</TableCell>
                  <TableCell>
                    {item.documents_retrieved && item.documents_retrieved.length > 0 ? (
                      item.documents_retrieved.map((doc) => (
                        <Chip 
                          key={doc.id} 
                          label={doc.title} 
                          size="small" 
                          sx={{ mr: 0.5, mb: 0.5 }} 
                        />
                      ))
                    ) : (
                      <Typography variant="body2" color="textSecondary">None</Typography>
                    )}
                  </TableCell>
                  <TableCell>
                    <Accordion>
                      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                        <Typography>View Response</Typography>
                      </AccordionSummary>
                      <AccordionDetails>
                        <Card>
                          <CardContent>
                            <Typography variant="h6" gutterBottom>Response</Typography>
                            <Paper elevation={0} sx={{ p: 2, bgcolor: '#f5f5f5' }}>
                              <ReactMarkdown>{item.response_text}</ReactMarkdown>
                            </Paper>
                          </CardContent>
                        </Card>
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