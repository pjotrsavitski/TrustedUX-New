from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from formtools.wizard.views import SessionWizardView
from django.forms.fields import Field
from datetime import date
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from djrichtextfield.widgets import RichTextWidget
from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget
from .models import AnonyData, sort_countries, gen_choices, edu_choices, age_choices
from django.utils.translation import  ugettext_lazy as _


setattr(Field, 'is_checkbox', lambda self: isinstance(self.widget, forms.CheckboxInput ))


from django.contrib import admin
from django import forms
from .models import Project
from django.forms import ModelForm
#from django.db.models import Count
#from django.utils.encoding import python_2_unicode_compatible
class contactforms(forms.Form):
    Project_Name=forms.ChoiceField(choices=[])
    class Meta:
        model = Project
        exclude= ('user','questionnaire_type','test_project','project_type','project_status','archived','closed','project_name')
    def __init__(self, user, *args, **kwargs):
        super(contactforms,self).__init__(*args,**kwargs)
        #self.fields['Project_Name'].choices = [(yr, yr) for yr in Project.objects.values_list('project_name', flat=True)]
        self.fields['Project_Name'].choices = [(yr, yr) for yr in Project.objects.values_list('project_name',flat=True).filter(user=user)]


project_choices = [(1,'Individual'),(2,'Comparision A and B'),(3, 'Comparision A, B and C'),(4, 'Comparision A, B, C and D'),(5, 'Comparision A, B, C, D and E')]
industry_choices = [('Advanced Technologies and Innovation','Advanced Technologies and Innovation'),('Education/Training','Education/Training'),('Finance','Finance'),('Government','Government'),('Healthcare and sport','Healthcare and sport'),('Information technologies','Information technologies'),('Manufacturing / Materials','Manufacturing / Materials'),('Privacy and security','Privacy and security'),('Travel/Tourism','Travel/Tourism')]
type_choices = [('Hardware','Hardware'),('Software','Software'),('Mobile application','Mobile application'),('Web application','Web application'),('Social network','Social network'),('Website','Website'),('Cloud technology','Cloud technology'),('Other','Other')]

class CreateForm1(forms.Form):

    project_name = forms.CharField(label='Study name',widget=forms.TextInput(attrs={'class':'form-control mb-4'}),max_length=100)
    project_type = forms.CharField(label='Evaluation type',widget=forms.Select(choices=project_choices,attrs={'class':'form-control mb-4'}))
    new = forms.BooleanField(widget=forms.HiddenInput(),required=False,initial=True)
    project_id = forms.IntegerField(widget=forms.HiddenInput(),required=False)
    product_type = forms.CharField(label='Product type',widget=forms.Select(choices=type_choices,attrs={'class':'form-control mb-4'}),max_length=100)
    product_industry = forms.CharField(label='Industry',widget=forms.Select(choices=industry_choices,attrs={'class':'form-control mb-4'}))



