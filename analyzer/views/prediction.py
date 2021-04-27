import os

from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from analyzer.utils import staff_check, predict, convert_pdf_to_txt
from analyzer.models import Attachment, Commentary


@login_required
@user_passes_test(staff_check)
def prediction(request, attachment_id: int) -> HttpResponse:
    """ Prediction make sentiment analysis of given pdf attachment and return result specific percent of positivity.
        Redirect to the prediction page.
    """
    if request.method == "POST":
        attachment = get_object_or_404(Attachment, pk=attachment_id)

        # Permissions
        if not (attachment.task.task_list.group in request.user.groups.all() or request.user.is_superuser):
            raise PermissionDenied

        txt = convert_pdf_to_txt(attachment.file.path)
        print(txt)

        txt_prediction = predict(txt)
        msg = "Prediction for file `" + str(os.path.basename(attachment.file.name)) + "`: " + \
              str(round(float(txt_prediction) * 100, 2)) + '%'
        print(msg)

        # posted comment with result of prediction
        Commentary.objects.create(author=request.user, task=attachment.task, body=msg)

        context = {'prediction': round(float(txt_prediction), 2) * 100, 'attachment': attachment.filename}

        return render(request, 'analyzer/predict.html', context)
