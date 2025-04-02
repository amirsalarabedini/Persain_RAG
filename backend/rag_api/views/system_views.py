import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..services import SystemService

# Configure logging
logger = logging.getLogger(__name__)

class SystemInfoView(APIView):
    """API view for retrieving system information."""
    
    def get(self, request):
        """Get RAG system information."""
        try:
            system_info = SystemService.get_system_info()
            return Response(system_info)
        except Exception as e:
            logger.error(f"Error fetching system info: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 