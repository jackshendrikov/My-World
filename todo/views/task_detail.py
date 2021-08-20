import datetime
import os

import bleach
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from todo.defaults import defaults
from todo.forms import AddEditTaskForm
from todo.models import Attachment, Comments, Task
from todo.utils import (staff_check, toggle_task_completed, user_can_read_task, )


def handle_add_comment(request, task):
    if not request.POST.get("add_comment"):
        return

    Comments.objects.create(author=request.user, task=task, body=bleach.clean(request.POST["comment-body"], strip=True))
    messages.success(request, "Comment posted.")


@login_required
@user_passes_test(staff_check)
def task_detail(request, task_id: int) -> HttpResponse:
    """View task details. Allow task details to be edited. Process new comments on task."""

    task = get_object_or_404(Task, pk=task_id)
    comment_list = Comments.objects.filter(task=task_id).order_by("-date")

    # Ensure user has permission to view task. Superusers can view all tasks.
    # Get the group this task belongs to, and check whether current user is a member of that group.
    if not user_can_read_task(task, request.user):
        raise PermissionDenied

    # Save submitted comments
    handle_add_comment(request, task)

    # Save task edits
    if not request.POST.get("add_edit_task"):
        form = AddEditTaskForm(request.user, instance=task, initial={"task_list": task.task_list})
    else:
        form = AddEditTaskForm(request.user, request.POST, instance=task, initial={"task_list": task.task_list})

        if form.is_valid():
            item = form.save(commit=False)
            item.note = bleach.clean(form.cleaned_data["note"], strip=True)
            item.title = bleach.clean(form.cleaned_data["title"], strip=True)
            item.save()
            messages.success(request, "The task has been edited.")
            return redirect("todo:list_detail", list_id=task.task_list.id, list_slug=task.task_list.slug)

    # Mark complete
    if request.POST.get("toggle_done"):
        results_changed = toggle_task_completed(task.id)
        if results_changed:
            messages.success(request, f"Changed completion status for task {task.id}")

        return redirect("todo:task_detail", task_id=task.id)

    if task.due_date:
        date = task.due_date
    else:
        date = datetime.datetime.now()

    # Handle uploaded files
    if request.FILES.get("attachment_file_input"):
        file = request.FILES.get("attachment_file_input")

        if file.size > defaults("TODO_MAXIMUM_ATTACHMENT_SIZE"):
            messages.error(request, f"File exceeds maximum attachment size.")
            return redirect("todo:task_detail", task_id=task.id)

        name, extension = os.path.splitext(file.name)

        if extension not in defaults("TODO_LIMIT_FILE_ATTACHMENTS"):
            messages.error(request, f"This site does not allow upload of {extension} files.")
            return redirect("todo:task_detail", task_id=task.id)

        Attachment.objects.create(task=task, added_by=request.user, timestamp=datetime.datetime.now(), file=file)
        messages.success(request, f"File attached successfully")
        return redirect("todo:task_detail", task_id=task.id)

    context = {
        "task": task,
        "comment_list": comment_list,
        "form": form,
        "thedate": date,
        "comment_classes": defaults("TODO_COMMENT_CLASSES"),
        "attachments_enabled": defaults("TODO_ALLOW_FILE_ATTACHMENTS"),
    }

    return render(request, "todo/task_detail.html", context)
