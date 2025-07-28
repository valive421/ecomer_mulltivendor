from rest_framework import pagination
from rest_framework.response import Response

# Custom pagination class for API responses
class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        # Returns paginated response with links and count
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'data': data
        })