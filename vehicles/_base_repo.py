import typing

from django.core.paginator import Page, Paginator
from django.db import models
from django.db.models import Q, QuerySet

class BaseRepo():

    __model: models.Model
    _is_transaction: bool
    _prefetch_tables: typing.List[str]

    def __init__(self, model: models.Model):
        self.__model = model
        self._is_transaction = False
        self._prefetch_tables = []
    
    # Get Single
    def _get_single(self, q: Q, include_deleted = False, query_transform_fn: typing.Callable[[QuerySet], QuerySet] = None):
        query = self.build_query(include_deleted=include_deleted)
        if query_transform_fn is not None:
            query = query_transform_fn(query)
        try: return query.get(q)
        except self.__model.DoesNotExist: return None
    
    # Get Many
    def _get_many(self, q: Q, pagination: dict, query_transform_fn: typing.Callable[[QuerySet], QuerySet] = None) -> Page:
        query = self.build_query().filter(q)
        if query_transform_fn is not None:
            query = query_transform_fn(query)

        page = pagination['page']
        per_page = pagination['per_page']
        sort_by = pagination['sort_by']
        sort_direction = pagination['sort_direction']

        query = query.order_by(('-' if sort_direction == 'desc' else '') + sort_by)
        paginator = Paginator(query, per_page)
        page = paginator.get_page(page)
        return page

    # Build Query
    def build_query(self, include_deleted = False):
        query = self.__model.objects if not include_deleted else self.__model.all_objects

        # Select for update for transactions
        if self._is_transaction:
            query = query.select_for_update()

        # Prefetch Tables
        for table in self._prefetch_tables:
            query = query.prefetch_related(table)
        
        return query
        

