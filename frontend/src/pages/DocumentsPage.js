import React, { useState, useEffect } from 'react';
import { 
  Typography, 
  Paper, 
  Button, 
  Table, 
  TableBody, 
  TableCell, 
  TableContainer, 
  TableHead, 
  TableRow,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  TextField,
  CircularProgress,
  Alert
} from '@mui/material';
import { CloudUpload as UploadIcon } from '@mui/icons-material';
import axios from 'axios';

const DocumentsPage = () => {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [uploadOpen, setUploadOpen] = useState(false);
  const [title, setTitle] = useState('');
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState(null);
  const [uploadSuccess, setUploadSuccess] = useState(false);

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      const response = await axios.get('/api/documents/');
      setDocuments(response.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to load documents');
      setLoading(false);
      console.error(err);
    }
  };

  const handleUploadOpen = () => {
    setUploadOpen(true);
    setTitle('');
    setFile(null);
    setUploadError(null);
    setUploadSuccess(false);
  };

  const handleUploadClose = () => {
    setUploadOpen(false);
    if (uploadSuccess) {
      fetchDocuments();
    }
  };

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleTitleChange = (event) => {
    setTitle(event.target.value);
  };

  const handleUpload = async () => {
    if (!file || !title) {
      setUploadError('Please provide both a title and a file');
      return;
    }

    setUploading(true);
    setUploadError(null);

    const formData = new FormData();
    formData.append('title', title);
    formData.append('file', file);

    try {
      await axios.post('/api/documents/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setUploadSuccess(true);
      setUploading(false);
    } catch (err) {
      setUploadError(err.response?.data?.error || 'Failed to upload document');
      setUploading(false);
      console.error(err);
    }
  };

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
        Documents
      </Typography>
      <Typography variant="subtitle1" paragraph>
        Manage your documents for the RAG system.
      </Typography>

      <Button 
        variant="contained" 
        startIcon={<UploadIcon />} 
        onClick={handleUploadOpen}
        sx={{ mb: 3 }}
      >
        Upload Document
      </Button>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Title</TableCell>
              <TableCell>File Name</TableCell>
              <TableCell>File Type</TableCell>
              <TableCell>Upload Date</TableCell>
              <TableCell>Chunk Count</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {documents.length === 0 ? (
              <TableRow>
                <TableCell colSpan={5} align="center">
                  No documents found. Upload a document to get started.
                </TableCell>
              </TableRow>
            ) : (
              documents.map((doc) => (
                <TableRow key={doc.id}>
                  <TableCell>{doc.title}</TableCell>
                  <TableCell>{doc.file_name}</TableCell>
                  <TableCell>{doc.file_type}</TableCell>
                  <TableCell>{new Date(doc.upload_date).toLocaleString()}</TableCell>
                  <TableCell>{doc.chunk_count}</TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Upload Dialog */}
      <Dialog open={uploadOpen} onClose={handleUploadClose}>
        <DialogTitle>Upload Document</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Upload a document to be processed by the RAG system. Supported formats include PDF, DOCX, and TXT.
          </DialogContentText>
          <TextField
            autoFocus
            margin="dense"
            id="title"
            label="Document Title"
            type="text"
            fullWidth
            variant="outlined"
            value={title}
            onChange={handleTitleChange}
            sx={{ mb: 2 }}
          />
          <input
            accept=".pdf,.docx,.txt"
            style={{ display: 'none' }}
            id="raised-button-file"
            type="file"
            onChange={handleFileChange}
          />
          <label htmlFor="raised-button-file">
            <Button variant="outlined" component="span" fullWidth>
              {file ? file.name : 'Select File'}
            </Button>
          </label>
          {uploadError && (
            <Alert severity="error" sx={{ mt: 2 }}>
              {uploadError}
            </Alert>
          )}
          {uploadSuccess && (
            <Alert severity="success" sx={{ mt: 2 }}>
              Document uploaded successfully!
            </Alert>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleUploadClose}>Cancel</Button>
          <Button 
            onClick={handleUpload} 
            variant="contained" 
            disabled={uploading}
          >
            {uploading ? <CircularProgress size={24} /> : 'Upload'}
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
};

export default DocumentsPage;