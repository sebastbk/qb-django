from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class PageNumberPaginationWithPage(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'page': self.page.number,
            'results': data
        })