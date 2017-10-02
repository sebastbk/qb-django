from functools import reduce
from django.db.models import Q
from django.shortcuts import reverse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.core.exceptions import ImproperlyConfigured
from django.db import transaction
from .shortcuts import get_object_or_none
from .models import Question, Difficulty
from .forms import QuestionForm, AnswersFormSet


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


class RawQueryMixin(object):
    """Mixin for retrieving the raw query string and returning it as a dictionary."""
    def get_raw_query_string(self):
        return self.request.META.get('QUERY_STRING', '')

    def get_raw_query_dict(self):
        raw_qs = self.get_raw_query_string()
        params = filter(None, raw_qs.split('&'))  # filter empty param list
        return {k: v for k, v in map(lambda x: x.split('='), params)}


class QuestionListView(RawQueryMixin, SearchView):
    model = Question
    template_name = 'questions/index.html'
    search_fields = ['category__name', 'text']

    def get_filter_difficulty(self):
        pk = self.request.GET.get('filter')
        return get_object_or_none(Difficulty, pk=pk)

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_difficulty = self.get_filter_difficulty()
        if filter_difficulty is not None:
            queryset = queryset.filter(difficulty=filter_difficulty)
        return queryset.select_related('difficulty', 'category').prefetch_related('answers')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'difficulties': Difficulty.objects.all(),
            'filter_difficulty': self.get_filter_difficulty(),
            'search_query': self.get_raw_query_dict().get('search_query', ''),
        })
        return context


class QuestionCreateView(CreateView):
    form_class = QuestionForm
    template_name = 'questions/create.html'

    def get_formset(self):
        args = [self.request.POST] if self.request.POST else []
        return AnswersFormSet(*args)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['answers'] = self.get_formset()
        return context

    def form_valid(self, form):
        answers = self.get_formset()
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
        if answers.is_valid():
            answers.instance = self.object
            answers.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('questions:list')
    