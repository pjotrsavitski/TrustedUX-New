from django.shortcuts import render
from django.http import HttpResponse
from .forms import CreateForm1,CreateForm2,CreateForm3,CreateForm4, lastForm, AnonyForm, CreateForm5, SurveyQuestion, AnonyForm
from formtools.wizard.views import SessionWizardView
from django import forms
from django.db import transaction
from .models import Project, Survey, Link, Submission, AnonyData, AnonyDataSetting
from django.contrib import messages
import uuid
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.db.models import Count
from datetime import date
from datetime import timedelta

from .forms import contactforms
from djqscsv import render_to_csv_response
import urllib
from djqscsv import render_to_csv_response
from django.db.models import Q, Sum, Avg, FloatField, Count
from datetime import datetime

from django.utils.translation import ugettext, ugettext_lazy as _






SUBMISSION_FORM = (
    ("survey", SurveyQuestion),
    ("anony", AnonyForm)
)

SUBMISSION_TEMPLATE = {'survey':"survey_form.html","anony":"survey_anony.html"}


CREATE_FORMS = (
    ("project", CreateForm1),
    ("survey", CreateForm2),
    ("participants", CreateForm3),
    ("summary",lastForm))

TEMPLATES = {"project": "create_project.html",
             "survey": "create_survey.html",
             "participants": "create_participation.html",
             "summary": "overview.html"}

# Code by been #################
def csvview(request):
    datablock = []
    response=Submission.objects.none()
    if request.method == "POST":
        form = contactforms(request.user, request.POST)
        if form.is_valid():
            studyidd = form.cleaned_data.get('Project_Name')
            print(studyidd)

            PID = Project.objects.filter(project_name=studyidd).values_list('id', flat=True)
            PID=PID[0]
            print(PID)

            SID = Survey.objects.filter(project_id=PID).values_list('id', flat=True)
            SID=SID[0]
            print(SID)

            LID = Link.objects.filter(survey_id=SID).values_list('id', flat=True)
            print(LID)
            if len(LID)==1:
                allData=Submission.objects.all().filter(link_id=LID[0])
            elif len(LID)==2:
                surveyOne=Submission.objects.all().filter(link_id=LID[0])
                surveyTwo=Submission.objects.all().filter(link_id=LID[1])
                allData=  surveyOne|surveyTwo
            elif  len(LID)==3:
                surveyOne=Submission.objects.all().filter(link_id=LID[0])
                surveyTwo=Submission.objects.all().filter(link_id=LID[1])
                surveyThree=Submission.objects.all().filter(link_id=LID[2])
                allData=  surveyOne|surveyTwo|surveyThree
            elif  len(LID)==4:
                surveyOne=Submission.objects.all().filter(link_id=LID[0])
                surveyTwo=Submission.objects.all().filter(link_id=LID[1])
                surveyThree=Submission.objects.all().filter(link_id=LID[2])
                surveyFour=Submission.objects.all().filter(link_id=LID[3])
                allData=  surveyOne|surveyTwo|surveyThree|surveyFour
            elif  len(LID)==5:
                surveyOne=Submission.objects.all().filter(link_id=LID[0])
                surveyTwo=Submission.objects.all().filter(link_id=LID[1])
                surveyThree=Submission.objects.all().filter(link_id=LID[2])
                surveyFour=Submission.objects.all().filter(link_id=LID[3])
                surveyFive=Submission.objects.all().filter(link_id=LID[4])
                allData=  surveyOne|surveyTwo|surveyThree|surveyFour|surveyFive
    return render_to_csv_response(allData)

# Project wise report

# Code bwith project id #################
def reportDownload(request,project_id):
    datablock = []
    response=Submission.objects.none()
    project = Project.objects.all().filter(id=project_id)

    if project.count() == 0:
        return HttpResponse('Invalid project id')


    studyidd = project[0].project_name


    SID = Survey.objects.filter(project_id=project_id).values_list('id', flat=True)
    SID=SID[0]
    print(SID)

    LID = Link.objects.filter(survey_id=SID).values_list('id', flat=True)
    print(LID)
    if len(LID)==1:
        allData=Submission.objects.all().filter(link_id=LID[0])
    elif len(LID)==2:
        surveyOne=Submission.objects.all().filter(link_id=LID[0])
        surveyTwo=Submission.objects.all().filter(link_id=LID[1])
        allData=  surveyOne|surveyTwo
    elif  len(LID)==3:
        surveyOne=Submission.objects.all().filter(link_id=LID[0])
        surveyTwo=Submission.objects.all().filter(link_id=LID[1])
        surveyThree=Submission.objects.all().filter(link_id=LID[2])
        allData=  surveyOne|surveyTwo|surveyThree
    elif  len(LID)==4:
        surveyOne=Submission.objects.all().filter(link_id=LID[0])
        surveyTwo=Submission.objects.all().filter(link_id=LID[1])
        surveyThree=Submission.objects.all().filter(link_id=LID[2])
        surveyFour=Submission.objects.all().filter(link_id=LID[3])
        allData=  surveyOne|surveyTwo|surveyThree|surveyFour
    elif  len(LID)==5:
        surveyOne=Submission.objects.all().filter(link_id=LID[0])
        surveyTwo=Submission.objects.all().filter(link_id=LID[1])
        surveyThree=Submission.objects.all().filter(link_id=LID[2])
        surveyFour=Submission.objects.all().filter(link_id=LID[3])
        surveyFive=Submission.objects.all().filter(link_id=LID[4])
        allData=  surveyOne|surveyTwo|surveyThree|surveyFour|surveyFive

    return render_to_csv_response(allData)






