import datetime
import os

import bleach
from django import forms
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from analyzer.defaults import defaults
from analyzer.features import HAS_TASK_MERGE
from analyzer.forms import AddEditTaskForm
from analyzer.models import Attachment, Commentary, Task
from analyzer.utils import (toggle_task_checked, user_can_read_task)


if HAS_TASK_MERGE:
    from dal import autocomplete


def handle_add_comment(request, task):
    if not request.POST.get("add_comment"):
        return

    Commentary.objects.create(author=request.user, task=task, body=bleach.clean(request.POST["comment-body"], strip=True))

    messages.success(request, "Comment posted.")


def task_detail(request, task_id: int) -> HttpResponse:
    """View task details. Allow task details to be edited. Process new comments on task."""

    task = get_object_or_404(Task, pk=task_id)
    comment_list = Commentary.objects.filter(task=task_id).order_by("-date")

    # Handle task merging
    if not HAS_TASK_MERGE:
        merge_form = None
    else:

        class MergeForm(forms.Form):
            merge_target = forms.ModelChoiceField(queryset=Task.objects.all(), widget=autocomplete.ModelSelect2(
                url=reverse("analyzer:task_autocomplete", kwargs={"task_id": task_id})), )

        # Handle task merging
        if not request.POST.get("merge_task_into"):
            merge_form = MergeForm()
        else:
            merge_form = MergeForm(request.POST)
            if merge_form.is_valid():
                merge_target = merge_form.cleaned_data["merge_target"]
            if not user_can_read_task(merge_target, request.user):
                raise PermissionDenied

            task.merge_into(merge_target)
            return redirect(reverse("analyzer:task_detail", kwargs={"task_id": merge_target.pk}))

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
            item.username = bleach.clean(form.cleaned_data["username"], strip=True)
            item.save()
            messages.success(request, "The task has been edited.")
            return redirect("analyzer:list_detail", list_id=task.task_list.id, list_slug=task.task_list.slug)

    # Mark complete
    if request.POST.get("toggle_done"):
        results_changed = toggle_task_checked(task.id)
        if results_changed:
            messages.success(request, f"Changed completion status for task {task.id}")

        return redirect("analyzer:task_detail", task_id=task.id)

    # Handle uploaded files
    if request.FILES.get("attachment_file_input"):
        file = request.FILES.get("attachment_file_input")

        if Attachment.objects.filter(task_id=task.id).count() >= defaults("MAXIMUM_ATTACHMENT_FILES"):
            messages.error(request, f"You can upload maximum 3 files, if you want re-upload, then delete something.")
            return redirect("analyzer:task_detail", task_id=task.id)

        if file.size > defaults("MAXIMUM_ATTACHMENT_SIZE"):
            messages.error(request, f"File exceeds maximum attachment size.")
            return redirect("analyzer:task_detail", task_id=task.id)

        name, extension = os.path.splitext(file.name)

        if extension not in defaults("LIMIT_FILE_ATTACHMENTS"):
            messages.error(request, f"This site allows you to upload only `pdf`, you can't upload {extension} files.")
            return redirect("analyzer:task_detail", task_id=task.id)

        Attachment.objects.create(task=task, timestamp=datetime.datetime.now(), file=file)
        messages.success(request, f"File attached successfully")
        return redirect("analyzer:task_detail", task_id=task.id)

    context = {
        "task": task,
        "comment_list": comment_list,
        "form": form,
        "merge_form": merge_form,
        "comment_classes": defaults("COMMENT_CLASSES"),
        "attachments_enabled": defaults("ALLOW_FILE_ATTACHMENTS"),
    }

    return render(request, "analyzer/task_detail.html", context)
