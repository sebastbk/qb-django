from functools import reduce
from django.db.models import Q
from django.views.generic.list import ListView
from django.core.exceptions import ImproperlyConfigured
from .models import Question, Difficulty


COMMON_WORDS = set(['to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'up', 'about', 'into', 'over', 'after', 'the', 'and', 'a', 'that', 'i', 'it', 'not', 'he', 'as', 'you', 'this', 'but', 'his', 'they', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their'])


class SearchView(ListView):
    search_fields = None

    def get_search_terms(self):
        search_query = self.request.GET.get('search_query', '')
        return [x.replace('_', ' ') for x in search_query.split() if x not in COMMON_WORDS] or None

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


class QuestionListView(SearchView):
    model = Question
    template_name = 'questions/index.html'
    search_fields = ['category__name', 'text']

    def get_raw_params(self):
        raw_qs = self.request.META.get('QUERY_STRING', '')
        params = filter(None, raw_qs.split('&'))  # filter empty param list
        return {k: v for k, v in map(lambda x: x.split('='), params)}

    def get_filter_difficulty(self):
        pk = self.request.GET.get('filter')
        try:
            return Difficulty.objects.get(pk=pk)
        except Difficulty.DoesNotExist:
            return None

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_difficulty = self.get_filter_difficulty()
        if filter_difficulty is not None:
            queryset = queryset.filter(difficulty=filter_difficulty)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['difficulties'] = Difficulty.objects.all()
        context['filter_difficulty'] = self.get_filter_difficulty()
        context['search_query'] = self.get_raw_params().get('search_query', '')
        return context