def Visualize(request):
    datablock = []
    response=Submission.objects.none()
    if request.method == "POST":
        form = contactforms(request.user, request.POST)
        if form.is_valid():
            studyidd = form.cleaned_data.get('Project_Name')
            print(studyidd)

            PID = Project.objects.filter(project_name=studyidd).values_list('id', flat=True)
            PID=PID[0]

            project_ids = Project.objects.all().filter(id=PID)

            project_id = project_ids[0]
            print(PID)

            SID = Survey.objects.filter(project_id=PID).values_list('id', flat=True)
            SID=SID[0]
            print(SID)

            LID = Link.objects.filter(survey_id=SID).values_list('id', flat=True)
            print(LID)
            y= len(LID)
    if y==1:
        labels = []
        data1 = []
        labels11 = []
        data11 = []
        queryset = Submission.objects.aggregate(
            overaltrust=
                Avg("q1", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q4", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q7", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q10", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q12", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            overalrisk=
                Avg("q1", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            overalbenevolence =
                Avg("q4", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[0]))),
            overalcompetence=
                Avg("q7", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            overalreciprocity=
                Avg("q10", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generaltrust=
                Avg("q12", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[0])), output_field=FloatField())
                )
        print(queryset)
        for key, entry in queryset.items():
            labels.append(key)
            data1.append(entry)
        queryset = Submission.objects.aggregate(
            risk1=Avg("q1", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            risk2=Avg("q2", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            risk3=Avg("q3", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            benevolence1=Avg("q4", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            benevolence2=Avg("q5", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            benevolence3=Avg("q6", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            competence1=Avg("q7", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            competence2=Avg("q8", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            competence3=Avg("q9", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            reciprocity1=Avg("q10", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            reciprocity2=Avg("q11", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generalTrust1=Avg("q12", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generalTrust2=Avg("q13", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generalTrust3=Avg("q14", filter=(Q(link_id=LID[0])), output_field=FloatField())
            )
        print(queryset)
        for key, entry in queryset.items():
            labels11.append(key)
            data11.append(entry)
        return render(request, 'pie_chart2.html', {
            'labels': labels,
            'data1': data1,
            'labels11': labels11,
            'data11': data11,
            'project_id':studyidd,
            })

    elif y==2:
        labels = []
        data1 = []
        data2=[]
        labels11 = []
        data11 = []
        data22=[]
        queryset = Submission.objects.aggregate(
            overaltrust=
                Avg("q1", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q4", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q7", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q10", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q12", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            overalrisk=
                Avg("q1", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            overalbenevolence =
                Avg("q4", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[0]))),
            overalcompetence=
                Avg("q7", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            overalreciprocity=
                Avg("q10", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generaltrust=
                Avg("q12", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[0])), output_field=FloatField())
                )
        print(queryset)
        for key, entry in queryset.items():
            labels.append(key)
            data1.append(entry)
        queryset = Submission.objects.aggregate(
            overaltrust=
                Avg("q1", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q4", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q7", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q10", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q12", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            overalrisk=
                Avg("q1", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            overalbenevolence =
                Avg("q4", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[1]))),
            overalcompetence=
                Avg("q7", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            overalreciprocity=
                Avg("q10", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            generaltrust=
                Avg("q12", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[1])), output_field=FloatField())
                )
        print(queryset)
        for key, entry in queryset.items():
            data2.append(entry)

        queryset = Submission.objects.aggregate(
            risk1=Avg("q1", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            risk2=Avg("q2", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            risk3=Avg("q3", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            benevolence1=Avg("q4", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            benevolence2=Avg("q5", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            benevolence3=Avg("q6", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            competence1=Avg("q7", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            competence2=Avg("q8", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            competence3=Avg("q9", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            reciprocity1=Avg("q10", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            reciprocity2=Avg("q11", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generalTrust1=Avg("q12", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generalTrust2=Avg("q13", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generalTrust3=Avg("q14", filter=(Q(link_id=LID[0])), output_field=FloatField())
            )
        print(queryset)
        for key, entry in queryset.items():
            labels11.append(key)
            data11.append(entry)
        queryset = Submission.objects.aggregate(
            risk1=Avg("q1", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            risk2=Avg("q2", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            risk3=Avg("q3", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            benevolence1=Avg("q4", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            benevolence2=Avg("q5", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            benevolence3=Avg("q6", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            competence1=Avg("q7", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            competence2=Avg("q8", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            competence3=Avg("q9", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            reciprocity1=Avg("q10", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            reciprocity2=Avg("q11", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            generalTrust1=Avg("q12", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            generalTrust2=Avg("q13", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            generalTrust3=Avg("q14", filter=(Q(link_id=LID[1])), output_field=FloatField())
            )
        print(queryset)
        for key, entry in queryset.items():
            data22.append(entry)
        return render(request, 'pie_chart2.html', {
            'labels': labels,
            'data1': data1,
            'data2': data2,
            'labels11': labels11,
            'data11': data11,
            'data22': data22,
            'project':studyidd,
            'project_id':project_id
            })
    elif y==3:
        labels = []
        data1 = []
        data2=[]
        data3=[]
        labels11 = []
        data11 = []
        data22=[]
        data33=[]
        queryset = Submission.objects.aggregate(
            overaltrust=
                Avg("q1", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q4", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q7", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q10", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q12", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            overalrisk=
                Avg("q1", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            overalbenevolence =
                Avg("q4", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[0]))),
            overalcompetence=
                Avg("q7", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            overalreciprocity=
                Avg("q10", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generaltrust=
                Avg("q12", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[0])), output_field=FloatField())
                )
        print(queryset)
        for key, entry in queryset.items():
            labels.append(key)
            data1.append(entry)
        queryset = Submission.objects.aggregate(
            overaltrust=
                Avg("q1", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q4", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q7", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q10", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q12", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            overalrisk=
                Avg("q1", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            overalbenevolence =
                Avg("q4", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[1]))),
            overalcompetence=
                Avg("q7", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            overalreciprocity=
                Avg("q10", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            generaltrust=
                Avg("q12", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[1])), output_field=FloatField())
                )
        print(queryset)
        for key, entry in queryset.items():
            data2.append(entry)
        queryset = Submission.objects.aggregate(
            overaltrust=
                Avg("q1", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q4", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q7", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q10", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q12", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            overalrisk=
                Avg("q1", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            overalbenevolence =
                Avg("q4", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[2]))),
            overalcompetence=
                Avg("q7", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            overalreciprocity=
                Avg("q10", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            generaltrust=
                Avg("q12", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[2])), output_field=FloatField())
                )
        print(queryset)
        for key, entry in queryset.items():
            data3.append(entry)

        queryset = Submission.objects.aggregate(
            risk1=Avg("q1", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            risk2=Avg("q2", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            risk3=Avg("q3", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            benevolence1=Avg("q4", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            benevolence2=Avg("q5", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            benevolence3=Avg("q6", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            competence1=Avg("q7", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            competence2=Avg("q8", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            competence3=Avg("q9", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            reciprocity1=Avg("q10", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            reciprocity2=Avg("q11", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generalTrust1=Avg("q12", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generalTrust2=Avg("q13", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generalTrust3=Avg("q14", filter=(Q(link_id=LID[0])), output_field=FloatField())
            )
        print(queryset)
        for key, entry in queryset.items():
            labels11.append(key)
            data11.append(entry)
        queryset = Submission.objects.aggregate(
            risk1=Avg("q1", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            risk2=Avg("q2", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            risk3=Avg("q3", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            benevolence1=Avg("q4", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            benevolence2=Avg("q5", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            benevolence3=Avg("q6", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            competence1=Avg("q7", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            competence2=Avg("q8", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            competence3=Avg("q9", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            reciprocity1=Avg("q10", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            reciprocity2=Avg("q11", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            generalTrust1=Avg("q12", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            generalTrust2=Avg("q13", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            generalTrust3=Avg("q14", filter=(Q(link_id=LID[1])), output_field=FloatField())
            )
        print(queryset)
        for key, entry in queryset.items():
            data22.append(entry)
        queryset = Submission.objects.aggregate(
            risk1=Avg("q1", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            risk2=Avg("q2", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            risk3=Avg("q3", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            benevolence1=Avg("q4", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            benevolence2=Avg("q5", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            benevolence3=Avg("q6", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            competence1=Avg("q7", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            competence2=Avg("q8", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            competence3=Avg("q9", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            reciprocity1=Avg("q10", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            reciprocity2=Avg("q11", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            generalTrust1=Avg("q12", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            generalTrust2=Avg("q13", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            generalTrust3=Avg("q14", filter=(Q(link_id=LID[2])), output_field=FloatField())
            )
        print(queryset)
        for key, entry in queryset.items():
            data33.append(entry)

        return render(request, 'pie_chart3.html', {
            'labels': labels,
            'data1': data1,
            'data2': data2,
            'data3': data3,
            'labels11': labels11,
            'data11': data11,
            'data22': data22,
            'data33': data33,
            'project':studyidd,
            'project_id':project_id
            })
    elif y==4:
        labels = []
        data1 = []
        data2=[]
        data3=[]
        data4=[]
        labels11 = []
        data11 = []
        data22=[]
        data33=[]
        data44=[]
        queryset = Submission.objects.aggregate(
            overaltrust=
                Avg("q1", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q4", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q7", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q10", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q12", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            overalrisk=
                Avg("q1", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            overalbenevolence =
                Avg("q4", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[0]))),
            overalcompetence=
                Avg("q7", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            overalreciprocity=
                Avg("q10", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generaltrust=
                Avg("q12", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[0])), output_field=FloatField())
                )
        print(queryset)
        for key, entry in queryset.items():
            labels.append(key)
            data1.append(entry)
        queryset = Submission.objects.aggregate(
            overaltrust=
                Avg("q1", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q4", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q7", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q10", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q12", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            overalrisk=
                Avg("q1", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            overalbenevolence =
                Avg("q4", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[1]))),
            overalcompetence=
                Avg("q7", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            overalreciprocity=
                Avg("q10", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            generaltrust=
                Avg("q12", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[1])), output_field=FloatField())
                )
        print(queryset)
        for key, entry in queryset.items():
            data2.append(entry)
        queryset = Submission.objects.aggregate(
            overaltrust=
                Avg("q1", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q4", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q7", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q10", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q12", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            overalrisk=
                Avg("q1", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            overalbenevolence =
                Avg("q4", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[2]))),
            overalcompetence=
                Avg("q7", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            overalreciprocity=
                Avg("q10", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            generaltrust=
                Avg("q12", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[2])), output_field=FloatField())
                )
        print(queryset)
        for key, entry in queryset.items():
            data3.append(entry)
        queryset = Submission.objects.aggregate(
            overaltrust=
                Avg("q1", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q4", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q7", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q10", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q12", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            overalrisk=
                Avg("q1", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            overalbenevolence =
                Avg("q4", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[3]))),
            overalcompetence=
                Avg("q7", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            overalreciprocity=
                Avg("q10", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            generaltrust=
                Avg("q12", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[3])), output_field=FloatField())
                )
        print(queryset)
        for key, entry in queryset.items():
            data4.append(entry)
        queryset = Submission.objects.aggregate(
            risk1=Avg("q1", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            risk2=Avg("q2", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            risk3=Avg("q3", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            benevolence1=Avg("q4", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            benevolence2=Avg("q5", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            benevolence3=Avg("q6", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            competence1=Avg("q7", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            competence2=Avg("q8", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            competence3=Avg("q9", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            reciprocity1=Avg("q10", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            reciprocity2=Avg("q11", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generalTrust1=Avg("q12", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generalTrust2=Avg("q13", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generalTrust3=Avg("q14", filter=(Q(link_id=LID[0])), output_field=FloatField())
            )
        print(queryset)
        for key, entry in queryset.items():
            labels11.append(key)
            data11.append(entry)
        queryset = Submission.objects.aggregate(
            risk1=Avg("q1", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            risk2=Avg("q2", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            risk3=Avg("q3", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            benevolence1=Avg("q4", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            benevolence2=Avg("q5", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            benevolence3=Avg("q6", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            competence1=Avg("q7", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            competence2=Avg("q8", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            competence3=Avg("q9", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            reciprocity1=Avg("q10", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            reciprocity2=Avg("q11", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            generalTrust1=Avg("q12", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            generalTrust2=Avg("q13", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            generalTrust3=Avg("q14", filter=(Q(link_id=LID[1])), output_field=FloatField())
            )
        print(queryset)
        for key, entry in queryset.items():
            data22.append(entry)
        queryset = Submission.objects.aggregate(
            risk1=Avg("q1", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            risk2=Avg("q2", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            risk3=Avg("q3", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            benevolence1=Avg("q4", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            benevolence2=Avg("q5", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            benevolence3=Avg("q6", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            competence1=Avg("q7", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            competence2=Avg("q8", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            competence3=Avg("q9", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            reciprocity1=Avg("q10", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            reciprocity2=Avg("q11", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            generalTrust1=Avg("q12", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            generalTrust2=Avg("q13", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            generalTrust3=Avg("q14", filter=(Q(link_id=LID[2])), output_field=FloatField())
            )
        print(queryset)
        for key, entry in queryset.items():
            data33.append(entry)
        queryset = Submission.objects.aggregate(
            risk1=Avg("q1", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            risk2=Avg("q2", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            risk3=Avg("q3", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            benevolence1=Avg("q4", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            benevolence2=Avg("q5", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            benevolence3=Avg("q6", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            competence1=Avg("q7", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            competence2=Avg("q8", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            competence3=Avg("q9", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            reciprocity1=Avg("q10", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            reciprocity2=Avg("q11", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            generalTrust1=Avg("q12", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            generalTrust2=Avg("q13", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            generalTrust3=Avg("q14", filter=(Q(link_id=LID[3])), output_field=FloatField())
            )
        print(queryset)
        for key, entry in queryset.items():
            data44.append(entry)


        return render(request, 'pie_chart4.html', {
            'labels': labels,
            'data1': data1,
            'data2': data2,
            'data3': data3,
            'data4': data4,
            'labels11': labels11,
            'data11': data11,
            'data22': data22,
            'data33': data33,
            'data44': data44,
            'project':studyidd,
            'project_id':project_id
            })
    elif y==5:
        labels = []
        data1 = []
        data2=[]
        data3=[]
        data4=[]
        data5=[]
        labels11 = []
        data11 = []
        data22=[]
        data33=[]
        data44=[]
        data55=[]
        queryset = Submission.objects.aggregate(
            overaltrust=
                Avg("q1", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q4", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q7", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q10", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q12", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            overalrisk=
                Avg("q1", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            overalbenevolence =
                Avg("q4", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[0]))),
            overalcompetence=
                Avg("q7", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            overalreciprocity=
                Avg("q10", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generaltrust=
                Avg("q12", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[0])), output_field=FloatField())
                )
        print(queryset)
        for key, entry in queryset.items():
            labels.append(key)
            data1.append(entry)
        queryset = Submission.objects.aggregate(
            overaltrust=
                Avg("q1", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q4", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q7", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q10", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q12", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            overalrisk=
                Avg("q1", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            overalbenevolence =
                Avg("q4", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[1]))),
            overalcompetence=
                Avg("q7", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            overalreciprocity=
                Avg("q10", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            generaltrust=
                Avg("q12", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[1])), output_field=FloatField())
                )
        print(queryset)
        for key, entry in queryset.items():
            data2.append(entry)
        queryset = Submission.objects.aggregate(
            overaltrust=
                Avg("q1", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q4", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q7", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q10", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q12", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            overalrisk=
                Avg("q1", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            overalbenevolence =
                Avg("q4", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[2]))),
            overalcompetence=
                Avg("q7", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            overalreciprocity=
                Avg("q10", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            generaltrust=
                Avg("q12", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[2])), output_field=FloatField())
                )
        print(queryset)
        for key, entry in queryset.items():
            data3.append(entry)
        queryset = Submission.objects.aggregate(
            overaltrust=
                Avg("q1", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q4", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q7", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q10", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q12", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            overalrisk=
                Avg("q1", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            overalbenevolence =
                Avg("q4", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[3]))),
            overalcompetence=
                Avg("q7", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            overalreciprocity=
                Avg("q10", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            generaltrust=
                Avg("q12", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[3])), output_field=FloatField())
                )
        print(queryset)
        for key, entry in queryset.items():
            data4.append(entry)
        queryset = Submission.objects.aggregate(
            overaltrust=
                Avg("q1", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q4", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q7", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q10", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q12", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[4])), output_field=FloatField()),
            overalrisk=
                Avg("q1", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[4])), output_field=FloatField()),
            overalbenevolence =
                Avg("q4", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[4]))),
            overalcompetence=
                Avg("q7", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[4])), output_field=FloatField()),
            overalreciprocity=
                Avg("q10", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[4])), output_field=FloatField()),
            generaltrust=
                Avg("q12", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[4])), output_field=FloatField())
                )
        print(queryset)
        for key, entry in queryset.items():
            data5.append(entry)
        queryset = Submission.objects.aggregate(
            risk1=Avg("q1", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            risk2=Avg("q2", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            risk3=Avg("q3", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            benevolence1=Avg("q4", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            benevolence2=Avg("q5", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            benevolence3=Avg("q6", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            competence1=Avg("q7", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            competence2=Avg("q8", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            competence3=Avg("q9", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            reciprocity1=Avg("q10", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            reciprocity2=Avg("q11", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generalTrust1=Avg("q12", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generalTrust2=Avg("q13", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generalTrust3=Avg("q14", filter=(Q(link_id=LID[0])), output_field=FloatField())
            )
        print(queryset)
        for key, entry in queryset.items():
            labels11.append(key)
            data11.append(entry)
        queryset = Submission.objects.aggregate(
            risk1=Avg("q1", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            risk2=Avg("q2", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            risk3=Avg("q3", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            benevolence1=Avg("q4", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            benevolence2=Avg("q5", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            benevolence3=Avg("q6", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            competence1=Avg("q7", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            competence2=Avg("q8", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            competence3=Avg("q9", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            reciprocity1=Avg("q10", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            reciprocity2=Avg("q11", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            generalTrust1=Avg("q12", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            generalTrust2=Avg("q13", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            generalTrust3=Avg("q14", filter=(Q(link_id=LID[1])), output_field=FloatField())
            )
        print(queryset)
        for key, entry in queryset.items():
            data22.append(entry)
        queryset = Submission.objects.aggregate(
            risk1=Avg("q1", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            risk2=Avg("q2", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            risk3=Avg("q3", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            benevolence1=Avg("q4", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            benevolence2=Avg("q5", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            benevolence3=Avg("q6", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            competence1=Avg("q7", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            competence2=Avg("q8", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            competence3=Avg("q9", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            reciprocity1=Avg("q10", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            reciprocity2=Avg("q11", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            generalTrust1=Avg("q12", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            generalTrust2=Avg("q13", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            generalTrust3=Avg("q14", filter=(Q(link_id=LID[2])), output_field=FloatField())
            )
        print(queryset)
        for key, entry in queryset.items():
            data33.append(entry)
        queryset = Submission.objects.aggregate(
            risk1=Avg("q1", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            risk2=Avg("q2", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            risk3=Avg("q3", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            benevolence1=Avg("q4", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            benevolence2=Avg("q5", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            benevolence3=Avg("q6", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            competence1=Avg("q7", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            competence2=Avg("q8", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            competence3=Avg("q9", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            reciprocity1=Avg("q10", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            reciprocity2=Avg("q11", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            generalTrust1=Avg("q12", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            generalTrust2=Avg("q13", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            generalTrust3=Avg("q14", filter=(Q(link_id=LID[3])), output_field=FloatField())
            )
        print(queryset)
        for key, entry in queryset.items():
            data44.append(entry)
        queryset = Submission.objects.aggregate(
            risk1=Avg("q1", filter=(Q(link_id=LID[4])), output_field=FloatField()),
            risk2=Avg("q2", filter=(Q(link_id=LID[4])), output_field=FloatField()),
            risk3=Avg("q3", filter=(Q(link_id=LID[4])), output_field=FloatField()),
            benevolence1=Avg("q4", filter=(Q(link_id=LID[4])), output_field=FloatField()),
            benevolence2=Avg("q5", filter=(Q(link_id=LID[4])), output_field=FloatField()),
            benevolence3=Avg("q6", filter=(Q(link_id=LID[4])), output_field=FloatField()),
            competence1=Avg("q7", filter=(Q(link_id=LID[4])), output_field=FloatField()),
            competence2=Avg("q8", filter=(Q(link_id=LID[4])), output_field=FloatField()),
            competence3=Avg("q9", filter=(Q(link_id=LID[4])), output_field=FloatField()),
            reciprocity1=Avg("q10", filter=(Q(link_id=LID[4])), output_field=FloatField()),
            reciprocity2=Avg("q11", filter=(Q(link_id=LID[4])), output_field=FloatField()),
            generalTrust1=Avg("q12", filter=(Q(link_id=LID[4])), output_field=FloatField()),
            generalTrust2=Avg("q13", filter=(Q(link_id=LID[4])), output_field=FloatField()),
            generalTrust3=Avg("q14", filter=(Q(link_id=LID[4])), output_field=FloatField())
            )
        print(queryset)
        for key, entry in queryset.items():
            data55.append(entry)
        return render(request, 'pie_chart5.html', {
            'labels': labels,
            'data1': data1,
            'data2': data2,
            'data3': data3,
            'data4': data4,
            'data5': data5,
            'labels11': labels11,
            'data11': data11,
            'data22': data22,
            'data33': data33,
            'data44': data44,
            'data55': data55,
            'project':studyidd,
            'project_id':project_id
            })


def GotoReport(request):
    form=contactforms(user=request.user)
    return render(request, 'report.html', {'form': form})


###############################

# view to visualize report using project id



def reportView(request,project_id):
    datablock = []
    response=Submission.objects.none()

    project = Project.objects.all().filter(id=project_id)

    if project.count() == 0:
        return HttpResponse('Invalid project id')


    studyidd = project[0].project_name

    SID = Survey.objects.filter(project_id=project_id).values_list('id', flat=True)
    SID=SID[0]
    print(SID)

    LID = Link.objects.filter(survey_id=SID).values_list('id', flat=True)
    print(LID)
    y= len(LID)
    if y==1:
        labels = []
        data1 = []
        labels11 = []
        data11 = []
        queryset = Submission.objects.aggregate(
            overaltrust=
                Avg("q1", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q4", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q7", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q10", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q12", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            overalrisk=
                Avg("q1", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            overalbenevolence =
                Avg("q4", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[0]))),
            overalcompetence=
                Avg("q7", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            overalreciprocity=
                Avg("q10", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generaltrust=
                Avg("q12", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[0])), output_field=FloatField())
                )
        print(queryset)
        for key, entry in queryset.items():
            labels.append(key)
            data1.append(entry)
        queryset = Submission.objects.aggregate(
            risk1=Avg("q1", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            risk2=Avg("q2", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            risk3=Avg("q3", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            benevolence1=Avg("q4", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            benevolence2=Avg("q5", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            benevolence3=Avg("q6", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            competence1=Avg("q7", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            competence2=Avg("q8", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            competence3=Avg("q9", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            reciprocity1=Avg("q10", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            reciprocity2=Avg("q11", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generalTrust1=Avg("q12", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generalTrust2=Avg("q13", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generalTrust3=Avg("q14", filter=(Q(link_id=LID[0])), output_field=FloatField())
            )
        print(queryset)
        for key, entry in queryset.items():
            labels11.append(key)
            data11.append(entry)
        return render(request, 'pie_chart2.html', {
            'labels': labels,
            'data1': data1,
            'labels11': labels11,
            'data11': data11,
            'project':studyidd,
            'project_id':project_id
            })

    elif y==2:
        labels = []
        data1 = []
        data2=[]
        labels11 = []
        data11 = []
        data22=[]
        queryset = Submission.objects.aggregate(
            overaltrust=
                Avg("q1", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q4", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q7", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q10", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q12", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            overalrisk=
                Avg("q1", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            overalbenevolence =
                Avg("q4", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[0]))),
            overalcompetence=
                Avg("q7", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            overalreciprocity=
                Avg("q10", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generaltrust=
                Avg("q12", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[0])), output_field=FloatField())
                )
        print(queryset)
        for key, entry in queryset.items():
            labels.append(key)
            data1.append(entry)
        queryset = Submission.objects.aggregate(
            overaltrust=
                Avg("q1", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q4", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q7", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q10", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q12", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            overalrisk=
                Avg("q1", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            overalbenevolence =
                Avg("q4", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[1]))),
            overalcompetence=
                Avg("q7", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            overalreciprocity=
                Avg("q10", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            generaltrust=
                Avg("q12", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[1])), output_field=FloatField())
                )
        print(queryset)
        for key, entry in queryset.items():
            data2.append(entry)

        queryset = Submission.objects.aggregate(
            risk1=Avg("q1", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            risk2=Avg("q2", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            risk3=Avg("q3", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            benevolence1=Avg("q4", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            benevolence2=Avg("q5", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            benevolence3=Avg("q6", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            competence1=Avg("q7", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            competence2=Avg("q8", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            competence3=Avg("q9", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            reciprocity1=Avg("q10", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            reciprocity2=Avg("q11", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generalTrust1=Avg("q12", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generalTrust2=Avg("q13", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generalTrust3=Avg("q14", filter=(Q(link_id=LID[0])), output_field=FloatField())
            )
        print(queryset)
        for key, entry in queryset.items():
            labels11.append(key)
            data11.append(entry)
        queryset = Submission.objects.aggregate(
            risk1=Avg("q1", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            risk2=Avg("q2", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            risk3=Avg("q3", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            benevolence1=Avg("q4", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            benevolence2=Avg("q5", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            benevolence3=Avg("q6", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            competence1=Avg("q7", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            competence2=Avg("q8", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            competence3=Avg("q9", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            reciprocity1=Avg("q10", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            reciprocity2=Avg("q11", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            generalTrust1=Avg("q12", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            generalTrust2=Avg("q13", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            generalTrust3=Avg("q14", filter=(Q(link_id=LID[1])), output_field=FloatField())
            )
        print(queryset)
        for key, entry in queryset.items():
            data22.append(entry)
        return render(request, 'pie_chart2.html', {
            'labels': labels,
            'data1': data1,
            'data2': data2,
            'labels11': labels11,
            'data11': data11,
            'data22': data22,
            'project':studyidd,
            'project_id':project_id
            })
    elif y==3:
        labels = []
        data1 = []
        data2=[]
        data3=[]
        labels11 = []
        data11 = []
        data22=[]
        data33=[]
        queryset = Submission.objects.aggregate(
            overaltrust=
                Avg("q1", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q4", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q7", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q10", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q12", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            overalrisk=
                Avg("q1", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            overalbenevolence =
                Avg("q4", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[0]))),
            overalcompetence=
                Avg("q7", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            overalreciprocity=
                Avg("q10", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generaltrust=
                Avg("q12", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[0])), output_field=FloatField())
                )
        print(queryset)
        for key, entry in queryset.items():
            labels.append(key)
            data1.append(entry)
        queryset = Submission.objects.aggregate(
            overaltrust=
                Avg("q1", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q4", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q7", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q10", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q12", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            overalrisk=
                Avg("q1", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            overalbenevolence =
                Avg("q4", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[1]))),
            overalcompetence=
                Avg("q7", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            overalreciprocity=
                Avg("q10", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            generaltrust=
                Avg("q12", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[1])), output_field=FloatField())
                )
        print(queryset)
        for key, entry in queryset.items():
            data2.append(entry)
        queryset = Submission.objects.aggregate(
            overaltrust=
                Avg("q1", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q4", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q7", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q10", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q12", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            overalrisk=
                Avg("q1", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            overalbenevolence =
                Avg("q4", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[2]))),
            overalcompetence=
                Avg("q7", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            overalreciprocity=
                Avg("q10", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            generaltrust=
                Avg("q12", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[2])), output_field=FloatField())
                )
        print(queryset)
        for key, entry in queryset.items():
            data3.append(entry)

        queryset = Submission.objects.aggregate(
            risk1=Avg("q1", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            risk2=Avg("q2", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            risk3=Avg("q3", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            benevolence1=Avg("q4", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            benevolence2=Avg("q5", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            benevolence3=Avg("q6", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            competence1=Avg("q7", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            competence2=Avg("q8", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            competence3=Avg("q9", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            reciprocity1=Avg("q10", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            reciprocity2=Avg("q11", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generalTrust1=Avg("q12", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generalTrust2=Avg("q13", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generalTrust3=Avg("q14", filter=(Q(link_id=LID[0])), output_field=FloatField())
            )
        print(queryset)
        for key, entry in queryset.items():
            labels11.append(key)
            data11.append(entry)
        queryset = Submission.objects.aggregate(
            risk1=Avg("q1", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            risk2=Avg("q2", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            risk3=Avg("q3", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            benevolence1=Avg("q4", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            benevolence2=Avg("q5", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            benevolence3=Avg("q6", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            competence1=Avg("q7", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            competence2=Avg("q8", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            competence3=Avg("q9", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            reciprocity1=Avg("q10", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            reciprocity2=Avg("q11", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            generalTrust1=Avg("q12", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            generalTrust2=Avg("q13", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            generalTrust3=Avg("q14", filter=(Q(link_id=LID[1])), output_field=FloatField())
            )
        print(queryset)
        for key, entry in queryset.items():
            data22.append(entry)
        queryset = Submission.objects.aggregate(
            risk1=Avg("q1", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            risk2=Avg("q2", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            risk3=Avg("q3", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            benevolence1=Avg("q4", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            benevolence2=Avg("q5", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            benevolence3=Avg("q6", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            competence1=Avg("q7", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            competence2=Avg("q8", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            competence3=Avg("q9", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            reciprocity1=Avg("q10", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            reciprocity2=Avg("q11", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            generalTrust1=Avg("q12", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            generalTrust2=Avg("q13", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            generalTrust3=Avg("q14", filter=(Q(link_id=LID[2])), output_field=FloatField())
            )
        print(queryset)
        for key, entry in queryset.items():
            data33.append(entry)

        return render(request, 'pie_chart3.html', {
            'labels': labels,
            'data1': data1,
            'data2': data2,
            'data3': data3,
            'labels11': labels11,
            'data11': data11,
            'data22': data22,
            'data33': data33,
            'project':studyidd,
            'project_id':project_id
            })
    elif y==4:
        labels = []
        data1 = []
        data2=[]
        data3=[]
        data4=[]
        labels11 = []
        data11 = []
        data22=[]
        data33=[]
        data44=[]
        queryset = Submission.objects.aggregate(
            overaltrust=
                Avg("q1", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q4", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q7", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q10", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q12", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            overalrisk=
                Avg("q1", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            overalbenevolence =
                Avg("q4", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[0]))),
            overalcompetence=
                Avg("q7", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            overalreciprocity=
                Avg("q10", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generaltrust=
                Avg("q12", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[0])), output_field=FloatField())
                )
        print(queryset)
        for key, entry in queryset.items():
            labels.append(key)
            data1.append(entry)
        queryset = Submission.objects.aggregate(
            overaltrust=
                Avg("q1", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q4", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q7", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q10", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q12", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            overalrisk=
                Avg("q1", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            overalbenevolence =
                Avg("q4", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[1]))),
            overalcompetence=
                Avg("q7", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            overalreciprocity=
                Avg("q10", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            generaltrust=
                Avg("q12", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[1])), output_field=FloatField())
                )
        print(queryset)
        for key, entry in queryset.items():
            data2.append(entry)
        queryset = Submission.objects.aggregate(
            overaltrust=
                Avg("q1", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q4", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q7", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q10", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q12", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            overalrisk=
                Avg("q1", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            overalbenevolence =
                Avg("q4", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[2]))),
            overalcompetence=
                Avg("q7", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            overalreciprocity=
                Avg("q10", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            generaltrust=
                Avg("q12", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[2])), output_field=FloatField())
                )
        print(queryset)
        for key, entry in queryset.items():
            data3.append(entry)
        queryset = Submission.objects.aggregate(
            overaltrust=
                Avg("q1", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q4", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q7", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q10", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q12", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            overalrisk=
                Avg("q1", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            overalbenevolence =
                Avg("q4", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[3]))),
            overalcompetence=
                Avg("q7", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            overalreciprocity=
                Avg("q10", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            generaltrust=
                Avg("q12", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[3])), output_field=FloatField())
                )
        print(queryset)
        for key, entry in queryset.items():
            data4.append(entry)
        queryset = Submission.objects.aggregate(
            risk1=Avg("q1", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            risk2=Avg("q2", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            risk3=Avg("q3", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            benevolence1=Avg("q4", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            benevolence2=Avg("q5", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            benevolence3=Avg("q6", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            competence1=Avg("q7", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            competence2=Avg("q8", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            competence3=Avg("q9", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            reciprocity1=Avg("q10", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            reciprocity2=Avg("q11", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generalTrust1=Avg("q12", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generalTrust2=Avg("q13", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generalTrust3=Avg("q14", filter=(Q(link_id=LID[0])), output_field=FloatField())
            )
        print(queryset)
        for key, entry in queryset.items():
            labels11.append(key)
            data11.append(entry)
        queryset = Submission.objects.aggregate(
            risk1=Avg("q1", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            risk2=Avg("q2", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            risk3=Avg("q3", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            benevolence1=Avg("q4", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            benevolence2=Avg("q5", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            benevolence3=Avg("q6", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            competence1=Avg("q7", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            competence2=Avg("q8", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            competence3=Avg("q9", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            reciprocity1=Avg("q10", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            reciprocity2=Avg("q11", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            generalTrust1=Avg("q12", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            generalTrust2=Avg("q13", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            generalTrust3=Avg("q14", filter=(Q(link_id=LID[1])), output_field=FloatField())
            )
        print(queryset)
        for key, entry in queryset.items():
            data22.append(entry)
        queryset = Submission.objects.aggregate(
            risk1=Avg("q1", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            risk2=Avg("q2", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            risk3=Avg("q3", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            benevolence1=Avg("q4", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            benevolence2=Avg("q5", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            benevolence3=Avg("q6", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            competence1=Avg("q7", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            competence2=Avg("q8", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            competence3=Avg("q9", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            reciprocity1=Avg("q10", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            reciprocity2=Avg("q11", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            generalTrust1=Avg("q12", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            generalTrust2=Avg("q13", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            generalTrust3=Avg("q14", filter=(Q(link_id=LID[2])), output_field=FloatField())
            )
        print(queryset)
        for key, entry in queryset.items():
            data33.append(entry)
        queryset = Submission.objects.aggregate(
            risk1=Avg("q1", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            risk2=Avg("q2", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            risk3=Avg("q3", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            benevolence1=Avg("q4", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            benevolence2=Avg("q5", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            benevolence3=Avg("q6", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            competence1=Avg("q7", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            competence2=Avg("q8", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            competence3=Avg("q9", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            reciprocity1=Avg("q10", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            reciprocity2=Avg("q11", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            generalTrust1=Avg("q12", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            generalTrust2=Avg("q13", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            generalTrust3=Avg("q14", filter=(Q(link_id=LID[3])), output_field=FloatField())
            )
        print(queryset)
        for key, entry in queryset.items():
            data44.append(entry)


        return render(request, 'pie_chart4.html', {
            'labels': labels,
            'data1': data1,
            'data2': data2,
            'data3': data3,
            'data4': data4,
            'labels11': labels11,
            'data11': data11,
            'data22': data22,
            'data33': data33,
            'data44': data44,
            'project':studyidd,
            'project_id':project_id
            })
    elif y==5:
        labels = []
        data1 = []
        data2=[]
        data3=[]
        data4=[]
        data5=[]
        labels11 = []
        data11 = []
        data22=[]
        data33=[]
        data44=[]
        data55=[]
        queryset = Submission.objects.aggregate(
            overaltrust=
                Avg("q1", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q4", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q7", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q10", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q12", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            overalrisk=
                Avg("q1", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            overalbenevolence =
                Avg("q4", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[0]))),
            overalcompetence=
                Avg("q7", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            overalreciprocity=
                Avg("q10", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generaltrust=
                Avg("q12", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[0])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[0])), output_field=FloatField())
                )
        print(queryset)
        for key, entry in queryset.items():
            labels.append(key)
            data1.append(entry)
        queryset = Submission.objects.aggregate(
            overaltrust=
                Avg("q1", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q4", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q7", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q10", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q12", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            overalrisk=
                Avg("q1", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            overalbenevolence =
                Avg("q4", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[1]))),
            overalcompetence=
                Avg("q7", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            overalreciprocity=
                Avg("q10", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            generaltrust=
                Avg("q12", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[1])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[1])), output_field=FloatField())
                )
        print(queryset)
        for key, entry in queryset.items():
            data2.append(entry)
        queryset = Submission.objects.aggregate(
            overaltrust=
                Avg("q1", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q4", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q7", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q10", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q12", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            overalrisk=
                Avg("q1", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            overalbenevolence =
                Avg("q4", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[2]))),
            overalcompetence=
                Avg("q7", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            overalreciprocity=
                Avg("q10", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            generaltrust=
                Avg("q12", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[2])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[2])), output_field=FloatField())
                )
        print(queryset)
        for key, entry in queryset.items():
            data3.append(entry)
        queryset = Submission.objects.aggregate(
            overaltrust=
                Avg("q1", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q4", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q7", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q10", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q12", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            overalrisk=
                Avg("q1", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            overalbenevolence =
                Avg("q4", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[3]))),
            overalcompetence=
                Avg("q7", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            overalreciprocity=
                Avg("q10", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            generaltrust=
                Avg("q12", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[3])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[3])), output_field=FloatField())
                )
        print(queryset)
        for key, entry in queryset.items():
            data4.append(entry)
        queryset = Submission.objects.aggregate(
            overaltrust=
                Avg("q1", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q4", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q7", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q10", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q12", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[4])), output_field=FloatField()),
            overalrisk=
                Avg("q1", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q2", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q3", filter=(Q(link_id=LID[4])), output_field=FloatField()),
            overalbenevolence =
                Avg("q4", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q5", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q6", filter=(Q(link_id=LID[4]))),
            overalcompetence=
                Avg("q7", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q8", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q9", filter=(Q(link_id=LID[4])), output_field=FloatField()),
            overalreciprocity=
                Avg("q10", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q11", filter=(Q(link_id=LID[4])), output_field=FloatField()),
            generaltrust=
                Avg("q12", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q13", filter=(Q(link_id=LID[4])), output_field=FloatField())+
                Avg("q14", filter=(Q(link_id=LID[4])), output_field=FloatField())
                )
        print(queryset)
        for key, entry in queryset.items():
            data5.append(entry)
        queryset = Submission.objects.aggregate(
            risk1=Avg("q1", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            risk2=Avg("q2", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            risk3=Avg("q3", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            benevolence1=Avg("q4", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            benevolence2=Avg("q5", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            benevolence3=Avg("q6", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            competence1=Avg("q7", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            competence2=Avg("q8", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            competence3=Avg("q9", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            reciprocity1=Avg("q10", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            reciprocity2=Avg("q11", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generalTrust1=Avg("q12", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generalTrust2=Avg("q13", filter=(Q(link_id=LID[0])), output_field=FloatField()),
            generalTrust3=Avg("q14", filter=(Q(link_id=LID[0])), output_field=FloatField())
            )
        print(queryset)
        for key, entry in queryset.items():
            labels11.append(key)
            data11.append(entry)
        queryset = Submission.objects.aggregate(
            risk1=Avg("q1", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            risk2=Avg("q2", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            risk3=Avg("q3", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            benevolence1=Avg("q4", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            benevolence2=Avg("q5", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            benevolence3=Avg("q6", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            competence1=Avg("q7", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            competence2=Avg("q8", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            competence3=Avg("q9", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            reciprocity1=Avg("q10", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            reciprocity2=Avg("q11", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            generalTrust1=Avg("q12", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            generalTrust2=Avg("q13", filter=(Q(link_id=LID[1])), output_field=FloatField()),
            generalTrust3=Avg("q14", filter=(Q(link_id=LID[1])), output_field=FloatField())
            )
        print(queryset)
        for key, entry in queryset.items():
            data22.append(entry)
        queryset = Submission.objects.aggregate(
            risk1=Avg("q1", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            risk2=Avg("q2", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            risk3=Avg("q3", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            benevolence1=Avg("q4", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            benevolence2=Avg("q5", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            benevolence3=Avg("q6", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            competence1=Avg("q7", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            competence2=Avg("q8", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            competence3=Avg("q9", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            reciprocity1=Avg("q10", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            reciprocity2=Avg("q11", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            generalTrust1=Avg("q12", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            generalTrust2=Avg("q13", filter=(Q(link_id=LID[2])), output_field=FloatField()),
            generalTrust3=Avg("q14", filter=(Q(link_id=LID[2])), output_field=FloatField())
            )
        print(queryset)
        for key, entry in queryset.items():
            data33.append(entry)
        queryset = Submission.objects.aggregate(
            risk1=Avg("q1", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            risk2=Avg("q2", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            risk3=Avg("q3", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            benevolence1=Avg("q4", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            benevolence2=Avg("q5", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            benevolence3=Avg("q6", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            competence1=Avg("q7", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            competence2=Avg("q8", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            competence3=Avg("q9", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            reciprocity1=Avg("q10", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            reciprocity2=Avg("q11", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            generalTrust1=Avg("q12", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            generalTrust2=Avg("q13", filter=(Q(link_id=LID[3])), output_field=FloatField()),
            generalTrust3=Avg("q14", filter=(Q(link_id=LID[3])), output_field=FloatField())
            )
        print(queryset)
        for key, entry in queryset.items():
            data44.append(entry)
        queryset = Submission.objects.aggregate(
            risk1=Avg("q1", filter=(Q(link_id=LID[4])), output_field=FloatField()),
            risk2=Avg("q2", filter=(Q(link_id=LID[4])), output_field=FloatField()),
            risk3=Avg("q3", filter=(Q(link_id=LID[4])), output_field=FloatField()),
            benevolence1=Avg("q4", filter=(Q(link_id=LID[4])), output_field=FloatField()),
            benevolence2=Avg("q5", filter=(Q(link_id=LID[4])), output_field=FloatField()),
            benevolence3=Avg("q6", filter=(Q(link_id=LID[4])), output_field=FloatField()),
            competence1=Avg("q7", filter=(Q(link_id=LID[4])), output_field=FloatField()),
            competence2=Avg("q8", filter=(Q(link_id=LID[4])), output_field=FloatField()),
            competence3=Avg("q9", filter=(Q(link_id=LID[4])), output_field=FloatField()),
            reciprocity1=Avg("q10", filter=(Q(link_id=LID[4])), output_field=FloatField()),
            reciprocity2=Avg("q11", filter=(Q(link_id=LID[4])), output_field=FloatField()),
            generalTrust1=Avg("q12", filter=(Q(link_id=LID[4])), output_field=FloatField()),
            generalTrust2=Avg("q13", filter=(Q(link_id=LID[4])), output_field=FloatField()),
            generalTrust3=Avg("q14", filter=(Q(link_id=LID[4])), output_field=FloatField())
            )
        print(queryset)
        for key, entry in queryset.items():
            data55.append(entry)
        return render(request, 'pie_chart5.html', {
            'labels': labels,
            'data1': data1,
            'data2': data2,
            'data3': data3,
            'data4': data4,
            'data5': data5,
            'labels11': labels11,
            'data11': data11,
            'data22': data22,
            'data33': data33,
            'data44': data44,
            'data55': data55,
            'project':studyidd,
            'project_id':project_id
            })








def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False

def getAnonyForm(request):
    if request.method == "POST":
        form = AnonyForm(request.POST)
        return HttpResponse('submitted')
    else:
        form = AnonyForm()
        return render(request,"anonymous-form.html",{'form':form})





    ##################################
    return HttpResponse('Report will be provided here')





def filterProjects(request,filter):
    current_site = get_current_site(request)


    print('Calling function')
    domain = current_site.domain
    if filter not in ['all','archived','closed','running']:
        messages.error(request,'Incorrect filter applied.')
        return redirect('project_home')
    else:
        projects = []
        if filter == 'all':
            projects = Project.objects.all().filter(user=request.user)
            if projects.count() == 0:
                messages.warning(request,'There are no projects.')
            else:
                messages.success(request,'All projects are fetched successfully!')
        elif filter == 'archived':
            projects = Project.objects.all().filter(user=request.user,archived=True)
            if projects.count() == 0:
                messages.warning(request,'There are no archived projects.')
            else:
                messages.success(request,'Archived projects are fetched successfully!')
        elif filter == 'running':
            print('calling function')
            projects = Project.objects.all().filter(user=request.user)
            project_list= set()
            for project in projects:
                print(datetime.now().date())

                survey_set = Survey.objects.all().filter(project=project)
                for survey in survey_set:
                    if survey.end_date > datetime.now().date():
                        project_list.add(project.id)

            projects = Project.objects.filter(pk__in = project_list)



            if projects.count() == 0:
                messages.warning(request,'There are no running projects.')
            else:
                messages.success(request,'Running projects are fetched successfully!')

        else:
            print('calling function')
            projects = Project.objects.all().filter(user=request.user)
            project_list= set()
            for project in projects:
                print(datetime.now().date())

                survey = Survey.objects.get(project=project)
                print(survey.end_date)
                if survey.end_date < datetime.now().date():
                    project_list.add(project.id)

            projects = Project.objects.filter(pk__in = project_list)



            if projects.count() == 0:
                messages.warning(request,'There are no finished projects.')
            else:
                messages.success(request,'Ended projects are fetched successfully!')



        return render(request, "dashboard.html",{'projects':projects,'site':current_site,'domain':domain})


def projectAction(request,project_id,type):
    if type not in ['activate','deactivate','archive','unarchive']:
        messages.error(request,'Unsupported action.')

    else:
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            messages.danger(request,'Project id does not exists.')
            project=None
        if project is not None:
            if type == 'activate':
                project.project_status = True
            elif type == 'deactivate':
                project.project_status = False
            elif type == 'archive':
                project.archived = True
            else:
                project.archived = False
            project.save()
            msg = 'Project '+project.project_name+' has been ' +type+'d successfully!'
            messages.success(request,msg)

    return redirect('project_home')

def surveyForm(request,link):
    if request.method == "POST":
        q1 = int(request.POST['q1'])
        q2 = int(request.POST['q2'])
        q3 = int(request.POST['q3'])
        q4 = int(request.POST['q4'])
        q5 = int(request.POST['q5'])
        q6 = int(request.POST['q6'])
        q7 = int(request.POST['q7'])
        q8 = int(request.POST['q8'])
        q9 = int(request.POST['q9'])
        q10 = int(request.POST['q10'])
        q11 = int(request.POST['q7'])
        q12 = int(request.POST['q8'])
        q13 = int(request.POST['q9'])
        q14 = int(request.POST['q10'])

        link_obj = Link.objects.get(url=link)
        submission = Submission.objects.create(link=link_obj,q1=q1,q2=q2,q3=q3,q4=q4,q5=q5,q6=q6,q7=q7,q8=q8,q9=q9,q10=q10,q11=q11,q12=q12,q13=q13,q14=q14)

        # add form for anonymous data submission
        anony_form = AnonyForm(initial={'submission':submission})
        print('Rendering anonymous form')

        return render(request, 'survey_anony.html',{'form':anony_form} )



    else:
        if checkSurveyLink(link):
            link_obj = Link.objects.get(url=link)
            Product = link_obj.survey.product_name
            Survey = link_obj.survey.survey_name
            return render(request,"survey_form.html",{'product':Product,'title':Survey})
        else:
            return render(request, "survey_msg.html",{'msg_title':'Invalid Link','msg_body':'The survey link is invalid.'})




def checkSurveyLink(link):
    if not is_valid_uuid(link):
        return False

    survey_url = Link.objects.all().filter(url=link)

    if survey_url.count() == 0:
        return False
    else:
        survey_url = Link.objects.get(url=link)

        if survey_url.survey.project.project_status:
            return True
    return False



def generateSurvey(request,link):
    if not is_valid_uuid(link):
        return render(request, "survey_msg.html",{'msg_title':'Invalid Link','msg_body':'The survey link is invalid.'})

    survey_url = Link.objects.all().filter(url=link)

    if survey_url.count() == 0:
        return render(request, "survey_msg.html",{'msg_title':'Invalid Link','msg_body':'The survey link is invalid.'})
    else:
        survey_url = Link.objects.get(url=link)

        if (survey_url.survey.start_date > datetime.now().date()):
            return render(request, "survey_msg.html",{'msg_title':'Not started yet','msg_body':'The survey is not started yet.'})

        if (survey_url.survey.end_date < datetime.now().date()):
            return render(request, "survey_msg.html",{'msg_title':'Expired survey','msg_body':'The survey is expired.'})





        if survey_url.survey.project.project_status and not survey_url.survey.project.archived:
            variables = {
                "PROJECT_NAME":survey_url.survey.project.project_name,
                "PRODUCT_NAME":survey_url.survey.product_name,
                "PRODUCT_INDUSTRY":survey_url.survey.project.product_industry,
                "TODAY":date.today(),
                "OWNER_NAME":survey_url.survey.owner,
                "OWNER_EMAIL":survey_url.survey.owner_email,
            }
            print(variables)
            title = survey_url.survey.title
            name = survey_url.survey.survey_name
            paragraph = survey_url.survey.paragraph

            lang = survey_url.survey.language

            title = title.format(**variables)

            paragraph = paragraph.format(**variables)

            #return surveyForm(request,link)
            return render(request,"survey_front.html",{'project_title':title,'paragraph':paragraph,'link':survey_url.url,'lang':lang,'name':name,'survey':survey_url.survey})
        else:
            return render(request, "survey_msg.html",{'msg_title':'Not active','msg_body':'The survey is not active.'})



# Create your views here.
def overview(request):
    projects = Project.objects.all().filter(user=request.user,archived=False).order_by('-created_at')
    current_site = get_current_site(request)
    domain = 'trustedux.herokuapp.com' #current_site.domain
    print(current_site)
    print('domain:',domain)

    return render(request, "dashboard.html",{'projects':projects,'site':current_site,'domain':domain})


def edit(request,project_id):

    projects = Project.objects.all().filter(id=project_id)
    if projects.count() ==0:
        messages.error(request,'Invalid project id')
        return redirect('project_home')

    project = projects[0]

    form1 = {}
    form2 = {}
    form3 = {}
    form4 = {}
    form5 = {}
    lastform ={}

    # form1 data
    form1['project_name'] = project.project_name
    form1['project_type'] = project.project_type

    form1['product_type'] = project.product_type
    form1['product_industry'] = project.product_industry
    form1['new'] = False
    form1['project_id'] = int(project_id)

    print('setting:',form1['project_id'],type(form1['project_id']))

    # form2 data
    survey = Survey.objects.all().filter(project=project)


    form2['name_of_survey1'] = survey[0].survey_name
    form2['questionnaire_language1'] = survey[0].language
    form2['start_date1'] = survey[0].start_date
    form2['end_date1'] = survey[0].end_date
    form2['product_name1'] = survey[0].product_name
    form2['survey_owner1'] = survey[0].owner
    form2['survey_owner_email1'] = survey[0].owner_email
    form2['title1'] = survey[0].title
    form2['paragraph1'] = survey[0].paragraph

    if survey.count() > 1:
        form2['name_of_survey2'] = survey[1].survey_name
        form2['questionnaire_language2'] = survey[1].language
        form2['start_date2'] = survey[1].start_date
        form2['end_date2'] = survey[1].end_date
        form2['product_name2'] = survey[1].product_name
        form2['survey_owner2'] = survey[1].owner
        form2['survey_owner_email2'] = survey[1].owner_email
        form2['title2'] = survey[1].title
        form2['paragraph2'] = survey[1].paragraph
    if survey.count() > 2:
        form2['name_of_survey3'] = survey[2].survey_name
        form2['questionnaire_language3'] = survey[2].language
        form2['start_date3'] = survey[2].start_date
        form2['end_date3'] = survey[2].end_date
        form2['product_name3'] = survey[2].product_name
        form2['survey_owner3'] = survey[2].owner
        form2['survey_owner_email3'] = survey[2].owner_email
        form2['title3'] = survey[2].title
        form2['paragraph3'] = survey[2].paragraph
    if survey.count() > 3:
        form2['name_of_survey4'] = survey[3].survey_name
        form2['questionnaire_language4'] = survey[3].language
        form2['start_date4'] = survey[3].start_date
        form2['end_date4'] = survey[3].end_date
        form2['product_name4'] = survey[3].product_name
        form2['survey_owner4'] = survey[3].owner
        form2['survey_owner_email4'] = survey[3].owner_email
        form2['title4'] = survey[3].title
        form2['paragraph4'] = survey[3].paragraph
    if survey.count() > 4:
        form2['name_of_survey5'] = survey[4].survey_name
        form2['questionnaire_language5'] = survey[4].language
        form2['start_date5'] = survey[4].start_date
        form2['end_date5'] = survey[4].end_date
        form2['product_name5'] = survey[4].product_name
        form2['survey_owner5'] = survey[4].owner
        form2['survey_owner_email5'] = survey[4].owner_email
        form2['title5'] = survey[4].title
        form2['paragraph5'] = survey[4].paragraph



    anony_setting = AnonyDataSetting.objects.get(project=project)




    #form5
    form2['age'] = anony_setting.age
    form2['gender'] = anony_setting.gender
    form2['nationality'] =anony_setting.nationality
    form2['education'] =anony_setting.education

    #last form
    lastform['project_status'] = project.project_status



    initial = {'project':form1,'survey':form2,'participants':form3,'summary':lastform}



    return CompleteForm.as_view(CREATE_FORMS,initial_dict=initial)(request)


class CompleteForm(SessionWizardView):
    type_of_study = -1


    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]



    def get_form(self, step=None, data=None, files=None):

        form = super().get_form(step, data, files)

        # determine the step if not given
        if step is None:
            step = self.steps.current




        if step == 'survey':
            #filled_data = self.fill_dummy('survey',data)
            print('Get form:',self.type_of_study)
            #form = super().get_form(step, filled_data, files)
        #print(form.data)
        return form


    def get_context_data(self, form, **kwargs):
        context = super(CompleteForm, self).get_context_data(form=form, **kwargs)
        #print('Step->',self.steps.current,':',self.get_all_cleaned_data())

        if self.steps.current =='summary':
            data = self.get_all_cleaned_data()
            print('------------------->')
            print(data['project_id'])

            context.update({'all_data': self.get_all_cleaned_data()})
            context.update({'type':self.type_of_study})



        if self.steps.current == "survey":

            data = self.get_all_cleaned_data()
            self.type_of_study = int(data['project_type'])

            #survey_dict = self.fill_dummy()
            ##self.initial_dict['survey'] = survey_dict


            context.update({'type':self.type_of_study})
            #form = self.fill_dummy(form)
            #initial = self.fill_dummy(form)

            #print('-----------------------------')
            #print(initial)
            #self.initial_dict['survey'] = initial
            #context = super(CompleteForm, self).get_context_data(form=form, **kwargs)

            #print('Type:',data['project_type'])
        return context


    def fill_dummy(self,step,initial):
        study = self.type_of_study

        k =  study + 1
        while k <= 5:

            initial['%s-name_of_survey%s' % (step,str(k))] = ['demo']
            initial['%s-questionnaire_language%s' % (step,str(k))] = ['En']
            initial['%s-start_date%s'%(step,str(k))] =  [datetime.now().today()]
            initial['%s-end_date%s'%(step,str(k))] = [datetime.now().today() + timedelta(days=1)]


            initial['%s-survey_owner%s'%(step,str(k))] = [self.request.user]
            initial['%s-survey_owner_email%s'%(step,str(k))] = [self.request.user.email]
            initial['%s-title%s'%(step,str(k))] =['demo']
            initial['%s-paragraph%s'%(step,str(k))] = ['para']
            k += 1
        print('returing initial')
        return initial




    @transaction.atomic
    def done(self, form_list, **kwargs):
        print('done called')
        all_data = self.get_all_cleaned_data()
        print(all_data['new'])
        print(all_data['project_id'])
        print('--------------->entering condition')
        if all_data['new']:
            print('New project')
            current_user = self.request.user
            project = Project.objects.create(user=current_user,project_name=all_data['project_name'],project_type=all_data['project_type'],project_status=all_data['project_status'],product_type=all_data['product_type'],product_industry=all_data['product_industry'])
            type = int(all_data['project_type'])

            for k in range(type):
                k += 1
                s_name_key = 'name_of_survey'+str(k)
                s_lang_key = 'questionnaire_language'+str(k)
                s_start_key = 'start_date' + str(k)
                s_end_key = 'end_date' + str(k)
                s_title_key = 'title' + str(k)
                s_paragraph_key = 'paragraph' + str(k)
                s_owner_key = 'survey_owner' + str(k)
                s_owner_email_key = 'survey_owner_email' + str(k)
                s_product_name_key = 'product_name' + str(k)

                survey = Survey.objects.create(project=project,product_name=all_data[s_product_name_key],survey_name = all_data[s_name_key],start_date=all_data[s_start_key],end_date=all_data[s_end_key],title=all_data[s_title_key],paragraph=all_data[s_paragraph_key],owner=all_data[s_owner_key],owner_email=all_data[s_owner_email_key],language=all_data[s_lang_key])

                survey_url = Link.objects.create(survey=survey,sequence=k)

            age = all_data['age']
            gender=all_data['gender']
            education=all_data['education']
            nationality=all_data['nationality']



            anony_settings = AnonyDataSetting.objects.create(project=project,age=age,gender=gender,education=education,nationality=nationality)



            messages.success(self.request, 'Project created successfully !')
        else:
            print('-------------------->',all_data['project_id'])
            project_id = int(all_data['project_id'])

            project = Project.objects.get(id=project_id)
            surveys = Survey.objects.all().filter(project=project).delete()


            surveys_count = int(all_data['project_type'])

            project.project_name = all_data['project_name']
            project.project_type = all_data['project_type']
            project.product_name= all_data['product_name']
            project.product_type=all_data['project_type']
            project.product_industry=all_data['product_industry']
            project.project_status=all_data['project_status']

            for k in range(surveys_count):
                k += 1
                s_name_key = 'name_of_survey'+str(k)
                s_lang_key = 'questionnaire_language'+str(k)
                s_start_key = 'start_date' + str(k)
                s_end_key = 'end_date' + str(k)
                s_title_key = 'title' + str(k)
                s_paragraph_key = 'paragraph' + str(k)
                s_owner_key = 'survey_owner' + str(k)
                s_owner_email_key = 'survey_owner_email' + str(k)
                s_product_name_key = 'product_name' + str(k)

                survey = Survey.objects.create(project=project,product_name=all_data[s_product_name_key],survey_name = all_data[s_name_key],start_date=all_data[s_start_key],end_date=all_data[s_end_key],title=all_data[s_title_key],paragraph=all_data[s_paragraph_key],owner=all_data[s_owner_key],owner_email=all_data[s_owner_email_key],language=all_data[s_lang_key])

                survey_url = Link.objects.create(survey=survey,sequence=k)






            project.save()

            messages.success(self.request,'Project is successfully updated')

        return redirect('project_home')

class CompleteSubmissionForm(SessionWizardView):
    def get_template_names(self):
        return [SUBMISSION_TEMPLATE[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        link_obj = Link.objects.get(url=self.kwargs['link'])
        survey_name = link_obj.survey.survey_name
        product = link_obj.survey.product_name
        project = link_obj.survey.project

        language = link_obj.survey.language
        context.update({'lang': language})

        anony_setting = AnonyDataSetting.objects.get(project=project)
        print('Anonymous object:',anony_setting, anony_setting.age)
        if self.steps.current == 'survey':
            context.update({'survey': survey_name,'product':product})

        if self.steps.current == 'anony':
            context.update({'all_data': self.get_all_cleaned_data(),'anony_setting':anony_setting})
            print(self.get_all_cleaned_data())
        return context

    @transaction.atomic
    def done(self, form_list, **kwargs):
        print('done called')
        all_data = self.get_all_cleaned_data()

        print(all_data)
        q1 = int(all_data['q1'])
        q2 = int(all_data['q2'])
        q3 = int(all_data['q3'])
        q4 = int(all_data['q4'])
        q5 = int(all_data['q5'])
        q6 = int(all_data['q6'])
        q7 = int(all_data['q7'])
        q8 = int(all_data['q8'])
        q9 = int(all_data['q9'])
        q10 = int(all_data['q10'])
        q11 = int(all_data['q7'])
        q12 = int(all_data['q8'])
        q13 = int(all_data['q9'])
        q14 = int(all_data['q10'])

        link_obj = Link.objects.get(url=self.kwargs['link'])
        submission = Submission.objects.create(link=link_obj,q1=q1,q2=q2,q3=q3,q4=q4,q5=q5,q6=q6,q7=q7,q8=q8,q9=q9,q10=q10,q11=q11,q12=q12,q13=q13,q14=q14)

        print(all_data)


        age = all_data['age'] if all_data['age'] != '' else -1
        education = all_data['education'] if all_data['education'] != '' else -1

        gender = all_data['gender']
        nationality = all_data['nationality']

        lang = link_obj.survey.language




        anony_data = AnonyData.objects.create(link=link_obj,age=age,gender=gender,education=education,nationality=nationality)

        return render(self.request,'survey_msg.html',{'msg_title':_('Successful Submission'),'msg_body':_('Your submissions are successfully saved. Thank you for your time.'),'lang':lang})
