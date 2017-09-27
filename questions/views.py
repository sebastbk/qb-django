from functools import reduce
from django.db.models import Q
from django.core.exceptions import ImproperlyConfigured
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.list import BaseListView
from .models import Question
from .forms import QuestionFilterForm


class FilteredFormMixin(object):
    form_class = None
    form = None

    def get_form_class(self):
        """
        Returns the form class to use in this view
        """
        return self.form_class

    def get_form(self, form_class=None):
        """
        Returns an instance of the form to be used in this view.
        """
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = {}

        if self.request.method in ('GET'):
            kwargs.update({
                'data': self.request.GET,
            })
        return kwargs

    def get_context_data(self, **kwargs):
        """
        Insert the form into the context dict.
        """
        if self.form is not None and 'form' not in kwargs:
            kwargs['form'] = self.form
        return super(FilteredFormMixin, self).get_context_data(**kwargs)


class FilteredListView(FilteredFormMixin, TemplateResponseMixin, BaseListView):
    search_terms = None
    search_fields = None

    def get_search_terms(self):
        return self.search_terms

    def get_queryset(self):
        if self.search_fields is None:
            raise ImproperlyConfigured(
                "No search fields provided. Please provide search fields.")
        queryset = super(FilteredListView, self).get_queryset()
        search_terms = self.get_search_terms()
        if search_terms is not None:
            query_params = ['%(field_name)s__contains' % {'field_name': field} for field in self.search_fields]
            return queryset.filter(reduce(lambda x, y: x | y, 
                [Q(**{param: term}) for param in query_params for term in search_terms]))
        return queryset

    def get(self, request, *args, **kwargs):
        self.form = self.get_form()
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = len(self.object_list) == 0
            if is_empty:
                raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.") % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data()
        return self.render_to_response(context)


COMMON_WORDS = set(['to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'up', 'about', 'into', 'over', 'after', 'the', 'and', 'a', 'that', 'i', 'it', 'not', 'he', 'as', 'you', 'this', 'but', 'his', 'they', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their'])

class QuestionListView(FilteredListView):
    model = Question
    template_name = 'questions/index.html'
    form_class = QuestionFilterForm
    search_fields = ['text', 'category__name']

    def get_search_terms(self):
        if self.form.is_valid():
            search_terms = self.form.cleaned_data.get('q', None)
            if search_terms is not None:
                return [x for x in search_terms.lower().split() if x not in COMMON_WORDS]
        return None
