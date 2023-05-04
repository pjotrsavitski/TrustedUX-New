from django.shortcuts import render
from django.http import HttpResponse
from .forms import CreateForm1,CreateForm2,CreateForm3,CreateForm4, lastForm, AnonyForm, CreateForm5, SurveyQuestion, AnonyForm, frontForm
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
from .models import AnonyData, sort_countries, gen_choices, edu_choices, age_choices
from .forms import contactforms
from djqscsv import render_to_csv_response
import urllib
from djqscsv import render_to_csv_response
from django.db.models import Q, F, Sum, Avg, FloatField, IntegerField,  Count
from datetime import datetime
import numpy as np
import pandas as df
from django.utils.translation import gettext, gettext_lazy as _
import math



"""

SUBMISSION_FORM = (
    ("survey", SurveyQuestion),
    ("anony", AnonyForm)
)

PLATE = {'survey':"survey_form.html","anony":"survey_anony.html"}
"""


SUBMISSION_FORM = (

    ("survey", SurveyQuestion),

)

SUBMISSION_TEMPLATE = {'survey':"survey_form_updated.html"}





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
    NumberOfSurveys=len(SID)


    #print(LID)
    if NumberOfSurveys==1:
        LID = Link.objects.filter(survey_id=SID[0]).values_list('id', flat=True)
        allData=Submission.objects.all().filter(link_id=LID[0])
    elif NumberOfSurveys==2:
        LID1 = Link.objects.filter(survey_id=SID[0]).values_list('id', flat=True)
        LID2 = Link.objects.filter(survey_id=SID[1]).values_list('id', flat=True)
        surveyOne=Submission.objects.all().filter(link_id=LID1[0])
        surveyTwo=Submission.objects.all().filter(link_id=LID2[0])
        allData=  surveyOne|surveyTwo
    elif NumberOfSurveys==3:
        LID1 = Link.objects.filter(survey_id=SID[0]).values_list('id', flat=True)
        LID2 = Link.objects.filter(survey_id=SID[1]).values_list('id', flat=True)
        LID3 = Link.objects.filter(survey_id=SID[2]).values_list('id', flat=True)
        surveyOne=Submission.objects.all().filter(link_id=LID1[0])
        surveyTwo=Submission.objects.all().filter(link_id=LID2[0])
        surveyThree=Submission.objects.all().filter(link_id=LID3[0])
        allData=  surveyOne|surveyTwo|surveyThree
    elif NumberOfSurveys==4:
        LID1 = Link.objects.filter(survey_id=SID[0]).values_list('id', flat=True)
        LID2 = Link.objects.filter(survey_id=SID[1]).values_list('id', flat=True)
        LID3 = Link.objects.filter(survey_id=SID[2]).values_list('id', flat=True)
        LID4 = Link.objects.filter(survey_id=SID[3]).values_list('id', flat=True)
        surveyOne=Submission.objects.all().filter(link_id=LID1[0])
        surveyTwo=Submission.objects.all().filter(link_id=LID2[0])
        surveyThree=Submission.objects.all().filter(link_id=LID3[0])
        surveyFour=Submission.objects.all().filter(link_id=LID4[0])
        allData=  surveyOne|surveyTwo|surveyThree|surveyFour
    elif NumberOfSurveys==4:
        LID1 = Link.objects.filter(survey_id=SID[0]).values_list('id', flat=True)
        LID2 = Link.objects.filter(survey_id=SID[1]).values_list('id', flat=True)
        LID3 = Link.objects.filter(survey_id=SID[2]).values_list('id', flat=True)
        LID4 = Link.objects.filter(survey_id=SID[3]).values_list('id', flat=True)
        LID5 = Link.objects.filter(survey_id=SID[4]).values_list('id', flat=True)
        surveyOne=Submission.objects.all().filter(link_id=LID1[0])
        surveyTwo=Submission.objects.all().filter(link_id=LID2[0])
        surveyThree=Submission.objects.all().filter(link_id=LID3[0])
        surveyFour=Submission.objects.all().filter(link_id=LID4[0])
        surveyFive=Submission.objects.all().filter(link_id=LID5[0])
        allData=  surveyOne|surveyTwo|surveyThree|surveyFour|surveyFive

    return render_to_csv_response(allData)


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

    NumberOfSurveys=len(SID)

    productname = Survey.objects.filter(id=SID[0]).values_list('product_name', flat=True)
    productname=productname[0]
#function calculate crobanch alpha
    def cronbach_alpha(df):
    # 1. Transform the df into a correlation matrix
        df_corr = df.corr()

    # 2.1 Calculate N
    # The number of variables equals the number of columns in the df
        N = df.shape[1]

    # 2.2 Calculate R
    # For this, we'll loop through the columns and append every
    # relevant correlation to an array calles "r_s". Then, we'll
    # calculate the mean of "r_s"
        rs = np.array([])
        for i, col in enumerate(df_corr.columns):
            sum_ = df_corr[col][i+1:].values
            rs = np.append(sum_, rs)
        mean_r = np.mean(rs)

   # 3. Use the formula to calculate Cronbach's Alpha
        cronbach_alpha = (N * mean_r) / (1 + (N - 1) * mean_r)
        return cronbach_alpha

    if NumberOfSurveys==1:
        #get the link ids for the two surveys
        LID1 = Link.objects.filter(survey_id=SID[0]).values_list('id', flat=True)

        #get the number of respondents by survey
        S1Count = Submission.objects.aggregate(
            responseS1= Count("q1", filter=(Q(link_id=LID1[0])), output_field=IntegerField()))

        S1Counts=[]

        for key, entry in S1Count.items():
            if entry is None:
                   S1Counts.append(0)
            else:
                S1Counts.append(entry)

        survey1Counts= S1Counts[0]

        #get number gender details for each survey
        S1CountMale = AnonyData.objects.filter(link_id=LID1[0], gender="M").count()
        S1CountFeMale = AnonyData.objects.filter(link_id=LID1[0], gender="F").count()
        S1CountOthers = AnonyData.objects.filter(link_id=LID1[0], gender="O").count()

            #appending the results to an array because the chartjs piechart expects the data in an array format
        S1CountGender = [S1CountMale, S1CountFeMale, S1CountOthers]

        #getting the age distribution for each survey
        #survey 1
        S1Count17Below = AnonyData.objects.filter(link_id=LID1[0], age="1").count()
        S1Count18To27 = AnonyData.objects.filter(link_id=LID1[0], age="2").count()
        S1Count28To37 = AnonyData.objects.filter(link_id=LID1[0], age="3").count()
        S1Count38To47 = AnonyData.objects.filter(link_id=LID1[0], age="4").count()
        S1Count48To57 = AnonyData.objects.filter(link_id=LID1[0], age="5").count()
        S1Count58Above = AnonyData.objects.filter(link_id=LID1[0], age="6").count()

            #appending the results to an array because the chartjs piechart expects the data in an array format
        S1CountAge = [S1Count17Below, S1Count18To27, S1Count28To37, S1Count38To47, S1Count48To57, S1Count58Above ]

        #check for null entries and replace them with 0
        for i in S1CountAge:
            if i == '':
                S1CountAge[i]=0
            else:
                S1CountAge[i] = S1CountAge[i]

        #print(S1CountAge)
        #print(S2CountAge)
        #get all response for each survey
        allRespS1= Submission.objects.values('q1','q2','q3','q4','q5','q6','q7','q8','q9','q10','q11','q12','q13','q14').filter(Q(link_id=LID1[0])).all()

        #convert the querryset into dataframe
        allRespS1=df.DataFrame.from_records(allRespS1)

        #compute the crobanch alpha for each survey using the aggregated responses in dataframe form above
        CrobanchAlphaS1=cronbach_alpha(allRespS1)

        #reducing the result to two decimal places
        CrobanchAlphaS1=float("{0:.4f}".format(CrobanchAlphaS1))

        if math.isnan(CrobanchAlphaS1):
            CrobanchAlphaS1=0.0
        else:
            CrobanchAlphaS1=CrobanchAlphaS1

#compute overall trust score for each survey begins from here
        OvrallTrustS1= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q2", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q3", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q4", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q5", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q6", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q7", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q8", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q9", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q10", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q11", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q12", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q13", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q14", filter=(Q(link_id=LID1[0])), output_field=FloatField()))


        OvrallTrustS1s=[]

        for key, entry in OvrallTrustS1.items():
            if entry is None:
                   OvrallTrustS1s.append(0)
            else:
                OvrallTrustS1s.append(entry)

        OvrallTrustS1s= OvrallTrustS1s[0]

        OvrallTrustS1s= (OvrallTrustS1s*100) / (70*survey1Counts)


        OvrallTrustS1s=float("{0:.1f}".format(OvrallTrustS1s))

#computing overall risk for each survey
        OvrallRiskS1= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q2", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q3", filter=(Q(link_id=LID1[0])), output_field=FloatField())
                )


        OvrallRiskS1s=[]

        for key, entry in OvrallRiskS1.items():
            if entry is None:
                   OvrallRiskS1s.append(0)
            else:
                OvrallRiskS1s.append(entry)


        OvrallRiskS1s= OvrallRiskS1s[0]

        OvrallRiskS1s= (OvrallRiskS1s*100) / (15*survey1Counts)


        OvrallRiskS1s=float("{0:.1f}".format(OvrallRiskS1s))

#computing benevolencerisk for each survey
        OvrallBenevolenceS1= Submission.objects.aggregate(
            overalBenevolence=
                Sum("q4", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q5", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q6", filter=(Q(link_id=LID1[0])), output_field=FloatField())
                )


        OvrallBenevolenceS1s=[]

        for key, entry in OvrallBenevolenceS1.items():
            if entry is None:
                   OvrallBenevolenceS1s.append(0)
            else:
                OvrallBenevolenceS1s.append(entry)

        OvrallBenevolenceS1s= OvrallBenevolenceS1s[0]

        OvrallBenevolenceS1s= (OvrallBenevolenceS1s*100) / (15*survey1Counts)


        OvrallBenevolenceS1s=float("{0:.1f}".format(OvrallBenevolenceS1s))

# computing competence for each survey
        OvrallCompetenceS1= Submission.objects.aggregate(
            overalCompetence=
                Sum("q7", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q8", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q9", filter=(Q(link_id=LID1[0])), output_field=FloatField()))

        OvrallCompetenceS1s=[]

        for key, entry in OvrallCompetenceS1.items():
            if entry is None:
                   OvrallCompetenceS1s.append(0)
            else:
                OvrallCompetenceS1s.append(entry)

        OvrallCompetenceS1s= OvrallCompetenceS1s[0]

        OvrallCompetenceS1s= (OvrallCompetenceS1s*100) / (15*survey1Counts)


        OvrallCompetenceS1s=float("{0:.1f}".format(OvrallCompetenceS1s))

# computing reciprocity
        OvrallReciprocityS1= Submission.objects.aggregate(
            overalReciprocity=
                Sum("q10", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q11", filter=(Q(link_id=LID1[0])), output_field=FloatField()))


        OvrallReciprocityS1s=[]

        for key, entry in OvrallReciprocityS1.items():
            if entry is None:
                   OvrallReciprocityS1s.append(0)
            else:
                OvrallReciprocityS1s.append(entry)

        OvrallReciprocityS1s= OvrallReciprocityS1s[0]

        OvrallReciprocityS1s= (OvrallReciprocityS1s*100) / (10*survey1Counts)


        OvrallReciprocityS1s=float("{0:.1f}".format(OvrallReciprocityS1s))


#Computing general trust for each survey
        OvrallGeneralTrustS1= Submission.objects.aggregate(
            overalGeneralTrust=
                Sum("q12", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q13", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q14", filter=(Q(link_id=LID1[0])), output_field=FloatField()))


        OvrallGeneralTrustS1s=[]

        for key, entry in OvrallGeneralTrustS1.items():
            if entry is None:
                   OvrallGeneralTrustS1s.append(0)
            else:
                OvrallGeneralTrustS1s.append(entry)

        OvrallGeneralTrustS1s= OvrallGeneralTrustS1s[0]

        OvrallGeneralTrustS1s= (OvrallGeneralTrustS1s*100) / (15*survey1Counts)


        OvrallGeneralTrustS1s=float("{0:.1f}".format(OvrallGeneralTrustS1s))


#Riesk Q1 for both questioniares
        RiskQ1S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID1[0])), output_field=FloatField()))


        RiskQ1S1s=[]

        for key, entry in RiskQ1S1.items():
            if entry is None:
                   RiskQ1S1s.append(0)
            else:
                RiskQ1S1s.append(entry)


        RiskQ1S1s= RiskQ1S1s[0]

        RiskQ1S1s= (RiskQ1S1s*100) / (5*survey1Counts)


        RiskQ1S1s=float("{0:.1f}".format(RiskQ1S1s))

#Riesk Q2 for both questioniares
        RiskQ2S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q2", filter=(Q(link_id=LID1[0])), output_field=FloatField()))


        RiskQ2S1s=[]

        for key, entry in RiskQ2S1.items():
            if entry is None:
                   RiskQ2S1s.append(0)
            else:
                RiskQ2S1s.append(entry)


        RiskQ2S1s= RiskQ2S1s[0]

        RiskQ2S1s= (RiskQ2S1s*100) / (5*survey1Counts)


        RiskQ2S1s=float("{0:.1f}".format(RiskQ2S1s))

#Riesk Q3 for both questioniares
        RiskQ3S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q3", filter=(Q(link_id=LID1[0])), output_field=FloatField()))


        RiskQ3S1s=[]

        for key, entry in RiskQ3S1.items():
            if entry is None:
                   RiskQ3S1s.append(0)
            else:
                RiskQ3S1s.append(entry)


        RiskQ3S1s= RiskQ3S1s[0]

        RiskQ3S1s= (RiskQ3S1s*100) / (5*survey1Counts)


        RiskQ3S1s=float("{0:.1f}".format(RiskQ3S1s))


#benevolence Q1 for both questioniares
        BenevlonceQ1S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q4", filter=(Q(link_id=LID1[0])), output_field=FloatField()))


        BenevlonceQ1S1s=[]

        for key, entry in BenevlonceQ1S1.items():
            if entry is None:
                   BenevlonceQ1S1s.append(0)
            else:
                BenevlonceQ1S1s.append(entry)

        BenevlonceQ1S1s= BenevlonceQ1S1s[0]

        BenevlonceQ1S1s= (BenevlonceQ1S1s*100) / (5*survey1Counts)


        BenevlonceQ1S1s=float("{0:.1f}".format(BenevlonceQ1S1s))

#benevolence Q2 for both questioniares
        BenevlonceQ2S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q5", filter=(Q(link_id=LID1[0])), output_field=FloatField()))


        BenevlonceQ2S1s=[]

        for key, entry in BenevlonceQ2S1.items():
            if entry is None:
                   BenevlonceQ2S1s.append(0)
            else:
                BenevlonceQ2S1s.append(entry)


        BenevlonceQ2S1s= BenevlonceQ2S1s[0]

        BenevlonceQ2S1s= (BenevlonceQ2S1s*100) / (5*survey1Counts)


        BenevlonceQ2S1s=float("{0:.1f}".format(BenevlonceQ2S1s))

#benevolence Q3 for both questioniares
        BenevlonceQ3S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q6", filter=(Q(link_id=LID1[0])), output_field=FloatField()))


        BenevlonceQ3S1s=[]

        for key, entry in BenevlonceQ3S1.items():
            if entry is None:
                   BenevlonceQ3S1s.append(0)
            else:
                BenevlonceQ3S1s.append(entry)

        BenevlonceQ3S1s= BenevlonceQ3S1s[0]

        BenevlonceQ3S1s= (BenevlonceQ3S1s*100) / (5*survey1Counts)


        BenevlonceQ3S1s=float("{0:.1f}".format(BenevlonceQ3S1s))

#Riesk Q1 for both questioniares
        CompetenceQ1S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q7", filter=(Q(link_id=LID1[0])), output_field=FloatField()))

        CompetenceQ1S1s=[]

        for key, entry in CompetenceQ1S1.items():
            if entry is None:
                   CompetenceQ1S1s.append(0)
            else:
                CompetenceQ1S1s.append(entry)


        CompetenceQ1S1s= CompetenceQ1S1s[0]

        CompetenceQ1S1s= (CompetenceQ1S1s*100) / (5*survey1Counts)


        CompetenceQ1S1s=float("{0:.1f}".format(CompetenceQ1S1s))

#Riesk Q2 for both questioniares
        CompetenceQ2S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q8", filter=(Q(link_id=LID1[0])), output_field=FloatField()))


        CompetenceQ2S1s=[]

        for key, entry in CompetenceQ2S1.items():
            if entry is None:
                   CompetenceQ2S1s.append(0)
            else:
                CompetenceQ2S1s.append(entry)

        CompetenceQ2S1s= CompetenceQ2S1s[0]

        CompetenceQ2S1s= (CompetenceQ2S1s*100) / (5*survey1Counts)


        CompetenceQ2S1s=float("{0:.1f}".format(CompetenceQ2S1s))

#Riesk Q3 for both questioniares
        CompetenceQ3S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q9", filter=(Q(link_id=LID1[0])), output_field=FloatField()))


        CompetenceQ3S1s=[]

        for key, entry in CompetenceQ3S1.items():
            if entry is None:
                   CompetenceQ3S1s.append(0)
            else:
                CompetenceQ3S1s.append(entry)


        CompetenceQ3S1s= CompetenceQ3S1s[0]

        CompetenceQ3S1s= (CompetenceQ3S1s*100) / (5*survey1Counts)


        CompetenceQ3S1s=float("{0:.1f}".format(CompetenceQ3S1s))

#Recirptocity Q1 for both questioniares
        ReciprocityQ1S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q7", filter=(Q(link_id=LID1[0])), output_field=FloatField()))


        ReciprocityQ1S1s=[]

        for key, entry in ReciprocityQ1S1.items():
            if entry is None:
                   ReciprocityQ1S1s.append(0)
            else:
                ReciprocityQ1S1s.append(entry)


        ReciprocityQ1S1s= ReciprocityQ1S1s[0]

        ReciprocityQ1S1s= (ReciprocityQ1S1s*100) / (5*survey1Counts)


        ReciprocityQ1S1s=float("{0:.1f}".format(ReciprocityQ1S1s))



#Recirprocity Q2 for both questioniares
        ReciprocityQ2S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q8", filter=(Q(link_id=LID1[0])), output_field=FloatField()))

        ReciprocityQ2S1s=[]

        for key, entry in ReciprocityQ2S1.items():
            if entry is None:
                   ReciprocityQ2S1s.append(0)
            else:
                ReciprocityQ2S1s.append(entry)


        ReciprocityQ2S1s= ReciprocityQ2S1s[0]

        ReciprocityQ2S1s= (ReciprocityQ2S1s*100) / (5*survey1Counts)


        ReciprocityQ2S1s=float("{0:.1f}".format(ReciprocityQ2S1s))

#Riesk Q1 for both questioniares
        GtrustQ1S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q12", filter=(Q(link_id=LID1[0])), output_field=FloatField()))


        GtrustQ1S1s=[]

        for key, entry in GtrustQ1S1.items():
            if entry is None:
                   GtrustQ1S1s.append(0)
            else:
                GtrustQ1S1s.append(entry)


        GtrustQ1S1s= GtrustQ1S1s[0]

        GtrustQ1S1s= (GtrustQ1S1s*100) / (5*survey1Counts)


        GtrustQ1S1s=float("{0:.1f}".format(GtrustQ1S1s))

#Riesk Q2 for both questioniares
        GtrustQ2S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q13", filter=(Q(link_id=LID1[0])), output_field=FloatField()))


        GtrustQ2S1s=[]

        for key, entry in GtrustQ2S1.items():
            if entry is None:
                   GtrustQ2S1s.append(0)
            else:
                GtrustQ2S1s.append(entry)


        GtrustQ2S1s= GtrustQ2S1s[0]

        GtrustQ2S1s= (GtrustQ2S1s*100) / (5*survey1Counts)


        GtrustQ2S1s=float("{0:.1f}".format(GtrustQ2S1s))

#Riesk Q3 for both questioniares
        GtrustQ3S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q14", filter=(Q(link_id=LID1[0])), output_field=FloatField()))


        GtrustQ3S1s=[]

        for key, entry in GtrustQ3S1.items():
            if entry is None:
                   GtrustQ3S1s.append(0)
            else:
                GtrustQ3S1s.append(entry)


        GtrustQ3S1s= GtrustQ3S1s[0]

        GtrustQ3S1s= (GtrustQ3S1s*100) / (5*survey1Counts)


        GtrustQ3S1s=float("{0:.1f}".format(GtrustQ3S1s))


        return render(request, 'pie_chart1.html', {
            'project_id':project_id,
            'productname':productname,
            'survey1Counts':survey1Counts,

            'S1CountGender':S1CountGender,

            'S1CountAge':S1CountAge,

            'CrobanchAlphaS1':CrobanchAlphaS1,

            'OvrallTrustS1s':OvrallTrustS1s,

            'OvrallRiskS1s':OvrallRiskS1s,

            'OvrallBenevolenceS1s':OvrallBenevolenceS1s,

            'OvrallCompetenceS1s':OvrallCompetenceS1s,

            'OvrallReciprocityS1s':OvrallReciprocityS1s,

            'OvrallGeneralTrustS1s':OvrallGeneralTrustS1s,

            'RiskQ1S1s':RiskQ1S1s,

            'RiskQ2S1s':RiskQ2S1s,

            'RiskQ3S1s':RiskQ3S1s,

            'BenevlonceQ1S1s':BenevlonceQ1S1s,

            'BenevlonceQ2S1s':BenevlonceQ2S1s,

            'BenevlonceQ3S1s':BenevlonceQ3S1s,

            'CompetenceQ1S1s':CompetenceQ1S1s,

            'CompetenceQ2S1s':CompetenceQ2S1s,

            'CompetenceQ3S1s':CompetenceQ3S1s,

            'ReciprocityQ1S1s':ReciprocityQ1S1s,

            'ReciprocityQ2S1s':ReciprocityQ2S1s,

            'GtrustQ1S1s':GtrustQ1S1s,

            'GtrustQ2S1s':GtrustQ2S1s,

            'GtrustQ3S1s':GtrustQ3S1s


            })


    elif NumberOfSurveys==2:
        #get the link ids for the two surveys
        LID1 = Link.objects.filter(survey_id=SID[0]).values_list('id', flat=True)
        LID2 = Link.objects.filter(survey_id=SID[1]).values_list('id', flat=True)
        #get the number of respondents by survey
        S1Count = Submission.objects.aggregate(
            responseS1= Count("q1", filter=(Q(link_id=LID1[0])), output_field=IntegerField()))
        S2Count = Submission.objects.aggregate(
            responseS1= Count("q1", filter=(Q(link_id=LID2[0])), output_field=IntegerField()))
        S1Counts=[]
        S2Counts=[]
        for key, entry in S1Count.items():
            if entry is None:
                   S1Counts.append(0)
            else:
                S1Counts.append(entry)
        for key, entry in S2Count.items():
            if entry is None:
                S2Counts.append(0)
            else:
                S2Counts.append(entry)
        survey1Counts= S1Counts[0]
        survey2Counts= S2Counts[0]
        #get number gender details for each survey
        S1CountMale = AnonyData.objects.filter(link_id=LID1[0], gender="M").count()
        S1CountFeMale = AnonyData.objects.filter(link_id=LID1[0], gender="F").count()
        S1CountOthers = AnonyData.objects.filter(link_id=LID1[0], gender="O").count()

        S2CountMale = AnonyData.objects.filter(link_id=LID2[0], gender="M").count()
        S2CountFeMale = AnonyData.objects.filter(link_id=LID2[0], gender="F").count()
        S2CountOthers = AnonyData.objects.filter(link_id=LID2[0], gender="O").count()
            #appending the results to an array because the chartjs piechart expects the data in an array format
        S1CountGender = [S1CountMale, S1CountFeMale, S1CountOthers]
        S2CountGender = [S2CountMale, S2CountFeMale, S2CountOthers]
        #getting the age distribution for each survey
        #survey 1
        S1Count17Below = AnonyData.objects.filter(link_id=LID1[0], age="1").count()
        S1Count18To27 = AnonyData.objects.filter(link_id=LID1[0], age="2").count()
        S1Count28To37 = AnonyData.objects.filter(link_id=LID1[0], age="3").count()
        S1Count38To47 = AnonyData.objects.filter(link_id=LID1[0], age="4").count()
        S1Count48To57 = AnonyData.objects.filter(link_id=LID1[0], age="5").count()
        S1Count58Above = AnonyData.objects.filter(link_id=LID1[0], age="6").count()
        #survey 2
        S2Count17Below = AnonyData.objects.filter(link_id=LID2[0], age="1").count()
        S2Count18To27 = AnonyData.objects.filter(link_id=LID2[0], age="2").count()
        S2Count28To37 = AnonyData.objects.filter(link_id=LID2[0], age="3").count()
        S2Count38To47 = AnonyData.objects.filter(link_id=LID2[0], age="4").count()
        S2Count48To57 = AnonyData.objects.filter(link_id=LID2[0], age="5").count()
        S2Count58Above = AnonyData.objects.filter(link_id=LID2[0], age="6").count()
            #appending the results to an array because the chartjs piechart expects the data in an array format
        S1CountAge = [S1Count17Below, S1Count18To27, S1Count28To37, S1Count38To47, S1Count48To57, S1Count58Above ]
        S2CountAge = [S2Count17Below, S2Count18To27, S2Count28To37, S2Count38To47, S2Count48To57, S2Count58Above ]
        #check for null entries and replace them with 0
        for i in S1CountAge:
            if i == '':
                S1CountAge[i]=0
            else:
                S1CountAge[i] = S1CountAge[i]

        for i in S2CountAge:
            if i == '':
                S2CountAge[i]=0
            else:
                S2CountAge[i] = S2CountAge[i]
        #print(S1CountAge)
        #print(S2CountAge)
        #get all response for each survey
        allRespS1= Submission.objects.values('q1','q2','q3','q4','q5','q6','q7','q8','q9','q10','q11','q12','q13','q14').filter(Q(link_id=LID1[0])).all()
        allRespS2= Submission.objects.values('q1','q2','q3','q4','q5','q6','q7','q8','q9','q10','q11','q12','q13','q14').filter(Q(link_id=LID2[0])).all()
        #convert the querryset into dataframe
        allRespS1=df.DataFrame.from_records(allRespS1)
        allRespS2=df.DataFrame.from_records(allRespS2)
        #compute the crobanch alpha for each survey using the aggregated responses in dataframe form above
        CrobanchAlphaS1=cronbach_alpha(allRespS1)
        CrobanchAlphaS2=cronbach_alpha(allRespS2)
        #reducing the result to two decimal places
        CrobanchAlphaS1=float("{0:.4f}".format(CrobanchAlphaS1))
        CrobanchAlphaS2=float("{0:.4f}".format(CrobanchAlphaS2))

        if math.isnan(CrobanchAlphaS1):
            CrobanchAlphaS1=0.0
        else:
            CrobanchAlphaS1=CrobanchAlphaS1

        if math.isnan(CrobanchAlphaS2):
            CrobanchAlphaS2=0.0
        else:
            CrobanchAlphaS2=CrobanchAlphaS2

#compute overall trust score for each survey begins from here
        OvrallTrustS1= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q2", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q3", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q4", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q5", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q6", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q7", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q8", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q9", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q10", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q11", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q12", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q13", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q14", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        OvrallTrustS2= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q2", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q3", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q4", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q5", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q6", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q7", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q8", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q9", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q10", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q11", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q12", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q13", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q14", filter=(Q(link_id=LID2[0])), output_field=FloatField()))

        OvrallTrustS1s=[]
        OvrallTrustS2s=[]
        for key, entry in OvrallTrustS1.items():
            if entry is None:
                   OvrallTrustS1s.append(0)
            else:
                OvrallTrustS1s.append(entry)

        for key, entry in OvrallTrustS2.items():
            if entry is None:
                OvrallTrustS2s.append(0)
            else:
                OvrallTrustS2s.append(entry)
        OvrallTrustS1s= OvrallTrustS1s[0]
        OvrallTrustS2s= OvrallTrustS2s[0]
        OvrallTrustS1s= (OvrallTrustS1s*100) / (70*survey1Counts)
        OvrallTrustS2s= (OvrallTrustS2s*100) / (70*survey2Counts)

        OvrallTrustS1s=float("{0:.1f}".format(OvrallTrustS1s))
        OvrallTrustS2s=float("{0:.1f}".format(OvrallTrustS2s))
#computing overall risk for each survey
        OvrallRiskS1= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q2", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q3", filter=(Q(link_id=LID1[0])), output_field=FloatField())
                )
        OvrallRiskS2= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q2", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q3", filter=(Q(link_id=LID2[0])), output_field=FloatField()))

        OvrallRiskS1s=[]
        OvrallRiskS2s=[]
        for key, entry in OvrallRiskS1.items():
            if entry is None:
                   OvrallRiskS1s.append(0)
            else:
                OvrallRiskS1s.append(entry)

        for key, entry in OvrallRiskS2.items():
            if entry is None:
                OvrallRiskS2s.append(0)
            else:
                OvrallRiskS2s.append(entry)
        OvrallRiskS1s= OvrallRiskS1s[0]
        OvrallRiskS2s= OvrallRiskS2s[0]
        OvrallRiskS1s= (OvrallRiskS1s*100) / (15*survey1Counts)
        OvrallRiskS2s= (OvrallRiskS2s*100) / (15*survey2Counts)

        OvrallRiskS1s=float("{0:.1f}".format(OvrallRiskS1s))
        OvrallRiskS2s=float("{0:.1f}".format(OvrallRiskS2s))
#computing benevolencerisk for each survey
        OvrallBenevolenceS1= Submission.objects.aggregate(
            overalBenevolence=
                Sum("q4", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q5", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q6", filter=(Q(link_id=LID1[0])), output_field=FloatField())
                )
        OvrallBenevolenceS2= Submission.objects.aggregate(
            overalBenevolence=
                Sum("q4", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q5", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q6", filter=(Q(link_id=LID2[0])), output_field=FloatField()))

        OvrallBenevolenceS1s=[]
        OvrallBenevolenceS2s=[]
        for key, entry in OvrallBenevolenceS1.items():
            if entry is None:
                   OvrallBenevolenceS1s.append(0)
            else:
                OvrallBenevolenceS1s.append(entry)

        for key, entry in OvrallBenevolenceS2.items():
            if entry is None:
                OvrallBenevolenceS2s.append(0)
            else:
                OvrallBenevolenceS2s.append(entry)
        OvrallBenevolenceS1s= OvrallBenevolenceS1s[0]
        OvrallBenevolenceS2s= OvrallBenevolenceS2s[0]
        OvrallBenevolenceS1s= (OvrallBenevolenceS1s*100) / (15*survey1Counts)
        OvrallBenevolenceS2s= (OvrallBenevolenceS2s*100) / (15*survey2Counts)

        OvrallBenevolenceS1s=float("{0:.1f}".format(OvrallBenevolenceS1s))
        OvrallBenevolenceS2s=float("{0:.1f}".format(OvrallBenevolenceS2s))
