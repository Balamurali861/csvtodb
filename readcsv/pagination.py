from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10


class CustomPagination(PageNumberPagination):
    page = DEFAULT_PAGE
    page_size = None
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'page': int(self.request.GET.get('page', DEFAULT_PAGE)),
            'page_size': int(self.request.GET.get('page_size', self.page_size)),
            'results': data
        })