class CreateForm2(forms.Form):
    lang_choices = [('En','English'),('Pt','Portugese'),('Et','Estonian')]
    CHOICES = [(1,'Yes'),(0,'No')]




    # Additional questions for collecting anonymous data about participants
    #age = forms.BooleanField(widget=DjangoToggleSwitchWidget(klass="django-toggle-switch-dark-success ml-2  mb-4"),required=False)
    #gender= forms.BooleanField(widget=DjangoToggleSwitchWidget(klass="django-toggle-switch-dark-success ml-2  mb-4"),required=False)
    #nationality = forms.BooleanField(widget=DjangoToggleSwitchWidget(klass="django-toggle-switch-dark-success ml-2  mb-4"),required=False)
    #education = forms.BooleanField(widget=DjangoToggleSwitchWidget(klass="django-toggle-switch-dark-success ml-2  mb-4"),required=False)

    age = forms.BooleanField(required=False)
    gender = forms.BooleanField(required=False)
    nationality = forms.BooleanField(required=False)
    education = forms.BooleanField(required=False)





    ## survey-1 Project is successfully updated
    #name_of_survey1 = forms.CharField(label="Survey name",widget=forms.TextInput(attrs={'class':'form-control mb-4'}),max_length=100)
    questionnaire_language1=forms.CharField(label="Language", widget=forms.Select(choices=lang_choices,attrs={'class':'form-control  mb-4'}))
    start_date1 = forms.DateField(label="Start date",widget=forms.DateInput(attrs={'class':'form-control  mb-4','type':'date'}))
    end_date1 = forms.DateField(label="End date",widget=forms.DateInput(attrs={'class':'form-control  mb-4','type':'date'}))
    product_name1 = forms.CharField(label='Product or service name',widget=forms.TextInput(attrs={'class':'form-control mb-4'}),max_length=100)


    survey_owner1=forms.CharField(label="Name", widget=forms.TextInput(attrs={'class':'form-control  mb-4'}))
    survey_owner_email1=forms.CharField(label="Email", widget=forms.EmailInput(attrs={'class':'form-control  mb-4'}))

    # Survey group front page
    title1 = forms.CharField(label='Title',initial="Assessment of {PRODUCT_NAME}",widget=forms.TextInput(attrs={'class':'form-control  mb-4'}),max_length=100)
    #subtitle1 = forms.CharField(initial="Welcome to the assessment of {PRODUCT_NAME}",widget=forms.TextInput(attrs={'class':'form-control  mb-4'}),max_length=100)
    paragraph1 = forms.CharField(label='Introduction',initial='Welcome to the assessment of {PRODUCT_NAME}! <br/><br/> Thank you for taking time to participate in this stdy. My name is {OWNER_NAME}. Through this survey, I would like to undertsand how likely you are to trust {PRODUCT_NAME}. <br/><br/> I would be very grateful if you complete this survey. This survey is anonymous. The record of your survey responses does not contain any identifying information about you. \n It will require approximately 10 minutes of your time. In case you have any questions, you can contact me via email {OWNER_EMAIL}',required=False,widget=RichTextWidget(),help_text=mark_safe('You can use following variables to use in title, subtitle and paragraph: <br/>{PROJECT_NAME} - Name of project <br/> {PRODUCT_NAME} - Name of product<br/> {SURVEY_NAME} - Name of survey <br/> {TODAY} - for today date.'))


    # survey-2
    #name_of_survey2 = forms.CharField(label="Survey name",widget=forms.TextInput(attrs={'class':'form-control mb-4'}),max_length=100)
    questionnaire_language2=forms.CharField(label="Language", widget=forms.Select(choices=lang_choices,attrs={'class':'form-control  mb-4'}))
    start_date2 = forms.DateField(label="Start date",widget=forms.DateInput(attrs={'class':'form-control  mb-4','type':'date'}))
    end_date2 = forms.DateField(label="End date",widget=forms.DateInput(attrs={'class':'form-control  mb-4','type':'date'}))
    product_name2 = forms.CharField(label='Product or service name',widget=forms.TextInput(attrs={'class':'form-control mb-4'}),max_length=100)


    survey_owner2=forms.CharField(label="Name", widget=forms.TextInput(attrs={'class':'form-control  mb-4'}))
    survey_owner_email2=forms.CharField(label="Email", widget=forms.EmailInput(attrs={'class':'form-control  mb-4'}))

    # Survey group front page
    title2 = forms.CharField(label='Title',initial="Assessment of {PRODUCT_NAME}",widget=forms.TextInput(attrs={'class':'form-control  mb-4'}),max_length=100)
    #subtitle2 = forms.CharField(initial="Welcome to the assessment of {PRODUCT_NAME}",widget=forms.TextInput(attrs={'class':'form-control  mb-4'}),max_length=100)
    paragraph2 = forms.CharField(label='Introduction',initial='Welcome to the assessment of {PRODUCT_NAME}! <br/><br/> Thank you for taking time to participate in this stdy. My name is {OWNER_NAME}. Through this survey, I would like to undertsand how likely you are to trust {PRODUCT_NAME}. <br/><br/> I would be very grateful if you complete this survey. This survey is anonymous. The record of your survey responses does not contain any identifying information about you. \n It will require approximately 10 minutes of your time. In case you have any questions, you can contact me via email {OWNER_EMAIL}',required=False,widget=RichTextWidget(),help_text=mark_safe('You can use following variables to use in title, subtitle and paragraph: <br/>{PROJECT_NAME} - Name of project <br/> {PRODUCT_NAME} - Name of product<br/> {SURVEY_NAME} - Name of survey <br/> {TODAY} - for today date.'))


    ## survey-3
    #name_of_survey3 = forms.CharField(label="Survey name",widget=forms.TextInput(attrs={'class':'form-control mb-4'}),max_length=100)
    questionnaire_language3=forms.CharField(label="Language", widget=forms.Select(choices=lang_choices,attrs={'class':'form-control  mb-4'}))
    start_date3 = forms.DateField(label="Start date",widget=forms.DateInput(attrs={'class':'form-control  mb-4','type':'date'}))
    end_date3 = forms.DateField(label="End date",widget=forms.DateInput(attrs={'class':'form-control  mb-4','type':'date'}))
    product_name3 = forms.CharField(label='Product or service name',widget=forms.TextInput(attrs={'class':'form-control mb-4'}),max_length=100)

    survey_owner3=forms.CharField(label="Name", widget=forms.TextInput(attrs={'class':'form-control  mb-4'}))
    survey_owner_email3=forms.CharField(label="Email", widget=forms.EmailInput(attrs={'class':'form-control  mb-4'}))

    # Survey group front page
    title3 = forms.CharField(label='Title',initial="Assessment of {PRODUCT_NAME}",widget=forms.TextInput(attrs={'class':'form-control  mb-4'}),max_length=100)
    #subtitle3 = forms.CharField(initial="Welcome to the assessment of {PRODUCT_NAME}",widget=forms.TextInput(attrs={'class':'form-control  mb-4'}),max_length=100)
    paragraph3 = forms.CharField(label='Introduction',initial='Welcome to the assessment of {PRODUCT_NAME}! <br/><br/> Thank you for taking time to participate in this stdy. My name is {OWNER_NAME}. Through this survey, I would like to undertsand how likely you are to trust {PRODUCT_NAME}. <br/><br/> I would be very grateful if you complete this survey. This survey is anonymous. The record of your survey responses does not contain any identifying information about you. \n It will require approximately 10 minutes of your time. In case you have any questions, you can contact me via email {OWNER_EMAIL}',required=False,widget=RichTextWidget(),help_text=mark_safe('You can use following variables to use in title, subtitle and paragraph: <br/>{PROJECT_NAME} - Name of project <br/> {PRODUCT_NAME} - Name of product<br/> {SURVEY_NAME} - Name of survey <br/> {TODAY} - for today date.'))


    ## survey-4
    #name_of_survey4 = forms.CharField(label="Survey name",widget=forms.TextInput(attrs={'class':'form-control mb-4'}),max_length=100)
    questionnaire_language4=forms.CharField(label="Language", widget=forms.Select(choices=lang_choices,attrs={'class':'form-control  mb-4'}))
    start_date4 = forms.DateField(label="Start date",widget=forms.DateInput(attrs={'class':'form-control  mb-4','type':'date'}))
    end_date4 = forms.DateField(label="End date",widget=forms.DateInput(attrs={'class':'form-control  mb-4','type':'date'}))
    product_name4 = forms.CharField(label='Product or service name',widget=forms.TextInput(attrs={'class':'form-control mb-4'}),max_length=100)

    survey_owner4=forms.CharField(label="Name", widget=forms.TextInput(attrs={'class':'form-control  mb-4'}))
    survey_owner_email4=forms.CharField(label="Email", widget=forms.EmailInput(attrs={'class':'form-control  mb-4'}))

    # Survey group front page
    title4 = forms.CharField(label='Title',initial="Assessment of {PRODUCT_NAME}",widget=forms.TextInput(attrs={'class':'form-control  mb-4'}),max_length=100)
    #subtitle4 = forms.CharField(initial="Welcome to the assessment of {PRODUCT_NAME}",widget=forms.TextInput(attrs={'class':'form-control  mb-4'}),max_length=100)
    paragraph4 = forms.CharField(label='Introduction',initial='Welcome to the assessment of {PRODUCT_NAME}! <br/><br/> Thank you for taking time to participate in this stdy. My name is {OWNER_NAME}. Through this survey, I would like to undertsand how likely you are to trust {PRODUCT_NAME}. <br/><br/> I would be very grateful if you complete this survey. This survey is anonymous. The record of your survey responses does not contain any identifying information about you. \n It will require approximately 10 minutes of your time. In case you have any questions, you can contact me via email {OWNER_EMAIL}',required=False,widget=RichTextWidget(),help_text=mark_safe('You can use following variables to use in title, subtitle and paragraph: <br/>{PROJECT_NAME} - Name of project <br/> {PRODUCT_NAME} - Name of product<br/> {SURVEY_NAME} - Name of survey <br/> {TODAY} - for today date.'))


    ## survey-5
    #name_of_survey5 = forms.CharField(label="Survey name",widget=forms.TextInput(attrs={'class':'form-control mb-4'}),max_length=100)
    questionnaire_language5=forms.CharField(label="Language", widget=forms.Select(choices=lang_choices,attrs={'class':'form-control  mb-4'}))
    start_date5 = forms.DateField(label="Start date",widget=forms.DateInput(attrs={'class':'form-control  mb-4','type':'date'}))
    end_date5 = forms.DateField(label="End date",widget=forms.DateInput(attrs={'class':'form-control  mb-4','type':'date'}))
    product_name5 = forms.CharField(label='Product or service name',widget=forms.TextInput(attrs={'class':'form-control mb-4'}),max_length=100)

    survey_owner5=forms.CharField(label="Name", widget=forms.TextInput(attrs={'class':'form-control  mb-4'}))
    survey_owner_email5=forms.CharField(label="Email", widget=forms.EmailInput(attrs={'class':'form-control  mb-4'}))

    # Survey group front page
    title5 = forms.CharField(label="Title",initial="Assessment of {PRODUCT_NAME}",widget=forms.TextInput(attrs={'class':'form-control  mb-4'}),max_length=100)
    #subtitle5 = forms.CharField(initial="Welcome to the assessment of {PRODUCT_NAME}",widget=forms.TextInput(attrs={'class':'form-control  mb-4'}),max_length=100)
    paragraph5 = forms.CharField(label='Introduction',initial='Welcome to the assessment of {PRODUCT_NAME}! <br/><br/> Thank you for taking time to participate in this stdy. My name is {OWNER_NAME}. Through this survey, I would like to undertsand how likely you are to trust {PRODUCT_NAME}. <br/><br/> I would be very grateful if you complete this survey. This survey is anonymous. The record of your survey responses does not contain any identifying information about you. \n It will require approximately 10 minutes of your time. In case you have any questions, you can contact me via email {OWNER_EMAIL}',required=False,widget=RichTextWidget(),help_text=mark_safe('You can use following variables to use in title, subtitle and paragraph: <br/>{PROJECT_NAME} - Name of project <br/> {PRODUCT_NAME} - Name of product<br/> {SURVEY_NAME} - Name of survey <br/> {TODAY} - for today date.'))



    # Additional questions for collecting anonymous data about participants
    #age = forms.BooleanField(widget=DjangoToggleSwitchWidget(klass="django-toggle-switch-dark-success ml-2  mb-4"),required=False)
    #gender= forms.BooleanField(widget=DjangoToggleSwitchWidget(klass="django-toggle-switch-dark-success ml-2  mb-4"),required=False)
    #nationality = forms.BooleanField(widget=DjangoToggleSwitchWidget(klass="django-toggle-switch-dark-success ml-2  mb-4"),required=False)
    #education = forms.BooleanField(widget=DjangoToggleSwitchWidget(klass="django-toggle-switch-dark-success ml-2  mb-4"),required=False)


    #product_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),max_length=100)
    #product_type = forms.CharField(widget=forms.Select(choices=type_choices,attrs={'class':'form-control'}),max_length=100)
    #product_industry = forms.CharField(widget=forms.Select(choices=industry_choices,attrs={'class':'form-control'}))
    """
    def clean_start_date1(self):
        start_date = self.cleaned_data['start_date1']
        if start_date < date.today():
            raise ValidationError('You can not choose start date in past.')
        else:
            return start_date
    def clean_start_date2(self):
        start_date = self.cleaned_data['start_date2']
        if start_date < date.today():
            raise ValidationError('You can not choose start date in past.')
        else:
            return start_date

    def clean_start_date3(self):
        start_date = self.cleaned_data['start_date3']
        if start_date < date.today():
            raise ValidationError('You can not choose start date in past.')
        else:
            return start_date
    def clean_start_date4(self):
        start_date = self.cleaned_data['start_date4']
        if start_date < date.today():
            raise ValidationError('You can not choose start date in past.')
        else:
            return start_date
    def clean_start_date5(self):
        start_date = self.cleaned_data['start_date5']
        if start_date < date.today():
            raise ValidationError('You can not choose start date in past.')
        else:
            return start_date


    def clean(self):
        cleaned_data = super().clean()





        start_date1 = cleaned_data.get('start_date1')
        end_date1 = cleaned_data.get('end_date1')



        start_date2 = cleaned_data.get('start_date2')
        end_date2 = cleaned_data.get('end_date2')

        start_date3 = cleaned_data.get('start_date3')
        end_date3 = cleaned_data.get('end_date3')

        start_date4 = cleaned_data.get('start_date4')
        end_date4 = cleaned_data.get('end_date4')

        start_date5 = cleaned_data.get('start_date5')
        end_date5 = cleaned_data.get('end_date5')


        if start_date1 and end_date1:
            if start_date1 > end_date1:
                raise ValidationError('Project end date must be after the start date.')

        if start_date2 and end_date:
            if start_date2 > end_date2:
                raise ValidationError('Project end date must be after the start date.')

        if start_date3 and end_date3:
            if start_date3 > end_date3:
                raise ValidationError('Project end date must be after the start date.')

        if start_date4 and end_date4:
            if start_date4 > end_date4:
                raise ValidationError('Project end date must be after the start date.')

        if start_date5 and end_date5:
            if start_date5 > end_date5:
                raise ValidationError('Project end date must be after the start date.')

    """