# computing competence for each survey
        OvrallCompetenceS1= Submission.objects.aggregate(
            overalCompetence=
                Sum("q7", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q8", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q9", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        OvrallCompetenceS2= Submission.objects.aggregate(
            overalCompetence=
                Sum("q7", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q8", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q9", filter=(Q(link_id=LID2[0])), output_field=FloatField()))

        OvrallCompetenceS1s=[]
        OvrallCompetenceS2s=[]
        for key, entry in OvrallCompetenceS1.items():
            if entry is None:
                   OvrallCompetenceS1s.append(0)
            else:
                OvrallCompetenceS1s.append(entry)

        for key, entry in OvrallCompetenceS2.items():
            if entry is None:
                OvrallCompetenceS2s.append(0)
            else:
                OvrallCompetenceS2s.append(entry)
        OvrallCompetenceS1s= OvrallCompetenceS1s[0]
        OvrallCompetenceS2s= OvrallCompetenceS2s[0]
        OvrallCompetenceS1s= (OvrallCompetenceS1s*100) / (15*survey1Counts)
        OvrallCompetenceS2s= (OvrallCompetenceS2s*100) / (15*survey2Counts)

        OvrallCompetenceS1s=float("{0:.1f}".format(OvrallCompetenceS1s))
        OvrallCompetenceS2s=float("{0:.1f}".format(OvrallCompetenceS2s))
# computing reciprocity
        OvrallReciprocityS1= Submission.objects.aggregate(
            overalReciprocity=
                Sum("q10", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q11", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        OvrallReciprocityS2= Submission.objects.aggregate(
            overalReciprocity=
                Sum("q10", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q11", filter=(Q(link_id=LID2[0])), output_field=FloatField()))

        OvrallReciprocityS1s=[]
        OvrallReciprocityS2s=[]
        for key, entry in OvrallReciprocityS1.items():
            if entry is None:
                   OvrallReciprocityS1s.append(0)
            else:
                OvrallReciprocityS1s.append(entry)

        for key, entry in OvrallReciprocityS2.items():
            if entry is None:
                OvrallReciprocityS2s.append(0)
            else:
                OvrallReciprocityS2s.append(entry)
        OvrallReciprocityS1s= OvrallReciprocityS1s[0]
        OvrallReciprocityS2s= OvrallReciprocityS2s[0]
        OvrallReciprocityS1s= (OvrallReciprocityS1s*100) / (10*survey1Counts)
        OvrallReciprocityS2s= (OvrallReciprocityS2s*100) / (10*survey2Counts)

        OvrallReciprocityS1s=float("{0:.1f}".format(OvrallReciprocityS1s))
        OvrallReciprocityS2s=float("{0:.1f}".format(OvrallReciprocityS2s))

#Computing general trust for each survey
        OvrallGeneralTrustS1= Submission.objects.aggregate(
            overalGeneralTrust=
                Sum("q12", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q13", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q14", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        OvrallGeneralTrustS2= Submission.objects.aggregate(
            overalGeneralTrust=
                Sum("q12", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q13", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q14", filter=(Q(link_id=LID2[0])), output_field=FloatField()))

        OvrallGeneralTrustS1s=[]
        OvrallGeneralTrustS2s=[]
        for key, entry in OvrallGeneralTrustS1.items():
            if entry is None:
                   OvrallGeneralTrustS1s.append(0)
            else:
                OvrallGeneralTrustS1s.append(entry)

        for key, entry in OvrallGeneralTrustS2.items():
            if entry is None:
                OvrallGeneralTrustS2s.append(0)
            else:
                OvrallGeneralTrustS2s.append(entry)
        OvrallGeneralTrustS1s= OvrallGeneralTrustS1s[0]
        OvrallGeneralTrustS2s= OvrallGeneralTrustS2s[0]
        OvrallGeneralTrustS1s= (OvrallGeneralTrustS1s*100) / (15*survey1Counts)
        OvrallGeneralTrustS2s= (OvrallGeneralTrustS2s*100) / (15*survey2Counts)

        OvrallGeneralTrustS1s=float("{0:.1f}".format(OvrallGeneralTrustS1s))
        OvrallGeneralTrustS2s=float("{0:.1f}".format(OvrallGeneralTrustS2s))

#Riesk Q1 for both questioniares
        RiskQ1S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        RiskQ1S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID2[0])), output_field=FloatField()))

        RiskQ1S1s=[]
        RiskQ1S2s=[]
        for key, entry in RiskQ1S1.items():
            if entry is None:
                   RiskQ1S1s.append(0)
            else:
                RiskQ1S1s.append(entry)

        for key, entry in RiskQ1S2.items():
            if entry is None:
                RiskQ1S2s.append(0)
            else:
                RiskQ1S2s.append(entry)

        RiskQ1S1s= RiskQ1S1s[0]
        RiskQ1S2s= RiskQ1S2s[0]
        RiskQ1S1s= (RiskQ1S1s*100) / (5*survey1Counts)
        RiskQ1S2s= (RiskQ1S2s*100) / (5*survey2Counts)

        RiskQ1S1s=float("{0:.1f}".format(RiskQ1S1s))
        RiskQ1S2s=float("{0:.1f}".format(RiskQ1S2s))
#Riesk Q2 for both questioniares
        RiskQ2S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q2", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        RiskQ2S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q2", filter=(Q(link_id=LID2[0])), output_field=FloatField()))

        RiskQ2S1s=[]
        RiskQ2S2s=[]
        for key, entry in RiskQ2S1.items():
            if entry is None:
                   RiskQ2S1s.append(0)
            else:
                RiskQ2S1s.append(entry)

        for key, entry in RiskQ2S2.items():
            if entry is None:
                RiskQ2S2s.append(0)
            else:
                RiskQ2S2s.append(entry)

        RiskQ2S1s= RiskQ2S1s[0]
        RiskQ2S2s= RiskQ2S2s[0]
        RiskQ2S1s= (RiskQ2S1s*100) / (5*survey1Counts)
        RiskQ2S2s= (RiskQ2S2s*100) / (5*survey2Counts)

        RiskQ2S1s=float("{0:.1f}".format(RiskQ2S1s))
        RiskQ2S2s=float("{0:.1f}".format(RiskQ2S2s))
#Riesk Q3 for both questioniares
        RiskQ3S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q3", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        RiskQ3S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q3", filter=(Q(link_id=LID2[0])), output_field=FloatField()))

        RiskQ3S1s=[]
        RiskQ3S2s=[]
        for key, entry in RiskQ3S1.items():
            if entry is None:
                   RiskQ3S1s.append(0)
            else:
                RiskQ3S1s.append(entry)

        for key, entry in RiskQ3S2.items():
            if entry is None:
                RiskQ3S2s.append(0)
            else:
                RiskQ3S2s.append(entry)

        RiskQ3S1s= RiskQ3S1s[0]
        RiskQ3S2s= RiskQ3S2s[0]
        RiskQ3S1s= (RiskQ3S1s*100) / (5*survey1Counts)
        RiskQ3S2s= (RiskQ3S2s*100) / (5*survey2Counts)

        RiskQ3S1s=float("{0:.1f}".format(RiskQ3S1s))
        RiskQ3S2s=float("{0:.1f}".format(RiskQ3S2s))

#benevolence Q1 for both questioniares
        BenevlonceQ1S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q4", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        BenevlonceQ1S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q4", filter=(Q(link_id=LID2[0])), output_field=FloatField()))

        BenevlonceQ1S1s=[]
        BenevlonceQ1S2s=[]
        for key, entry in BenevlonceQ1S1.items():
            if entry is None:
                   BenevlonceQ1S1s.append(0)
            else:
                BenevlonceQ1S1s.append(entry)

        for key, entry in BenevlonceQ1S2.items():
            if entry is None:
                BenevlonceQ1S2s.append(0)
            else:
                BenevlonceQ1S2s.append(entry)

        BenevlonceQ1S1s= BenevlonceQ1S1s[0]
        BenevlonceQ1S2s= BenevlonceQ1S2s[0]
        BenevlonceQ1S1s= (BenevlonceQ1S1s*100) / (5*survey1Counts)
        BenevlonceQ1S2s= (BenevlonceQ1S2s*100) / (5*survey2Counts)

        BenevlonceQ1S1s=float("{0:.1f}".format(BenevlonceQ1S1s))
        BenevlonceQ1S2s=float("{0:.1f}".format(BenevlonceQ1S2s))
#benevolence Q2 for both questioniares
        BenevlonceQ2S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q5", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        BenevlonceQ2S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q5", filter=(Q(link_id=LID2[0])), output_field=FloatField()))

        BenevlonceQ2S1s=[]
        BenevlonceQ2S2s=[]
        for key, entry in BenevlonceQ2S1.items():
            if entry is None:
                   BenevlonceQ2S1s.append(0)
            else:
                BenevlonceQ2S1s.append(entry)

        for key, entry in BenevlonceQ2S2.items():
            if entry is None:
                BenevlonceQ2S2s.append(0)
            else:
                BenevlonceQ2S2s.append(entry)

        BenevlonceQ2S1s= BenevlonceQ2S1s[0]
        BenevlonceQ2S2s= BenevlonceQ2S2s[0]
        BenevlonceQ2S1s= (BenevlonceQ2S1s*100) / (5*survey1Counts)
        BenevlonceQ2S2s= (BenevlonceQ2S2s*100) / (5*survey2Counts)

        BenevlonceQ2S1s=float("{0:.1f}".format(BenevlonceQ2S1s))
        BenevlonceQ2S2s=float("{0:.1f}".format(BenevlonceQ2S2s))
#benevolence Q3 for both questioniares
        BenevlonceQ3S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q6", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        BenevlonceQ3S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q6", filter=(Q(link_id=LID2[0])), output_field=FloatField()))

        BenevlonceQ3S1s=[]
        BenevlonceQ3S2s=[]
        for key, entry in BenevlonceQ3S1.items():
            if entry is None:
                   BenevlonceQ3S1s.append(0)
            else:
                BenevlonceQ3S1s.append(entry)

        for key, entry in BenevlonceQ3S2.items():
            if entry is None:
                BenevlonceQ3S2s.append(0)
            else:
                BenevlonceQ3S2s.append(entry)

        BenevlonceQ3S1s= BenevlonceQ3S1s[0]
        BenevlonceQ3S2s= BenevlonceQ3S2s[0]
        BenevlonceQ3S1s= (BenevlonceQ3S1s*100) / (5*survey1Counts)
        BenevlonceQ3S2s= (BenevlonceQ3S2s*100) / (5*survey2Counts)

        BenevlonceQ3S1s=float("{0:.1f}".format(BenevlonceQ3S1s))
        BenevlonceQ3S2s=float("{0:.1f}".format(BenevlonceQ3S2s))
#Riesk Q1 for both questioniares
        CompetenceQ1S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q7", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        CompetenceQ1S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q7", filter=(Q(link_id=LID2[0])), output_field=FloatField()))

        CompetenceQ1S1s=[]
        CompetenceQ1S2s=[]
        for key, entry in CompetenceQ1S1.items():
            if entry is None:
                   CompetenceQ1S1s.append(0)
            else:
                CompetenceQ1S1s.append(entry)

        for key, entry in CompetenceQ1S2.items():
            if entry is None:
                CompetenceQ1S2s.append(0)
            else:
                CompetenceQ1S2s.append(entry)

        CompetenceQ1S1s= CompetenceQ1S1s[0]
        CompetenceQ1S2s= CompetenceQ1S2s[0]
        CompetenceQ1S1s= (CompetenceQ1S1s*100) / (5*survey1Counts)
        CompetenceQ1S2s= (CompetenceQ1S2s*100) / (5*survey2Counts)

        CompetenceQ1S1s=float("{0:.1f}".format(CompetenceQ1S1s))
        CompetenceQ1S2s=float("{0:.1f}".format(CompetenceQ1S2s))
        print(CompetenceQ1S1s)
#Riesk Q2 for both questioniares
        CompetenceQ2S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q8", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        CompetenceQ2S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q8", filter=(Q(link_id=LID2[0])), output_field=FloatField()))

        CompetenceQ2S1s=[]
        CompetenceQ2S2s=[]
        for key, entry in CompetenceQ2S1.items():
            if entry is None:
                   CompetenceQ2S1s.append(0)
            else:
                CompetenceQ2S1s.append(entry)

        for key, entry in CompetenceQ2S2.items():
            if entry is None:
                CompetenceQ2S2s.append(0)
            else:
                CompetenceQ2S2s.append(entry)

        CompetenceQ2S1s= CompetenceQ2S1s[0]
        CompetenceQ2S2s= CompetenceQ2S2s[0]
        CompetenceQ2S1s= (CompetenceQ2S1s*100) / (5*survey1Counts)
        CompetenceQ2S2s= (CompetenceQ2S2s*100) / (5*survey2Counts)

        CompetenceQ2S1s=float("{0:.1f}".format(CompetenceQ2S1s))
        CompetenceQ2S2s=float("{0:.1f}".format(CompetenceQ2S2s))
#Riesk Q3 for both questioniares
        CompetenceQ3S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q9", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        CompetenceQ3S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q9", filter=(Q(link_id=LID2[0])), output_field=FloatField()))

        CompetenceQ3S1s=[]
        CompetenceQ3S2s=[]
        for key, entry in CompetenceQ3S1.items():
            if entry is None:
                   CompetenceQ3S1s.append(0)
            else:
                CompetenceQ3S1s.append(entry)

        for key, entry in CompetenceQ3S2.items():
            if entry is None:
                CompetenceQ3S2s.append(0)
            else:
                CompetenceQ3S2s.append(entry)

        CompetenceQ3S1s= CompetenceQ3S1s[0]
        CompetenceQ3S2s= CompetenceQ3S2s[0]
        CompetenceQ3S1s= (CompetenceQ3S1s*100) / (5*survey1Counts)
        CompetenceQ3S2s= (CompetenceQ3S2s*100) / (5*survey2Counts)

        CompetenceQ3S1s=float("{0:.1f}".format(CompetenceQ3S1s))
        CompetenceQ3S2s=float("{0:.1f}".format(CompetenceQ3S2s))
#Recirptocity Q1 for both questioniares
        ReciprocityQ1S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q7", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        ReciprocityQ1S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q7", filter=(Q(link_id=LID2[0])), output_field=FloatField()))

        ReciprocityQ1S1s=[]
        ReciprocityQ1S2s=[]
        for key, entry in ReciprocityQ1S1.items():
            if entry is None:
                   ReciprocityQ1S1s.append(0)
            else:
                ReciprocityQ1S1s.append(entry)

        for key, entry in ReciprocityQ1S2.items():
            if entry is None:
                ReciprocityQ1S2s.append(0)
            else:
                ReciprocityQ1S2s.append(entry)

        ReciprocityQ1S1s= ReciprocityQ1S1s[0]
        ReciprocityQ1S2s= ReciprocityQ1S2s[0]
        ReciprocityQ1S1s= (ReciprocityQ1S1s*100) / (5*survey1Counts)
        ReciprocityQ1S2s= (ReciprocityQ1S2s*100) / (5*survey2Counts)

        ReciprocityQ1S1s=float("{0:.1f}".format(ReciprocityQ1S1s))
        ReciprocityQ1S2s=float("{0:.1f}".format(ReciprocityQ1S2s))


#Recirprocity Q2 for both questioniares
        ReciprocityQ2S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q8", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        ReciprocityQ2S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q8", filter=(Q(link_id=LID2[0])), output_field=FloatField()))

        ReciprocityQ2S1s=[]
        ReciprocityQ2S2s=[]
        for key, entry in ReciprocityQ2S1.items():
            if entry is None:
                   ReciprocityQ2S1s.append(0)
            else:
                ReciprocityQ2S1s.append(entry)

        for key, entry in ReciprocityQ2S2.items():
            if entry is None:
                ReciprocityQ2S2s.append(0)
            else:
                ReciprocityQ2S2s.append(entry)

        ReciprocityQ2S1s= ReciprocityQ2S1s[0]
        ReciprocityQ2S2s= ReciprocityQ2S2s[0]
        ReciprocityQ2S1s= (ReciprocityQ2S1s*100) / (5*survey1Counts)
        ReciprocityQ2S2s= (ReciprocityQ2S2s*100) / (5*survey2Counts)

        ReciprocityQ2S1s=float("{0:.1f}".format(ReciprocityQ2S1s))
        ReciprocityQ2S2s=float("{0:.1f}".format(ReciprocityQ2S2s))
#Riesk Q1 for both questioniares
        GtrustQ1S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q12", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        GtrustQ1S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q12", filter=(Q(link_id=LID2[0])), output_field=FloatField()))

        GtrustQ1S1s=[]
        GtrustQ1S2s=[]
        for key, entry in GtrustQ1S1.items():
            if entry is None:
                   GtrustQ1S1s.append(0)
            else:
                GtrustQ1S1s.append(entry)

        for key, entry in GtrustQ1S2.items():
            if entry is None:
                GtrustQ1S2s.append(0)
            else:
                GtrustQ1S2s.append(entry)

        GtrustQ1S1s= GtrustQ1S1s[0]
        GtrustQ1S2s= GtrustQ1S2s[0]
        GtrustQ1S1s= (GtrustQ1S1s*100) / (5*survey1Counts)
        GtrustQ1S2s= (GtrustQ1S2s*100) / (5*survey2Counts)

        GtrustQ1S1s=float("{0:.1f}".format(GtrustQ1S1s))
        GtrustQ1S2s=float("{0:.1f}".format(GtrustQ1S2s))
#Riesk Q2 for both questioniares
        GtrustQ2S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q13", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        GtrustQ2S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q13", filter=(Q(link_id=LID2[0])), output_field=FloatField()))

        GtrustQ2S1s=[]
        GtrustQ2S2s=[]
        for key, entry in GtrustQ2S1.items():
            if entry is None:
                   GtrustQ2S1s.append(0)
            else:
                GtrustQ2S1s.append(entry)

        for key, entry in GtrustQ2S2.items():
            if entry is None:
                GtrustQ2S2s.append(0)
            else:
                GtrustQ2S2s.append(entry)

        GtrustQ2S1s= GtrustQ2S1s[0]
        GtrustQ2S2s= GtrustQ2S2s[0]
        GtrustQ2S1s= (GtrustQ2S1s*100) / (5*survey1Counts)
        GtrustQ2S2s= (GtrustQ2S2s*100) / (5*survey2Counts)

        GtrustQ2S1s=float("{0:.1f}".format(GtrustQ2S1s))
        GtrustQ2S2s=float("{0:.1f}".format(GtrustQ2S2s))
#Riesk Q3 for both questioniares
        GtrustQ3S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q14", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        GtrustQ3S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q14", filter=(Q(link_id=LID2[0])), output_field=FloatField()))

        GtrustQ3S1s=[]
        GtrustQ3S2s=[]
        for key, entry in GtrustQ3S1.items():
            if entry is None:
                   GtrustQ3S1s.append(0)
            else:
                GtrustQ3S1s.append(entry)

        for key, entry in GtrustQ3S2.items():
            if entry is None:
                GtrustQ3S2s.append(0)
            else:
                GtrustQ3S2s.append(entry)

        GtrustQ3S1s= GtrustQ3S1s[0]
        GtrustQ3S2s= GtrustQ3S2s[0]
        GtrustQ3S1s= (GtrustQ3S1s*100) / (5*survey1Counts)
        GtrustQ3S2s= (GtrustQ3S2s*100) / (5*survey2Counts)

        GtrustQ3S1s=float("{0:.1f}".format(GtrustQ3S1s))
        GtrustQ3S2s=float("{0:.1f}".format(GtrustQ3S2s))

        return render(request, 'pie_chart2.html', {
            'project_id':project_id,
            'productname':productname,
            'survey1Counts':survey1Counts,
            'survey2Counts':survey2Counts,
            'S1CountGender':S1CountGender,
            'S2CountGender':S2CountGender,
            'S1CountAge':S1CountAge,
            'S2CountAge':S2CountAge,
            'CrobanchAlphaS1':CrobanchAlphaS1,
            'CrobanchAlphaS2':CrobanchAlphaS2,
            'OvrallTrustS1s':OvrallTrustS1s,
            'OvrallTrustS2s':OvrallTrustS2s,
            'OvrallRiskS1s':OvrallRiskS1s,
            'OvrallRiskS2s':OvrallRiskS2s,
            'OvrallBenevolenceS1s':OvrallBenevolenceS1s,
            'OvrallBenevolenceS2s':OvrallBenevolenceS2s,
            'OvrallCompetenceS1s':OvrallCompetenceS1s,
            'OvrallCompetenceS2s':OvrallCompetenceS2s,
            'OvrallReciprocityS1s':OvrallReciprocityS1s,
            'OvrallReciprocityS2s':OvrallReciprocityS2s,
            'OvrallGeneralTrustS1s':OvrallGeneralTrustS1s,
            'OvrallGeneralTrustS2s':OvrallGeneralTrustS2s,
            'RiskQ1S1s':RiskQ1S1s,
            'RiskQ1S2s':RiskQ1S2s,
            'RiskQ2S1s':RiskQ2S1s,
            'RiskQ2S2s':RiskQ2S2s,
            'RiskQ3S1s':RiskQ3S1s,
            'RiskQ3S2s':RiskQ3S2s,
            'BenevlonceQ1S1s':BenevlonceQ1S1s,
            'BenevlonceQ1S2s':BenevlonceQ1S2s,
            'BenevlonceQ2S1s':BenevlonceQ2S1s,
            'BenevlonceQ2S2s':BenevlonceQ2S2s,
            'BenevlonceQ3S1s':BenevlonceQ3S1s,
            'BenevlonceQ3S2s':BenevlonceQ3S2s,
            'CompetenceQ1S1s':CompetenceQ1S1s,
            'CompetenceQ1S2s':CompetenceQ1S2s,
            'CompetenceQ2S1s':CompetenceQ2S1s,
            'CompetenceQ2S2s':CompetenceQ2S2s,
            'CompetenceQ3S1s':CompetenceQ3S1s,
            'CompetenceQ3S2s':CompetenceQ3S2s,
            'ReciprocityQ1S1s':ReciprocityQ1S1s,
            'ReciprocityQ1S2s':ReciprocityQ1S2s,
            'ReciprocityQ2S1s':ReciprocityQ2S1s,
            'ReciprocityQ2S2s':ReciprocityQ2S2s,
            'GtrustQ1S1s':GtrustQ1S1s,
            'GtrustQ1S2s':GtrustQ1S2s,
            'GtrustQ2S1s':GtrustQ2S1s,
            'GtrustQ2S2s':GtrustQ2S2s,
            'GtrustQ3S1s':GtrustQ3S1s,
            'GtrustQ3S2s':GtrustQ3S2s

            })

    elif NumberOfSurveys==3:
        #get the link ids for the two surveys
        LID1 = Link.objects.filter(survey_id=SID[0]).values_list('id', flat=True)
        LID2 = Link.objects.filter(survey_id=SID[1]).values_list('id', flat=True)
        LID3 = Link.objects.filter(survey_id=SID[2]).values_list('id', flat=True)
        #get the number of respondents by survey
        S1Count = Submission.objects.aggregate(
            responseS1= Count("q1", filter=(Q(link_id=LID1[0])), output_field=IntegerField()))
        S2Count = Submission.objects.aggregate(
            responseS1= Count("q1", filter=(Q(link_id=LID2[0])), output_field=IntegerField()))
        S3Count = Submission.objects.aggregate(
            responseS1= Count("q1", filter=(Q(link_id=LID3[0])), output_field=IntegerField()))
        S1Counts=[]
        S2Counts=[]
        S3Counts=[]
        for key, entry in S1Count.items():
            if entry is None:
                   S1Counts.append(0)
            else:
                S1Counts.append(entry)
        for key, entry in S2Count.items():
            if entry is None:
                S2Counts.append(0)
            else:
                S2Counts.append(entry)
        for key, entry in S3Count.items():
            if entry is None:
                S3Counts.append(0)
            else:
                S3Counts.append(entry)
        survey1Counts= S1Counts[0]
        survey2Counts= S2Counts[0]
        survey3Counts= S3Counts[0]

        #get number gender details for each survey
        S1CountMale = AnonyData.objects.filter(link_id=LID1[0], gender="M").count()
        S1CountFeMale = AnonyData.objects.filter(link_id=LID1[0], gender="F").count()
        S1CountOthers = AnonyData.objects.filter(link_id=LID1[0], gender="O").count()

        S2CountMale = AnonyData.objects.filter(link_id=LID2[0], gender="M").count()
        S2CountFeMale = AnonyData.objects.filter(link_id=LID2[0], gender="F").count()
        S2CountOthers = AnonyData.objects.filter(link_id=LID2[0], gender="O").count()

        S3CountMale = AnonyData.objects.filter(link_id=LID3[0], gender="M").count()
        S3CountFeMale = AnonyData.objects.filter(link_id=LID3[0], gender="F").count()
        S3CountOthers = AnonyData.objects.filter(link_id=LID3[0], gender="O").count()
            #appending the results to an array because the chartjs piechart expects the data in an array format
        S1CountGender = [S1CountMale, S1CountFeMale, S1CountOthers]
        S2CountGender = [S2CountMale, S2CountFeMale, S2CountOthers]
        S3CountGender = [S3CountMale, S3CountFeMale, S3CountOthers]
        print(S1CountGender)
        print(S2CountGender)
        print(S3CountGender)
        #getting the age distribution for each survey
        #survey 1
        S1Count17Below = AnonyData.objects.filter(link_id=LID1[0], age="1").count()
        S1Count18To27 = AnonyData.objects.filter(link_id=LID1[0], age="2").count()
        S1Count28To37 = AnonyData.objects.filter(link_id=LID1[0], age="3").count()
        S1Count38To47 = AnonyData.objects.filter(link_id=LID1[0], age="4").count()
        S1Count48To57 = AnonyData.objects.filter(link_id=LID1[0], age="5").count()
        S1Count58Above = AnonyData.objects.filter(link_id=LID1[0], age="6").count()
        #survey 2
        S2Count17Below = AnonyData.objects.filter(link_id=LID2[0], age="1").count()
        S2Count18To27 = AnonyData.objects.filter(link_id=LID2[0], age="2").count()
        S2Count28To37 = AnonyData.objects.filter(link_id=LID2[0], age="3").count()
        S2Count38To47 = AnonyData.objects.filter(link_id=LID2[0], age="4").count()
        S2Count48To57 = AnonyData.objects.filter(link_id=LID2[0], age="5").count()
        S2Count58Above = AnonyData.objects.filter(link_id=LID2[0], age="6").count()
        #survey 3
        S3Count17Below = AnonyData.objects.filter(link_id=LID3[0], age="1").count()
        S3Count18To27 = AnonyData.objects.filter(link_id=LID3[0], age="2").count()
        S3Count28To37 = AnonyData.objects.filter(link_id=LID3[0], age="3").count()
        S3Count38To47 = AnonyData.objects.filter(link_id=LID3[0], age="4").count()
        S3Count48To57 = AnonyData.objects.filter(link_id=LID3[0], age="5").count()
        S3Count58Above = AnonyData.objects.filter(link_id=LID3[0], age="6").count()
            #appending the results to an array because the chartjs piechart expects the data in an array format
        S1CountAge = [S1Count17Below, S1Count18To27, S1Count28To37, S1Count38To47, S1Count48To57, S1Count58Above ]
        S2CountAge = [S2Count17Below, S2Count18To27, S2Count28To37, S2Count38To47, S2Count48To57, S2Count58Above ]
        S3CountAge = [S3Count17Below, S3Count18To27, S3Count28To37, S3Count38To47, S3Count48To57, S3Count58Above ]
        #check for null entries and replace them with 0
        for i in S1CountAge:
            if i == '':
                S1CountAge[i]=0
            else:
                S1CountAge[i] = S1CountAge[i]

        for i in S2CountAge:
            if i == '':
                S2CountAge[i]=0
            else:
                S2CountAge[i] = S2CountAge[i]

        for i in S3CountAge:
            if i == '':
                S3CountAge[i]=0
            else:
                S3CountAge[i] = S2CountAge[i]
        #print(S1CountAge)
        #print(S2CountAge)
        #get all response for each survey
        allRespS1= Submission.objects.values('q1','q2','q3','q4','q5','q6','q7','q8','q9','q10','q11','q12','q13','q14').filter(Q(link_id=LID1[0])).all()
        allRespS2= Submission.objects.values('q1','q2','q3','q4','q5','q6','q7','q8','q9','q10','q11','q12','q13','q14').filter(Q(link_id=LID2[0])).all()
        allRespS3= Submission.objects.values('q1','q2','q3','q4','q5','q6','q7','q8','q9','q10','q11','q12','q13','q14').filter(Q(link_id=LID3[0])).all()
        #convert the querryset into dataframe
        allRespS1=df.DataFrame.from_records(allRespS1)
        allRespS2=df.DataFrame.from_records(allRespS2)
        allRespS3=df.DataFrame.from_records(allRespS3)
        #compute the crobanch alpha for each survey using the aggregated responses in dataframe form above
        CrobanchAlphaS1=cronbach_alpha(allRespS1)
        CrobanchAlphaS2=cronbach_alpha(allRespS2)
        CrobanchAlphaS3=cronbach_alpha(allRespS3)
        #reducing the result to two decimal places
        CrobanchAlphaS1=float("{0:.4f}".format(CrobanchAlphaS1))
        CrobanchAlphaS2=float("{0:.4f}".format(CrobanchAlphaS2))
        CrobanchAlphaS3=float("{0:.4f}".format(CrobanchAlphaS3))

        if math.isnan(CrobanchAlphaS1):
            CrobanchAlphaS1=0.0
        else:
            CrobanchAlphaS1=CrobanchAlphaS1

        if math.isnan(CrobanchAlphaS2):
            CrobanchAlphaS2=0.0
        else:
            CrobanchAlphaS2=CrobanchAlphaS2

        if math.isnan(CrobanchAlphaS3):
            CrobanchAlphaS3=0.0
        else:
            CrobanchAlphaS3=CrobanchAlphaS3
