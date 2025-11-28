from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import TodoForm
from .models import Todo


def todo_list(request):
    todos = Todo.objects.all()
    return render(request, "home.html", {"todos": todos})


@require_http_methods(["GET", "POST"])
def todo_create(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tasks:list")
    else:
        form = TodoForm()
    return render(request, "todo_form.html", {"form": form, "action": "Create"})


@require_http_methods(["GET", "POST"])
def todo_update(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect("tasks:list")
    else:
        form = TodoForm(instance=todo)
    return render(
        request,
        "todo_form.html",
        {
            "form": form,
            "action": "Update",
            "todo": todo,
        },
    )


@require_http_methods(["POST"])
def todo_toggle_resolved(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.is_resolved = not todo.is_resolved
    todo.save()
    return redirect("tasks:list")


@require_http_methods(["POST"])
def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.delete()
    return redirect("tasks:list")