class CreateForm3(forms.Form):
    CHOICES = [('A','Create link to share')]
    type_of_participation=forms.CharField(widget=forms.Select(choices=CHOICES,attrs={'class':'form-control'}))

class CreateForm4(forms.Form):
    CHOICES = [('En','English'),('Pt','Portugese'),('Est','Estonian')]
    questionnaire_language=forms.CharField( widget=forms.Select(choices=CHOICES,attrs={'class':'form-control'}))
    title = forms.CharField(initial="Assessment of {PRODUCT_NAME}",widget=forms.TextInput(attrs={'class':'form-control'}),max_length=100)
    subtitle = forms.CharField(initial="Welcome to the assessment of {PRODUCT_NAME}",widget=forms.TextInput(attrs={'class':'form-control'}),max_length=100)
    paragraph = forms.CharField(required=False,widget=RichTextWidget(),help_text=mark_safe('You can use following variables to use in title, subtitle and paragraph: <br/>{PROJECT_NAME} - Name of project <br/> {PRODUCT_NAME} - Name of product<br/> {SURVEY_NAME} - Name of survey <br/> {TODAY} - for today date.'))


class CreateForm5(forms.Form):
    CHOICES = [(1,'Yes'),(0,'No')]
    age = forms.BooleanField(widget=DjangoToggleSwitchWidget(klass="django-toggle-switch-dark-success"),required=False)
    gender= forms.BooleanField(widget=DjangoToggleSwitchWidget(klass="django-toggle-switch-dark-success"),required=False)
    nationality = forms.BooleanField(widget=DjangoToggleSwitchWidget(klass="django-toggle-switch-dark-success"),required=False)
    education = forms.BooleanField(widget=DjangoToggleSwitchWidget(klass="django-toggle-switch-dark-success"),required=False)

