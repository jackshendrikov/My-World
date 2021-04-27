from django.urls import path

from . import views
from analyzer.features import HAS_TASK_MERGE

app_name = 'analyzer'

urlpatterns = [
    path('', views.list_lists,  name="lists"),

    # View reorder_tasks is only called by JQuery for drag/drop task ordering.
    path('reorder_tasks/', views.reorder_tasks, name="reorder_tasks"),

    # Three paths into `list_detail` view
    path('mine/', views.list_detail, {'list_slug': 'mine'}, name="mine"),

    path('<int:list_id>/<str:list_slug>/checked/', views.list_detail, {'view_checked': True},
         name='list_detail_checked'),
    path('<int:list_id>/<str:list_slug>/', views.list_detail, name='list_detail'),
    path('<int:list_id>/<str:list_slug>/delete/', views.del_list, name="del_list"),

    path('add_list/', views.add_list, name="add_list"),
    path('task/<str:task_id>/', views.task_detail, name='task_detail'),
    path('attachment/remove/<int:attachment_id>/', views.remove_attachment, name='remove_attachment'),
    path('attachment/predict/<int:attachment_id>/', views.prediction, name='prediction'),
]

if HAS_TASK_MERGE:
    # ensure mail tracker autocomplete is optional
    from analyzer.views.task_autocomplete import TaskAutocomplete
    urlpatterns.append(path('task/<str:task_id>/autocomplete/', TaskAutocomplete.as_view(), name='task_autocomplete'))

urlpatterns.extend([
    path('toggle_done/<str:task_id>/', views.toggle_done, name='task_toggle_done'),
    path('delete/<str:task_id>/', views.delete_task, name='delete_task'),
    path('search/', views.search, name="search"),
    path('import_csv/', views.import_csv, name="import_csv"),
])
