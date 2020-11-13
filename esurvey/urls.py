from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required
from .views import CompleteForm, CompleteSubmissionForm, CREATE_FORMS, SUBMISSION_FORM
initial = {'questionnaire':{'new':True}}
urlpatterns = [
    path("esurvey/<link>/start", login_required(CompleteSubmissionForm.as_view(SUBMISSION_FORM)), name="survey_form"),
    path("esurvey/<link>", login_required(views.generateSurvey), name="get_survey"),
    path("projects/filter/<filter>", login_required(views.filterProjects), name="project_filter"),

    path("projects/", login_required(views.overview), name="project_home"),  # <-- added
    path("projects/edit/<project_id>",login_required(views.edit), name="edit"),
    path("projects/action/<type>/<project_id>", login_required(views.projectAction), name="project_action"),

    path("projects/new/",login_required(CompleteForm.as_view(CREATE_FORMS,initial_dict=initial)), name="create"),
    path("GotoReport/",login_required(views.GotoReport), name="GotoReport"),
    path('csv_view/', login_required(views.csvview), name='csv_view'),
    #path('Visualize/', login_required(views.Visualize), name='Visualize'),
    path('projects/report/<project_id>/download', login_required(views.reportDownload), name='report_download'),
    path('projects/report/<project_id>/visualize', login_required(views.reportView), name='report_view'),

]
