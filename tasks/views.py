from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import TodoItem, Category

from django.views.decorators.cache import cache_page
from datetime import datetime
from django.http import HttpResponse


def index(request):
    from django.db.models import Count

    counts = Category.objects.annotate(total_tasks=Count(
        'todoitem')).order_by("-total_tasks")
    counts = {c.name: c.total_tasks for c in counts}

    high_priorities = TodoItem.objects.filter(priority='1').count()
    medium_priorities = TodoItem.objects.filter(priority='2').count()
    low_priorities = TodoItem.objects.filter(priority='3').count()

    return render(request, "tasks/index.html",
                  {"counts": counts,
                   "high_priorities": high_priorities,
                   "medium_priorities": medium_priorities,
                   "low_priorities": low_priorities,
                   })


def filter_tasks(tags_by_task):
    return set(sum(tags_by_task, []))


def tasks_by_cat(request, cat_slug=None):
    u = request.user
    tasks = TodoItem.objects.filter(owner=u).all()

    cat = None
    if cat_slug:
        cat = get_object_or_404(Category, slug=cat_slug)
        tasks = tasks.filter(category__in=[cat])

    categories = []
    for t in tasks:
        for cat in t.category.all():
            if cat not in categories:
                categories.append(cat)

    return render(
        request,
        "tasks/list_by_cat.html",
        {"category": cat, "tasks": tasks, "categories": categories},
    )


class TaskListView(ListView):
    model = TodoItem
    context_object_name = "tasks"
    template_name = "tasks/list.html"

    def get_queryset(self):
        u = self.request.user
        qs = super().get_queryset()
        return qs.filter(owner=u)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_tasks = self.get_queryset()
        tags = []
        for t in user_tasks:
            tags.append(list(t.category.all()))

            categories = []
            for cat in t.category.all():
                if cat not in categories:
                    categories.append(cat)
            context["categories"] = categories

        return context


class TaskDetailsView(DetailView):
    model = TodoItem
    template_name = "tasks/details.html"


@cache_page(60 * 5)
def dt_in_cache(request):
    dt = datetime.now()
    dt_cache = dt.strftime("%A, %d %B %Y, %H:%M:%S")
    return render(request, "c_date.html", context={"dt_cache": dt_cache})
    # return HttpResponse(dt_cache)
