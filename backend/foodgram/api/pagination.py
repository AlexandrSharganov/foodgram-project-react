from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """Параметр пагинации при запросе."""

    page_size_query_param = 'limit'
