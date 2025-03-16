import React, { useState, useEffect } from 'react';
import { Typography, Paper, Grid, Card, CardContent, CircularProgress } from '@mui/material';
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
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      <Typography variant="subtitle1" paragraph>
        Welcome to the RAG System Dashboard. Here you can see an overview of the system.
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                System Information
              </Typography>
              {systemInfo && (
                <>
                  <Typography variant="body1">
                    <strong>Document Count:</strong> {systemInfo.document_count}
                  </Typography>
                  <Typography variant="body1">
                    <strong>Collection Name:</strong> {systemInfo.collection_name}
                  </Typography>
                  <Typography variant="body1">
                    <strong>Persist Directory:</strong> {systemInfo.persist_directory}
                  </Typography>
                </>
              )}
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Configuration
              </Typography>
              {systemInfo && (
                <>
                  <Typography variant="body1">
                    <strong>Chunk Size:</strong> {systemInfo.chunk_size}
                  </Typography>
                  <Typography variant="body1">
                    <strong>Chunk Overlap:</strong> {systemInfo.chunk_overlap}
                  </Typography>
                  <Typography variant="body1">
                    <strong>Top K Results:</strong> {systemInfo.top_k_results}
                  </Typography>
                </>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </div>
  );
};

export default Dashboard;