#compute overall trust score for each survey begins from here
        OvrallTrustS1= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q2", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q3", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q4", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q5", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q6", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q7", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q8", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q9", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q10", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q11", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q12", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q13", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q14", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        OvrallTrustS2= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q2", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q3", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q4", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q5", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q6", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q7", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q8", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q9", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q10", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q11", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q12", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q13", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q14", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        OvrallTrustS3= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q2", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q3", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q4", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q5", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q6", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q7", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q8", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q9", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q10", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q11", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q12", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q13", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q14", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        OvrallTrustS1s=[]
        OvrallTrustS2s=[]
        OvrallTrustS3s=[]
        for key, entry in OvrallTrustS1.items():
            if entry is None:
                   OvrallTrustS1s.append(0)
            else:
                OvrallTrustS1s.append(entry)

        for key, entry in OvrallTrustS2.items():
            if entry is None:
                OvrallTrustS2s.append(0)
            else:
                OvrallTrustS2s.append(entry)

        for key, entry in OvrallTrustS3.items():
            if entry is None:
                OvrallTrustS3s.append(0)
            else:
                OvrallTrustS3s.append(entry)

        OvrallTrustS1s= OvrallTrustS1s[0]
        OvrallTrustS2s= OvrallTrustS2s[0]
        OvrallTrustS3s= OvrallTrustS3s[0]
        OvrallTrustS1s= (OvrallTrustS1s*100) / (70*survey1Counts)
        OvrallTrustS2s= (OvrallTrustS2s*100) / (70*survey2Counts)
        OvrallTrustS3s= (OvrallTrustS3s*100) / (70*survey3Counts)

        OvrallTrustS1s=float("{0:.1f}".format(OvrallTrustS1s))
        OvrallTrustS2s=float("{0:.1f}".format(OvrallTrustS2s))
        OvrallTrustS3s=float("{0:.1f}".format(OvrallTrustS3s))
#computing overall risk for each survey
        OvrallRiskS1= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q2", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q3", filter=(Q(link_id=LID1[0])), output_field=FloatField())
                )
        OvrallRiskS2= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q2", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q3", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        OvrallRiskS3= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q2", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q3", filter=(Q(link_id=LID3[0])), output_field=FloatField()))

        OvrallRiskS1s=[]
        OvrallRiskS2s=[]
        OvrallRiskS3s=[]
        for key, entry in OvrallRiskS1.items():
            if entry is None:
                   OvrallRiskS1s.append(0)
            else:
                OvrallRiskS1s.append(entry)

        for key, entry in OvrallRiskS2.items():
            if entry is None:
                OvrallRiskS2s.append(0)
            else:
                OvrallRiskS2s.append(entry)

        for key, entry in OvrallRiskS3.items():
            if entry is None:
                OvrallRiskS3s.append(0)
            else:
                OvrallRiskS3s.append(entry)
        OvrallRiskS1s= OvrallRiskS1s[0]
        OvrallRiskS2s= OvrallRiskS2s[0]
        OvrallRiskS3s= OvrallRiskS3s[0]
        OvrallRiskS1s= (OvrallRiskS1s*100) / (15*survey1Counts)
        OvrallRiskS2s= (OvrallRiskS2s*100) / (15*survey2Counts)
        OvrallRiskS3s= (OvrallRiskS3s*100) / (15*survey3Counts)

        OvrallRiskS1s=float("{0:.1f}".format(OvrallRiskS1s))
        OvrallRiskS2s=float("{0:.1f}".format(OvrallRiskS2s))
        OvrallRiskS3s=float("{0:.1f}".format(OvrallRiskS3s))
