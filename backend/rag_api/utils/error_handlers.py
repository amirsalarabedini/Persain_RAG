import logging
from rest_framework import status
from rest_framework.exceptions import APIException as DRFAPIException
from rest_framework.views import exception_handler
from rest_framework.response import Response

# Configure logging
logger = logging.getLogger(__name__)

class APIException(DRFAPIException):
    """Custom API Exception with standardized format."""
    
    def __init__(self, detail=None, code=None, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.status_code = status_code
        super().__init__(detail, code)


def handle_exception(exc, context):
    """Custom exception handler for consistent API error responses."""
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # If response is None, it's an unhandled exception
    if response is None:
        logger.error(f"Unhandled exception: {str(exc)}")
        return Response(
            {"error": "An unexpected error occurred"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Format the response to have a standard structure
    if not isinstance(response.data, dict):
        response.data = {"error": response.data}
    elif "detail" in response.data:
        response.data = {"error": response.data["detail"]}
    
    return response 