from functools import reduce
from django.db.models import Q
from django.views.generic.list import ListView
from django.core.exceptions import ImproperlyConfigured
from .models import Question


COMMON_WORDS = set(['to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'up', 'about', 'into', 'over', 'after', 'the', 'and', 'a', 'that', 'i', 'it', 'not', 'he', 'as', 'you', 'this', 'but', 'his', 'they', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their'])


class FilterView(ListView):
    search_fields = None

    def get_search_terms(self):
        query = self.request.GET.get('q', '')
        return [x.replace('_', ' ') for x in query.split() if x not in COMMON_WORDS] or None

    def get_queryset(self):
        if self.search_fields is None:
            raise ImproperlyConfigured(
                "No search fields provided. Please provide search fields.")
        queryset = super().get_queryset()
        search_terms = self.get_search_terms()
        if search_terms is not None:
            query_params = ('%(field_name)s__contains' % {'field_name': field} for field in self.search_fields)
            return queryset.filter(reduce(lambda x, y: x | y, 
                [Q(**{param: term}) for param in query_params for term in search_terms]))
        return queryset


class QuestionListView(FilterView):
    model = Question
    template_name = 'questions/index.html'
    search_fields = ['category__name', 'text']