#computing benevolencerisk for each survey
        OvrallBenevolenceS1= Submission.objects.aggregate(
            overalBenevolence=
                Sum("q4", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q5", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q6", filter=(Q(link_id=LID1[0])), output_field=FloatField())
                )
        OvrallBenevolenceS2= Submission.objects.aggregate(
            overalBenevolence=
                Sum("q4", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q5", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q6", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        OvrallBenevolenceS3= Submission.objects.aggregate(
            overalBenevolence=
                Sum("q4", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q5", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q6", filter=(Q(link_id=LID3[0])), output_field=FloatField()))

        OvrallBenevolenceS1s=[]
        OvrallBenevolenceS2s=[]
        OvrallBenevolenceS3s=[]
        for key, entry in OvrallBenevolenceS1.items():
            if entry is None:
                   OvrallBenevolenceS1s.append(0)
            else:
                OvrallBenevolenceS1s.append(entry)

        for key, entry in OvrallBenevolenceS2.items():
            if entry is None:
                OvrallBenevolenceS2s.append(0)
            else:
                OvrallBenevolenceS2s.append(entry)

        for key, entry in OvrallBenevolenceS3.items():
            if entry is None:
                OvrallBenevolenceS3s.append(0)
            else:
                OvrallBenevolenceS3s.append(entry)
        OvrallBenevolenceS1s= OvrallBenevolenceS1s[0]
        OvrallBenevolenceS2s= OvrallBenevolenceS2s[0]
        OvrallBenevolenceS3s= OvrallBenevolenceS3s[0]
        OvrallBenevolenceS1s= (OvrallBenevolenceS1s*100) / (15*survey1Counts)
        OvrallBenevolenceS2s= (OvrallBenevolenceS2s*100) / (15*survey2Counts)
        OvrallBenevolenceS3s= (OvrallBenevolenceS3s*100) / (15*survey3Counts)

        OvrallBenevolenceS1s=float("{0:.1f}".format(OvrallBenevolenceS1s))
        OvrallBenevolenceS2s=float("{0:.1f}".format(OvrallBenevolenceS2s))
        OvrallBenevolenceS3s=float("{0:.1f}".format(OvrallBenevolenceS3s))
# computing competence for each survey
        OvrallCompetenceS1= Submission.objects.aggregate(
            overalCompetence=
                Sum("q7", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q8", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q9", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        OvrallCompetenceS2= Submission.objects.aggregate(
            overalCompetence=
                Sum("q7", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q8", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q9", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        OvrallCompetenceS3= Submission.objects.aggregate(
            overalCompetence=
                Sum("q7", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q8", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q9", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        OvrallCompetenceS1s=[]
        OvrallCompetenceS2s=[]
        OvrallCompetenceS3s=[]
        for key, entry in OvrallCompetenceS1.items():
            if entry is None:
                   OvrallCompetenceS1s.append(0)
            else:
                OvrallCompetenceS1s.append(entry)

        for key, entry in OvrallCompetenceS2.items():
            if entry is None:
                OvrallCompetenceS2s.append(0)
            else:
                OvrallCompetenceS2s.append(entry)
        for key, entry in OvrallCompetenceS3.items():
            if entry is None:
                OvrallCompetenceS3s.append(0)
            else:
                OvrallCompetenceS3s.append(entry)
        OvrallCompetenceS1s= OvrallCompetenceS1s[0]
        OvrallCompetenceS2s= OvrallCompetenceS2s[0]
        OvrallCompetenceS3s= OvrallCompetenceS3s[0]
        OvrallCompetenceS1s= (OvrallCompetenceS1s*100) / (15*survey1Counts)
        OvrallCompetenceS2s= (OvrallCompetenceS2s*100) / (15*survey2Counts)
        OvrallCompetenceS3s= (OvrallCompetenceS3s*100) / (15*survey3Counts)

        OvrallCompetenceS1s=float("{0:.1f}".format(OvrallCompetenceS1s))
        OvrallCompetenceS2s=float("{0:.1f}".format(OvrallCompetenceS2s))
        OvrallCompetenceS3s=float("{0:.1f}".format(OvrallCompetenceS3s))
# computing reciprocity
        OvrallReciprocityS1= Submission.objects.aggregate(
            overalReciprocity=
                Sum("q10", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q11", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        OvrallReciprocityS2= Submission.objects.aggregate(
            overalReciprocity=
                Sum("q10", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q11", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        OvrallReciprocityS3= Submission.objects.aggregate(
            overalReciprocity=
                Sum("q10", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q11", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        OvrallReciprocityS1s=[]
        OvrallReciprocityS2s=[]
        OvrallReciprocityS3s=[]
        for key, entry in OvrallReciprocityS1.items():
            if entry is None:
                   OvrallReciprocityS1s.append(0)
            else:
                OvrallReciprocityS1s.append(entry)

        for key, entry in OvrallReciprocityS2.items():
            if entry is None:
                OvrallReciprocityS2s.append(0)
            else:
                OvrallReciprocityS2s.append(entry)

        for key, entry in OvrallReciprocityS3.items():
            if entry is None:
                OvrallReciprocityS3s.append(0)
            else:
                OvrallReciprocityS3s.append(entry)

        OvrallReciprocityS1s= OvrallReciprocityS1s[0]
        OvrallReciprocityS2s= OvrallReciprocityS2s[0]
        OvrallReciprocityS3s= OvrallReciprocityS3s[0]
        OvrallReciprocityS1s= (OvrallReciprocityS1s*100) / (10*survey1Counts)
        OvrallReciprocityS2s= (OvrallReciprocityS2s*100) / (10*survey2Counts)
        OvrallReciprocityS3s= (OvrallReciprocityS3s*100) / (10*survey3Counts)

        OvrallReciprocityS1s=float("{0:.1f}".format(OvrallReciprocityS1s))
        OvrallReciprocityS2s=float("{0:.1f}".format(OvrallReciprocityS2s))
        OvrallReciprocityS3s=float("{0:.1f}".format(OvrallReciprocityS3s))

#Computing general trust for each survey
        OvrallGeneralTrustS1= Submission.objects.aggregate(
            overalGeneralTrust=
                Sum("q12", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q13", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q14", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        OvrallGeneralTrustS2= Submission.objects.aggregate(
            overalGeneralTrust=
                Sum("q12", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q13", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q14", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        OvrallGeneralTrustS3= Submission.objects.aggregate(
            overalGeneralTrust=
                Sum("q12", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q13", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q14", filter=(Q(link_id=LID3[0])), output_field=FloatField()))

        OvrallGeneralTrustS1s=[]
        OvrallGeneralTrustS2s=[]
        OvrallGeneralTrustS3s=[]
        for key, entry in OvrallGeneralTrustS1.items():
            if entry is None:
                   OvrallGeneralTrustS1s.append(0)
            else:
                OvrallGeneralTrustS1s.append(entry)

        for key, entry in OvrallGeneralTrustS2.items():
            if entry is None:
                OvrallGeneralTrustS2s.append(0)
            else:
                OvrallGeneralTrustS2s.append(entry)

        for key, entry in OvrallGeneralTrustS3.items():
            if entry is None:
                OvrallGeneralTrustS3s.append(0)
            else:
                OvrallGeneralTrustS3s.append(entry)
        OvrallGeneralTrustS1s= OvrallGeneralTrustS1s[0]
        OvrallGeneralTrustS2s= OvrallGeneralTrustS2s[0]
        OvrallGeneralTrustS3s= OvrallGeneralTrustS3s[0]
        OvrallGeneralTrustS1s= (OvrallGeneralTrustS1s*100) / (15*survey1Counts)
        OvrallGeneralTrustS2s= (OvrallGeneralTrustS2s*100) / (15*survey2Counts)
        OvrallGeneralTrustS3s= (OvrallGeneralTrustS3s*100) / (15*survey3Counts)

        OvrallGeneralTrustS1s=float("{0:.1f}".format(OvrallGeneralTrustS1s))
        OvrallGeneralTrustS2s=float("{0:.1f}".format(OvrallGeneralTrustS2s))
        OvrallGeneralTrustS3s=float("{0:.1f}".format(OvrallGeneralTrustS3s))

#Riesk Q1 for both questioniares
        RiskQ1S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        RiskQ1S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        RiskQ1S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID3[0])), output_field=FloatField()))

        RiskQ1S1s=[]
        RiskQ1S2s=[]
        RiskQ1S3s=[]
        for key, entry in RiskQ1S1.items():
            if entry is None:
                   RiskQ1S1s.append(0)
            else:
                RiskQ1S1s.append(entry)

        for key, entry in RiskQ1S2.items():
            if entry is None:
                RiskQ1S2s.append(0)
            else:
                RiskQ1S2s.append(entry)

        for key, entry in RiskQ1S3.items():
            if entry is None:
                RiskQ1S3s.append(0)
            else:
                RiskQ1S3s.append(entry)

        RiskQ1S1s= RiskQ1S1s[0]
        RiskQ1S2s= RiskQ1S2s[0]
        RiskQ1S3s= RiskQ1S3s[0]
        RiskQ1S1s= (RiskQ1S1s*100) / (5*survey1Counts)
        RiskQ1S2s= (RiskQ1S2s*100) / (5*survey2Counts)
        RiskQ1S3s= (RiskQ1S3s*100) / (5*survey3Counts)

        RiskQ1S1s=float("{0:.1f}".format(RiskQ1S1s))
        RiskQ1S2s=float("{0:.1f}".format(RiskQ1S2s))
        RiskQ1S3s=float("{0:.1f}".format(RiskQ1S3s))
#Riesk Q2 for both questioniares
        RiskQ2S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q2", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        RiskQ2S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q2", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        RiskQ2S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q2", filter=(Q(link_id=LID3[0])), output_field=FloatField()))

        RiskQ2S1s=[]
        RiskQ2S2s=[]
        RiskQ2S3s=[]
        for key, entry in RiskQ2S1.items():
            if entry is None:
                   RiskQ2S1s.append(0)
            else:
                RiskQ2S1s.append(entry)

        for key, entry in RiskQ2S2.items():
            if entry is None:
                RiskQ2S2s.append(0)
            else:
                RiskQ2S2s.append(entry)

        for key, entry in RiskQ2S3.items():
            if entry is None:
                RiskQ2S3s.append(0)
            else:
                RiskQ2S3s.append(entry)
        RiskQ2S1s= RiskQ2S1s[0]
        RiskQ2S2s= RiskQ2S2s[0]
        RiskQ2S3s= RiskQ2S3s[0]
        RiskQ2S1s= (RiskQ2S1s*100) / (5*survey1Counts)
        RiskQ2S2s= (RiskQ2S2s*100) / (5*survey1Counts)
        RiskQ2S3s= (RiskQ2S3s*100) / (5*survey3Counts)

        RiskQ2S1s=float("{0:.1f}".format(RiskQ2S1s))
        RiskQ2S2s=float("{0:.1f}".format(RiskQ2S2s))
        RiskQ2S3s=float("{0:.1f}".format(RiskQ2S3s))
#Riesk Q3 for both questioniares
        RiskQ3S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q3", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        RiskQ3S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q3", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        RiskQ3S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q3", filter=(Q(link_id=LID3[0])), output_field=FloatField()))

        RiskQ3S1s=[]
        RiskQ3S2s=[]
        RiskQ3S3s=[]
        for key, entry in RiskQ3S1.items():
            if entry is None:
                   RiskQ3S1s.append(0)
            else:
                RiskQ3S1s.append(entry)

        for key, entry in RiskQ3S2.items():
            if entry is None:
                RiskQ3S2s.append(0)
            else:
                RiskQ3S2s.append(entry)

        for key, entry in RiskQ3S3.items():
            if entry is None:
                RiskQ3S3s.append(0)
            else:
                RiskQ3S3s.append(entry)
        RiskQ3S1s= RiskQ3S1s[0]
        RiskQ3S2s= RiskQ3S2s[0]
        RiskQ3S3s= RiskQ3S3s[0]
        RiskQ3S1s= (RiskQ3S1s*100) / (5*survey1Counts)
        RiskQ3S2s= (RiskQ3S2s*100) / (5*survey1Counts)
        RiskQ3S3s= (RiskQ3S3s*100) / (5*survey3Counts)

        RiskQ3S1s=float("{0:.1f}".format(RiskQ3S1s))
        RiskQ3S2s=float("{0:.1f}".format(RiskQ3S2s))
        RiskQ3S3s=float("{0:.1f}".format(RiskQ3S3s))

#benevolence Q1 for both questioniares
        BenevlonceQ1S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q4", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        BenevlonceQ1S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q4", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        BenevlonceQ1S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q4", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        BenevlonceQ1S1s=[]
        BenevlonceQ1S2s=[]
        BenevlonceQ1S3s=[]
        for key, entry in BenevlonceQ1S1.items():
            if entry is None:
                   BenevlonceQ1S1s.append(0)
            else:
                BenevlonceQ1S1s.append(entry)

        for key, entry in BenevlonceQ1S2.items():
            if entry is None:
                BenevlonceQ1S2s.append(0)
            else:
                BenevlonceQ1S2s.append(entry)

        for key, entry in BenevlonceQ1S3.items():
            if entry is None:
                BenevlonceQ1S3s.append(0)
            else:
                BenevlonceQ1S3s.append(entry)

        BenevlonceQ1S1s= BenevlonceQ1S1s[0]
        BenevlonceQ1S2s= BenevlonceQ1S2s[0]
        BenevlonceQ1S3s= BenevlonceQ1S3s[0]

        BenevlonceQ1S1s= (BenevlonceQ1S1s*100) / (5*survey1Counts)
        BenevlonceQ1S2s= (BenevlonceQ1S2s*100) / (5*survey1Counts)
        BenevlonceQ1S3s= (BenevlonceQ1S3s*100) / (5*survey3Counts)

        BenevlonceQ1S1s=float("{0:.1f}".format(BenevlonceQ1S1s))
        BenevlonceQ1S2s=float("{0:.1f}".format(BenevlonceQ1S2s))
        BenevlonceQ1S3s=float("{0:.1f}".format(BenevlonceQ1S3s))
#benevolence Q2 for both questioniares
        BenevlonceQ2S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q5", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        BenevlonceQ2S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q5", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        BenevlonceQ2S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q5", filter=(Q(link_id=LID3[0])), output_field=FloatField()))

        BenevlonceQ2S1s=[]
        BenevlonceQ2S2s=[]
        BenevlonceQ2S3s=[]
        for key, entry in BenevlonceQ2S1.items():
            if entry is None:
                   BenevlonceQ2S1s.append(0)
            else:
                BenevlonceQ2S1s.append(entry)

        for key, entry in BenevlonceQ2S2.items():
            if entry is None:
                BenevlonceQ2S2s.append(0)
            else:
                BenevlonceQ2S2s.append(entry)

        for key, entry in BenevlonceQ2S3.items():
            if entry is None:
                BenevlonceQ2S3s.append(0)
            else:
                BenevlonceQ2S3s.append(entry)

        BenevlonceQ2S1s= BenevlonceQ2S1s[0]
        BenevlonceQ2S2s= BenevlonceQ2S2s[0]
        BenevlonceQ2S3s= BenevlonceQ2S3s[0]
        BenevlonceQ2S1s= (BenevlonceQ2S1s*100) / (5*survey1Counts)
        BenevlonceQ2S2s= (BenevlonceQ2S2s*100) / (5*survey1Counts)
        BenevlonceQ2S3s= (BenevlonceQ2S3s*100) / (5*survey3Counts)

        BenevlonceQ2S1s=float("{0:.1f}".format(BenevlonceQ2S1s))
        BenevlonceQ2S2s=float("{0:.1f}".format(BenevlonceQ2S2s))
        BenevlonceQ2S3s=float("{0:.1f}".format(BenevlonceQ2S3s))

#benevolence Q3 for both questioniares
        BenevlonceQ3S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q6", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        BenevlonceQ3S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q6", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        BenevlonceQ3S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q6", filter=(Q(link_id=LID3[0])), output_field=FloatField()))

        BenevlonceQ3S1s=[]
        BenevlonceQ3S2s=[]
        BenevlonceQ3S3s=[]
        for key, entry in BenevlonceQ3S1.items():
            if entry is None:
                   BenevlonceQ3S1s.append(0)
            else:
                BenevlonceQ3S1s.append(entry)

        for key, entry in BenevlonceQ3S2.items():
            if entry is None:
                BenevlonceQ3S2s.append(0)
            else:
                BenevlonceQ3S2s.append(entry)

        for key, entry in BenevlonceQ3S3.items():
            if entry is None:
                BenevlonceQ3S3s.append(0)
            else:
                BenevlonceQ3S3s.append(entry)

        BenevlonceQ3S1s= BenevlonceQ3S1s[0]
        BenevlonceQ3S2s= BenevlonceQ3S2s[0]
        BenevlonceQ3S3s= BenevlonceQ3S3s[0]

        BenevlonceQ3S1s= (BenevlonceQ3S1s*100) / (5*survey1Counts)
        BenevlonceQ3S2s= (BenevlonceQ3S2s*100) / (5*survey2Counts)
        BenevlonceQ3S3s= (BenevlonceQ3S3s*100) / (5*survey3Counts)

        BenevlonceQ3S1s=float("{0:.1f}".format(BenevlonceQ3S1s))
        BenevlonceQ3S2s=float("{0:.1f}".format(BenevlonceQ3S2s))
        BenevlonceQ3S3s=float("{0:.1f}".format(BenevlonceQ3S3s))

#Riesk Q1 for both questioniares
        CompetenceQ1S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q7", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        CompetenceQ1S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q7", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        CompetenceQ1S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q7", filter=(Q(link_id=LID3[0])), output_field=FloatField()))

        CompetenceQ1S1s=[]
        CompetenceQ1S2s=[]
        CompetenceQ1S3s=[]
        for key, entry in CompetenceQ1S1.items():
            if entry is None:
                   CompetenceQ1S1s.append(0)
            else:
                CompetenceQ1S1s.append(entry)

        for key, entry in CompetenceQ1S2.items():
            if entry is None:
                CompetenceQ1S2s.append(0)
            else:
                CompetenceQ1S2s.append(entry)

        for key, entry in CompetenceQ1S3.items():
            if entry is None:
                CompetenceQ1S3s.append(0)
            else:
                CompetenceQ1S3s.append(entry)

        CompetenceQ1S1s= CompetenceQ1S1s[0]
        CompetenceQ1S2s= CompetenceQ1S2s[0]
        CompetenceQ1S3s= CompetenceQ1S3s[0]

        CompetenceQ1S1s= (CompetenceQ1S1s*100) / (5*survey1Counts)
        CompetenceQ1S2s= (CompetenceQ1S2s*100) / (5*survey2Counts)
        CompetenceQ1S3s= (CompetenceQ1S3s*100) / (5*survey3Counts)

        CompetenceQ1S1s=float("{0:.1f}".format(CompetenceQ1S1s))
        CompetenceQ1S2s=float("{0:.1f}".format(CompetenceQ1S2s))
        CompetenceQ1S3s=float("{0:.1f}".format(CompetenceQ1S3s))

#Riesk Q2 for both questioniares
        CompetenceQ2S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q8", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        CompetenceQ2S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q8", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        CompetenceQ2S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q8", filter=(Q(link_id=LID3[0])), output_field=FloatField()))

        CompetenceQ2S1s=[]
        CompetenceQ2S2s=[]
        CompetenceQ2S3s=[]
        for key, entry in CompetenceQ2S1.items():
            if entry is None:
                   CompetenceQ2S1s.append(0)
            else:
                CompetenceQ2S1s.append(entry)

        for key, entry in CompetenceQ2S2.items():
            if entry is None:
                CompetenceQ2S2s.append(0)
            else:
                CompetenceQ2S2s.append(entry)

        for key, entry in CompetenceQ2S3.items():
            if entry is None:
                CompetenceQ2S3s.append(0)
            else:
                CompetenceQ2S3s.append(entry)

        CompetenceQ2S1s= CompetenceQ2S1s[0]
        CompetenceQ2S2s= CompetenceQ2S2s[0]
        CompetenceQ2S3s= CompetenceQ2S3s[0]

        CompetenceQ2S1s= (CompetenceQ2S1s*100) / (5*survey1Counts)
        CompetenceQ2S2s= (CompetenceQ2S2s*100) / (5*survey2Counts)
        CompetenceQ2S3s= (CompetenceQ2S3s*100) / (5*survey3Counts)

        CompetenceQ2S1s=float("{0:.1f}".format(CompetenceQ2S1s))
        CompetenceQ2S2s=float("{0:.1f}".format(CompetenceQ2S2s))
        CompetenceQ2S3s=float("{0:.1f}".format(CompetenceQ2S3s))
#Riesk Q3 for both questioniares
        CompetenceQ3S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q9", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        CompetenceQ3S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q9", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        CompetenceQ3S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q9", filter=(Q(link_id=LID3[0])), output_field=FloatField()))

        CompetenceQ3S1s=[]
        CompetenceQ3S2s=[]
        CompetenceQ3S3s=[]
        for key, entry in CompetenceQ3S1.items():
            if entry is None:
                   CompetenceQ3S1s.append(0)
            else:
                CompetenceQ3S1s.append(entry)

        for key, entry in CompetenceQ3S2.items():
            if entry is None:
                CompetenceQ3S2s.append(0)
            else:
                CompetenceQ3S2s.append(entry)

        for key, entry in CompetenceQ3S3.items():
            if entry is None:
                CompetenceQ3S3s.append(0)
            else:
                CompetenceQ3S3s.append(entry)

        CompetenceQ3S1s= CompetenceQ3S1s[0]
        CompetenceQ3S2s= CompetenceQ3S2s[0]
        CompetenceQ3S3s= CompetenceQ3S3s[0]
        CompetenceQ3S1s= (CompetenceQ3S1s*100) / (5*survey1Counts)
        CompetenceQ3S2s= (CompetenceQ3S2s*100) / (5*survey2Counts)
        CompetenceQ3S3s= (CompetenceQ3S3s*100) / (5*survey3Counts)

        CompetenceQ3S1s=float("{0:.1f}".format(CompetenceQ3S1s))
        CompetenceQ3S2s=float("{0:.1f}".format(CompetenceQ3S2s))
        CompetenceQ3S3s=float("{0:.1f}".format(CompetenceQ3S3s))
#Recirptocity Q1 for both questioniares
        ReciprocityQ1S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q7", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        ReciprocityQ1S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q7", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        ReciprocityQ1S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q7", filter=(Q(link_id=LID3[0])), output_field=FloatField()))

        ReciprocityQ1S1s=[]
        ReciprocityQ1S2s=[]
        ReciprocityQ1S3s=[]
        for key, entry in ReciprocityQ1S1.items():
            if entry is None:
                   ReciprocityQ1S1s.append(0)
            else:
                ReciprocityQ1S1s.append(entry)

        for key, entry in ReciprocityQ1S2.items():
            if entry is None:
                ReciprocityQ1S2s.append(0)
            else:
                ReciprocityQ1S2s.append(entry)

        for key, entry in ReciprocityQ1S3.items():
            if entry is None:
                ReciprocityQ1S3s.append(0)
            else:
                ReciprocityQ1S3s.append(entry)

        ReciprocityQ1S1s= ReciprocityQ1S1s[0]
        ReciprocityQ1S2s= ReciprocityQ1S2s[0]
        ReciprocityQ1S3s= ReciprocityQ1S3s[0]
        ReciprocityQ1S1s= (ReciprocityQ1S1s*100) / (5*survey1Counts)
        ReciprocityQ1S2s= (ReciprocityQ1S2s*100) / (5*survey2Counts)
        ReciprocityQ1S3s= (ReciprocityQ1S3s*100) / (5*survey3Counts)

        ReciprocityQ1S1s=float("{0:.1f}".format(ReciprocityQ1S1s))
        ReciprocityQ1S2s=float("{0:.1f}".format(ReciprocityQ1S2s))
        ReciprocityQ1S3s=float("{0:.1f}".format(ReciprocityQ1S3s))


#Recirprocity Q2 for both questioniares
        ReciprocityQ2S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q8", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        ReciprocityQ2S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q8", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        ReciprocityQ2S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q8", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        ReciprocityQ2S1s=[]
        ReciprocityQ2S2s=[]
        ReciprocityQ2S3s=[]
        for key, entry in ReciprocityQ2S1.items():
            if entry is None:
                   ReciprocityQ2S1s.append(0)
            else:
                ReciprocityQ2S1s.append(entry)

        for key, entry in ReciprocityQ2S2.items():
            if entry is None:
                ReciprocityQ2S2s.append(0)
            else:
                ReciprocityQ2S2s.append(entry)

        for key, entry in ReciprocityQ2S3.items():
            if entry is None:
                ReciprocityQ2S3s.append(0)
            else:
                ReciprocityQ2S3s.append(entry)

        ReciprocityQ2S1s= ReciprocityQ2S1s[0]
        ReciprocityQ2S2s= ReciprocityQ2S2s[0]
        ReciprocityQ2S3s= ReciprocityQ2S3s[0]

        ReciprocityQ2S1s= (ReciprocityQ2S1s*100) / (5*survey1Counts)
        ReciprocityQ2S2s= (ReciprocityQ2S2s*100) / (5*survey2Counts)
        ReciprocityQ2S3s= (ReciprocityQ2S3s*100) / (5*survey3Counts)

        ReciprocityQ2S1s=float("{0:.1f}".format(ReciprocityQ2S1s))
        ReciprocityQ2S2s=float("{0:.1f}".format(ReciprocityQ2S2s))
        ReciprocityQ2S3s=float("{0:.1f}".format(ReciprocityQ2S3s))
#Riesk Q1 for both questioniares
        GtrustQ1S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q12", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        GtrustQ1S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q12", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        GtrustQ1S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q12", filter=(Q(link_id=LID3[0])), output_field=FloatField()))

        GtrustQ1S1s=[]
        GtrustQ1S2s=[]
        GtrustQ1S3s=[]
        for key, entry in GtrustQ1S1.items():
            if entry is None:
                   GtrustQ1S1s.append(0)
            else:
                GtrustQ1S1s.append(entry)

        for key, entry in GtrustQ1S2.items():
            if entry is None:
                GtrustQ1S2s.append(0)
            else:
                GtrustQ1S2s.append(entry)

        for key, entry in GtrustQ1S3.items():
            if entry is None:
                GtrustQ1S3s.append(0)
            else:
                GtrustQ1S3s.append(entry)

        GtrustQ1S1s= GtrustQ1S1s[0]
        GtrustQ1S2s= GtrustQ1S2s[0]
        GtrustQ1S3s= GtrustQ1S3s[0]
        GtrustQ1S1s= (GtrustQ1S1s*100) / (5*survey1Counts)
        GtrustQ1S2s= (GtrustQ1S2s*100) / (5*survey2Counts)
        GtrustQ1S3s= (GtrustQ1S3s*100) / (5*survey3Counts)

        GtrustQ1S1s=float("{0:.1f}".format(GtrustQ1S1s))
        GtrustQ1S2s=float("{0:.1f}".format(GtrustQ1S2s))
        GtrustQ1S3s=float("{0:.1f}".format(GtrustQ1S3s))
#Riesk Q2 for both questioniares
        GtrustQ2S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q13", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        GtrustQ2S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q13", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        GtrustQ2S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q13", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        GtrustQ2S1s=[]
        GtrustQ2S2s=[]
        GtrustQ2S3s=[]
        for key, entry in GtrustQ2S1.items():
            if entry is None:
                   GtrustQ2S1s.append(0)
            else:
                GtrustQ2S1s.append(entry)

        for key, entry in GtrustQ2S2.items():
            if entry is None:
                GtrustQ2S2s.append(0)
            else:
                GtrustQ2S2s.append(entry)

        for key, entry in GtrustQ2S3.items():
            if entry is None:
                GtrustQ2S3s.append(0)
            else:
                GtrustQ2S3s.append(entry)

        GtrustQ2S1s= GtrustQ2S1s[0]
        GtrustQ2S2s= GtrustQ2S2s[0]
        GtrustQ2S3s= GtrustQ2S3s[0]
        GtrustQ2S1s= (GtrustQ2S1s*100) / (5*survey1Counts)
        GtrustQ2S2s= (GtrustQ2S2s*100) / (5*survey2Counts)
        GtrustQ2S3s= (GtrustQ2S3s*100) / (5*survey3Counts)

        GtrustQ2S1s=float("{0:.1f}".format(GtrustQ2S1s))
        GtrustQ2S2s=float("{0:.1f}".format(GtrustQ2S2s))
        GtrustQ2S3s=float("{0:.1f}".format(GtrustQ2S3s))
#Riesk Q3 for both questioniares
        GtrustQ3S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q14", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        GtrustQ3S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q14", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        GtrustQ3S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q14", filter=(Q(link_id=LID3[0])), output_field=FloatField()))

        GtrustQ3S1s=[]
        GtrustQ3S2s=[]
        GtrustQ3S3s=[]
        for key, entry in GtrustQ3S1.items():
            if entry is None:
                   GtrustQ3S1s.append(0)
            else:
                GtrustQ3S1s.append(entry)

        for key, entry in GtrustQ3S2.items():
            if entry is None:
                GtrustQ3S2s.append(0)
            else:
                GtrustQ3S2s.append(entry)

        for key, entry in GtrustQ3S3.items():
            if entry is None:
                GtrustQ3S3s.append(0)
            else:
                GtrustQ3S3s.append(entry)

        GtrustQ3S1s= GtrustQ3S1s[0]
        GtrustQ3S2s= GtrustQ3S2s[0]
        GtrustQ3S3s= GtrustQ3S3s[0]
        GtrustQ3S1s= (GtrustQ3S1s*100) / (5*survey1Counts)
        GtrustQ3S2s= (GtrustQ3S2s*100) / (5*survey2Counts)
        GtrustQ3S3s= (GtrustQ3S3s*100) / (5*survey3Counts)

        GtrustQ3S1s=float("{0:.1f}".format(GtrustQ3S1s))
        GtrustQ3S2s=float("{0:.1f}".format(GtrustQ3S2s))
        GtrustQ3S3s=float("{0:.1f}".format(GtrustQ3S3s))

        return render(request, 'pie_chart3.html', {
            'project_id':project_id,
            'productname':productname,
            'survey1Counts':survey1Counts,
            'survey2Counts':survey2Counts,
            'survey3Counts':survey3Counts,
            'S1CountGender':S1CountGender,
            'S2CountGender':S2CountGender,
            'S3CountGender':S3CountGender,
            'S1CountAge':S1CountAge,
            'S2CountAge':S2CountAge,
            'S3CountAge':S3CountAge,
            'CrobanchAlphaS1':CrobanchAlphaS1,
            'CrobanchAlphaS2':CrobanchAlphaS2,
            'CrobanchAlphaS3':CrobanchAlphaS3,
            'OvrallTrustS1s':OvrallTrustS1s,
            'OvrallTrustS2s':OvrallTrustS2s,
            'OvrallTrustS3s':OvrallTrustS3s,
            'OvrallRiskS1s':OvrallRiskS1s,
            'OvrallRiskS2s':OvrallRiskS2s,
            'OvrallRiskS3s':OvrallRiskS3s,
            'OvrallBenevolenceS1s':OvrallBenevolenceS1s,
            'OvrallBenevolenceS2s':OvrallBenevolenceS2s,
            'OvrallBenevolenceS3s':OvrallBenevolenceS3s,
            'OvrallCompetenceS1s':OvrallCompetenceS1s,
            'OvrallCompetenceS2s':OvrallCompetenceS2s,
            'OvrallCompetenceS3s':OvrallCompetenceS3s,
            'OvrallReciprocityS1s':OvrallReciprocityS1s,
            'OvrallReciprocityS2s':OvrallReciprocityS2s,
            'OvrallReciprocityS3s':OvrallReciprocityS3s,
            'OvrallGeneralTrustS1s':OvrallGeneralTrustS1s,
            'OvrallGeneralTrustS2s':OvrallGeneralTrustS2s,
            'OvrallGeneralTrustS3s':OvrallGeneralTrustS3s,
            'RiskQ1S1s':RiskQ1S1s,
            'RiskQ1S2s':RiskQ1S2s,
            'RiskQ1S3s':RiskQ1S3s,
            'RiskQ2S1s':RiskQ2S1s,
            'RiskQ2S2s':RiskQ2S2s,
            'RiskQ2S3s':RiskQ2S3s,
            'RiskQ3S1s':RiskQ3S1s,
            'RiskQ3S2s':RiskQ3S2s,
            'RiskQ3S3s':RiskQ3S3s,
            'BenevlonceQ1S1s':BenevlonceQ1S1s,
            'BenevlonceQ1S2s':BenevlonceQ1S2s,
            'BenevlonceQ1S3s':BenevlonceQ1S3s,
            'BenevlonceQ2S1s':BenevlonceQ2S1s,
            'BenevlonceQ2S2s':BenevlonceQ2S2s,
            'BenevlonceQ2S3s':BenevlonceQ2S3s,
            'BenevlonceQ3S1s':BenevlonceQ3S1s,
            'BenevlonceQ3S2s':BenevlonceQ3S2s,
            'BenevlonceQ3S3s':BenevlonceQ3S3s,
            'CompetenceQ1S1s':CompetenceQ1S1s,
            'CompetenceQ1S2s':CompetenceQ1S2s,
            'CompetenceQ1S3s':CompetenceQ1S3s,
            'CompetenceQ2S1s':CompetenceQ2S1s,
            'CompetenceQ2S2s':CompetenceQ2S2s,
            'CompetenceQ2S3s':CompetenceQ2S3s,
            'CompetenceQ3S1s':CompetenceQ3S1s,
            'CompetenceQ3S2s':CompetenceQ3S2s,
            'CompetenceQ3S3s':CompetenceQ3S3s,
            'ReciprocityQ1S1s':ReciprocityQ1S1s,
            'ReciprocityQ1S2s':ReciprocityQ1S2s,
            'ReciprocityQ1S3s':ReciprocityQ1S3s,
            'ReciprocityQ2S1s':ReciprocityQ2S1s,
            'ReciprocityQ2S2s':ReciprocityQ2S2s,
            'ReciprocityQ2S3s':ReciprocityQ2S3s,
            'GtrustQ1S1s':GtrustQ1S1s,
            'GtrustQ1S2s':GtrustQ1S2s,
            'GtrustQ1S3s':GtrustQ1S3s,
            'GtrustQ2S1s':GtrustQ2S1s,
            'GtrustQ2S2s':GtrustQ2S2s,
            'GtrustQ2S3s':GtrustQ2S3s,
            'GtrustQ3S1s':GtrustQ3S1s,
            'GtrustQ3S2s':GtrustQ3S2s,
            'GtrustQ3S3s':GtrustQ3S3s

            })
    elif NumberOfSurveys==4:
        #get the link ids for the two surveys
        LID1 = Link.objects.filter(survey_id=SID[0]).values_list('id', flat=True)
        LID2 = Link.objects.filter(survey_id=SID[1]).values_list('id', flat=True)
        LID3 = Link.objects.filter(survey_id=SID[2]).values_list('id', flat=True)
        LID4 = Link.objects.filter(survey_id=SID[3]).values_list('id', flat=True)
        #get the number of respondents by survey
        S1Count = Submission.objects.aggregate(
            responseS1= Count("q1", filter=(Q(link_id=LID1[0])), output_field=IntegerField()))
        S2Count = Submission.objects.aggregate(
            responseS1= Count("q1", filter=(Q(link_id=LID2[0])), output_field=IntegerField()))
        S3Count = Submission.objects.aggregate(
            responseS1= Count("q1", filter=(Q(link_id=LID3[0])), output_field=IntegerField()))
        S4Count = Submission.objects.aggregate(
            responseS1= Count("q1", filter=(Q(link_id=LID4[0])), output_field=IntegerField()))
        S1Counts=[]
        S2Counts=[]
        S3Counts=[]
        S4Counts=[]
        for key, entry in S1Count.items():
            if entry is None:
                   S1Counts.append(0)
            else:
                S1Counts.append(entry)
        for key, entry in S2Count.items():
            if entry is None:
                S2Counts.append(0)
            else:
                S2Counts.append(entry)
        for key, entry in S3Count.items():
            if entry is None:
                S3Counts.append(0)
            else:
                S3Counts.append(entry)
        for key, entry in S4Count.items():
            if entry is None:
                S4Counts.append(0)
            else:
                S4Counts.append(entry)
        survey1Counts= S1Counts[0]
        survey2Counts= S2Counts[0]
        survey3Counts= S3Counts[0]
        survey4Counts= S4Counts[0]
        #get number gender details for each survey
        S1CountMale = AnonyData.objects.filter(link_id=LID1[0], gender="M").count()
        S1CountFeMale = AnonyData.objects.filter(link_id=LID1[0], gender="F").count()
        S1CountOthers = AnonyData.objects.filter(link_id=LID1[0], gender="O").count()

        S2CountMale = AnonyData.objects.filter(link_id=LID2[0], gender="M").count()
        S2CountFeMale = AnonyData.objects.filter(link_id=LID2[0], gender="F").count()
        S2CountOthers = AnonyData.objects.filter(link_id=LID2[0], gender="O").count()

        S3CountMale = AnonyData.objects.filter(link_id=LID3[0], gender="M").count()
        S3CountFeMale = AnonyData.objects.filter(link_id=LID3[0], gender="F").count()
        S3CountOthers = AnonyData.objects.filter(link_id=LID3[0], gender="O").count()

        S4CountMale = AnonyData.objects.filter(link_id=LID4[0], gender="M").count()
        S4CountFeMale = AnonyData.objects.filter(link_id=LID4[0], gender="F").count()
        S4CountOthers = AnonyData.objects.filter(link_id=LID4[0], gender="O").count()
            #appending the results to an array because the chartjs piechart expects the data in an array format
        S1CountGender = [S1CountMale, S1CountFeMale, S1CountOthers]
        S2CountGender = [S2CountMale, S2CountFeMale, S2CountOthers]
        S3CountGender = [S3CountMale, S3CountFeMale, S3CountOthers]
        S4CountGender = [S4CountMale, S4CountFeMale, S4CountOthers]
        #getting the age distribution for each survey
        #survey 1
        S1Count17Below = AnonyData.objects.filter(link_id=LID1[0], age="1").count()
        S1Count18To27 = AnonyData.objects.filter(link_id=LID1[0], age="2").count()
        S1Count28To37 = AnonyData.objects.filter(link_id=LID1[0], age="3").count()
        S1Count38To47 = AnonyData.objects.filter(link_id=LID1[0], age="4").count()
        S1Count48To57 = AnonyData.objects.filter(link_id=LID1[0], age="5").count()
        S1Count58Above = AnonyData.objects.filter(link_id=LID1[0], age="6").count()
        #survey 2
        S2Count17Below = AnonyData.objects.filter(link_id=LID2[0], age="1").count()
        S2Count18To27 = AnonyData.objects.filter(link_id=LID2[0], age="2").count()
        S2Count28To37 = AnonyData.objects.filter(link_id=LID2[0], age="3").count()
        S2Count38To47 = AnonyData.objects.filter(link_id=LID2[0], age="4").count()
        S2Count48To57 = AnonyData.objects.filter(link_id=LID2[0], age="5").count()
        S2Count58Above = AnonyData.objects.filter(link_id=LID2[0], age="6").count()
        #survey 3
        S3Count17Below = AnonyData.objects.filter(link_id=LID3[0], age="1").count()
        S3Count18To27 = AnonyData.objects.filter(link_id=LID3[0], age="2").count()
        S3Count28To37 = AnonyData.objects.filter(link_id=LID3[0], age="3").count()
        S3Count38To47 = AnonyData.objects.filter(link_id=LID3[0], age="4").count()
        S3Count48To57 = AnonyData.objects.filter(link_id=LID3[0], age="5").count()
        S3Count58Above = AnonyData.objects.filter(link_id=LID3[0], age="6").count()

        #survey 4
        S4Count17Below = AnonyData.objects.filter(link_id=LID4[0], age="1").count()
        S4Count18To27 = AnonyData.objects.filter(link_id=LID4[0], age="2").count()
        S4Count28To37 = AnonyData.objects.filter(link_id=LID4[0], age="3").count()
        S4Count38To47 = AnonyData.objects.filter(link_id=LID4[0], age="4").count()
        S4Count48To57 = AnonyData.objects.filter(link_id=LID4[0], age="5").count()
        S4Count58Above = AnonyData.objects.filter(link_id=LID4[0], age="6").count()

            #appending the results to an array because the chartjs piechart expects the data in an array format
        S1CountAge = [S1Count17Below, S1Count18To27, S1Count28To37, S1Count38To47, S1Count48To57, S1Count58Above ]
        S2CountAge = [S2Count17Below, S2Count18To27, S2Count28To37, S2Count38To47, S2Count48To57, S2Count58Above ]
        S3CountAge = [S3Count17Below, S3Count18To27, S3Count28To37, S3Count38To47, S3Count48To57, S3Count58Above ]
        S4CountAge = [S4Count17Below, S4Count18To27, S4Count28To37, S4Count38To47, S4Count48To57, S4Count58Above ]
        #check for null entries and replace them with 0
        for i in S1CountAge:
            if i == '':
                S1CountAge[i]=0
            else:
                S1CountAge[i] = S1CountAge[i]

        for i in S2CountAge:
            if i == '':
                S2CountAge[i]=0
            else:
                S2CountAge[i] = S2CountAge[i]

        for i in S3CountAge:
            if i == '':
                S3CountAge[i]=0
            else:
                S3CountAge[i] = S2CountAge[i]

        for i in S4CountAge:
            if i == '':
                S4CountAge[i]=0
            else:
                S4CountAge[i] = S4CountAge[i]
        #print(S1CountAge)
        #print(S2CountAge)
        #get all response for each survey
        allRespS1= Submission.objects.values('q1','q2','q3','q4','q5','q6','q7','q8','q9','q10','q11','q12','q13','q14').filter(Q(link_id=LID1[0])).all()
        allRespS2= Submission.objects.values('q1','q2','q3','q4','q5','q6','q7','q8','q9','q10','q11','q12','q13','q14').filter(Q(link_id=LID2[0])).all()
        allRespS3= Submission.objects.values('q1','q2','q3','q4','q5','q6','q7','q8','q9','q10','q11','q12','q13','q14').filter(Q(link_id=LID3[0])).all()
        allRespS4= Submission.objects.values('q1','q2','q3','q4','q5','q6','q7','q8','q9','q10','q11','q12','q13','q14').filter(Q(link_id=LID4[0])).all()
        #convert the querryset into dataframe
        allRespS1=df.DataFrame.from_records(allRespS1)
        allRespS2=df.DataFrame.from_records(allRespS2)
        allRespS3=df.DataFrame.from_records(allRespS3)
        allRespS4=df.DataFrame.from_records(allRespS4)
        #compute the crobanch alpha for each survey using the aggregated responses in dataframe form above
        CrobanchAlphaS1=cronbach_alpha(allRespS1)
        CrobanchAlphaS2=cronbach_alpha(allRespS2)
        CrobanchAlphaS3=cronbach_alpha(allRespS3)
        CrobanchAlphaS4=cronbach_alpha(allRespS4)


        #reducing the result to two decimal places
        CrobanchAlphaS1=float("{0:.4f}".format(CrobanchAlphaS1))
        CrobanchAlphaS2=float("{0:.4f}".format(CrobanchAlphaS2))
        CrobanchAlphaS3=float("{0:.4f}".format(CrobanchAlphaS3))
        CrobanchAlphaS4=float("{0:.4f}".format(CrobanchAlphaS4))

        if math.isnan(CrobanchAlphaS1):
            CrobanchAlphaS1=0.0
        else:
            CrobanchAlphaS1=CrobanchAlphaS1

        if math.isnan(CrobanchAlphaS2):
            CrobanchAlphaS2=0.0
        else:
            CrobanchAlphaS2=CrobanchAlphaS2

        if math.isnan(CrobanchAlphaS3):
            CrobanchAlphaS3=0.0
        else:
            CrobanchAlphaS3=CrobanchAlphaS3

        if math.isnan(CrobanchAlphaS4):
            CrobanchAlphaS4=0.0
        else:
            CrobanchAlphaS4=CrobanchAlphaS4
#compute overall trust score for each survey begins from here
        OvrallTrustS1= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q2", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q3", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q4", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q5", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q6", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q7", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q8", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q9", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q10", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q11", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q12", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q13", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q14", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        OvrallTrustS2= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q2", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q3", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q4", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q5", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q6", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q7", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q8", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q9", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q10", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q11", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q12", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q13", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q14", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        OvrallTrustS3= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q2", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q3", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q4", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q5", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q6", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q7", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q8", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q9", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q10", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q11", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q12", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q13", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q14", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        OvrallTrustS4= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q2", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q3", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q4", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q5", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q6", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q7", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q8", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q9", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q10", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q11", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q12", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q13", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q14", filter=(Q(link_id=LID4[0])), output_field=FloatField()))
        OvrallTrustS1s=[]
        OvrallTrustS2s=[]
        OvrallTrustS3s=[]
        OvrallTrustS4s=[]
        for key, entry in OvrallTrustS1.items():
            if entry is None:
                   OvrallTrustS1s.append(0)
            else:
                OvrallTrustS1s.append(entry)

        for key, entry in OvrallTrustS2.items():
            if entry is None:
                OvrallTrustS2s.append(0)
            else:
                OvrallTrustS2s.append(entry)

        for key, entry in OvrallTrustS3.items():
            if entry is None:
                OvrallTrustS3s.append(0)
            else:
                OvrallTrustS3s.append(entry)

        for key, entry in OvrallTrustS4.items():
            if entry is None:
                OvrallTrustS4s.append(0)
            else:
                OvrallTrustS4s.append(entry)

        OvrallTrustS1s= OvrallTrustS1s[0]
        OvrallTrustS2s= OvrallTrustS2s[0]
        OvrallTrustS3s= OvrallTrustS3s[0]
        OvrallTrustS4s= OvrallTrustS4s[0]
        OvrallTrustS1s= (OvrallTrustS1s*100) / (70*survey1Counts)
        OvrallTrustS2s= (OvrallTrustS2s*100) / (70*survey2Counts)
        OvrallTrustS3s= (OvrallTrustS3s*100) / (70*survey3Counts)
        OvrallTrustS4s= (OvrallTrustS4s*100) / (70*survey4Counts)

        OvrallTrustS1s=float("{0:.1f}".format(OvrallTrustS1s))
        OvrallTrustS2s=float("{0:.1f}".format(OvrallTrustS2s))
        OvrallTrustS3s=float("{0:.1f}".format(OvrallTrustS3s))
        OvrallTrustS4s=float("{0:.1f}".format(OvrallTrustS4s))
#computing overall risk for each survey
        OvrallRiskS1= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q2", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q3", filter=(Q(link_id=LID1[0])), output_field=FloatField())
                )
        OvrallRiskS2= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q2", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q3", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        OvrallRiskS3= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q2", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q3", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        OvrallRiskS4= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q2", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q3", filter=(Q(link_id=LID4[0])), output_field=FloatField()))

        OvrallRiskS1s=[]
        OvrallRiskS2s=[]
        OvrallRiskS3s=[]
        OvrallRiskS4s=[]
        for key, entry in OvrallRiskS1.items():
            if entry is None:
                   OvrallRiskS1s.append(0)
            else:
                OvrallRiskS1s.append(entry)

        for key, entry in OvrallRiskS2.items():
            if entry is None:
                OvrallRiskS2s.append(0)
            else:
                OvrallRiskS2s.append(entry)

        for key, entry in OvrallRiskS3.items():
            if entry is None:
                OvrallRiskS3s.append(0)
            else:
                OvrallRiskS3s.append(entry)

        for key, entry in OvrallRiskS4.items():
            if entry is None:
                OvrallRiskS4s.append(0)
            else:
                OvrallRiskS4s.append(entry)

        OvrallRiskS1s= OvrallRiskS1s[0]
        OvrallRiskS2s= OvrallRiskS2s[0]
        OvrallRiskS3s= OvrallRiskS3s[0]
        OvrallRiskS4s= OvrallRiskS4s[0]
        OvrallRiskS1s= (OvrallRiskS1s*100) / (15*survey1Counts)
        OvrallRiskS2s= (OvrallRiskS2s*100) / (15*survey2Counts)
        OvrallRiskS3s= (OvrallRiskS3s*100) / (15*survey3Counts)
        OvrallRiskS4s= (OvrallRiskS4s*100) / (15*survey4Counts)

        OvrallRiskS1s=float("{0:.1f}".format(OvrallRiskS1s))
        OvrallRiskS2s=float("{0:.1f}".format(OvrallRiskS2s))
        OvrallRiskS3s=float("{0:.1f}".format(OvrallRiskS3s))
        OvrallRiskS4s=float("{0:.1f}".format(OvrallRiskS4s))
#computing benevolencerisk for each survey
        OvrallBenevolenceS1= Submission.objects.aggregate(
            overalBenevolence=
                Sum("q4", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q5", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q6", filter=(Q(link_id=LID1[0])), output_field=FloatField())
                )
        OvrallBenevolenceS2= Submission.objects.aggregate(
            overalBenevolence=
                Sum("q4", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q5", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q6", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        OvrallBenevolenceS3= Submission.objects.aggregate(
            overalBenevolence=
                Sum("q4", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q5", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q6", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        OvrallBenevolenceS4= Submission.objects.aggregate(
            overalBenevolence=
                Sum("q4", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q5", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q6", filter=(Q(link_id=LID4[0])), output_field=FloatField()))

        OvrallBenevolenceS1s=[]
        OvrallBenevolenceS2s=[]
        OvrallBenevolenceS3s=[]
        OvrallBenevolenceS4s=[]
        for key, entry in OvrallBenevolenceS1.items():
            if entry is None:
                   OvrallBenevolenceS1s.append(0)
            else:
                OvrallBenevolenceS1s.append(entry)

        for key, entry in OvrallBenevolenceS2.items():
            if entry is None:
                OvrallBenevolenceS2s.append(0)
            else:
                OvrallBenevolenceS2s.append(entry)

        for key, entry in OvrallBenevolenceS3.items():
            if entry is None:
                OvrallBenevolenceS3s.append(0)
            else:
                OvrallBenevolenceS3s.append(entry)

        for key, entry in OvrallBenevolenceS4.items():
            if entry is None:
                OvrallBenevolenceS4s.append(0)
            else:
                OvrallBenevolenceS4s.append(entry)

        OvrallBenevolenceS1s= OvrallBenevolenceS1s[0]
        OvrallBenevolenceS2s= OvrallBenevolenceS2s[0]
        OvrallBenevolenceS3s= OvrallBenevolenceS3s[0]
        OvrallBenevolenceS4s= OvrallBenevolenceS4s[0]

        OvrallBenevolenceS1s= (OvrallBenevolenceS1s*100) / (15*survey1Counts)
        OvrallBenevolenceS2s= (OvrallBenevolenceS2s*100) / (15*survey2Counts)
        OvrallBenevolenceS3s= (OvrallBenevolenceS3s*100) / (15*survey3Counts)
        OvrallBenevolenceS4s= (OvrallBenevolenceS4s*100) / (15*survey4Counts)

        OvrallBenevolenceS1s=float("{0:.1f}".format(OvrallBenevolenceS1s))
        OvrallBenevolenceS2s=float("{0:.1f}".format(OvrallBenevolenceS2s))
        OvrallBenevolenceS3s=float("{0:.1f}".format(OvrallBenevolenceS3s))
        OvrallBenevolenceS4s=float("{0:.1f}".format(OvrallBenevolenceS4s))

# computing competence for each survey
        OvrallCompetenceS1= Submission.objects.aggregate(
            overalCompetence=
                Sum("q7", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q8", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q9", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        OvrallCompetenceS2= Submission.objects.aggregate(
            overalCompetence=
                Sum("q7", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q8", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q9", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        OvrallCompetenceS3= Submission.objects.aggregate(
            overalCompetence=
                Sum("q7", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q8", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q9", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        OvrallCompetenceS4= Submission.objects.aggregate(
            overalCompetence=
                Sum("q7", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q8", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q9", filter=(Q(link_id=LID4[0])), output_field=FloatField()))


        OvrallCompetenceS1s=[]
        OvrallCompetenceS2s=[]
        OvrallCompetenceS3s=[]
        OvrallCompetenceS4s=[]

        for key, entry in OvrallCompetenceS1.items():
            if entry is None:
                   OvrallCompetenceS1s.append(0)
            else:
                OvrallCompetenceS1s.append(entry)

        for key, entry in OvrallCompetenceS2.items():
            if entry is None:
                OvrallCompetenceS2s.append(0)
            else:
                OvrallCompetenceS2s.append(entry)

        for key, entry in OvrallCompetenceS3.items():
            if entry is None:
                OvrallCompetenceS3s.append(0)
            else:
                OvrallCompetenceS3s.append(entry)

        for key, entry in OvrallCompetenceS4.items():
            if entry is None:
                OvrallCompetenceS4s.append(0)
            else:
                OvrallCompetenceS4s.append(entry)

        OvrallCompetenceS1s= OvrallCompetenceS1s[0]
        OvrallCompetenceS2s= OvrallCompetenceS2s[0]
        OvrallCompetenceS3s= OvrallCompetenceS3s[0]
        OvrallCompetenceS4s= OvrallCompetenceS4s[0]

        OvrallCompetenceS1s= (OvrallCompetenceS1s*100) / (15*survey1Counts)
        OvrallCompetenceS2s= (OvrallCompetenceS2s*100) / (15*survey2Counts)
        OvrallCompetenceS3s= (OvrallCompetenceS3s*100) / (15*survey3Counts)
        OvrallCompetenceS4s= (OvrallCompetenceS4s*100) / (15*survey4Counts)

        OvrallCompetenceS1s=float("{0:.1f}".format(OvrallCompetenceS1s))
        OvrallCompetenceS2s=float("{0:.1f}".format(OvrallCompetenceS2s))
        OvrallCompetenceS3s=float("{0:.1f}".format(OvrallCompetenceS3s))
        OvrallCompetenceS4s=float("{0:.1f}".format(OvrallCompetenceS4s))
# computing reciprocity
        OvrallReciprocityS1= Submission.objects.aggregate(
            overalReciprocity=
                Sum("q10", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q11", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        OvrallReciprocityS2= Submission.objects.aggregate(
            overalReciprocity=
                Sum("q10", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q11", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        OvrallReciprocityS3= Submission.objects.aggregate(
            overalReciprocity=
                Sum("q10", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q11", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        OvrallReciprocityS4= Submission.objects.aggregate(
            overalReciprocity=
                Sum("q10", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q11", filter=(Q(link_id=LID4[0])), output_field=FloatField()))
        OvrallReciprocityS1s=[]
        OvrallReciprocityS2s=[]
        OvrallReciprocityS3s=[]
        OvrallReciprocityS4s=[]
        for key, entry in OvrallReciprocityS1.items():
            if entry is None:
                   OvrallReciprocityS1s.append(0)
            else:
                OvrallReciprocityS1s.append(entry)

        for key, entry in OvrallReciprocityS2.items():
            if entry is None:
                OvrallReciprocityS2s.append(0)
            else:
                OvrallReciprocityS2s.append(entry)

        for key, entry in OvrallReciprocityS3.items():
            if entry is None:
                OvrallReciprocityS3s.append(0)
            else:
                OvrallReciprocityS3s.append(entry)
        for key, entry in OvrallReciprocityS4.items():
            if entry is None:
                OvrallReciprocityS4s.append(0)
            else:
                OvrallReciprocityS4s.append(entry)

        OvrallReciprocityS1s= OvrallReciprocityS1s[0]
        OvrallReciprocityS2s= OvrallReciprocityS2s[0]
        OvrallReciprocityS3s= OvrallReciprocityS3s[0]
        OvrallReciprocityS4s= OvrallReciprocityS4s[0]
        OvrallReciprocityS1s= (OvrallReciprocityS1s*100) / (10*survey1Counts)
        OvrallReciprocityS2s= (OvrallReciprocityS2s*100) / (10*survey2Counts)
        OvrallReciprocityS3s= (OvrallReciprocityS3s*100) / (10*survey3Counts)
        OvrallReciprocityS4s= (OvrallReciprocityS4s*100) / (10*survey4Counts)

        OvrallReciprocityS1s=float("{0:.1f}".format(OvrallReciprocityS1s))
        OvrallReciprocityS2s=float("{0:.1f}".format(OvrallReciprocityS2s))
        OvrallReciprocityS3s=float("{0:.1f}".format(OvrallReciprocityS3s))
        OvrallReciprocityS4s=float("{0:.1f}".format(OvrallReciprocityS4s))

#Computing general trust for each survey
        OvrallGeneralTrustS1= Submission.objects.aggregate(
            overalGeneralTrust=
                Sum("q12", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q13", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q14", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        OvrallGeneralTrustS2= Submission.objects.aggregate(
            overalGeneralTrust=
                Sum("q12", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q13", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q14", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        OvrallGeneralTrustS3= Submission.objects.aggregate(
            overalGeneralTrust=
                Sum("q12", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q13", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q14", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        OvrallGeneralTrustS4= Submission.objects.aggregate(
            overalGeneralTrust=
                Sum("q12", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q13", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q14", filter=(Q(link_id=LID4[0])), output_field=FloatField()))

        OvrallGeneralTrustS1s=[]
        OvrallGeneralTrustS2s=[]
        OvrallGeneralTrustS3s=[]
        OvrallGeneralTrustS4s=[]
        for key, entry in OvrallGeneralTrustS1.items():
            if entry is None:
                   OvrallGeneralTrustS1s.append(0)
            else:
                OvrallGeneralTrustS1s.append(entry)

        for key, entry in OvrallGeneralTrustS2.items():
            if entry is None:
                OvrallGeneralTrustS2s.append(0)
            else:
                OvrallGeneralTrustS2s.append(entry)

        for key, entry in OvrallGeneralTrustS3.items():
            if entry is None:
                OvrallGeneralTrustS3s.append(0)
            else:
                OvrallGeneralTrustS3s.append(entry)
        for key, entry in OvrallGeneralTrustS4.items():
            if entry is None:
                OvrallGeneralTrustS4s.append(0)
            else:
                OvrallGeneralTrustS4s.append(entry)

        OvrallGeneralTrustS1s= OvrallGeneralTrustS1s[0]
        OvrallGeneralTrustS2s= OvrallGeneralTrustS2s[0]
        OvrallGeneralTrustS3s= OvrallGeneralTrustS3s[0]
        OvrallGeneralTrustS4s= OvrallGeneralTrustS4s[0]
        OvrallGeneralTrustS1s= (OvrallGeneralTrustS1s*100) / (15*survey1Counts)
        OvrallGeneralTrustS2s= (OvrallGeneralTrustS2s*100) / (15*survey2Counts)
        OvrallGeneralTrustS3s= (OvrallGeneralTrustS3s*100) / (15*survey3Counts)
        OvrallGeneralTrustS4s= (OvrallGeneralTrustS4s*100) / (15*survey4Counts)

        OvrallGeneralTrustS1s=float("{0:.1f}".format(OvrallGeneralTrustS1s))
        OvrallGeneralTrustS2s=float("{0:.1f}".format(OvrallGeneralTrustS2s))
        OvrallGeneralTrustS3s=float("{0:.1f}".format(OvrallGeneralTrustS3s))
        OvrallGeneralTrustS4s=float("{0:.1f}".format(OvrallGeneralTrustS4s))

#Riesk Q1 for both questioniares
        RiskQ1S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        RiskQ1S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        RiskQ1S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        RiskQ1S4= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID4[0])), output_field=FloatField()))

        RiskQ1S1s=[]
        RiskQ1S2s=[]
        RiskQ1S3s=[]
        RiskQ1S4s=[]
        for key, entry in RiskQ1S1.items():
            if entry is None:
                   RiskQ1S1s.append(0)
            else:
                RiskQ1S1s.append(entry)

        for key, entry in RiskQ1S2.items():
            if entry is None:
                RiskQ1S2s.append(0)
            else:
                RiskQ1S2s.append(entry)

        for key, entry in RiskQ1S3.items():
            if entry is None:
                RiskQ1S3s.append(0)
            else:
                RiskQ1S3s.append(entry)
        for key, entry in RiskQ1S4.items():
            if entry is None:
                RiskQ1S4s.append(0)
            else:
                RiskQ1S4s.append(entry)

        RiskQ1S1s= RiskQ1S1s[0]
        RiskQ1S2s= RiskQ1S2s[0]
        RiskQ1S3s= RiskQ1S3s[0]
        RiskQ1S4s= RiskQ1S4s[0]
        RiskQ1S1s= (RiskQ1S1s*100) / (5*survey1Counts)
        RiskQ1S2s= (RiskQ1S2s*100) / (5*survey2Counts)
        RiskQ1S3s= (RiskQ1S3s*100) / (5*survey3Counts)
        RiskQ1S4s= (RiskQ1S4s*100) / (5*survey4Counts)

        RiskQ1S1s=float("{0:.1f}".format(RiskQ1S1s))
        RiskQ1S2s=float("{0:.1f}".format(RiskQ1S2s))
        RiskQ1S3s=float("{0:.1f}".format(RiskQ1S3s))
        RiskQ1S4s=float("{0:.1f}".format(RiskQ1S4s))
#Riesk Q2 for both questioniares
        RiskQ2S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q2", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        RiskQ2S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q2", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        RiskQ2S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q2", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        RiskQ2S4= Submission.objects.aggregate(
            overaltrust=
                Sum("q2", filter=(Q(link_id=LID4[0])), output_field=FloatField()))

        RiskQ2S1s=[]
        RiskQ2S2s=[]
        RiskQ2S3s=[]
        RiskQ2S4s=[]
        for key, entry in RiskQ2S1.items():
            if entry is None:
                   RiskQ2S1s.append(0)
            else:
                RiskQ2S1s.append(entry)

        for key, entry in RiskQ2S2.items():
            if entry is None:
                RiskQ2S2s.append(0)
            else:
                RiskQ2S2s.append(entry)

        for key, entry in RiskQ2S3.items():
            if entry is None:
                RiskQ2S3s.append(0)
            else:
                RiskQ2S3s.append(entry)
        for key, entry in RiskQ2S4.items():
            if entry is None:
                RiskQ2S4s.append(0)
            else:
                RiskQ2S4s.append(entry)
        RiskQ2S1s= RiskQ2S1s[0]
        RiskQ2S2s= RiskQ2S2s[0]
        RiskQ2S3s= RiskQ2S3s[0]
        RiskQ2S4s= RiskQ2S4s[0]
        RiskQ2S1s= (RiskQ2S1s*100) / (5*survey1Counts)
        RiskQ2S2s= (RiskQ2S2s*100) / (5*survey1Counts)
        RiskQ2S3s= (RiskQ2S3s*100) / (5*survey3Counts)
        RiskQ2S4s= (RiskQ2S4s*100) / (5*survey4Counts)

        RiskQ2S1s=float("{0:.1f}".format(RiskQ2S1s))
        RiskQ2S2s=float("{0:.1f}".format(RiskQ2S2s))
        RiskQ2S3s=float("{0:.1f}".format(RiskQ2S3s))
        RiskQ2S4s=float("{0:.1f}".format(RiskQ2S4s))
#Riesk Q3 for both questioniares
        RiskQ3S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q3", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        RiskQ3S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q3", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        RiskQ3S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q3", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        RiskQ3S4= Submission.objects.aggregate(
            overaltrust=
                Sum("q3", filter=(Q(link_id=LID4[0])), output_field=FloatField()))

        RiskQ3S1s=[]
        RiskQ3S2s=[]
        RiskQ3S3s=[]
        RiskQ3S4s=[]
        for key, entry in RiskQ3S1.items():
            if entry is None:
                   RiskQ3S1s.append(0)
            else:
                RiskQ3S1s.append(entry)

        for key, entry in RiskQ3S2.items():
            if entry is None:
                RiskQ3S2s.append(0)
            else:
                RiskQ3S2s.append(entry)

        for key, entry in RiskQ3S3.items():
            if entry is None:
                RiskQ3S3s.append(0)
            else:
                RiskQ3S3s.append(entry)

        for key, entry in RiskQ3S4.items():
            if entry is None:
                RiskQ3S4s.append(0)
            else:
                RiskQ3S4s.append(entry)

        RiskQ3S1s= RiskQ3S1s[0]
        RiskQ3S2s= RiskQ3S2s[0]
        RiskQ3S3s= RiskQ3S3s[0]
        RiskQ3S4s= RiskQ3S4s[0]
        RiskQ3S1s= (RiskQ3S1s*100) / (5*survey1Counts)
        RiskQ3S2s= (RiskQ3S2s*100) / (5*survey1Counts)
        RiskQ3S3s= (RiskQ3S3s*100) / (5*survey3Counts)
        RiskQ3S4s= (RiskQ3S4s*100) / (5*survey4Counts)

        RiskQ3S1s=float("{0:.1f}".format(RiskQ3S1s))
        RiskQ3S2s=float("{0:.1f}".format(RiskQ3S2s))
        RiskQ3S3s=float("{0:.1f}".format(RiskQ3S3s))
        RiskQ3S4s=float("{0:.1f}".format(RiskQ3S4s))

#benevolence Q1 for both questioniares
        BenevlonceQ1S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q4", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        BenevlonceQ1S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q4", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        BenevlonceQ1S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q4", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        BenevlonceQ1S4= Submission.objects.aggregate(
            overaltrust=
                Sum("q4", filter=(Q(link_id=LID4[0])), output_field=FloatField()))
        BenevlonceQ1S1s=[]
        BenevlonceQ1S2s=[]
        BenevlonceQ1S3s=[]
        BenevlonceQ1S4s=[]
        for key, entry in BenevlonceQ1S1.items():
            if entry is None:
                   BenevlonceQ1S1s.append(0)
            else:
                BenevlonceQ1S1s.append(entry)

        for key, entry in BenevlonceQ1S2.items():
            if entry is None:
                BenevlonceQ1S2s.append(0)
            else:
                BenevlonceQ1S2s.append(entry)

        for key, entry in BenevlonceQ1S3.items():
            if entry is None:
                BenevlonceQ1S3s.append(0)
            else:
                BenevlonceQ1S3s.append(entry)
        for key, entry in BenevlonceQ1S4.items():
            if entry is None:
                BenevlonceQ1S4s.append(0)
            else:
                BenevlonceQ1S4s.append(entry)

        BenevlonceQ1S1s= BenevlonceQ1S1s[0]
        BenevlonceQ1S2s= BenevlonceQ1S2s[0]
        BenevlonceQ1S3s= BenevlonceQ1S3s[0]
        BenevlonceQ1S4s= BenevlonceQ1S4s[0]

        BenevlonceQ1S1s= (BenevlonceQ1S1s*100) / (5*survey1Counts)
        BenevlonceQ1S2s= (BenevlonceQ1S2s*100) / (5*survey1Counts)
        BenevlonceQ1S3s= (BenevlonceQ1S3s*100) / (5*survey3Counts)
        BenevlonceQ1S4s= (BenevlonceQ1S4s*100) / (5*survey4Counts)

        BenevlonceQ1S1s=float("{0:.1f}".format(BenevlonceQ1S1s))
        BenevlonceQ1S2s=float("{0:.1f}".format(BenevlonceQ1S2s))
        BenevlonceQ1S3s=float("{0:.1f}".format(BenevlonceQ1S3s))
        BenevlonceQ1S4s=float("{0:.1f}".format(BenevlonceQ1S4s))
#benevolence Q2 for both questioniares
        BenevlonceQ2S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q5", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        BenevlonceQ2S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q5", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        BenevlonceQ2S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q5", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        BenevlonceQ2S4= Submission.objects.aggregate(
            overaltrust=
                Sum("q5", filter=(Q(link_id=LID4[0])), output_field=FloatField()))


        BenevlonceQ2S1s=[]
        BenevlonceQ2S2s=[]
        BenevlonceQ2S3s=[]
        BenevlonceQ2S4s=[]
        for key, entry in BenevlonceQ2S1.items():
            if entry is None:
                   BenevlonceQ2S1s.append(0)
            else:
                BenevlonceQ2S1s.append(entry)

        for key, entry in BenevlonceQ2S2.items():
            if entry is None:
                BenevlonceQ2S2s.append(0)
            else:
                BenevlonceQ2S2s.append(entry)

        for key, entry in BenevlonceQ2S3.items():
            if entry is None:
                BenevlonceQ2S3s.append(0)
            else:
                BenevlonceQ2S3s.append(entry)

        for key, entry in BenevlonceQ2S4.items():
            if entry is None:
                BenevlonceQ2S4s.append(0)
            else:
                BenevlonceQ2S4s.append(entry)

        BenevlonceQ2S1s= BenevlonceQ2S1s[0]
        BenevlonceQ2S2s= BenevlonceQ2S2s[0]
        BenevlonceQ2S3s= BenevlonceQ2S3s[0]
        BenevlonceQ2S4s= BenevlonceQ2S4s[0]
        BenevlonceQ2S1s= (BenevlonceQ2S1s*100) / (5*survey1Counts)
        BenevlonceQ2S2s= (BenevlonceQ2S2s*100) / (5*survey1Counts)
        BenevlonceQ2S3s= (BenevlonceQ2S3s*100) / (5*survey3Counts)
        BenevlonceQ2S4s= (BenevlonceQ2S4s*100) / (5*survey4Counts)

        BenevlonceQ2S1s=float("{0:.1f}".format(BenevlonceQ2S1s))
        BenevlonceQ2S2s=float("{0:.1f}".format(BenevlonceQ2S2s))
        BenevlonceQ2S3s=float("{0:.1f}".format(BenevlonceQ2S3s))
        BenevlonceQ2S4s=float("{0:.1f}".format(BenevlonceQ2S4s))

#benevolence Q3 for both questioniares
        BenevlonceQ3S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q6", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        BenevlonceQ3S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q6", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        BenevlonceQ3S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q6", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        BenevlonceQ3S4= Submission.objects.aggregate(
            overaltrust=
                Sum("q6", filter=(Q(link_id=LID4[0])), output_field=FloatField()))

        BenevlonceQ3S1s=[]
        BenevlonceQ3S2s=[]
        BenevlonceQ3S3s=[]
        BenevlonceQ3S4s=[]
        for key, entry in BenevlonceQ3S1.items():
            if entry is None:
                   BenevlonceQ3S1s.append(0)
            else:
                BenevlonceQ3S1s.append(entry)

        for key, entry in BenevlonceQ3S2.items():
            if entry is None:
                BenevlonceQ3S2s.append(0)
            else:
                BenevlonceQ3S2s.append(entry)

        for key, entry in BenevlonceQ3S3.items():
            if entry is None:
                BenevlonceQ3S3s.append(0)
            else:
                BenevlonceQ3S3s.append(entry)

        for key, entry in BenevlonceQ3S4.items():
            if entry is None:
                BenevlonceQ3S4s.append(0)
            else:
                BenevlonceQ3S4s.append(entry)

        BenevlonceQ3S1s= BenevlonceQ3S1s[0]
        BenevlonceQ3S2s= BenevlonceQ3S2s[0]
        BenevlonceQ3S3s= BenevlonceQ3S3s[0]
        BenevlonceQ3S4s= BenevlonceQ3S4s[0]

        BenevlonceQ3S1s= (BenevlonceQ3S1s*100) / (5*survey1Counts)
        BenevlonceQ3S2s= (BenevlonceQ3S2s*100) / (5*survey2Counts)
        BenevlonceQ3S3s= (BenevlonceQ3S3s*100) / (5*survey3Counts)
        BenevlonceQ3S4s= (BenevlonceQ3S4s*100) / (5*survey4Counts)

        BenevlonceQ3S1s=float("{0:.1f}".format(BenevlonceQ3S1s))
        BenevlonceQ3S2s=float("{0:.1f}".format(BenevlonceQ3S2s))
        BenevlonceQ3S3s=float("{0:.1f}".format(BenevlonceQ3S3s))
        BenevlonceQ3S4s=float("{0:.1f}".format(BenevlonceQ3S4s))

#Riesk Q1 for both questioniares
        CompetenceQ1S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q7", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        CompetenceQ1S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q7", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        CompetenceQ1S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q7", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        CompetenceQ1S4= Submission.objects.aggregate(
            overaltrust=
                Sum("q7", filter=(Q(link_id=LID4[0])), output_field=FloatField()))

        CompetenceQ1S1s=[]
        CompetenceQ1S2s=[]
        CompetenceQ1S3s=[]
        CompetenceQ1S4s=[]
        for key, entry in CompetenceQ1S1.items():
            if entry is None:
                   CompetenceQ1S1s.append(0)
            else:
                CompetenceQ1S1s.append(entry)

        for key, entry in CompetenceQ1S2.items():
            if entry is None:
                CompetenceQ1S2s.append(0)
            else:
                CompetenceQ1S2s.append(entry)

        for key, entry in CompetenceQ1S3.items():
            if entry is None:
                CompetenceQ1S3s.append(0)
            else:
                CompetenceQ1S3s.append(entry)

        for key, entry in CompetenceQ1S4.items():
            if entry is None:
                CompetenceQ1S4s.append(0)
            else:
                CompetenceQ1S4s.append(entry)

        CompetenceQ1S1s= CompetenceQ1S1s[0]
        CompetenceQ1S2s= CompetenceQ1S2s[0]
        CompetenceQ1S3s= CompetenceQ1S3s[0]
        CompetenceQ1S4s= CompetenceQ1S4s[0]

        CompetenceQ1S1s= (CompetenceQ1S1s*100) / (5*survey1Counts)
        CompetenceQ1S2s= (CompetenceQ1S2s*100) / (5*survey2Counts)
        CompetenceQ1S3s= (CompetenceQ1S3s*100) / (5*survey3Counts)
        CompetenceQ1S4s= (CompetenceQ1S4s*100) / (5*survey4Counts)

        CompetenceQ1S1s=float("{0:.1f}".format(CompetenceQ1S1s))
        CompetenceQ1S2s=float("{0:.1f}".format(CompetenceQ1S2s))
        CompetenceQ1S3s=float("{0:.1f}".format(CompetenceQ1S3s))
        CompetenceQ1S4s=float("{0:.1f}".format(CompetenceQ1S4s))

#Riesk Q2 for both questioniares
        CompetenceQ2S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q8", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        CompetenceQ2S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q8", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        CompetenceQ2S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q8", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        CompetenceQ2S4= Submission.objects.aggregate(
            overaltrust=
                Sum("q8", filter=(Q(link_id=LID4[0])), output_field=FloatField()))

        CompetenceQ2S1s=[]
        CompetenceQ2S2s=[]
        CompetenceQ2S3s=[]
        CompetenceQ2S4s=[]
        for key, entry in CompetenceQ2S1.items():
            if entry is None:
                   CompetenceQ2S1s.append(0)
            else:
                CompetenceQ2S1s.append(entry)

        for key, entry in CompetenceQ2S2.items():
            if entry is None:
                CompetenceQ2S2s.append(0)
            else:
                CompetenceQ2S2s.append(entry)

        for key, entry in CompetenceQ2S3.items():
            if entry is None:
                CompetenceQ2S3s.append(0)
            else:
                CompetenceQ2S3s.append(entry)
        for key, entry in CompetenceQ2S4.items():
            if entry is None:
                CompetenceQ2S4s.append(0)
            else:
                CompetenceQ2S4s.append(entry)

        CompetenceQ2S1s= CompetenceQ2S1s[0]
        CompetenceQ2S2s= CompetenceQ2S2s[0]
        CompetenceQ2S3s= CompetenceQ2S3s[0]
        CompetenceQ2S4s= CompetenceQ2S4s[0]

        CompetenceQ2S1s= (CompetenceQ2S1s*100) / (5*survey1Counts)
        CompetenceQ2S2s= (CompetenceQ2S2s*100) / (5*survey2Counts)
        CompetenceQ2S3s= (CompetenceQ2S3s*100) / (5*survey3Counts)
        CompetenceQ2S4s= (CompetenceQ2S4s*100) / (5*survey4Counts)

        CompetenceQ2S1s=float("{0:.1f}".format(CompetenceQ2S1s))
        CompetenceQ2S2s=float("{0:.1f}".format(CompetenceQ2S2s))
        CompetenceQ2S3s=float("{0:.1f}".format(CompetenceQ2S3s))
        CompetenceQ2S4s=float("{0:.1f}".format(CompetenceQ2S4s))
#Riesk Q3 for both questioniares
        CompetenceQ3S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q9", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        CompetenceQ3S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q9", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        CompetenceQ3S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q9", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        CompetenceQ3S4= Submission.objects.aggregate(
            overaltrust=
                Sum("q9", filter=(Q(link_id=LID4[0])), output_field=FloatField()))

        CompetenceQ3S1s=[]
        CompetenceQ3S2s=[]
        CompetenceQ3S3s=[]
        CompetenceQ3S4s=[]
        for key, entry in CompetenceQ3S1.items():
            if entry is None:
                   CompetenceQ3S1s.append(0)
            else:
                CompetenceQ3S1s.append(entry)

        for key, entry in CompetenceQ3S2.items():
            if entry is None:
                CompetenceQ3S2s.append(0)
            else:
                CompetenceQ3S2s.append(entry)

        for key, entry in CompetenceQ3S3.items():
            if entry is None:
                CompetenceQ3S3s.append(0)
            else:
                CompetenceQ3S3s.append(entry)

        for key, entry in CompetenceQ3S4.items():
            if entry is None:
                CompetenceQ3S4s.append(0)
            else:
                CompetenceQ3S4s.append(entry)

        CompetenceQ3S1s= CompetenceQ3S1s[0]
        CompetenceQ3S2s= CompetenceQ3S2s[0]
        CompetenceQ3S3s= CompetenceQ3S3s[0]
        CompetenceQ3S4s= CompetenceQ3S4s[0]

        CompetenceQ3S1s= (CompetenceQ3S1s*100) / (5*survey1Counts)
        CompetenceQ3S2s= (CompetenceQ3S2s*100) / (5*survey2Counts)
        CompetenceQ3S3s= (CompetenceQ3S3s*100) / (5*survey3Counts)
        CompetenceQ3S4s= (CompetenceQ3S4s*100) / (5*survey4Counts)

        CompetenceQ3S1s=float("{0:.1f}".format(CompetenceQ3S1s))
        CompetenceQ3S2s=float("{0:.1f}".format(CompetenceQ3S2s))
        CompetenceQ3S3s=float("{0:.1f}".format(CompetenceQ3S3s))
        CompetenceQ3S4s=float("{0:.1f}".format(CompetenceQ3S4s))
#Recirptocity Q1 for both questioniares
        ReciprocityQ1S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q7", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        ReciprocityQ1S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q7", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        ReciprocityQ1S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q7", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        ReciprocityQ1S4= Submission.objects.aggregate(
            overaltrust=
                Sum("q7", filter=(Q(link_id=LID4[0])), output_field=FloatField()))

        ReciprocityQ1S1s=[]
        ReciprocityQ1S2s=[]
        ReciprocityQ1S3s=[]
        ReciprocityQ1S4s=[]

        for key, entry in ReciprocityQ1S1.items():
            if entry is None:
                   ReciprocityQ1S1s.append(0)
            else:
                ReciprocityQ1S1s.append(entry)

        for key, entry in ReciprocityQ1S2.items():
            if entry is None:
                ReciprocityQ1S2s.append(0)
            else:
                ReciprocityQ1S2s.append(entry)

        for key, entry in ReciprocityQ1S3.items():
            if entry is None:
                ReciprocityQ1S3s.append(0)
            else:
                ReciprocityQ1S3s.append(entry)
        for key, entry in ReciprocityQ1S4.items():
            if entry is None:
                ReciprocityQ1S4s.append(0)
            else:
                ReciprocityQ1S4s.append(entry)

        ReciprocityQ1S1s= ReciprocityQ1S1s[0]
        ReciprocityQ1S2s= ReciprocityQ1S2s[0]
        ReciprocityQ1S3s= ReciprocityQ1S3s[0]
        ReciprocityQ1S4s= ReciprocityQ1S4s[0]

        ReciprocityQ1S1s= (ReciprocityQ1S1s*100) / (5*survey1Counts)
        ReciprocityQ1S2s= (ReciprocityQ1S2s*100) / (5*survey2Counts)
        ReciprocityQ1S3s= (ReciprocityQ1S3s*100) / (5*survey3Counts)
        ReciprocityQ1S4s= (ReciprocityQ1S4s*100) / (5*survey4Counts)

        ReciprocityQ1S1s=float("{0:.1f}".format(ReciprocityQ1S1s))
        ReciprocityQ1S2s=float("{0:.1f}".format(ReciprocityQ1S2s))
        ReciprocityQ1S3s=float("{0:.1f}".format(ReciprocityQ1S3s))
        ReciprocityQ1S4s=float("{0:.1f}".format(ReciprocityQ1S4s))


#Recirprocity Q2 for both questioniares
        ReciprocityQ2S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q8", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        ReciprocityQ2S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q8", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        ReciprocityQ2S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q8", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        ReciprocityQ2S4= Submission.objects.aggregate(
            overaltrust=
                Sum("q8", filter=(Q(link_id=LID4[0])), output_field=FloatField()))
        ReciprocityQ2S1s=[]
        ReciprocityQ2S2s=[]
        ReciprocityQ2S3s=[]
        ReciprocityQ2S4s=[]

        for key, entry in ReciprocityQ2S1.items():
            if entry is None:
                   ReciprocityQ2S1s.append(0)
            else:
                ReciprocityQ2S1s.append(entry)

        for key, entry in ReciprocityQ2S2.items():
            if entry is None:
                ReciprocityQ2S2s.append(0)
            else:
                ReciprocityQ2S2s.append(entry)

        for key, entry in ReciprocityQ2S3.items():
            if entry is None:
                ReciprocityQ2S3s.append(0)
            else:
                ReciprocityQ2S3s.append(entry)

        for key, entry in ReciprocityQ2S4.items():
            if entry is None:
                ReciprocityQ2S4s.append(0)
            else:
                ReciprocityQ2S4s.append(entry)

        ReciprocityQ2S1s= ReciprocityQ2S1s[0]
        ReciprocityQ2S2s= ReciprocityQ2S2s[0]
        ReciprocityQ2S3s= ReciprocityQ2S3s[0]
        ReciprocityQ2S4s= ReciprocityQ2S4s[0]

        ReciprocityQ2S1s= (ReciprocityQ2S1s*100) / (5*survey1Counts)
        ReciprocityQ2S2s= (ReciprocityQ2S2s*100) / (5*survey2Counts)
        ReciprocityQ2S3s= (ReciprocityQ2S3s*100) / (5*survey3Counts)
        ReciprocityQ2S4s= (ReciprocityQ2S4s*100) / (5*survey4Counts)

        ReciprocityQ2S1s=float("{0:.1f}".format(ReciprocityQ2S1s))
        ReciprocityQ2S2s=float("{0:.1f}".format(ReciprocityQ2S2s))
        ReciprocityQ2S3s=float("{0:.1f}".format(ReciprocityQ2S3s))
        ReciprocityQ2S4s=float("{0:.1f}".format(ReciprocityQ2S4s))
#Riesk Q1 for both questioniares
        GtrustQ1S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q12", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        GtrustQ1S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q12", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        GtrustQ1S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q12", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        GtrustQ1S4= Submission.objects.aggregate(
            overaltrust=
                Sum("q12", filter=(Q(link_id=LID4[0])), output_field=FloatField()))

        GtrustQ1S1s=[]
        GtrustQ1S2s=[]
        GtrustQ1S3s=[]
        GtrustQ1S4s=[]
        for key, entry in GtrustQ1S1.items():
            if entry is None:
                   GtrustQ1S1s.append(0)
            else:
                GtrustQ1S1s.append(entry)

        for key, entry in GtrustQ1S2.items():
            if entry is None:
                GtrustQ1S2s.append(0)
            else:
                GtrustQ1S2s.append(entry)

        for key, entry in GtrustQ1S3.items():
            if entry is None:
                GtrustQ1S3s.append(0)
            else:
                GtrustQ1S3s.append(entry)

        for key, entry in GtrustQ1S4.items():
            if entry is None:
                GtrustQ1S4s.append(0)
            else:
                GtrustQ1S4s.append(entry)

        GtrustQ1S1s= GtrustQ1S1s[0]
        GtrustQ1S2s= GtrustQ1S2s[0]
        GtrustQ1S3s= GtrustQ1S3s[0]
        GtrustQ1S4s= GtrustQ1S4s[0]
        GtrustQ1S1s= (GtrustQ1S1s*100) / (5*survey1Counts)
        GtrustQ1S2s= (GtrustQ1S2s*100) / (5*survey2Counts)
        GtrustQ1S3s= (GtrustQ1S3s*100) / (5*survey3Counts)
        GtrustQ1S4s= (GtrustQ1S4s*100) / (5*survey4Counts)

        GtrustQ1S1s=float("{0:.1f}".format(GtrustQ1S1s))
        GtrustQ1S2s=float("{0:.1f}".format(GtrustQ1S2s))
        GtrustQ1S3s=float("{0:.1f}".format(GtrustQ1S3s))
        GtrustQ1S4s=float("{0:.1f}".format(GtrustQ1S4s))
#Riesk Q2 for both questioniares
        GtrustQ2S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q13", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        GtrustQ2S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q13", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        GtrustQ2S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q13", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        GtrustQ2S4= Submission.objects.aggregate(
            overaltrust=
                Sum("q13", filter=(Q(link_id=LID4[0])), output_field=FloatField()))
        GtrustQ2S1s=[]
        GtrustQ2S2s=[]
        GtrustQ2S3s=[]
        GtrustQ2S4s=[]
        for key, entry in GtrustQ2S1.items():
            if entry is None:
                   GtrustQ2S1s.append(0)
            else:
                GtrustQ2S1s.append(entry)

        for key, entry in GtrustQ2S2.items():
            if entry is None:
                GtrustQ2S2s.append(0)
            else:
                GtrustQ2S2s.append(entry)

        for key, entry in GtrustQ2S3.items():
            if entry is None:
                GtrustQ2S3s.append(0)
            else:
                GtrustQ2S3s.append(entry)

        for key, entry in GtrustQ2S4.items():
            if entry is None:
                GtrustQ2S4s.append(0)
            else:
                GtrustQ2S4s.append(entry)

        GtrustQ2S1s= GtrustQ2S1s[0]
        GtrustQ2S2s= GtrustQ2S2s[0]
        GtrustQ2S3s= GtrustQ2S3s[0]
        GtrustQ2S4s= GtrustQ2S4s[0]
        GtrustQ2S1s= (GtrustQ2S1s*100) / (5*survey1Counts)
        GtrustQ2S2s= (GtrustQ2S2s*100) / (5*survey2Counts)
        GtrustQ2S3s= (GtrustQ2S3s*100) / (5*survey3Counts)
        GtrustQ2S4s= (GtrustQ2S4s*100) / (5*survey4Counts)

        GtrustQ2S1s=float("{0:.1f}".format(GtrustQ2S1s))
        GtrustQ2S2s=float("{0:.1f}".format(GtrustQ2S2s))
        GtrustQ2S3s=float("{0:.1f}".format(GtrustQ2S3s))
        GtrustQ2S4s=float("{0:.1f}".format(GtrustQ2S4s))
#Riesk Q3 for both questioniares
        GtrustQ3S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q14", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        GtrustQ3S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q14", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        GtrustQ3S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q14", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        GtrustQ3S4= Submission.objects.aggregate(
            overaltrust=
                Sum("q14", filter=(Q(link_id=LID4[0])), output_field=FloatField()))

        GtrustQ3S1s=[]
        GtrustQ3S2s=[]
        GtrustQ3S3s=[]
        GtrustQ3S4s=[]

        for key, entry in GtrustQ3S1.items():
            if entry is None:
                   GtrustQ3S1s.append(0)
            else:
                GtrustQ3S1s.append(entry)

        for key, entry in GtrustQ3S2.items():
            if entry is None:
                GtrustQ3S2s.append(0)
            else:
                GtrustQ3S2s.append(entry)

        for key, entry in GtrustQ3S3.items():
            if entry is None:
                GtrustQ3S3s.append(0)
            else:
                GtrustQ3S3s.append(entry)
        for key, entry in GtrustQ3S4.items():
            if entry is None:
                GtrustQ3S4s.append(0)
            else:
                GtrustQ3S4s.append(entry)

        GtrustQ3S1s= GtrustQ3S1s[0]
        GtrustQ3S2s= GtrustQ3S2s[0]
        GtrustQ3S3s= GtrustQ3S3s[0]
        GtrustQ3S4s= GtrustQ3S4s[0]
        GtrustQ3S1s= (GtrustQ3S1s*100) / (5*survey1Counts)
        GtrustQ3S2s= (GtrustQ3S2s*100) / (5*survey2Counts)
        GtrustQ3S3s= (GtrustQ3S3s*100) / (5*survey3Counts)
        GtrustQ3S4s= (GtrustQ3S4s*100) / (5*survey4Counts)

        GtrustQ3S1s=float("{0:.1f}".format(GtrustQ3S1s))
        GtrustQ3S2s=float("{0:.1f}".format(GtrustQ3S2s))
        GtrustQ3S3s=float("{0:.1f}".format(GtrustQ3S3s))
        GtrustQ3S4s=float("{0:.1f}".format(GtrustQ3S4s))

        return render(request, 'pie_chart4.html', {
            'project_id':project_id,
            'productname':productname,
            'survey1Counts':survey1Counts,
            'survey2Counts':survey2Counts,
            'survey3Counts':survey3Counts,
            'survey4Counts':survey4Counts,
            'S1CountGender':S1CountGender,
            'S2CountGender':S2CountGender,
            'S3CountGender':S3CountGender,
            'S4CountGender':S4CountGender,
            'S1CountAge':S1CountAge,
            'S2CountAge':S2CountAge,
            'S3CountAge':S3CountAge,
            'S4CountAge':S4CountAge,
            'CrobanchAlphaS1':CrobanchAlphaS1,
            'CrobanchAlphaS2':CrobanchAlphaS2,
            'CrobanchAlphaS3':CrobanchAlphaS3,
            'CrobanchAlphaS4':CrobanchAlphaS4,
            'OvrallTrustS1s':OvrallTrustS1s,
            'OvrallTrustS2s':OvrallTrustS2s,
            'OvrallTrustS3s':OvrallTrustS3s,
            'OvrallTrustS4s':OvrallTrustS4s,
            'OvrallRiskS1s':OvrallRiskS1s,
            'OvrallRiskS2s':OvrallRiskS2s,
            'OvrallRiskS3s':OvrallRiskS3s,
            'OvrallRiskS4s':OvrallRiskS4s,
            'OvrallBenevolenceS1s':OvrallBenevolenceS1s,
            'OvrallBenevolenceS2s':OvrallBenevolenceS2s,
            'OvrallBenevolenceS3s':OvrallBenevolenceS3s,
            'OvrallBenevolenceS4s':OvrallBenevolenceS4s,
            'OvrallCompetenceS1s':OvrallCompetenceS1s,
            'OvrallCompetenceS2s':OvrallCompetenceS2s,
            'OvrallCompetenceS3s':OvrallCompetenceS3s,
            'OvrallCompetenceS4s':OvrallCompetenceS4s,
            'OvrallReciprocityS1s':OvrallReciprocityS1s,
            'OvrallReciprocityS2s':OvrallReciprocityS2s,
            'OvrallReciprocityS3s':OvrallReciprocityS3s,
            'OvrallReciprocityS4s':OvrallReciprocityS4s,
            'OvrallGeneralTrustS1s':OvrallGeneralTrustS1s,
            'OvrallGeneralTrustS2s':OvrallGeneralTrustS2s,
            'OvrallGeneralTrustS3s':OvrallGeneralTrustS3s,
            'OvrallGeneralTrustS4s':OvrallGeneralTrustS4s,
            'RiskQ1S1s':RiskQ1S1s,
            'RiskQ1S2s':RiskQ1S2s,
            'RiskQ1S3s':RiskQ1S3s,
            'RiskQ1S4s':RiskQ1S4s,
            'RiskQ2S1s':RiskQ2S1s,
            'RiskQ2S2s':RiskQ2S2s,
            'RiskQ2S3s':RiskQ2S3s,
            'RiskQ2S4s':RiskQ2S4s,
            'RiskQ3S1s':RiskQ3S1s,
            'RiskQ3S2s':RiskQ3S2s,
            'RiskQ3S3s':RiskQ3S3s,
            'RiskQ3S4s':RiskQ3S4s,
            'BenevlonceQ1S1s':BenevlonceQ1S1s,
            'BenevlonceQ1S2s':BenevlonceQ1S2s,
            'BenevlonceQ1S3s':BenevlonceQ1S3s,
            'BenevlonceQ1S4s':BenevlonceQ1S4s,
            'BenevlonceQ2S1s':BenevlonceQ2S1s,
            'BenevlonceQ2S2s':BenevlonceQ2S2s,
            'BenevlonceQ2S3s':BenevlonceQ2S3s,
            'BenevlonceQ2S4s':BenevlonceQ2S4s,
            'BenevlonceQ3S1s':BenevlonceQ3S1s,
            'BenevlonceQ3S2s':BenevlonceQ3S2s,
            'BenevlonceQ3S3s':BenevlonceQ3S3s,
            'BenevlonceQ3S4s':BenevlonceQ3S4s,
            'CompetenceQ1S1s':CompetenceQ1S1s,
            'CompetenceQ1S2s':CompetenceQ1S2s,
            'CompetenceQ1S3s':CompetenceQ1S3s,
            'CompetenceQ1S4s':CompetenceQ1S4s,
            'CompetenceQ2S1s':CompetenceQ2S1s,
            'CompetenceQ2S2s':CompetenceQ2S2s,
            'CompetenceQ2S3s':CompetenceQ2S3s,
            'CompetenceQ2S4s':CompetenceQ2S4s,
            'CompetenceQ3S1s':CompetenceQ3S1s,
            'CompetenceQ3S2s':CompetenceQ3S2s,
            'CompetenceQ3S3s':CompetenceQ3S3s,
            'CompetenceQ3S4s':CompetenceQ3S4s,
            'ReciprocityQ1S1s':ReciprocityQ1S1s,
            'ReciprocityQ1S2s':ReciprocityQ1S2s,
            'ReciprocityQ1S3s':ReciprocityQ1S3s,
            'ReciprocityQ1S4s':ReciprocityQ1S4s,
            'ReciprocityQ2S1s':ReciprocityQ2S1s,
            'ReciprocityQ2S2s':ReciprocityQ2S2s,
            'ReciprocityQ2S3s':ReciprocityQ2S3s,
            'ReciprocityQ2S4s':ReciprocityQ2S4s,
            'GtrustQ1S1s':GtrustQ1S1s,
            'GtrustQ1S2s':GtrustQ1S2s,
            'GtrustQ1S3s':GtrustQ1S3s,
            'GtrustQ1S4s':GtrustQ1S4s,
            'GtrustQ2S1s':GtrustQ2S1s,
            'GtrustQ2S2s':GtrustQ2S2s,
            'GtrustQ2S3s':GtrustQ2S3s,
            'GtrustQ2S4s':GtrustQ2S4s,
            'GtrustQ3S1s':GtrustQ3S1s,
            'GtrustQ3S2s':GtrustQ3S2s,
            'GtrustQ3S3s':GtrustQ3S3s,
            'GtrustQ3S4s':GtrustQ3S4s

            })
    elif NumberOfSurveys==5:
        #get the link ids for the two surveys
        LID1 = Link.objects.filter(survey_id=SID[0]).values_list('id', flat=True)
        LID2 = Link.objects.filter(survey_id=SID[1]).values_list('id', flat=True)
        LID3 = Link.objects.filter(survey_id=SID[2]).values_list('id', flat=True)
        LID4 = Link.objects.filter(survey_id=SID[3]).values_list('id', flat=True)
        LID5 = Link.objects.filter(survey_id=SID[4]).values_list('id', flat=True)
        #get the number of respondents by survey
        S1Count = Submission.objects.aggregate(
            responseS1= Count("q1", filter=(Q(link_id=LID1[0])), output_field=IntegerField()))
        S2Count = Submission.objects.aggregate(
            responseS1= Count("q1", filter=(Q(link_id=LID2[0])), output_field=IntegerField()))
        S3Count = Submission.objects.aggregate(
            responseS1= Count("q1", filter=(Q(link_id=LID3[0])), output_field=IntegerField()))
        S4Count = Submission.objects.aggregate(
            responseS1= Count("q1", filter=(Q(link_id=LID4[0])), output_field=IntegerField()))
        S5Count = Submission.objects.aggregate(
            responseS1= Count("q1", filter=(Q(link_id=LID5[0])), output_field=IntegerField()))
        S1Counts=[]
        S2Counts=[]
        S3Counts=[]
        S4Counts=[]
        S5Counts=[]
        for key, entry in S1Count.items():
            if entry is None:
                   S1Counts.append(0)
            else:
                S1Counts.append(entry)
        for key, entry in S2Count.items():
            if entry is None:
                S2Counts.append(0)
            else:
                S2Counts.append(entry)
        for key, entry in S3Count.items():
            if entry is None:
                S3Counts.append(0)
            else:
                S3Counts.append(entry)
        for key, entry in S4Count.items():
            if entry is None:
                S4Counts.append(0)
            else:
                S4Counts.append(entry)
        for key, entry in S5Count.items():
            if entry is None:
                S5Counts.append(0)
            else:
                S5Counts.append(entry)
        survey1Counts= S1Counts[0]
        survey2Counts= S2Counts[0]
        survey3Counts= S3Counts[0]
        survey4Counts= S4Counts[0]
        survey5Counts= S5Counts[0]
        #get number gender details for each survey
        S1CountMale = AnonyData.objects.filter(link_id=LID1[0], gender="M").count()
        S1CountFeMale = AnonyData.objects.filter(link_id=LID1[0], gender="F").count()
        S1CountOthers = AnonyData.objects.filter(link_id=LID1[0], gender="O").count()

        S2CountMale = AnonyData.objects.filter(link_id=LID2[0], gender="M").count()
        S2CountFeMale = AnonyData.objects.filter(link_id=LID2[0], gender="F").count()
        S2CountOthers = AnonyData.objects.filter(link_id=LID2[0], gender="O").count()

        S3CountMale = AnonyData.objects.filter(link_id=LID3[0], gender="M").count()
        S3CountFeMale = AnonyData.objects.filter(link_id=LID3[0], gender="F").count()
        S3CountOthers = AnonyData.objects.filter(link_id=LID3[0], gender="O").count()

        S4CountMale = AnonyData.objects.filter(link_id=LID4[0], gender="M").count()
        S4CountFeMale = AnonyData.objects.filter(link_id=LID4[0], gender="F").count()
        S4CountOthers = AnonyData.objects.filter(link_id=LID4[0], gender="O").count()


        S5CountMale = AnonyData.objects.filter(link_id=LID5[0], gender="M").count()
        S5CountFeMale = AnonyData.objects.filter(link_id=LID5[0], gender="F").count()
        S5CountOthers = AnonyData.objects.filter(link_id=LID5[0], gender="O").count()
            #appending the results to an array because the chartjs piechart expects the data in an array format
        S1CountGender = [S1CountMale, S1CountFeMale, S1CountOthers]
        S2CountGender = [S2CountMale, S2CountFeMale, S2CountOthers]
        S3CountGender = [S3CountMale, S3CountFeMale, S3CountOthers]
        S4CountGender = [S4CountMale, S4CountFeMale, S4CountOthers]
        S5CountGender = [S5CountMale, S4CountFeMale, S4CountOthers]
        #getting the age distribution for each survey
        #survey 1
        S1Count17Below = AnonyData.objects.filter(link_id=LID1[0], age="1").count()
        S1Count18To27 = AnonyData.objects.filter(link_id=LID1[0], age="2").count()
        S1Count28To37 = AnonyData.objects.filter(link_id=LID1[0], age="3").count()
        S1Count38To47 = AnonyData.objects.filter(link_id=LID1[0], age="4").count()
        S1Count48To57 = AnonyData.objects.filter(link_id=LID1[0], age="5").count()
        S1Count58Above = AnonyData.objects.filter(link_id=LID1[0], age="6").count()
        #survey 2
        S2Count17Below = AnonyData.objects.filter(link_id=LID2[0], age="1").count()
        S2Count18To27 = AnonyData.objects.filter(link_id=LID2[0], age="2").count()
        S2Count28To37 = AnonyData.objects.filter(link_id=LID2[0], age="3").count()
        S2Count38To47 = AnonyData.objects.filter(link_id=LID2[0], age="4").count()
        S2Count48To57 = AnonyData.objects.filter(link_id=LID2[0], age="5").count()
        S2Count58Above = AnonyData.objects.filter(link_id=LID2[0], age="6").count()
        #survey 3
        S3Count17Below = AnonyData.objects.filter(link_id=LID3[0], age="1").count()
        S3Count18To27 = AnonyData.objects.filter(link_id=LID3[0], age="2").count()
        S3Count28To37 = AnonyData.objects.filter(link_id=LID3[0], age="3").count()
        S3Count38To47 = AnonyData.objects.filter(link_id=LID3[0], age="4").count()
        S3Count48To57 = AnonyData.objects.filter(link_id=LID3[0], age="5").count()
        S3Count58Above = AnonyData.objects.filter(link_id=LID3[0], age="6").count()

        #survey 4
        S4Count17Below = AnonyData.objects.filter(link_id=LID4[0], age="1").count()
        S4Count18To27 = AnonyData.objects.filter(link_id=LID4[0], age="2").count()
        S4Count28To37 = AnonyData.objects.filter(link_id=LID4[0], age="3").count()
        S4Count38To47 = AnonyData.objects.filter(link_id=LID4[0], age="4").count()
        S4Count48To57 = AnonyData.objects.filter(link_id=LID4[0], age="5").count()
        S4Count58Above = AnonyData.objects.filter(link_id=LID4[0], age="6").count()

        #survey 4
        S5Count17Below = AnonyData.objects.filter(link_id=LID5[0], age="1").count()
        S5Count18To27 = AnonyData.objects.filter(link_id=LID5[0], age="2").count()
        S5Count28To37 = AnonyData.objects.filter(link_id=LID5[0], age="3").count()
        S5Count38To47 = AnonyData.objects.filter(link_id=LID5[0], age="4").count()
        S5Count48To57 = AnonyData.objects.filter(link_id=LID5[0], age="5").count()
        S5Count58Above = AnonyData.objects.filter(link_id=LID5[0], age="6").count()

            #appending the results to an array because the chartjs piechart expects the data in an array format
        S1CountAge = [S1Count17Below, S1Count18To27, S1Count28To37, S1Count38To47, S1Count48To57, S1Count58Above ]
        S2CountAge = [S2Count17Below, S2Count18To27, S2Count28To37, S2Count38To47, S2Count48To57, S2Count58Above ]
        S3CountAge = [S3Count17Below, S3Count18To27, S3Count28To37, S3Count38To47, S3Count48To57, S3Count58Above ]
        S4CountAge = [S4Count17Below, S4Count18To27, S4Count28To37, S4Count38To47, S4Count48To57, S4Count58Above ]
        S5CountAge = [S5Count17Below, S5Count18To27, S5Count28To37, S5Count38To47, S5Count48To57, S5Count58Above ]
        #check for null entries and replace them with 0
        for i in S1CountAge:
            if i == '':
                S1CountAge[i]=0
            else:
                S1CountAge[i] = S1CountAge[i]

        for i in S2CountAge:
            if i == '':
                S2CountAge[i]=0
            else:
                S2CountAge[i] = S2CountAge[i]

        for i in S3CountAge:
            if i == '':
                S3CountAge[i]=0
            else:
                S3CountAge[i] = S2CountAge[i]

        for i in S4CountAge:
            if i == '':
                S4CountAge[i]=0
            else:
                S4CountAge[i] = S4CountAge[i]

        for i in S5CountAge:
            if i == '':
                S5CountAge[i]=0
            else:
                S5CountAge[i] = S5CountAge[i]
        #print(S1CountAge)
        #print(S2CountAge)
        #get all response for each survey
        allRespS1= Submission.objects.values('q1','q2','q3','q4','q5','q6','q7','q8','q9','q10','q11','q12','q13','q14').filter(Q(link_id=LID1[0])).all()
        allRespS2= Submission.objects.values('q1','q2','q3','q4','q5','q6','q7','q8','q9','q10','q11','q12','q13','q14').filter(Q(link_id=LID2[0])).all()
        allRespS3= Submission.objects.values('q1','q2','q3','q4','q5','q6','q7','q8','q9','q10','q11','q12','q13','q14').filter(Q(link_id=LID3[0])).all()
        allRespS4= Submission.objects.values('q1','q2','q3','q4','q5','q6','q7','q8','q9','q10','q11','q12','q13','q14').filter(Q(link_id=LID4[0])).all()
        allRespS5= Submission.objects.values('q1','q2','q3','q4','q5','q6','q7','q8','q9','q10','q11','q12','q13','q14').filter(Q(link_id=LID5[0])).all()
        #convert the querryset into dataframe
        allRespS1=df.DataFrame.from_records(allRespS1)
        allRespS2=df.DataFrame.from_records(allRespS2)
        allRespS3=df.DataFrame.from_records(allRespS3)
        allRespS4=df.DataFrame.from_records(allRespS4)
        allRespS5=df.DataFrame.from_records(allRespS5)
        #compute the crobanch alpha for each survey using the aggregated responses in dataframe form above
        CrobanchAlphaS1=cronbach_alpha(allRespS1)
        CrobanchAlphaS2=cronbach_alpha(allRespS2)
        CrobanchAlphaS3=cronbach_alpha(allRespS3)
        CrobanchAlphaS4=cronbach_alpha(allRespS4)
        CrobanchAlphaS5=cronbach_alpha(allRespS5)
        #reducing the result to two decimal places
        CrobanchAlphaS1=float("{0:.4f}".format(CrobanchAlphaS1))
        CrobanchAlphaS2=float("{0:.4f}".format(CrobanchAlphaS2))
        CrobanchAlphaS3=float("{0:.4f}".format(CrobanchAlphaS3))
        CrobanchAlphaS4=float("{0:.4f}".format(CrobanchAlphaS4))
        CrobanchAlphaS5=float("{0:.4f}".format(CrobanchAlphaS5))

        if math.isnan(CrobanchAlphaS1):
            CrobanchAlphaS1=0.0
        else:
            CrobanchAlphaS1=CrobanchAlphaS1

        if math.isnan(CrobanchAlphaS2):
            CrobanchAlphaS2=0.0
        else:
            CrobanchAlphaS2=CrobanchAlphaS2

        if math.isnan(CrobanchAlphaS3):
            CrobanchAlphaS3=0.0
        else:
            CrobanchAlphaS3=CrobanchAlphaS3

        if math.isnan(CrobanchAlphaS4):
            CrobanchAlphaS4=0.0
        else:
            CrobanchAlphaS4=CrobanchAlphaS4

        if math.isnan(CrobanchAlphaS5):
            CrobanchAlphaS5=0.0
        else:
            CrobanchAlphaS5=CrobanchAlphaS5
        print(CrobanchAlphaS5)
#compute overall trust score for each survey begins from here
        OvrallTrustS1= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q2", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q3", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q4", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q5", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q6", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q7", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q8", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q9", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q10", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q11", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q12", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q13", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q14", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        OvrallTrustS2= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q2", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q3", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q4", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q5", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q6", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q7", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q8", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q9", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q10", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q11", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q12", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q13", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q14", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        OvrallTrustS3= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q2", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q3", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q4", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q5", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q6", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q7", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q8", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q9", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q10", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q11", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q12", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q13", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q14", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        OvrallTrustS4= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q2", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q3", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q4", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q5", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q6", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q7", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q8", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q9", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q10", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q11", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q12", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q13", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q14", filter=(Q(link_id=LID4[0])), output_field=FloatField()))
        OvrallTrustS5= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID5[0])), output_field=FloatField())+
                Sum("q2", filter=(Q(link_id=LID5[0])), output_field=FloatField())+
                Sum("q3", filter=(Q(link_id=LID5[0])), output_field=FloatField())+
                Sum("q4", filter=(Q(link_id=LID5[0])), output_field=FloatField())+
                Sum("q5", filter=(Q(link_id=LID5[0])), output_field=FloatField())+
                Sum("q6", filter=(Q(link_id=LID5[0])), output_field=FloatField())+
                Sum("q7", filter=(Q(link_id=LID5[0])), output_field=FloatField())+
                Sum("q8", filter=(Q(link_id=LID5[0])), output_field=FloatField())+
                Sum("q9", filter=(Q(link_id=LID5[0])), output_field=FloatField())+
                Sum("q10", filter=(Q(link_id=LID5[0])), output_field=FloatField())+
                Sum("q11", filter=(Q(link_id=LID5[0])), output_field=FloatField())+
                Sum("q12", filter=(Q(link_id=LID5[0])), output_field=FloatField())+
                Sum("q13", filter=(Q(link_id=LID5[0])), output_field=FloatField())+
                Sum("q14", filter=(Q(link_id=LID5[0])), output_field=FloatField()))
        OvrallTrustS1s=[]
        OvrallTrustS2s=[]
        OvrallTrustS3s=[]
        OvrallTrustS4s=[]
        OvrallTrustS5s=[]
        for key, entry in OvrallTrustS1.items():
            if entry is None:
                   OvrallTrustS1s.append(0)
            else:
                OvrallTrustS1s.append(entry)

        for key, entry in OvrallTrustS2.items():
            if entry is None:
                OvrallTrustS2s.append(0)
            else:
                OvrallTrustS2s.append(entry)

        for key, entry in OvrallTrustS3.items():
            if entry is None:
                OvrallTrustS3s.append(0)
            else:
                OvrallTrustS3s.append(entry)

        for key, entry in OvrallTrustS4.items():
            if entry is None:
                OvrallTrustS4s.append(0)
            else:
                OvrallTrustS4s.append(entry)

        for key, entry in OvrallTrustS5.items():
            if entry is None:
                OvrallTrustS5s.append(0)
            else:
                OvrallTrustS5s.append(entry)

        OvrallTrustS1s= OvrallTrustS1s[0]
        OvrallTrustS2s= OvrallTrustS2s[0]
        OvrallTrustS3s= OvrallTrustS3s[0]
        OvrallTrustS4s= OvrallTrustS4s[0]
        OvrallTrustS5s= OvrallTrustS5s[0]

        OvrallTrustS1s= (OvrallTrustS1s*100) / (70*survey1Counts)
        OvrallTrustS2s= (OvrallTrustS2s*100) / (70*survey2Counts)
        OvrallTrustS3s= (OvrallTrustS3s*100) / (70*survey3Counts)
        OvrallTrustS4s= (OvrallTrustS4s*100) / (70*survey4Counts)
        OvrallTrustS5s= (OvrallTrustS5s*100) / (70*survey5Counts)

        OvrallTrustS1s=float("{0:.1f}".format(OvrallTrustS1s))
        OvrallTrustS2s=float("{0:.1f}".format(OvrallTrustS2s))
        OvrallTrustS3s=float("{0:.1f}".format(OvrallTrustS3s))
        OvrallTrustS4s=float("{0:.1f}".format(OvrallTrustS4s))
        OvrallTrustS5s=float("{0:.1f}".format(OvrallTrustS5s))
#computing overall risk for each survey
        OvrallRiskS1= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q2", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q3", filter=(Q(link_id=LID1[0])), output_field=FloatField())
                )
        OvrallRiskS2= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q2", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q3", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        OvrallRiskS3= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q2", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q3", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        OvrallRiskS4= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q2", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q3", filter=(Q(link_id=LID4[0])), output_field=FloatField()))
        OvrallRiskS5= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID5[0])), output_field=FloatField())+
                Sum("q2", filter=(Q(link_id=LID5[0])), output_field=FloatField())+
                Sum("q3", filter=(Q(link_id=LID5[0])), output_field=FloatField()))

        OvrallRiskS1s=[]
        OvrallRiskS2s=[]
        OvrallRiskS3s=[]
        OvrallRiskS4s=[]
        OvrallRiskS5s=[]
        for key, entry in OvrallRiskS1.items():
            if entry is None:
                   OvrallRiskS1s.append(0)
            else:
                OvrallRiskS1s.append(entry)

        for key, entry in OvrallRiskS2.items():
            if entry is None:
                OvrallRiskS2s.append(0)
            else:
                OvrallRiskS2s.append(entry)

        for key, entry in OvrallRiskS3.items():
            if entry is None:
                OvrallRiskS3s.append(0)
            else:
                OvrallRiskS3s.append(entry)

        for key, entry in OvrallRiskS4.items():
            if entry is None:
                OvrallRiskS4s.append(0)
            else:
                OvrallRiskS4s.append(entry)

        for key, entry in OvrallRiskS5.items():
            if entry is None:
                OvrallRiskS5s.append(0)
            else:
                OvrallRiskS5s.append(entry)

        OvrallRiskS1s= OvrallRiskS1s[0]
        OvrallRiskS2s= OvrallRiskS2s[0]
        OvrallRiskS3s= OvrallRiskS3s[0]
        OvrallRiskS4s= OvrallRiskS4s[0]
        OvrallRiskS5s= OvrallRiskS5s[0]
        OvrallRiskS1s= (OvrallRiskS1s*100) / (15*survey1Counts)
        OvrallRiskS2s= (OvrallRiskS2s*100) / (15*survey2Counts)
        OvrallRiskS3s= (OvrallRiskS3s*100) / (15*survey3Counts)
        OvrallRiskS4s= (OvrallRiskS4s*100) / (15*survey4Counts)
        OvrallRiskS5s= (OvrallRiskS5s*100) / (15*survey5Counts)

        OvrallRiskS1s=float("{0:.1f}".format(OvrallRiskS1s))
        OvrallRiskS2s=float("{0:.1f}".format(OvrallRiskS2s))
        OvrallRiskS3s=float("{0:.1f}".format(OvrallRiskS3s))
        OvrallRiskS4s=float("{0:.1f}".format(OvrallRiskS4s))
        OvrallRiskS5s=float("{0:.1f}".format(OvrallRiskS5s))
