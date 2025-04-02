import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from ..services import DocumentService
from ..serializers import DocumentSerializer, DocumentUploadSerializer

# Configure logging
logger = logging.getLogger(__name__)

class DocumentListView(APIView):
    """API view for listing documents."""
    
    def get(self, request):
        """Get all documents."""
        try:
            documents = DocumentService.get_all_documents()
            serializer = DocumentSerializer(documents, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error fetching documents: {str(e)}")
            return Response(
                {"error": "Failed to fetch documents"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DocumentUploadView(APIView):
    """API view for uploading documents."""
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        """Upload and process a document."""
        serializer = DocumentUploadSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                # Get uploaded file and title
                uploaded_file = serializer.validated_data['file']
                title = serializer.validated_data['title']
                
                # Process and save document
                document = DocumentService.process_and_save_document(uploaded_file, title)
                
                return Response(
                    DocumentSerializer(document).data,
                    status=status.HTTP_201_CREATED
                )
                
            except Exception as e:
                logger.error(f"Error uploading document: {str(e)}")
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 