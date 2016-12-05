"""Managers for ss_utils."""
from django.db import models
from ss_utils.models import FieldType, FilterOperator

class AbstractManager(models.Manager):
    """Abstract Manager class with support of filtering."""

    methods = {
        FilterOperator.EQUAL: {
            'method': 'filter',
            'lookup': 'iexact',
            'val_method': {
                FieldType.Number: 'get_num',
                FieldType.Date: 'get_date',
                FieldType.String: 'get_val'
                }
            },
        FilterOperator.NOT_EQUAL: {
            'method': 'exclude',
            'lookup': 'iexact',
            'val_method': {
                FieldType.Number: 'get_num',
                FieldType.Date: 'get_date',
                FieldType.String: 'get_val'
                }
            },
        FilterOperator.IN: {
            'method': 'filter',
            'lookup': 'in',
            'val_method': {
                FieldType.Number: 'get_num_vals'
                }
            },
        FilterOperator.NOT_IN: {
            'method': 'exclude',
            'lookup': 'in',
            'val_method': {
                FieldType.Number: 'get_num_vals'
                }
            },
        FilterOperator.CONTAIN: {
            'method': 'filter',
            'lookup': 'icontains',
            'val_method': {
                FieldType.String: 'get_val'
                }
            },
        FilterOperator.DOES_NOT_CONTAIN: {
            'method': 'exclude',
            'lookup': 'icontains',
            'val_method': {
                FieldType.String: 'get_val'
                }
            },
        FilterOperator.STARTS_WITH: {
            'method': 'filter',
            'lookup': 'istartswith',
            'val_method': {
                FieldType.String: 'get_val'
                }
            },
        FilterOperator.ENDS_WITH: {
            'method': 'filter',
            'lookup': 'iendswith',
            'val_method': {
                FieldType.String: 'get_val'
                }
            },
        FilterOperator.GREATER_THAN: {
            'method': 'filter',
            'lookup': 'gt',
            'val_method': {
                FieldType.String: 'get_val',
                FieldType.Date: 'get_date'
                }
            },
        FilterOperator.GREATER_THAN_EQUAL: {
            'method': 'filter',
            'lookup': 'gte',
            'val_method': {
                FieldType.String: 'get_val',
                FieldType.Date: 'get_date'
                }
            },
        FilterOperator.LESS_THAN: {
            'method': 'filter',
            'lookup': 'lt',
            'val_method': {
                FieldType.String: 'get_val',
                FieldType.Date: 'get_date'
                }
            },
        FilterOperator.LESS_THAN_EQUAL: {
            'method': 'filter',
            'lookup': 'lte',
            'val_method': {
                FieldType.String: 'get_val',
                FieldType.Date: 'get_date'
                }
            },
        FilterOperator.BETWEEN: {
            'method': 'filter',
            'lookup': 'range',
            'val_method': {
                FieldType.Number: 'get_num_vals',
                FieldType.Date: 'get_dates'
                }
            },
        FilterOperator.IS_EMPTY: {
            'method': 'filter',
            'lookup': 'isnull',
            'val_method': {
                FieldType.Number: 'get_is_empty',
                FieldType.Date: 'get_is_empty',
                FieldType.String: 'get_is_empty'
                }
            },
        FilterOperator.IS_NOT_EMPTY: {
            'method': 'filter',
            'lookup': 'isnull',
            'val_method': {
                FieldType.Number: 'get_is_not_empty',
                FieldType.Date: 'get_is_not_empty',
                FieldType.String: 'get_is_not_empty'
            }
        }
    }

    def __init__(self, filter_fields):
        super().__init__()
        self.filter_fields = filter_fields

    def get_search_queryset(self, filters, view="Default"):
        """Method to create queryset based on filters passed."""
        query_set = super().get_queryset()
        for filtr in filters:
            # check field is allowed to be filtered
            # TODO find how we can filter fields based on roles
            if filtr.field in self.filter_fields:
                # get field type
                field_type = self.filter_fields[filtr.field]
                # get operator related methods
                oper_method = AbstractManager.methods[filtr.operator]
                # check whether field type supports this operator
                if field_type not in oper_method['val_method']:
                    continue
                val_func = getattr(filtr, oper_method['val_method'][field_type])
                kwargs = {
                    '{0}__{1}'.format(filtr.field, oper_method['lookup']):val_func()
                }
                # get the query method filter(), exclude() base on operator type
                query_method = getattr(query_set, oper_method['method'])
                query_set = query_method(**kwargs)
        return query_set

    def get_count(self, filters):
        """Method to find count of rows based on filters"""
        query_set = self.get_search_queryset(filters)
        return query_set.count()
