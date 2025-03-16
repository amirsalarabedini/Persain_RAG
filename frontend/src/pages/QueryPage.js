import React, { useState } from 'react';
import { 
  Typography, 
  Paper, 
  TextField, 
  Button, 
  CircularProgress, 
  Box,
  Card,
  CardContent,
  Divider,
  List,
  ListItem,
  ListItemText,
  Chip
} from '@mui/material';
import { Send as SendIcon } from '@mui/icons-material';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

const QueryPage = () => {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleQueryChange = (event) => {
    setQuery(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    
    if (!query.trim()) {
      setError('Please enter a query');
      return;
    }

    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const result = await axios.post('/api/query/', { query });
      setResponse(result.data);
      setLoading(false);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to process query');
      setLoading(false);
      console.error(err);
    }
  };

  return (
    <div>
      <Typography variant="h4" gutterBottom>
        Query
      </Typography>
      <Typography variant="subtitle1" paragraph>
        Ask questions about your documents using the RAG system.
      </Typography>

      <Paper elevation={2} sx={{ p: 3, mb: 4 }}>
        <form onSubmit={handleSubmit}>
          <TextField
            label="Enter your query"
            variant="outlined"
            fullWidth
            multiline
            rows={3}
            value={query}
            onChange={handleQueryChange}
            sx={{ mb: 2 }}
          />
          <Button 
            type="submit" 
            variant="contained" 
            endIcon={<SendIcon />}
            disabled={loading}
          >
            {loading ? <CircularProgress size={24} /> : 'Submit Query'}
          </Button>
        </form>
      </Paper>

      {error && (
        <Paper elevation={2} sx={{ p: 3, mb: 4, bgcolor: '#ffebee' }}>
          <Typography color="error">{error}</Typography>
        </Paper>
      )}

      {response && (
        <Box>
          <Card sx={{ mb: 4 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Response
              </Typography>
              <Box sx={{ p: 2, bgcolor: '#f5f5f5', borderRadius: 1 }}>
                <ReactMarkdown>{response.response}</ReactMarkdown>
              </Box>
            </CardContent>
          </Card>

          {response.sources && response.sources.length > 0 && (
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Sources
                </Typography>
                <List>
                  {response.sources.map((source, index) => (
                    <React.Fragment key={index}>
                      <ListItem alignItems="flex-start">
                        <ListItemText
                          primary={
                            <Box display="flex" alignItems="center">
                              <Chip 
                                label={`Source ${index + 1}`} 
                                size="small" 
                                color="primary" 
                                sx={{ mr: 1 }}
                              />
                              {source.metadata.source && (
                                <Typography variant="body2" color="textSecondary">
                                  {source.metadata.source.split('/').pop()}
                                </Typography>
                              )}
                            </Box>
                          }
                          secondary={
                            <Typography
                              variant="body2"
                              color="textPrimary"
                              component="span"
                              sx={{ 
                                display: 'inline',
                                whiteSpace: 'pre-wrap',
                                bgcolor: '#f8f9fa',
                                p: 1,
                                borderRadius: 1,
                                display: 'block',
                                mt: 1,
                                fontFamily: 'monospace'
                              }}
                            >
                              {source.content}
                            </Typography>
                          }
                        />
                      </ListItem>
                      {index < response.sources.length - 1 && <Divider />}
                    </React.Fragment>
                  ))}
                </List>
              </CardContent>
            </Card>
          )}
        </Box>
      )}
    </div>
  );
};

export default QueryPage;