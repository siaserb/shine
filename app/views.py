from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from app.forms import TopicNameSearchForm, NewspaperTitleSearchForm, RedactorUsernameSearchForm, RedactorCreateForm, \
    RedactorUpdateForm
from app.models import Redactor, Newspaper, Topic


@login_required
def index(request):

    num_redactors = Redactor.objects.count()
    num_newspapers = Newspaper.objects.count()
    num_topics = Topic.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_redactors": num_redactors,
        "num_newspapers": num_newspapers,
        "num_topics": num_topics,
        "num_visits": num_visits + 1,
    }

    return render(request, "app/index.html", context=context)


class TopicListView(LoginRequiredMixin, ListView):
    model = Topic
    context_object_name = "topics"
    template_name = "app/topic_list.html"
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TopicListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TopicNameSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Topic.objects.all()
        form = TopicNameSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class TopicCreateView(LoginRequiredMixin, CreateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("app:topic-list")


class TopicUpdateView(LoginRequiredMixin, UpdateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("app:topic-list")


class TopicDeleteView(LoginRequiredMixin, DeleteView):
    model = Topic
    success_url = reverse_lazy("app:topic-list")


class NewspaperListView(LoginRequiredMixin, ListView):
    model = Newspaper
    context_object_name = "newspapers"
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewspaperListView, self).get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        context["search_form"] = NewspaperTitleSearchForm(initial={"title": title})
        return context

    def get_queryset(self):
        queryset = Newspaper.objects.prefetch_related("topics")
        form = NewspaperTitleSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(title__icontains=form.cleaned_data["title"])
        return queryset


class NewspaperCreateView(LoginRequiredMixin, CreateView):
    model = Newspaper
    fields = "__all__"
    success_url = reverse_lazy("app:newspaper-list")


class NewspaperDetailView(LoginRequiredMixin, DetailView):
    model = Newspaper
    queryset = Newspaper.objects.all()


class NewspaperUpdateView(LoginRequiredMixin, UpdateView):
    model = Newspaper
    fields = "__all__"
    success_url = reverse_lazy("app:newspaper-list")


class NewspaperDeleteView(LoginRequiredMixin, DeleteView):
    model = Newspaper
    success_url = reverse_lazy("app:newspaper-list")


class RedactorListView(ListView):
    model = Redactor
    context_object_name = "redactors"
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RedactorListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = RedactorUsernameSearchForm(initial={"username": username})
        return context

    def get_queryset(self):
        queryset = Redactor.objects.all()
        form = RedactorUsernameSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(usename__icontains=form.cleaned_data["username"])
        return queryset


class RedactorDetailView(DetailView):
    model = Redactor
    queryset = Redactor.objects.prefetch_related("newspapers__topics")


class RedactorCreateView(LoginRequiredMixin, CreateView):
    model = Redactor
    form_class = RedactorCreateForm
    success_url = reverse_lazy("app:redactor-list")


class RedactorUpdateView(LoginRequiredMixin, UpdateView):
    model = Redactor
    form_class = RedactorUpdateForm
    success_url = reverse_lazy("app:redactor-list")


class RedactorDeleteView(LoginRequiredMixin, DeleteView):
    model = Redactor
    success_url = reverse_lazy("app:redactor-list")


@login_required
def toggle_assign_to_newspaper(request, pk):
    redactor = Redactor.objects.get(id=request.user.id)
    if (
        Newspaper.objects.get(id=pk) in redactor.newspapers.all()
    ):
        redactor.newspapers.remove(pk)
    else:
        redactor.newspapers.add(pk)
    return HttpResponseRedirect(reverse_lazy("app:redactor-detail", args=[pk]))