class lastForm(forms.Form):
    CHOICES=[(True,'Final'),(False,'Draft')]
    project_status = forms.ChoiceField(label='Study state', choices=CHOICES, widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}),initial=True)
    #project_status = forms.BooleanField( widget=forms.HiddenInput(),initial=True)




class SurveyQuestion(forms.Form):

    # new code added
    """
    age = forms.CharField(label='Age',required=False,widget=forms.Select(choices=age_choices,attrs={'class':'form-control mb-4'}))
    gender = forms.CharField(label='Gender',required=False,widget=forms.Select(choices=gen_choices,attrs={'class':'form-control mb-4'}))
    education = forms.CharField(label='Education',required=False,widget=forms.Select(choices=edu_choices,attrs={'class':'form-control mb-4'}))
    nationality = forms.CharField(label='Nationality',required=False,widget=forms.Select(choices=sort_countries,attrs={'class':'form-control mb-4'}))
    """

    age = forms.CharField(label='Age',required=False,widget=forms.HiddenInput())
    gender = forms.CharField(label='Gender',required=False,widget=forms.HiddenInput())
    education = forms.CharField(label='Education',required=False,widget=forms.HiddenInput())
    nationality = forms.CharField(label='Nationality',required=False,widget=forms.HiddenInput())

    # end new code

    q1  = forms.CharField(max_length=12,required=False,widget=forms.HiddenInput())
    q2  = forms.CharField(max_length=12,required=False,widget=forms.HiddenInput())
    q3  = forms.CharField(max_length=12,required=False,widget=forms.HiddenInput())
    q4  = forms.CharField(max_length=12,required=False,widget=forms.HiddenInput())
    q5  = forms.CharField(max_length=12,required=False,widget=forms.HiddenInput())
    q6  = forms.CharField(max_length=12,required=False,widget=forms.HiddenInput())
    q7  = forms.CharField(max_length=12,required=False,widget=forms.HiddenInput())
    q8  = forms.CharField(max_length=12,required=False,widget=forms.HiddenInput())
    q9  = forms.CharField(max_length=12,required=False,widget=forms.HiddenInput())
    q10  = forms.CharField(max_length=12,required=False,widget=forms.HiddenInput(),initial=0)
    q11  = forms.CharField(max_length=12,required=False,widget=forms.HiddenInput(),initial=0)
    q12  = forms.CharField(max_length=12,required=False,widget=forms.HiddenInput(),initial=0)
    q13  = forms.CharField(max_length=12,required=False,widget=forms.HiddenInput(),initial=0)
    q14  = forms.CharField(max_length=12,required=False,widget=forms.HiddenInput(),initial=0)


class frontForm(forms.Form):
    demo = forms.BooleanField(widget=forms.HiddenInput(),required=False)


class AnonyForm(forms.ModelForm):
    class Meta:
        model = AnonyData
        fields = ['age','gender','education','nationality']
        widgets= {
            'age': forms.Select(attrs={'class':'form-control'}),
            'gender': forms.Select(attrs={'class':'form-control'}),
            'education': forms.Select(attrs={'class':'form-control'}),
            'nationality': forms.Select(attrs={'class':'form-control'})
        }
