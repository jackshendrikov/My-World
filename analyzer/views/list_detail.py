import bleach
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404, redirect, render

from analyzer.forms import AddEditTaskForm
from analyzer.models import Task, TaskList


def list_detail(request, list_id=None, list_slug=None, view_checked=False) -> HttpResponse:
    """Display and manage tasks in a list."""

    # Defaults
    task_list = None
    form = None

    # Which tasks to show on this list view?
    if list_slug == "mine":
        tasks = Task.objects.filter(assigned_to=request.user)

    else:
        # Show a specific list, ensuring permissions.
        task_list = get_object_or_404(TaskList, id=list_id)
        tasks = Task.objects.filter(task_list=task_list.id)

    # Additional filtering
    if view_checked:
        tasks = tasks.filter(checked=True)
    else:
        tasks = tasks.filter(checked=False)

    # ######################
    #  Add New Task Form
    # ######################

    if request.POST.getlist("add_edit_task"):
        form = AddEditTaskForm(request.user, request.POST,
                               initial={"assigned_to": request.user.id, "priority": 999, "task_list": task_list}, )

        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.created_by = bleach.clean(form.cleaned_data["username"], strip=True)
            new_task.note = bleach.clean(form.cleaned_data["note"], strip=True)

            try:
                validate_email(new_task.email)

                form.save()

                messages.success(request, 'New task from {t} has been added!'.format(t=new_task.username))
                messages.info(request, mark_safe('You can add your attachments here: '
                                                 '<a href="../../task/' + new_task.id + '">' + new_task.id + '</a>.'))

                return redirect(request.path)
            except ValidationError:
                messages.error(request, 'Enter correct email!')
    else:
        # Don't allow adding new tasks on some views
        if list_slug not in ["mine", "recent-add", "recent-complete"]:
            form = AddEditTaskForm(request.user,
                                   initial={"assigned_to": request.user.id, "priority": 999, "task_list": task_list}, )

    context = {
        "list_id": list_id,
        "list_slug": list_slug,
        "task_list": task_list,
        "form": form,
        "tasks": tasks,
        "view_checked": view_checked,
    }

    return render(request, "analyzer/list_detail.html", context)