#computing benevolencerisk for each survey
        OvrallBenevolenceS1= Submission.objects.aggregate(
            overalBenevolence=
                Sum("q4", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q5", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q6", filter=(Q(link_id=LID1[0])), output_field=FloatField())
                )
        OvrallBenevolenceS2= Submission.objects.aggregate(
            overalBenevolence=
                Sum("q4", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q5", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q6", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        OvrallBenevolenceS3= Submission.objects.aggregate(
            overalBenevolence=
                Sum("q4", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q5", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q6", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        OvrallBenevolenceS4= Submission.objects.aggregate(
            overalBenevolence=
                Sum("q4", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q5", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q6", filter=(Q(link_id=LID4[0])), output_field=FloatField()))
        OvrallBenevolenceS5= Submission.objects.aggregate(
            overalBenevolence=
                Sum("q4", filter=(Q(link_id=LID5[0])), output_field=FloatField())+
                Sum("q5", filter=(Q(link_id=LID5[0])), output_field=FloatField())+
                Sum("q6", filter=(Q(link_id=LID5[0])), output_field=FloatField()))
        OvrallBenevolenceS1s=[]
        OvrallBenevolenceS2s=[]
        OvrallBenevolenceS3s=[]
        OvrallBenevolenceS4s=[]
        OvrallBenevolenceS5s=[]
        for key, entry in OvrallBenevolenceS1.items():
            if entry is None:
                   OvrallBenevolenceS1s.append(0)
            else:
                OvrallBenevolenceS1s.append(entry)

        for key, entry in OvrallBenevolenceS2.items():
            if entry is None:
                OvrallBenevolenceS2s.append(0)
            else:
                OvrallBenevolenceS2s.append(entry)

        for key, entry in OvrallBenevolenceS3.items():
            if entry is None:
                OvrallBenevolenceS3s.append(0)
            else:
                OvrallBenevolenceS3s.append(entry)

        for key, entry in OvrallBenevolenceS4.items():
            if entry is None:
                OvrallBenevolenceS4s.append(0)
            else:
                OvrallBenevolenceS4s.append(entry)

        for key, entry in OvrallBenevolenceS5.items():
            if entry is None:
                OvrallBenevolenceS5s.append(0)
            else:
                OvrallBenevolenceS5s.append(entry)

        OvrallBenevolenceS1s= OvrallBenevolenceS1s[0]
        OvrallBenevolenceS2s= OvrallBenevolenceS2s[0]
        OvrallBenevolenceS3s= OvrallBenevolenceS3s[0]
        OvrallBenevolenceS4s= OvrallBenevolenceS4s[0]
        OvrallBenevolenceS5s= OvrallBenevolenceS5s[0]

        OvrallBenevolenceS1s= (OvrallBenevolenceS1s*100) / (15*survey1Counts)
        OvrallBenevolenceS2s= (OvrallBenevolenceS2s*100) / (15*survey2Counts)
        OvrallBenevolenceS3s= (OvrallBenevolenceS3s*100) / (15*survey3Counts)
        OvrallBenevolenceS4s= (OvrallBenevolenceS4s*100) / (15*survey4Counts)
        OvrallBenevolenceS5s= (OvrallBenevolenceS5s*100) / (15*survey5Counts)

        OvrallBenevolenceS1s=float("{0:.1f}".format(OvrallBenevolenceS1s))
        OvrallBenevolenceS2s=float("{0:.1f}".format(OvrallBenevolenceS2s))
        OvrallBenevolenceS3s=float("{0:.1f}".format(OvrallBenevolenceS3s))
        OvrallBenevolenceS4s=float("{0:.1f}".format(OvrallBenevolenceS4s))
        OvrallBenevolenceS5s=float("{0:.1f}".format(OvrallBenevolenceS5s))

# computing competence for each survey
        OvrallCompetenceS1= Submission.objects.aggregate(
            overalCompetence=
                Sum("q7", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q8", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q9", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        OvrallCompetenceS2= Submission.objects.aggregate(
            overalCompetence=
                Sum("q7", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q8", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q9", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        OvrallCompetenceS3= Submission.objects.aggregate(
            overalCompetence=
                Sum("q7", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q8", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q9", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        OvrallCompetenceS4= Submission.objects.aggregate(
            overalCompetence=
                Sum("q7", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q8", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q9", filter=(Q(link_id=LID4[0])), output_field=FloatField()))
        OvrallCompetenceS5= Submission.objects.aggregate(
            overalCompetence=
                Sum("q7", filter=(Q(link_id=LID5[0])), output_field=FloatField())+
                Sum("q8", filter=(Q(link_id=LID5[0])), output_field=FloatField())+
                Sum("q9", filter=(Q(link_id=LID5[0])), output_field=FloatField()))



        OvrallCompetenceS1s=[]
        OvrallCompetenceS2s=[]
        OvrallCompetenceS3s=[]
        OvrallCompetenceS4s=[]
        OvrallCompetenceS5s=[]

        for key, entry in OvrallCompetenceS1.items():
            if entry is None:
                   OvrallCompetenceS1s.append(0)
            else:
                OvrallCompetenceS1s.append(entry)

        for key, entry in OvrallCompetenceS2.items():
            if entry is None:
                OvrallCompetenceS2s.append(0)
            else:
                OvrallCompetenceS2s.append(entry)

        for key, entry in OvrallCompetenceS3.items():
            if entry is None:
                OvrallCompetenceS3s.append(0)
            else:
                OvrallCompetenceS3s.append(entry)

        for key, entry in OvrallCompetenceS4.items():
            if entry is None:
                OvrallCompetenceS4s.append(0)
            else:
                OvrallCompetenceS4s.append(entry)

        for key, entry in OvrallCompetenceS5.items():
            if entry is None:
                OvrallCompetenceS5s.append(0)
            else:
                OvrallCompetenceS5s.append(entry)

        OvrallCompetenceS1s= OvrallCompetenceS1s[0]
        OvrallCompetenceS2s= OvrallCompetenceS2s[0]
        OvrallCompetenceS3s= OvrallCompetenceS3s[0]
        OvrallCompetenceS4s= OvrallCompetenceS4s[0]
        OvrallCompetenceS5s= OvrallCompetenceS5s[0]

        OvrallCompetenceS1s= (OvrallCompetenceS1s*100) / (15*survey1Counts)
        OvrallCompetenceS2s= (OvrallCompetenceS2s*100) / (15*survey2Counts)
        OvrallCompetenceS3s= (OvrallCompetenceS3s*100) / (15*survey3Counts)
        OvrallCompetenceS4s= (OvrallCompetenceS4s*100) / (15*survey4Counts)
        OvrallCompetenceS5s= (OvrallCompetenceS5s*100) / (15*survey5Counts)

        OvrallCompetenceS1s=float("{0:.1f}".format(OvrallCompetenceS1s))
        OvrallCompetenceS2s=float("{0:.1f}".format(OvrallCompetenceS2s))
        OvrallCompetenceS3s=float("{0:.1f}".format(OvrallCompetenceS3s))
        OvrallCompetenceS4s=float("{0:.1f}".format(OvrallCompetenceS4s))
        OvrallCompetenceS5s=float("{0:.1f}".format(OvrallCompetenceS5s))
# computing reciprocity
        OvrallReciprocityS1= Submission.objects.aggregate(
            overalReciprocity=
                Sum("q10", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q11", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        OvrallReciprocityS2= Submission.objects.aggregate(
            overalReciprocity=
                Sum("q10", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q11", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        OvrallReciprocityS3= Submission.objects.aggregate(
            overalReciprocity=
                Sum("q10", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q11", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        OvrallReciprocityS4= Submission.objects.aggregate(
            overalReciprocity=
                Sum("q10", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q11", filter=(Q(link_id=LID4[0])), output_field=FloatField()))
        OvrallReciprocityS5= Submission.objects.aggregate(
            overalReciprocity=
                Sum("q10", filter=(Q(link_id=LID5[0])), output_field=FloatField())+
                Sum("q11", filter=(Q(link_id=LID5[0])), output_field=FloatField()))

        OvrallReciprocityS1s=[]
        OvrallReciprocityS2s=[]
        OvrallReciprocityS3s=[]
        OvrallReciprocityS4s=[]
        OvrallReciprocityS5s=[]
        for key, entry in OvrallReciprocityS1.items():
            if entry is None:
                   OvrallReciprocityS1s.append(0)
            else:
                OvrallReciprocityS1s.append(entry)

        for key, entry in OvrallReciprocityS2.items():
            if entry is None:
                OvrallReciprocityS2s.append(0)
            else:
                OvrallReciprocityS2s.append(entry)

        for key, entry in OvrallReciprocityS3.items():
            if entry is None:
                OvrallReciprocityS3s.append(0)
            else:
                OvrallReciprocityS3s.append(entry)
        for key, entry in OvrallReciprocityS4.items():
            if entry is None:
                OvrallReciprocityS4s.append(0)
            else:
                OvrallReciprocityS4s.append(entry)
        for key, entry in OvrallReciprocityS5.items():
            if entry is None:
                OvrallReciprocityS5s.append(0)
            else:
                OvrallReciprocityS5s.append(entry)

        OvrallReciprocityS1s= OvrallReciprocityS1s[0]
        OvrallReciprocityS2s= OvrallReciprocityS2s[0]
        OvrallReciprocityS3s= OvrallReciprocityS3s[0]
        OvrallReciprocityS4s= OvrallReciprocityS4s[0]
        OvrallReciprocityS5s= OvrallReciprocityS5s[0]
        OvrallReciprocityS1s= (OvrallReciprocityS1s*100) / (10*survey1Counts)
        OvrallReciprocityS2s= (OvrallReciprocityS2s*100) / (10*survey2Counts)
        OvrallReciprocityS3s= (OvrallReciprocityS3s*100) / (10*survey3Counts)
        OvrallReciprocityS4s= (OvrallReciprocityS4s*100) / (10*survey4Counts)
        OvrallReciprocityS5s= (OvrallReciprocityS5s*100) / (10*survey5Counts)

        OvrallReciprocityS1s=float("{0:.1f}".format(OvrallReciprocityS1s))
        OvrallReciprocityS2s=float("{0:.1f}".format(OvrallReciprocityS2s))
        OvrallReciprocityS3s=float("{0:.1f}".format(OvrallReciprocityS3s))
        OvrallReciprocityS4s=float("{0:.1f}".format(OvrallReciprocityS4s))
        OvrallReciprocityS5s=float("{0:.1f}".format(OvrallReciprocityS5s))

#Computing general trust for each survey
        OvrallGeneralTrustS1= Submission.objects.aggregate(
            overalGeneralTrust=
                Sum("q12", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q13", filter=(Q(link_id=LID1[0])), output_field=FloatField())+
                Sum("q14", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        OvrallGeneralTrustS2= Submission.objects.aggregate(
            overalGeneralTrust=
                Sum("q12", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q13", filter=(Q(link_id=LID2[0])), output_field=FloatField())+
                Sum("q14", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        OvrallGeneralTrustS3= Submission.objects.aggregate(
            overalGeneralTrust=
                Sum("q12", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q13", filter=(Q(link_id=LID3[0])), output_field=FloatField())+
                Sum("q14", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        OvrallGeneralTrustS4= Submission.objects.aggregate(
            overalGeneralTrust=
                Sum("q12", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q13", filter=(Q(link_id=LID4[0])), output_field=FloatField())+
                Sum("q14", filter=(Q(link_id=LID4[0])), output_field=FloatField()))
        OvrallGeneralTrustS5= Submission.objects.aggregate(
            overalGeneralTrust=
                Sum("q12", filter=(Q(link_id=LID5[0])), output_field=FloatField())+
                Sum("q13", filter=(Q(link_id=LID5[0])), output_field=FloatField())+
                Sum("q14", filter=(Q(link_id=LID5[0])), output_field=FloatField()))

        OvrallGeneralTrustS1s=[]
        OvrallGeneralTrustS2s=[]
        OvrallGeneralTrustS3s=[]
        OvrallGeneralTrustS4s=[]
        OvrallGeneralTrustS5s=[]
        for key, entry in OvrallGeneralTrustS1.items():
            if entry is None:
                   OvrallGeneralTrustS1s.append(0)
            else:
                OvrallGeneralTrustS1s.append(entry)

        for key, entry in OvrallGeneralTrustS2.items():
            if entry is None:
                OvrallGeneralTrustS2s.append(0)
            else:
                OvrallGeneralTrustS2s.append(entry)

        for key, entry in OvrallGeneralTrustS3.items():
            if entry is None:
                OvrallGeneralTrustS3s.append(0)
            else:
                OvrallGeneralTrustS3s.append(entry)
        for key, entry in OvrallGeneralTrustS4.items():
            if entry is None:
                OvrallGeneralTrustS4s.append(0)
            else:
                OvrallGeneralTrustS4s.append(entry)
        for key, entry in OvrallGeneralTrustS5.items():
            if entry is None:
                OvrallGeneralTrustS5s.append(0)
            else:
                OvrallGeneralTrustS5s.append(entry)

        OvrallGeneralTrustS1s= OvrallGeneralTrustS1s[0]
        OvrallGeneralTrustS2s= OvrallGeneralTrustS2s[0]
        OvrallGeneralTrustS3s= OvrallGeneralTrustS3s[0]
        OvrallGeneralTrustS4s= OvrallGeneralTrustS4s[0]
        OvrallGeneralTrustS5s= OvrallGeneralTrustS5s[0]

        OvrallGeneralTrustS1s= (OvrallGeneralTrustS1s*100) / (15*survey1Counts)
        OvrallGeneralTrustS2s= (OvrallGeneralTrustS2s*100) / (15*survey2Counts)
        OvrallGeneralTrustS3s= (OvrallGeneralTrustS3s*100) / (15*survey3Counts)
        OvrallGeneralTrustS4s= (OvrallGeneralTrustS4s*100) / (15*survey4Counts)
        OvrallGeneralTrustS5s= (OvrallGeneralTrustS5s*100) / (15*survey5Counts)

        OvrallGeneralTrustS1s=float("{0:.1f}".format(OvrallGeneralTrustS1s))
        OvrallGeneralTrustS2s=float("{0:.1f}".format(OvrallGeneralTrustS2s))
        OvrallGeneralTrustS3s=float("{0:.1f}".format(OvrallGeneralTrustS3s))
        OvrallGeneralTrustS4s=float("{0:.1f}".format(OvrallGeneralTrustS4s))
        OvrallGeneralTrustS5s=float("{0:.1f}".format(OvrallGeneralTrustS5s))

#Riesk Q1 for both questioniares
        RiskQ1S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        RiskQ1S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        RiskQ1S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        RiskQ1S4= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID4[0])), output_field=FloatField()))
        RiskQ1S5= Submission.objects.aggregate(
            overaltrust=
                Sum("q1", filter=(Q(link_id=LID5[0])), output_field=FloatField()))

        RiskQ1S1s=[]
        RiskQ1S2s=[]
        RiskQ1S3s=[]
        RiskQ1S4s=[]
        RiskQ1S5s=[]
        for key, entry in RiskQ1S1.items():
            if entry is None:
                   RiskQ1S1s.append(0)
            else:
                RiskQ1S1s.append(entry)

        for key, entry in RiskQ1S2.items():
            if entry is None:
                RiskQ1S2s.append(0)
            else:
                RiskQ1S2s.append(entry)

        for key, entry in RiskQ1S3.items():
            if entry is None:
                RiskQ1S3s.append(0)
            else:
                RiskQ1S3s.append(entry)
        for key, entry in RiskQ1S4.items():
            if entry is None:
                RiskQ1S4s.append(0)
            else:
                RiskQ1S4s.append(entry)
        for key, entry in RiskQ1S5.items():
            if entry is None:
                RiskQ1S5s.append(0)
            else:
                RiskQ1S5s.append(entry)

        RiskQ1S1s= RiskQ1S1s[0]
        RiskQ1S2s= RiskQ1S2s[0]
        RiskQ1S3s= RiskQ1S3s[0]
        RiskQ1S4s= RiskQ1S4s[0]
        RiskQ1S5s= RiskQ1S5s[0]

        RiskQ1S1s= (RiskQ1S1s*100) / (5*survey1Counts)
        RiskQ1S2s= (RiskQ1S2s*100) / (5*survey2Counts)
        RiskQ1S3s= (RiskQ1S3s*100) / (5*survey3Counts)
        RiskQ1S4s= (RiskQ1S4s*100) / (5*survey4Counts)
        RiskQ1S4s= (RiskQ1S5s*100) / (5*survey5Counts)

        RiskQ1S1s=float("{0:.1f}".format(RiskQ1S1s))
        RiskQ1S2s=float("{0:.1f}".format(RiskQ1S2s))
        RiskQ1S3s=float("{0:.1f}".format(RiskQ1S3s))
        RiskQ1S4s=float("{0:.1f}".format(RiskQ1S4s))
        RiskQ1S5s=float("{0:.1f}".format(RiskQ1S5s))
#Riesk Q2 for both questioniares
        RiskQ2S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q2", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        RiskQ2S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q2", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        RiskQ2S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q2", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        RiskQ2S4= Submission.objects.aggregate(
            overaltrust=
                Sum("q2", filter=(Q(link_id=LID4[0])), output_field=FloatField()))
        RiskQ2S5= Submission.objects.aggregate(
            overaltrust=
                Sum("q2", filter=(Q(link_id=LID5[0])), output_field=FloatField()))
        RiskQ2S1s=[]
        RiskQ2S2s=[]
        RiskQ2S3s=[]
        RiskQ2S4s=[]
        RiskQ2S5s=[]
        for key, entry in RiskQ2S1.items():
            if entry is None:
                   RiskQ2S1s.append(0)
            else:
                RiskQ2S1s.append(entry)

        for key, entry in RiskQ2S2.items():
            if entry is None:
                RiskQ2S2s.append(0)
            else:
                RiskQ2S2s.append(entry)

        for key, entry in RiskQ2S3.items():
            if entry is None:
                RiskQ2S3s.append(0)
            else:
                RiskQ2S3s.append(entry)
        for key, entry in RiskQ2S4.items():
            if entry is None:
                RiskQ2S4s.append(0)
            else:
                RiskQ2S4s.append(entry)
        for key, entry in RiskQ2S5.items():
            if entry is None:
                RiskQ2S5s.append(0)
            else:
                RiskQ2S5s.append(entry)
        RiskQ2S1s= RiskQ2S1s[0]
        RiskQ2S2s= RiskQ2S2s[0]
        RiskQ2S3s= RiskQ2S3s[0]
        RiskQ2S4s= RiskQ2S4s[0]
        RiskQ2S5s= RiskQ2S5s[0]
        RiskQ2S1s= (RiskQ2S1s*100) / (5*survey1Counts)
        RiskQ2S2s= (RiskQ2S2s*100) / (5*survey1Counts)
        RiskQ2S3s= (RiskQ2S3s*100) / (5*survey3Counts)
        RiskQ2S4s= (RiskQ2S4s*100) / (5*survey4Counts)
        RiskQ2S5s= (RiskQ2S5s*100) / (5*survey5Counts)


        RiskQ2S1s=float("{0:.1f}".format(RiskQ2S1s))
        RiskQ2S2s=float("{0:.1f}".format(RiskQ2S2s))
        RiskQ2S3s=float("{0:.1f}".format(RiskQ2S3s))
        RiskQ2S4s=float("{0:.1f}".format(RiskQ2S4s))
        RiskQ2S5s=float("{0:.1f}".format(RiskQ2S5s))
#Riesk Q3 for both questioniares
        RiskQ3S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q3", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        RiskQ3S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q3", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        RiskQ3S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q3", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        RiskQ3S4= Submission.objects.aggregate(
            overaltrust=
                Sum("q3", filter=(Q(link_id=LID4[0])), output_field=FloatField()))
        RiskQ3S5= Submission.objects.aggregate(
            overaltrust=
                Sum("q3", filter=(Q(link_id=LID5[0])), output_field=FloatField()))

        RiskQ3S1s=[]
        RiskQ3S2s=[]
        RiskQ3S3s=[]
        RiskQ3S4s=[]
        RiskQ3S5s=[]
        for key, entry in RiskQ3S1.items():
            if entry is None:
                   RiskQ3S1s.append(0)
            else:
                RiskQ3S1s.append(entry)

        for key, entry in RiskQ3S2.items():
            if entry is None:
                RiskQ3S2s.append(0)
            else:
                RiskQ3S2s.append(entry)

        for key, entry in RiskQ3S3.items():
            if entry is None:
                RiskQ3S3s.append(0)
            else:
                RiskQ3S3s.append(entry)

        for key, entry in RiskQ3S4.items():
            if entry is None:
                RiskQ3S4s.append(0)
            else:
                RiskQ3S4s.append(entry)

        for key, entry in RiskQ3S5.items():
            if entry is None:
                RiskQ3S5s.append(0)
            else:
                RiskQ3S5s.append(entry)

        RiskQ3S1s= RiskQ3S1s[0]
        RiskQ3S2s= RiskQ3S2s[0]
        RiskQ3S3s= RiskQ3S3s[0]
        RiskQ3S4s= RiskQ3S4s[0]
        RiskQ3S5s= RiskQ3S5s[0]
        RiskQ3S1s= (RiskQ3S1s*100) / (5*survey1Counts)
        RiskQ3S2s= (RiskQ3S2s*100) / (5*survey1Counts)
        RiskQ3S3s= (RiskQ3S3s*100) / (5*survey3Counts)
        RiskQ3S4s= (RiskQ3S4s*100) / (5*survey4Counts)
        RiskQ3S5s= (RiskQ3S5s*100) / (5*survey5Counts)

        RiskQ3S1s=float("{0:.1f}".format(RiskQ3S1s))
        RiskQ3S2s=float("{0:.1f}".format(RiskQ3S2s))
        RiskQ3S3s=float("{0:.1f}".format(RiskQ3S3s))
        RiskQ3S4s=float("{0:.1f}".format(RiskQ3S4s))
        RiskQ3S5s=float("{0:.1f}".format(RiskQ3S5s))

#benevolence Q1 for both questioniares
        BenevlonceQ1S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q4", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        BenevlonceQ1S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q4", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        BenevlonceQ1S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q4", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        BenevlonceQ1S4= Submission.objects.aggregate(
            overaltrust=
                Sum("q4", filter=(Q(link_id=LID4[0])), output_field=FloatField()))
        BenevlonceQ1S5= Submission.objects.aggregate(
            overaltrust=
                Sum("q4", filter=(Q(link_id=LID5[0])), output_field=FloatField()))

        BenevlonceQ1S1s=[]
        BenevlonceQ1S2s=[]
        BenevlonceQ1S3s=[]
        BenevlonceQ1S4s=[]
        BenevlonceQ1S5s=[]
        for key, entry in BenevlonceQ1S1.items():
            if entry is None:
                   BenevlonceQ1S1s.append(0)
            else:
                BenevlonceQ1S1s.append(entry)

        for key, entry in BenevlonceQ1S2.items():
            if entry is None:
                BenevlonceQ1S2s.append(0)
            else:
                BenevlonceQ1S2s.append(entry)

        for key, entry in BenevlonceQ1S3.items():
            if entry is None:
                BenevlonceQ1S3s.append(0)
            else:
                BenevlonceQ1S3s.append(entry)
        for key, entry in BenevlonceQ1S4.items():
            if entry is None:
                BenevlonceQ1S4s.append(0)
            else:
                BenevlonceQ1S4s.append(entry)
        for key, entry in BenevlonceQ1S5.items():
            if entry is None:
                BenevlonceQ1S5s.append(0)
            else:
                BenevlonceQ1S5s.append(entry)

        BenevlonceQ1S1s= BenevlonceQ1S1s[0]
        BenevlonceQ1S2s= BenevlonceQ1S2s[0]
        BenevlonceQ1S3s= BenevlonceQ1S3s[0]
        BenevlonceQ1S4s= BenevlonceQ1S4s[0]
        BenevlonceQ1S5s= BenevlonceQ1S5s[0]

        BenevlonceQ1S1s= (BenevlonceQ1S1s*100) / (5*survey1Counts)
        BenevlonceQ1S2s= (BenevlonceQ1S2s*100) / (5*survey1Counts)
        BenevlonceQ1S3s= (BenevlonceQ1S3s*100) / (5*survey3Counts)
        BenevlonceQ1S4s= (BenevlonceQ1S4s*100) / (5*survey4Counts)
        BenevlonceQ1S5s= (BenevlonceQ1S5s*100) / (5*survey5Counts)

        BenevlonceQ1S1s=float("{0:.1f}".format(BenevlonceQ1S1s))
        BenevlonceQ1S2s=float("{0:.1f}".format(BenevlonceQ1S2s))
        BenevlonceQ1S3s=float("{0:.1f}".format(BenevlonceQ1S3s))
        BenevlonceQ1S4s=float("{0:.1f}".format(BenevlonceQ1S4s))
        BenevlonceQ1S5s=float("{0:.1f}".format(BenevlonceQ1S5s))
#benevolence Q2 for both questioniares
        BenevlonceQ2S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q5", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        BenevlonceQ2S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q5", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        BenevlonceQ2S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q5", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        BenevlonceQ2S4= Submission.objects.aggregate(
            overaltrust=
                Sum("q5", filter=(Q(link_id=LID4[0])), output_field=FloatField()))
        BenevlonceQ2S5= Submission.objects.aggregate(
            overaltrust=
                Sum("q5", filter=(Q(link_id=LID5[0])), output_field=FloatField()))

        BenevlonceQ2S1s=[]
        BenevlonceQ2S2s=[]
        BenevlonceQ2S3s=[]
        BenevlonceQ2S4s=[]
        BenevlonceQ2S5s=[]
        for key, entry in BenevlonceQ2S1.items():
            if entry is None:
                   BenevlonceQ2S1s.append(0)
            else:
                BenevlonceQ2S1s.append(entry)

        for key, entry in BenevlonceQ2S2.items():
            if entry is None:
                BenevlonceQ2S2s.append(0)
            else:
                BenevlonceQ2S2s.append(entry)

        for key, entry in BenevlonceQ2S3.items():
            if entry is None:
                BenevlonceQ2S3s.append(0)
            else:
                BenevlonceQ2S3s.append(entry)

        for key, entry in BenevlonceQ2S4.items():
            if entry is None:
                BenevlonceQ2S4s.append(0)
            else:
                BenevlonceQ2S4s.append(entry)

        for key, entry in BenevlonceQ2S5.items():
            if entry is None:
                BenevlonceQ2S5s.append(0)
            else:
                BenevlonceQ2S5s.append(entry)


        BenevlonceQ2S1s= BenevlonceQ2S1s[0]
        BenevlonceQ2S2s= BenevlonceQ2S2s[0]
        BenevlonceQ2S3s= BenevlonceQ2S3s[0]
        BenevlonceQ2S4s= BenevlonceQ2S4s[0]
        BenevlonceQ2S5s= BenevlonceQ2S5s[0]


        BenevlonceQ2S1s= (BenevlonceQ2S1s*100) / (5*survey1Counts)
        BenevlonceQ2S2s= (BenevlonceQ2S2s*100) / (5*survey1Counts)
        BenevlonceQ2S3s= (BenevlonceQ2S3s*100) / (5*survey3Counts)
        BenevlonceQ2S4s= (BenevlonceQ2S4s*100) / (5*survey4Counts)
        BenevlonceQ2S5s= (BenevlonceQ2S5s*100) / (5*survey5Counts)

        BenevlonceQ2S1s=float("{0:.1f}".format(BenevlonceQ2S1s))
        BenevlonceQ2S2s=float("{0:.1f}".format(BenevlonceQ2S2s))
        BenevlonceQ2S3s=float("{0:.1f}".format(BenevlonceQ2S3s))
        BenevlonceQ2S4s=float("{0:.1f}".format(BenevlonceQ2S4s))
        BenevlonceQ2S5s=float("{0:.1f}".format(BenevlonceQ2S5s))

#benevolence Q3 for both questioniares
        BenevlonceQ3S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q6", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        BenevlonceQ3S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q6", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        BenevlonceQ3S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q6", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        BenevlonceQ3S4= Submission.objects.aggregate(
            overaltrust=
                Sum("q6", filter=(Q(link_id=LID4[0])), output_field=FloatField()))
        BenevlonceQ3S5= Submission.objects.aggregate(
            overaltrust=
                Sum("q6", filter=(Q(link_id=LID5[0])), output_field=FloatField()))

        BenevlonceQ3S1s=[]
        BenevlonceQ3S2s=[]
        BenevlonceQ3S3s=[]
        BenevlonceQ3S4s=[]
        BenevlonceQ3S5s=[]
        for key, entry in BenevlonceQ3S1.items():
            if entry is None:
                   BenevlonceQ3S1s.append(0)
            else:
                BenevlonceQ3S1s.append(entry)

        for key, entry in BenevlonceQ3S2.items():
            if entry is None:
                BenevlonceQ3S2s.append(0)
            else:
                BenevlonceQ3S2s.append(entry)

        for key, entry in BenevlonceQ3S3.items():
            if entry is None:
                BenevlonceQ3S3s.append(0)
            else:
                BenevlonceQ3S3s.append(entry)

        for key, entry in BenevlonceQ3S4.items():
            if entry is None:
                BenevlonceQ3S4s.append(0)
            else:
                BenevlonceQ3S4s.append(entry)

        for key, entry in BenevlonceQ3S5.items():
            if entry is None:
                BenevlonceQ3S5s.append(0)
            else:
                BenevlonceQ3S5s.append(entry)


        BenevlonceQ3S1s= BenevlonceQ3S1s[0]
        BenevlonceQ3S2s= BenevlonceQ3S2s[0]
        BenevlonceQ3S3s= BenevlonceQ3S3s[0]
        BenevlonceQ3S4s= BenevlonceQ3S4s[0]
        BenevlonceQ3S5s= BenevlonceQ3S5s[0]


        BenevlonceQ3S1s= (BenevlonceQ3S1s*100) / (5*survey1Counts)
        BenevlonceQ3S2s= (BenevlonceQ3S2s*100) / (5*survey2Counts)
        BenevlonceQ3S3s= (BenevlonceQ3S3s*100) / (5*survey3Counts)
        BenevlonceQ3S4s= (BenevlonceQ3S4s*100) / (5*survey4Counts)
        BenevlonceQ3S5s= (BenevlonceQ3S5s*100) / (5*survey5Counts)


        BenevlonceQ3S1s=float("{0:.1f}".format(BenevlonceQ3S1s))
        BenevlonceQ3S2s=float("{0:.1f}".format(BenevlonceQ3S2s))
        BenevlonceQ3S3s=float("{0:.1f}".format(BenevlonceQ3S3s))
        BenevlonceQ3S4s=float("{0:.1f}".format(BenevlonceQ3S4s))
        BenevlonceQ3S5s=float("{0:.1f}".format(BenevlonceQ3S5s))

#Riesk Q1 for both questioniares
        CompetenceQ1S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q7", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        CompetenceQ1S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q7", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        CompetenceQ1S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q7", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        CompetenceQ1S4= Submission.objects.aggregate(
            overaltrust=
                Sum("q7", filter=(Q(link_id=LID4[0])), output_field=FloatField()))
        CompetenceQ1S5= Submission.objects.aggregate(
            overaltrust=
                Sum("q7", filter=(Q(link_id=LID5[0])), output_field=FloatField()))
        CompetenceQ1S1s=[]
        CompetenceQ1S2s=[]
        CompetenceQ1S3s=[]
        CompetenceQ1S4s=[]
        CompetenceQ1S5s=[]
        for key, entry in CompetenceQ1S1.items():
            if entry is None:
                   CompetenceQ1S1s.append(0)
            else:
                CompetenceQ1S1s.append(entry)

        for key, entry in CompetenceQ1S2.items():
            if entry is None:
                CompetenceQ1S2s.append(0)
            else:
                CompetenceQ1S2s.append(entry)

        for key, entry in CompetenceQ1S3.items():
            if entry is None:
                CompetenceQ1S3s.append(0)
            else:
                CompetenceQ1S3s.append(entry)

        for key, entry in CompetenceQ1S4.items():
            if entry is None:
                CompetenceQ1S4s.append(0)
            else:
                CompetenceQ1S4s.append(entry)

        for key, entry in CompetenceQ1S5.items():
            if entry is None:
                CompetenceQ1S5s.append(0)
            else:
                CompetenceQ1S5s.append(entry)

        CompetenceQ1S1s= CompetenceQ1S1s[0]
        CompetenceQ1S2s= CompetenceQ1S2s[0]
        CompetenceQ1S3s= CompetenceQ1S3s[0]
        CompetenceQ1S4s= CompetenceQ1S4s[0]
        CompetenceQ1S5s= CompetenceQ1S5s[0]

        CompetenceQ1S1s= (CompetenceQ1S1s*100) / (5*survey1Counts)
        CompetenceQ1S2s= (CompetenceQ1S2s*100) / (5*survey2Counts)
        CompetenceQ1S3s= (CompetenceQ1S3s*100) / (5*survey3Counts)
        CompetenceQ1S4s= (CompetenceQ1S4s*100) / (5*survey4Counts)
        CompetenceQ1S5s= (CompetenceQ1S5s*100) / (5*survey5Counts)

        CompetenceQ1S1s=float("{0:.1f}".format(CompetenceQ1S1s))
        CompetenceQ1S2s=float("{0:.1f}".format(CompetenceQ1S2s))
        CompetenceQ1S3s=float("{0:.1f}".format(CompetenceQ1S3s))
        CompetenceQ1S4s=float("{0:.1f}".format(CompetenceQ1S4s))
        CompetenceQ1S5s=float("{0:.1f}".format(CompetenceQ1S5s))

#Riesk Q2 for both questioniares
        CompetenceQ2S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q8", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        CompetenceQ2S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q8", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        CompetenceQ2S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q8", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        CompetenceQ2S4= Submission.objects.aggregate(
            overaltrust=
                Sum("q8", filter=(Q(link_id=LID4[0])), output_field=FloatField()))
        CompetenceQ2S5= Submission.objects.aggregate(
            overaltrust=
                Sum("q8", filter=(Q(link_id=LID5[0])), output_field=FloatField()))

        CompetenceQ2S1s=[]
        CompetenceQ2S2s=[]
        CompetenceQ2S3s=[]
        CompetenceQ2S4s=[]
        CompetenceQ2S5s=[]

        for key, entry in CompetenceQ2S1.items():
            if entry is None:
                   CompetenceQ2S1s.append(0)
            else:
                CompetenceQ2S1s.append(entry)

        for key, entry in CompetenceQ2S2.items():
            if entry is None:
                CompetenceQ2S2s.append(0)
            else:
                CompetenceQ2S2s.append(entry)

        for key, entry in CompetenceQ2S3.items():
            if entry is None:
                CompetenceQ2S3s.append(0)
            else:
                CompetenceQ2S3s.append(entry)
        for key, entry in CompetenceQ2S4.items():
            if entry is None:
                CompetenceQ2S4s.append(0)
            else:
                CompetenceQ2S4s.append(entry)
        for key, entry in CompetenceQ2S5.items():
            if entry is None:
                CompetenceQ2S5s.append(0)
            else:
                CompetenceQ2S5s.append(entry)

        CompetenceQ2S1s= CompetenceQ2S1s[0]
        CompetenceQ2S2s= CompetenceQ2S2s[0]
        CompetenceQ2S3s= CompetenceQ2S3s[0]
        CompetenceQ2S4s= CompetenceQ2S4s[0]
        CompetenceQ2S5s= CompetenceQ2S5s[0]

        CompetenceQ2S1s= (CompetenceQ2S1s*100) / (5*survey1Counts)
        CompetenceQ2S2s= (CompetenceQ2S2s*100) / (5*survey2Counts)
        CompetenceQ2S3s= (CompetenceQ2S3s*100) / (5*survey3Counts)
        CompetenceQ2S4s= (CompetenceQ2S4s*100) / (5*survey4Counts)
        CompetenceQ2S5s= (CompetenceQ2S5s*100) / (5*survey5Counts)

        CompetenceQ2S1s=float("{0:.1f}".format(CompetenceQ2S1s))
        CompetenceQ2S2s=float("{0:.1f}".format(CompetenceQ2S2s))
        CompetenceQ2S3s=float("{0:.1f}".format(CompetenceQ2S3s))
        CompetenceQ2S4s=float("{0:.1f}".format(CompetenceQ2S4s))
        CompetenceQ2S5s=float("{0:.1f}".format(CompetenceQ2S5s))
#Riesk Q3 for both questioniares
        CompetenceQ3S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q9", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        CompetenceQ3S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q9", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        CompetenceQ3S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q9", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        CompetenceQ3S4= Submission.objects.aggregate(
            overaltrust=
                Sum("q9", filter=(Q(link_id=LID4[0])), output_field=FloatField()))
        CompetenceQ3S5= Submission.objects.aggregate(
            overaltrust=
                Sum("q9", filter=(Q(link_id=LID5[0])), output_field=FloatField()))

        CompetenceQ3S1s=[]
        CompetenceQ3S2s=[]
        CompetenceQ3S3s=[]
        CompetenceQ3S4s=[]
        CompetenceQ3S5s=[]
        for key, entry in CompetenceQ3S1.items():
            if entry is None:
                   CompetenceQ3S1s.append(0)
            else:
                CompetenceQ3S1s.append(entry)

        for key, entry in CompetenceQ3S2.items():
            if entry is None:
                CompetenceQ3S2s.append(0)
            else:
                CompetenceQ3S2s.append(entry)

        for key, entry in CompetenceQ3S3.items():
            if entry is None:
                CompetenceQ3S3s.append(0)
            else:
                CompetenceQ3S3s.append(entry)

        for key, entry in CompetenceQ3S4.items():
            if entry is None:
                CompetenceQ3S4s.append(0)
            else:
                CompetenceQ3S4s.append(entry)

        for key, entry in CompetenceQ3S5.items():
            if entry is None:
                CompetenceQ3S5s.append(0)
            else:
                CompetenceQ3S5s.append(entry)

        CompetenceQ3S1s= CompetenceQ3S1s[0]
        CompetenceQ3S2s= CompetenceQ3S2s[0]
        CompetenceQ3S3s= CompetenceQ3S3s[0]
        CompetenceQ3S4s= CompetenceQ3S4s[0]
        CompetenceQ3S5s= CompetenceQ3S5s[0]

        CompetenceQ3S1s= (CompetenceQ3S1s*100) / (5*survey1Counts)
        CompetenceQ3S2s= (CompetenceQ3S2s*100) / (5*survey2Counts)
        CompetenceQ3S3s= (CompetenceQ3S3s*100) / (5*survey3Counts)
        CompetenceQ3S4s= (CompetenceQ3S4s*100) / (5*survey4Counts)
        CompetenceQ3S5s= (CompetenceQ3S5s*100) / (5*survey5Counts)

        CompetenceQ3S1s=float("{0:.1f}".format(CompetenceQ3S1s))
        CompetenceQ3S2s=float("{0:.1f}".format(CompetenceQ3S2s))
        CompetenceQ3S3s=float("{0:.1f}".format(CompetenceQ3S3s))
        CompetenceQ3S4s=float("{0:.1f}".format(CompetenceQ3S4s))
        CompetenceQ3S5s=float("{0:.1f}".format(CompetenceQ3S5s))
#Recirptocity Q1 for both questioniares
        ReciprocityQ1S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q7", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        ReciprocityQ1S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q7", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        ReciprocityQ1S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q7", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        ReciprocityQ1S4= Submission.objects.aggregate(
            overaltrust=
                Sum("q7", filter=(Q(link_id=LID4[0])), output_field=FloatField()))
        ReciprocityQ1S5= Submission.objects.aggregate(
            overaltrust=
                Sum("q7", filter=(Q(link_id=LID5[0])), output_field=FloatField()))

        ReciprocityQ1S1s=[]
        ReciprocityQ1S2s=[]
        ReciprocityQ1S3s=[]
        ReciprocityQ1S4s=[]
        ReciprocityQ1S5s=[]

        for key, entry in ReciprocityQ1S1.items():
            if entry is None:
                   ReciprocityQ1S1s.append(0)
            else:
                ReciprocityQ1S1s.append(entry)

        for key, entry in ReciprocityQ1S2.items():
            if entry is None:
                ReciprocityQ1S2s.append(0)
            else:
                ReciprocityQ1S2s.append(entry)

        for key, entry in ReciprocityQ1S3.items():
            if entry is None:
                ReciprocityQ1S3s.append(0)
            else:
                ReciprocityQ1S3s.append(entry)
        for key, entry in ReciprocityQ1S4.items():
            if entry is None:
                ReciprocityQ1S4s.append(0)
            else:
                ReciprocityQ1S4s.append(entry)
        for key, entry in ReciprocityQ1S5.items():
            if entry is None:
                ReciprocityQ1S5s.append(0)
            else:
                ReciprocityQ1S5s.append(entry)

        ReciprocityQ1S1s= ReciprocityQ1S1s[0]
        ReciprocityQ1S2s= ReciprocityQ1S2s[0]
        ReciprocityQ1S3s= ReciprocityQ1S3s[0]
        ReciprocityQ1S4s= ReciprocityQ1S4s[0]
        ReciprocityQ1S5s= ReciprocityQ1S5s[0]

        ReciprocityQ1S1s= (ReciprocityQ1S1s*100) / (5*survey1Counts)
        ReciprocityQ1S2s= (ReciprocityQ1S2s*100) / (5*survey2Counts)
        ReciprocityQ1S3s= (ReciprocityQ1S3s*100) / (5*survey3Counts)
        ReciprocityQ1S4s= (ReciprocityQ1S4s*100) / (5*survey4Counts)
        ReciprocityQ1S5s= (ReciprocityQ1S5s*100) / (5*survey5Counts)

        ReciprocityQ1S1s=float("{0:.1f}".format(ReciprocityQ1S1s))
        ReciprocityQ1S2s=float("{0:.1f}".format(ReciprocityQ1S2s))
        ReciprocityQ1S3s=float("{0:.1f}".format(ReciprocityQ1S3s))
        ReciprocityQ1S4s=float("{0:.1f}".format(ReciprocityQ1S4s))
        ReciprocityQ1S5s=float("{0:.1f}".format(ReciprocityQ1S5s))


#Recirprocity Q2 for both questioniares
        ReciprocityQ2S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q8", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        ReciprocityQ2S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q8", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        ReciprocityQ2S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q8", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        ReciprocityQ2S4= Submission.objects.aggregate(
            overaltrust=
                Sum("q8", filter=(Q(link_id=LID4[0])), output_field=FloatField()))
        ReciprocityQ2S5= Submission.objects.aggregate(
            overaltrust=
                Sum("q8", filter=(Q(link_id=LID5[0])), output_field=FloatField()))

        ReciprocityQ2S1s=[]
        ReciprocityQ2S2s=[]
        ReciprocityQ2S3s=[]
        ReciprocityQ2S4s=[]
        ReciprocityQ2S5s=[]

        for key, entry in ReciprocityQ2S1.items():
            if entry is None:
                   ReciprocityQ2S1s.append(0)
            else:
                ReciprocityQ2S1s.append(entry)

        for key, entry in ReciprocityQ2S2.items():
            if entry is None:
                ReciprocityQ2S2s.append(0)
            else:
                ReciprocityQ2S2s.append(entry)

        for key, entry in ReciprocityQ2S3.items():
            if entry is None:
                ReciprocityQ2S3s.append(0)
            else:
                ReciprocityQ2S3s.append(entry)

        for key, entry in ReciprocityQ2S4.items():
            if entry is None:
                ReciprocityQ2S4s.append(0)
            else:
                ReciprocityQ2S4s.append(entry)
        for key, entry in ReciprocityQ2S5.items():
            if entry is None:
                ReciprocityQ2S5s.append(0)
            else:
                ReciprocityQ2S5s.append(entry)

        ReciprocityQ2S1s= ReciprocityQ2S1s[0]
        ReciprocityQ2S2s= ReciprocityQ2S2s[0]
        ReciprocityQ2S3s= ReciprocityQ2S3s[0]
        ReciprocityQ2S4s= ReciprocityQ2S4s[0]
        ReciprocityQ2S5s= ReciprocityQ2S5s[0]

        ReciprocityQ2S1s= (ReciprocityQ2S1s*100) / (5*survey1Counts)
        ReciprocityQ2S2s= (ReciprocityQ2S2s*100) / (5*survey2Counts)
        ReciprocityQ2S3s= (ReciprocityQ2S3s*100) / (5*survey3Counts)
        ReciprocityQ2S4s= (ReciprocityQ2S4s*100) / (5*survey4Counts)
        ReciprocityQ2S5s= (ReciprocityQ2S5s*100) / (5*survey5Counts)

        ReciprocityQ2S1s=float("{0:.1f}".format(ReciprocityQ2S1s))
        ReciprocityQ2S2s=float("{0:.1f}".format(ReciprocityQ2S2s))
        ReciprocityQ2S3s=float("{0:.1f}".format(ReciprocityQ2S3s))
        ReciprocityQ2S4s=float("{0:.1f}".format(ReciprocityQ2S4s))
        ReciprocityQ2S5s=float("{0:.1f}".format(ReciprocityQ2S5s))
#Riesk Q1 for both questioniares
        GtrustQ1S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q12", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        GtrustQ1S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q12", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        GtrustQ1S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q12", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        GtrustQ1S4= Submission.objects.aggregate(
            overaltrust=
                Sum("q12", filter=(Q(link_id=LID4[0])), output_field=FloatField()))
        GtrustQ1S5= Submission.objects.aggregate(
            overaltrust=
                Sum("q12", filter=(Q(link_id=LID5[0])), output_field=FloatField()))
        GtrustQ1S1s=[]
        GtrustQ1S2s=[]
        GtrustQ1S3s=[]
        GtrustQ1S4s=[]
        GtrustQ1S5s=[]
        for key, entry in GtrustQ1S1.items():
            if entry is None:
                   GtrustQ1S1s.append(0)
            else:
                GtrustQ1S1s.append(entry)

        for key, entry in GtrustQ1S2.items():
            if entry is None:
                GtrustQ1S2s.append(0)
            else:
                GtrustQ1S2s.append(entry)

        for key, entry in GtrustQ1S3.items():
            if entry is None:
                GtrustQ1S3s.append(0)
            else:
                GtrustQ1S3s.append(entry)

        for key, entry in GtrustQ1S4.items():
            if entry is None:
                GtrustQ1S4s.append(0)
            else:
                GtrustQ1S4s.append(entry)

        for key, entry in GtrustQ1S5.items():
            if entry is None:
                GtrustQ1S5s.append(0)
            else:
                GtrustQ1S5s.append(entry)

        GtrustQ1S1s= GtrustQ1S1s[0]
        GtrustQ1S2s= GtrustQ1S2s[0]
        GtrustQ1S3s= GtrustQ1S3s[0]
        GtrustQ1S4s= GtrustQ1S4s[0]
        GtrustQ1S5s= GtrustQ1S5s[0]
        GtrustQ1S1s= (GtrustQ1S1s*100) / (5*survey1Counts)
        GtrustQ1S2s= (GtrustQ1S2s*100) / (5*survey2Counts)
        GtrustQ1S3s= (GtrustQ1S3s*100) / (5*survey3Counts)
        GtrustQ1S4s= (GtrustQ1S4s*100) / (5*survey4Counts)
        GtrustQ1S5s= (GtrustQ1S5s*100) / (5*survey5Counts)

        GtrustQ1S1s=float("{0:.1f}".format(GtrustQ1S1s))
        GtrustQ1S2s=float("{0:.1f}".format(GtrustQ1S2s))
        GtrustQ1S3s=float("{0:.1f}".format(GtrustQ1S3s))
        GtrustQ1S4s=float("{0:.1f}".format(GtrustQ1S4s))
        GtrustQ1S5s=float("{0:.1f}".format(GtrustQ1S5s))

#Riesk Q2 for both questioniares
        GtrustQ2S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q13", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        GtrustQ2S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q13", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        GtrustQ2S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q13", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        GtrustQ2S4= Submission.objects.aggregate(
            overaltrust=
                Sum("q13", filter=(Q(link_id=LID4[0])), output_field=FloatField()))
        GtrustQ2S5= Submission.objects.aggregate(
            overaltrust=
                Sum("q13", filter=(Q(link_id=LID5[0])), output_field=FloatField()))
        GtrustQ2S1s=[]
        GtrustQ2S2s=[]
        GtrustQ2S3s=[]
        GtrustQ2S4s=[]
        GtrustQ2S5s=[]
        for key, entry in GtrustQ2S1.items():
            if entry is None:
                   GtrustQ2S1s.append(0)
            else:
                GtrustQ2S1s.append(entry)

        for key, entry in GtrustQ2S2.items():
            if entry is None:
                GtrustQ2S2s.append(0)
            else:
                GtrustQ2S2s.append(entry)

        for key, entry in GtrustQ2S3.items():
            if entry is None:
                GtrustQ2S3s.append(0)
            else:
                GtrustQ2S3s.append(entry)

        for key, entry in GtrustQ2S4.items():
            if entry is None:
                GtrustQ2S4s.append(0)
            else:
                GtrustQ2S4s.append(entry)

        for key, entry in GtrustQ2S5.items():
            if entry is None:
                GtrustQ2S5s.append(0)
            else:
                GtrustQ2S5s.append(entry)

        GtrustQ2S1s= GtrustQ2S1s[0]
        GtrustQ2S2s= GtrustQ2S2s[0]
        GtrustQ2S3s= GtrustQ2S3s[0]
        GtrustQ2S4s= GtrustQ2S4s[0]
        GtrustQ2S5s= GtrustQ2S5s[0]

        GtrustQ2S1s= (GtrustQ2S1s*100) / (5*survey1Counts)
        GtrustQ2S2s= (GtrustQ2S2s*100) / (5*survey2Counts)
        GtrustQ2S3s= (GtrustQ2S3s*100) / (5*survey3Counts)
        GtrustQ2S4s= (GtrustQ2S4s*100) / (5*survey4Counts)
        GtrustQ2S5s= (GtrustQ2S5s*100) / (5*survey5Counts)

        GtrustQ2S1s=float("{0:.1f}".format(GtrustQ2S1s))
        GtrustQ2S2s=float("{0:.1f}".format(GtrustQ2S2s))
        GtrustQ2S3s=float("{0:.1f}".format(GtrustQ2S3s))
        GtrustQ2S4s=float("{0:.1f}".format(GtrustQ2S4s))
        GtrustQ2S5s=float("{0:.1f}".format(GtrustQ2S5s))
#Riesk Q3 for both questioniares
        GtrustQ3S1= Submission.objects.aggregate(
            overaltrust=
                Sum("q14", filter=(Q(link_id=LID1[0])), output_field=FloatField()))
        GtrustQ3S2= Submission.objects.aggregate(
            overaltrust=
                Sum("q14", filter=(Q(link_id=LID2[0])), output_field=FloatField()))
        GtrustQ3S3= Submission.objects.aggregate(
            overaltrust=
                Sum("q14", filter=(Q(link_id=LID3[0])), output_field=FloatField()))
        GtrustQ3S4= Submission.objects.aggregate(
            overaltrust=
                Sum("q14", filter=(Q(link_id=LID4[0])), output_field=FloatField()))
        GtrustQ3S5= Submission.objects.aggregate(
            overaltrust=
                Sum("q14", filter=(Q(link_id=LID5[0])), output_field=FloatField()))

        GtrustQ3S1s=[]
        GtrustQ3S2s=[]
        GtrustQ3S3s=[]
        GtrustQ3S4s=[]
        GtrustQ3S5s=[]

        for key, entry in GtrustQ3S1.items():
            if entry is None:
                   GtrustQ3S1s.append(0)
            else:
                GtrustQ3S1s.append(entry)

        for key, entry in GtrustQ3S2.items():
            if entry is None:
                GtrustQ3S2s.append(0)
            else:
                GtrustQ3S2s.append(entry)

        for key, entry in GtrustQ3S3.items():
            if entry is None:
                GtrustQ3S3s.append(0)
            else:
                GtrustQ3S3s.append(entry)
        for key, entry in GtrustQ3S4.items():
            if entry is None:
                GtrustQ3S4s.append(0)
            else:
                GtrustQ3S4s.append(entry)

        for key, entry in GtrustQ3S5.items():
            if entry is None:
                GtrustQ3S5s.append(0)
            else:
                GtrustQ3S5s.append(entry)

        GtrustQ3S1s= GtrustQ3S1s[0]
        GtrustQ3S2s= GtrustQ3S2s[0]
        GtrustQ3S3s= GtrustQ3S3s[0]
        GtrustQ3S4s= GtrustQ3S4s[0]
        GtrustQ3S5s= GtrustQ3S5s[0]


        GtrustQ3S1s= (GtrustQ3S1s*100) / (5*survey1Counts)
        GtrustQ3S2s= (GtrustQ3S2s*100) / (5*survey2Counts)
        GtrustQ3S3s= (GtrustQ3S3s*100) / (5*survey3Counts)
        GtrustQ3S4s= (GtrustQ3S4s*100) / (5*survey4Counts)
        GtrustQ3S5s= (GtrustQ3S5s*100) / (5*survey5Counts)

        GtrustQ3S1s=float("{0:.1f}".format(GtrustQ3S1s))
        GtrustQ3S2s=float("{0:.1f}".format(GtrustQ3S2s))
        GtrustQ3S3s=float("{0:.1f}".format(GtrustQ3S3s))
        GtrustQ3S4s=float("{0:.1f}".format(GtrustQ3S4s))
        GtrustQ3S5s=float("{0:.1f}".format(GtrustQ3S5s))

        return render(request, 'pie_chart5.html', {
            'project_id':project_id,
            'productname':productname,
            'survey1Counts':survey1Counts,
            'survey2Counts':survey2Counts,
            'survey3Counts':survey3Counts,
            'survey4Counts':survey4Counts,
            'survey5Counts':survey5Counts,
            'S1CountGender':S1CountGender,
            'S2CountGender':S2CountGender,
            'S3CountGender':S3CountGender,
            'S4CountGender':S4CountGender,
            'S5CountGender':S5CountGender,
            'S1CountAge':S1CountAge,
            'S2CountAge':S2CountAge,
            'S3CountAge':S3CountAge,
            'S4CountAge':S4CountAge,
            'S5CountAge':S5CountAge,
            'CrobanchAlphaS1':CrobanchAlphaS1,
            'CrobanchAlphaS2':CrobanchAlphaS2,
            'CrobanchAlphaS3':CrobanchAlphaS3,
            'CrobanchAlphaS4':CrobanchAlphaS4,
            'CrobanchAlphaS5':CrobanchAlphaS5,
            'OvrallTrustS1s':OvrallTrustS1s,
            'OvrallTrustS2s':OvrallTrustS2s,
            'OvrallTrustS3s':OvrallTrustS3s,
            'OvrallTrustS4s':OvrallTrustS4s,
            'OvrallTrustS5s':OvrallTrustS5s,
            'OvrallRiskS1s':OvrallRiskS1s,
            'OvrallRiskS2s':OvrallRiskS2s,
            'OvrallRiskS3s':OvrallRiskS3s,
            'OvrallRiskS4s':OvrallRiskS4s,
            'OvrallRiskS5s':OvrallRiskS5s,
            'OvrallBenevolenceS1s':OvrallBenevolenceS1s,
            'OvrallBenevolenceS2s':OvrallBenevolenceS2s,
            'OvrallBenevolenceS3s':OvrallBenevolenceS3s,
            'OvrallBenevolenceS4s':OvrallBenevolenceS4s,
            'OvrallBenevolenceS5s':OvrallBenevolenceS5s,
            'OvrallCompetenceS1s':OvrallCompetenceS1s,
            'OvrallCompetenceS2s':OvrallCompetenceS2s,
            'OvrallCompetenceS3s':OvrallCompetenceS3s,
            'OvrallCompetenceS4s':OvrallCompetenceS4s,
            'OvrallCompetenceS5s':OvrallCompetenceS5s,
            'OvrallReciprocityS1s':OvrallReciprocityS1s,
            'OvrallReciprocityS2s':OvrallReciprocityS2s,
            'OvrallReciprocityS3s':OvrallReciprocityS3s,
            'OvrallReciprocityS4s':OvrallReciprocityS4s,
            'OvrallReciprocityS5s':OvrallReciprocityS5s,
            'OvrallGeneralTrustS1s':OvrallGeneralTrustS1s,
            'OvrallGeneralTrustS2s':OvrallGeneralTrustS2s,
            'OvrallGeneralTrustS3s':OvrallGeneralTrustS3s,
            'OvrallGeneralTrustS4s':OvrallGeneralTrustS4s,
            'OvrallGeneralTrustS5s':OvrallGeneralTrustS5s,
            'RiskQ1S1s':RiskQ1S1s,
            'RiskQ1S2s':RiskQ1S2s,
            'RiskQ1S3s':RiskQ1S3s,
            'RiskQ1S4s':RiskQ1S4s,
            'RiskQ1S5s':RiskQ1S5s,
            'RiskQ2S1s':RiskQ2S1s,
            'RiskQ2S2s':RiskQ2S2s,
            'RiskQ2S3s':RiskQ2S3s,
            'RiskQ2S4s':RiskQ2S4s,
            'RiskQ2S5s':RiskQ2S5s,
            'RiskQ3S1s':RiskQ3S1s,
            'RiskQ3S2s':RiskQ3S2s,
            'RiskQ3S3s':RiskQ3S3s,
            'RiskQ3S4s':RiskQ3S4s,
            'RiskQ3S5s':RiskQ3S5s,
            'BenevlonceQ1S1s':BenevlonceQ1S1s,
            'BenevlonceQ1S2s':BenevlonceQ1S2s,
            'BenevlonceQ1S3s':BenevlonceQ1S3s,
            'BenevlonceQ1S4s':BenevlonceQ1S4s,
            'BenevlonceQ1S5s':BenevlonceQ1S5s,
            'BenevlonceQ2S1s':BenevlonceQ2S1s,
            'BenevlonceQ2S2s':BenevlonceQ2S2s,
            'BenevlonceQ2S3s':BenevlonceQ2S3s,
            'BenevlonceQ2S4s':BenevlonceQ2S4s,
            'BenevlonceQ2S5s':BenevlonceQ2S5s,
            'BenevlonceQ3S1s':BenevlonceQ3S1s,
            'BenevlonceQ3S2s':BenevlonceQ3S2s,
            'BenevlonceQ3S3s':BenevlonceQ3S3s,
            'BenevlonceQ3S4s':BenevlonceQ3S4s,
            'BenevlonceQ3S5s':BenevlonceQ3S5s,
            'CompetenceQ1S1s':CompetenceQ1S1s,
            'CompetenceQ1S2s':CompetenceQ1S2s,
            'CompetenceQ1S3s':CompetenceQ1S3s,
            'CompetenceQ1S4s':CompetenceQ1S4s,
            'CompetenceQ1S5s':CompetenceQ1S5s,
            'CompetenceQ2S1s':CompetenceQ2S1s,
            'CompetenceQ2S2s':CompetenceQ2S2s,
            'CompetenceQ2S3s':CompetenceQ2S3s,
            'CompetenceQ2S4s':CompetenceQ2S4s,
            'CompetenceQ2S5s':CompetenceQ2S5s,
            'CompetenceQ3S1s':CompetenceQ3S1s,
            'CompetenceQ3S2s':CompetenceQ3S2s,
            'CompetenceQ3S3s':CompetenceQ3S3s,
            'CompetenceQ3S4s':CompetenceQ3S4s,
            'CompetenceQ3S5s':CompetenceQ3S5s,
            'ReciprocityQ1S1s':ReciprocityQ1S1s,
            'ReciprocityQ1S2s':ReciprocityQ1S2s,
            'ReciprocityQ1S3s':ReciprocityQ1S3s,
            'ReciprocityQ1S4s':ReciprocityQ1S4s,
            'ReciprocityQ1S5s':ReciprocityQ1S5s,
            'ReciprocityQ2S1s':ReciprocityQ2S1s,
            'ReciprocityQ2S2s':ReciprocityQ2S2s,
            'ReciprocityQ2S3s':ReciprocityQ2S3s,
            'ReciprocityQ2S4s':ReciprocityQ2S4s,
            'ReciprocityQ2S5s':ReciprocityQ2S5s,
            'GtrustQ1S1s':GtrustQ1S1s,
            'GtrustQ1S2s':GtrustQ1S2s,
            'GtrustQ1S3s':GtrustQ1S3s,
            'GtrustQ1S4s':GtrustQ1S4s,
            'GtrustQ1S5s':GtrustQ1S5s,
            'GtrustQ2S1s':GtrustQ2S1s,
            'GtrustQ2S2s':GtrustQ2S2s,
            'GtrustQ2S3s':GtrustQ2S3s,
            'GtrustQ2S4s':GtrustQ2S4s,
            'GtrustQ2S5s':GtrustQ2S5s,
            'GtrustQ3S1s':GtrustQ3S1s,
            'GtrustQ3S2s':GtrustQ3S2s,
            'GtrustQ3S3s':GtrustQ3S3s,
            'GtrustQ3S4s':GtrustQ3S4s,
            'GtrustQ3S5s':GtrustQ3S5s

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



        return render(request, "dashboard.html",{'projects':projects,'projects_count':projects.count(),'site':current_site,'domain':domain})


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
            Survey = link_obj.survey.title
            print('survey--->',Survey)
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

        print(survey_url.survey.start_date)
        print(datetime.now().date())
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
            print(title)
            name = survey_url.survey.survey_name
            paragraph = survey_url.survey.paragraph

            lang = survey_url.survey.language

            title = title.format(**variables)
            print('after',title)

            paragraph = paragraph.format(**variables)

            #return surveyForm(request,link)
            return render(request,"survey_front.html",{'project_title':title,'paragraph':paragraph,'link':survey_url.url,'lang':lang,'name':name,'survey':survey_url.survey})
        else:
            return render(request, "survey_msg.html",{'msg_title':'Not active','msg_body':'The survey is not active.'})




# Create your views here.
def overview(request):
    projects = Project.objects.all().filter(user=request.user,archived=False).order_by('-created_at')
    current_site = get_current_site(request)
    domain = current_site.domain
    #domain = 'trustedux.herokuapp.com'
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
    survey = Survey.objects.all().filter(project=project,deleted=False)


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
            new = data['new']
            print(new)
            if not new:
                project_id = int(data['project_id'])
                project = Project.objects.get(id=project_id)
                surveys = Survey.objects.all().filter(project=project)

                org_count = surveys.count()
                new_count = int(data['project_type'])

                print(org_count,' ',new_count)

                if org_count > new_count:
                    context.update({'err_msg':True})
                else:
                    context.update({'err_msg':False})




            context.update({'all_data': self.get_all_cleaned_data()})
            context.update({'NewOrEdit':data['new']})
            context.update({'type':self.type_of_study})



        if self.steps.current == "survey":

            data = self.get_all_cleaned_data()
            self.type_of_study = int(data['project_type'])

            #survey_dict = self.fill_dummy()
            ##self.initial_dict['survey'] = survey_dict

            context.update({'NewOrEdit':data['new']})
            context.update({'type':self.type_of_study})
            #form = self.fill_dummy(form)
            #initial = self.fill_dummy(form)

            #print('-----------------------------')
            #print(initial)
            #self.initial_dict['survey'] = initial
            #context = super(CompleteForm, self).get_context_data(form=form, **kwargs)

            #print('Type:',data['project_type'])



        if self.steps.current == 'participants':
            data = self.get_all_cleaned_data()
            context.update({'NewOrEdit':data['new']})
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

                survey = Survey.objects.create(project=project,product_name=all_data[s_product_name_key],survey_name = "",start_date=all_data[s_start_key],end_date=all_data[s_end_key],title=all_data[s_title_key],paragraph=all_data[s_paragraph_key],owner=all_data[s_owner_key],owner_email=all_data[s_owner_email_key],language=all_data[s_lang_key])

                survey_url = Link.objects.create(survey=survey,sequence=k)

            age = all_data['age']
            gender=all_data['gender']
            education=all_data['education']
            nationality=all_data['nationality']



            anony_settings = AnonyDataSetting.objects.create(project=project,age=age,gender=gender,education=education,nationality=nationality)



            messages.success(self.request, 'Study is created successfully !')
        else:
            print('-------------------->',all_data['project_id'])
            project_id = int(all_data['project_id'])

            project = Project.objects.get(id=project_id)
            surveys = Survey.objects.all().filter(project=project)

            org_count = surveys.count()
            surveys_count = int(all_data['project_type'])

            project.project_name = all_data['project_name']
            project.project_type = all_data['project_type']

            project.product_type=all_data['project_type']
            project.product_industry=all_data['product_industry']
            project.project_status=all_data['project_status']

            anony_settings = AnonyDataSetting.objects.get(project=project)


            anony_settings.age = all_data['age']
            anony_settings.gender=all_data['gender']
            anony_settings.education=all_data['education']
            anony_settings.nationality=all_data['nationality']

            anony_settings.save()

            for k in range(surveys_count):
                print('loop:',k)
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



                if k > org_count:
                    survey = Survey.objects.create(project=project,deleted=False,product_name=all_data[s_product_name_key],survey_name = "",start_date=all_data[s_start_key],end_date=all_data[s_end_key],title=all_data[s_title_key],paragraph=all_data[s_paragraph_key],owner=all_data[s_owner_key],owner_email=all_data[s_owner_email_key],language=all_data[s_lang_key])

                    survey_url = Link.objects.create(survey=survey,sequence=k)
                else:
                    cur_survey = surveys[k-1]
                    cur_survey.product_name=all_data[s_product_name_key]
                    cur_survey.start_date=all_data[s_start_key]
                    cur_survey.end_date=all_data[s_end_key]
                    cur_survey.title=all_data[s_title_key]
                    cur_survey.paragraph=all_data[s_paragraph_key]
                    cur_survey.owner=all_data[s_owner_key]
                    cur_survey.owner_email=all_data[s_owner_email_key]
                    cur_survey.language=all_data[s_lang_key]

                    print('updating survey',k)

                    cur_survey.save()

            for i,v in enumerate(surveys):
                print(i,' ',v)

            # if number of surveys link reduced then mark deleted flag as True
            if org_count > surveys_count:
                print('condition checked-->',surveys_count,org_count)
                survey_del = surveys_count
                print(surveys)
                while (survey_del < org_count):
                    print('deleting..',survey_del,org_count)
                    sur_obj = surveys[survey_del]



                    sur_obj.delete()




                    survey_del += 1






            project.save()

            messages.success(self.request,'Study is successfully updated')

        return redirect('project_home')

class CompleteSubmissionForm(SessionWizardView):
    def get_template_names(self):
        return [SUBMISSION_TEMPLATE[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        link_obj = Link.objects.get(url=self.kwargs['link'])
        survey_name = link_obj.survey.title
        product = link_obj.survey.product_name
        project = link_obj.survey.project

        language = link_obj.survey.language
        context.update({'lang': language})

        anony_setting = AnonyDataSetting.objects.get(project=project)
        print('Anonymous object:',anony_setting, anony_setting.age)
        if self.steps.current == 'survey':
            print('Product:',product,' ',)
            context.update({'survey': product,'product':product,'anony_setting':anony_setting})
            context.update({'all_data': self.get_all_cleaned_data(),'anony_setting':anony_setting})
            context.update({'countries':sort_countries})
            print(sort_countries)
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
        #q10 = int(all_data['q10'])
        #q11 = int(all_data['q7'])
        #q12 = int(all_data['q8'])
        #q13 = int(all_data['q9'])
        #q14 = int(all_data['q10'])

        link_obj = Link.objects.get(url=self.kwargs['link'])
        submission = Submission.objects.create(link=link_obj,q1=q1,q2=q2,q3=q3,q4=q4,q5=q5,q6=q6,q7=q7,q8=q8,q9=q9,q10=0,q11=0,q12=0,q13=0,q14=0)

        print(all_data)


        age = all_data['age'] if all_data['age'] != '' else -1
        education = all_data['education'] if all_data['education'] != '' else -1

        gender = all_data['gender']
        nationality = all_data['nationality']

        lang = link_obj.survey.language




        anony_data = AnonyData.objects.create(link=link_obj,age=age,gender=gender,education=education,nationality=nationality)

        return render(self.request,'survey_msg.html',{'msg_title':_('Successful Submission'),'msg_body':_('Your submissions are successfully saved. Thank you for your time.'),'lang':lang})
