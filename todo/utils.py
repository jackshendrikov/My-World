import logging
import os


from todo.defaults import defaults
from todo.models import Attachment, Task

log = logging.getLogger(__name__)


def staff_check(user):
    if defaults("TODO_STAFF_ONLY"):
        return user.is_staff
    else:
        # If unset or False, allow all logged in users
        return True


def user_can_read_task(task, user):
    return task.task_list.group in user.groups.all() or user.is_superuser


def toggle_task_completed(task_id: int) -> bool:
    """Toggle the `completed` bool on Task from True to False or vice versa."""
    try:
        task = Task.objects.get(id=task_id)
        task.completed = not task.completed
        task.save()
        return True

    except Task.DoesNotExist:
        log.info(f"Task {task_id} not found.")
        return False


def remove_attachment_file(attachment_id: int) -> bool:
    """Delete an Attachment object  from the filesystem."""
    try:
        attachment = Attachment.objects.get(id=attachment_id)
        if attachment.file:
            if os.path.isfile(attachment.file.path):
                os.remove(attachment.file.path)

        attachment.delete()
        return True

    except Attachment.DoesNotExist:
        log.info(f"Attachment {attachment_id} not found.")
        return False
