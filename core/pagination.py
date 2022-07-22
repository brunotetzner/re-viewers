from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page'
    max_page_size = 10
    page_size_query_param = 'data'