import React, { useState, useEffect } from 'react';
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
  Chip,
  Alert
} from '@mui/material';
import { Send as SendIcon } from '@mui/icons-material';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

const QueryPage = () => {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState(null);
  const [sources, setSources] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingSources, setLoadingSources] = useState(false);
  const [loadingResponse, setLoadingResponse] = useState(false);
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
    setSources(null);
    setLoadingSources(true);
    setLoadingResponse(true);

    try {
      // First, get sources immediately
      const sourcesResult = await axios.post('/api/query/sources/', { query });
      setSources(sourcesResult.data);
      setLoadingSources(false);
      
      // Then, get the full response with Gemini's answer
      const fullResult = await axios.post('/api/query/', { query });
      setResponse(fullResult.data);
      setLoadingResponse(false);
      setLoading(false);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to process query');
      setLoadingSources(false);
      setLoadingResponse(false);
      setLoading(false);
      console.error(err);
    }
  };

  return (
    <div>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom fontWeight="600">
          Query
        </Typography>
        <Typography variant="subtitle1" paragraph sx={{ opacity: 0.8 }}>
          Ask questions about your documents using the RAG system.
        </Typography>
      </Box>

      <Paper 
        elevation={0} 
        sx={{ 
          p: { xs: 2, sm: 3 }, 
          mb: 4, 
          border: '1px solid',
          borderColor: 'rgba(0, 0, 0, 0.06)',
          borderRadius: 3,
          transition: 'all 0.2s ease',
          '&:hover': {
            boxShadow: '0px 4px 20px rgba(0, 0, 0, 0.05)'
          }
        }}
      >
        <form onSubmit={handleSubmit}>
          <TextField
            label="Enter your query"
            variant="outlined"
            fullWidth
            multiline
            rows={3}
            value={query}
            onChange={handleQueryChange}
            sx={{ 
              mb: 2,
              '& .MuiOutlinedInput-root': {
                borderRadius: 2,
                '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                  borderColor: theme => theme.palette.primary.main,
                  borderWidth: '1px'
                }
              }
            }}
          />
          <Button 
            type="submit" 
            variant="contained" 
            endIcon={loading ? null : <SendIcon />}
            disabled={loading}
            sx={{ 
              borderRadius: 2,
              fontWeight: 500,
              py: 1
            }}
          >
            Submit Query
          </Button>
        </form>
      </Paper>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>
      )}

      {(loadingResponse || response) && (
        <Paper 
          elevation={0} 
          sx={{ 
            p: { xs: 2, sm: 3 }, 
            mb: 4, 
            border: '1px solid',
            borderColor: 'rgba(0, 0, 0, 0.06)',
            borderRadius: 3
          }}
        >
          <Typography variant="h6" gutterBottom>
            Response
          </Typography>
          {loadingResponse ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
              <CircularProgress />
            </Box>
          ) : (
            <Box sx={{ mt: 2 }}>
              <ReactMarkdown>{response?.answer || ''}</ReactMarkdown>
            </Box>
          )}
        </Paper>
      )}

      {(loadingSources || sources) && (
        <Paper 
          elevation={0} 
          sx={{ 
            p: { xs: 2, sm: 3 }, 
            border: '1px solid',
            borderColor: 'rgba(0, 0, 0, 0.06)',
            borderRadius: 3
          }}
        >
          <Typography variant="h6" gutterBottom>
            Sources
          </Typography>
          {loadingSources ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
              <CircularProgress />
            </Box>
          ) : (
            <List>
              {sources?.map((source, index) => (
                <ListItem key={index} sx={{ px: 0, py: 2, borderBottom: '1px solid', borderColor: 'rgba(0, 0, 0, 0.06)' }}>
                  <ListItemText
                    primary={
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                        <Typography variant="subtitle1" sx={{ fontWeight: 500 }}>
                          {source.document_title || 'Document'}
                        </Typography>
                        <Chip 
                          label={`Score: ${Math.round(source.score * 100) / 100}`} 
                          size="small" 
                          sx={{ ml: 2 }}
                        />
                      </Box>
                    }
                    secondary={source.content}
                  />
                </ListItem>
              ))}
            </List>
          )}
        </Paper>
      )}
    </div>
  );
};

export default QueryPage;