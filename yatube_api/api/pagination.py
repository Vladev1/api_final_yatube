from rest_framework.pagination import LimitOffsetPagination


class PostPagination(LimitOffsetPagination):
    """Поведение деления страниц."""
    page_size = 20
