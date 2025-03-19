import React, { useState, useEffect } from 'react';
import { Typography, Paper, Grid, Card, CardContent, CircularProgress, Box } from '@mui/material';
import axios from 'axios';

const Dashboard = () => {
  const [systemInfo, setSystemInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSystemInfo = async () => {
      try {
        const response = await axios.get('/api/system/info/');
        setSystemInfo(response.data);
        setLoading(false);
      } catch (err) {
        setError('Failed to load system information');
        setLoading(false);
        console.error(err);
      }
    };

    fetchSystemInfo();
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
          Dashboard
        </Typography>
        <Typography variant="subtitle1" paragraph sx={{ opacity: 0.8 }}>
          Welcome to the RAG System Dashboard. Here you can see an overview of the system.
        </Typography>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card 
            elevation={0}
            sx={{ 
              height: '100%',
              border: '1px solid',
              borderColor: 'rgba(0, 0, 0, 0.06)',
              transition: 'all 0.2s ease',
              '&:hover': {
                boxShadow: '0px 4px 20px rgba(0, 0, 0, 0.05)',
                transform: 'translateY(-2px)'
              }
            }}
          >
            <CardContent sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom sx={{ fontSize: '1.1rem', color: 'primary.main', mb: 2 }}>
                System Information
              </Typography>
              {systemInfo && (
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <Typography variant="body2" sx={{ fontWeight: 500, minWidth: 140, color: 'text.secondary' }}>
                      Document Count
                    </Typography>
                    <Typography variant="body1" sx={{ fontWeight: 600 }}>
                      {systemInfo.document_count}
                    </Typography>
                  </Box>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <Typography variant="body2" sx={{ fontWeight: 500, minWidth: 140, color: 'text.secondary' }}>
                      Collection Name
                    </Typography>
                    <Typography variant="body1">
                      {systemInfo.collection_name}
                    </Typography>
                  </Box>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <Typography variant="body2" sx={{ fontWeight: 500, minWidth: 140, color: 'text.secondary' }}>
                      Vector Store
                    </Typography>
                    <Typography variant="body1">
                      {systemInfo.vector_store || 'Chroma'}
                    </Typography>
                  </Box>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </div>
  );
};

export default Dashboard;