from django import forms
from .models import *
from multiupload.fields import MultiFileField


# create forms  

class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = [
            'car_model', 
            'car_make',  
            'specifications',  
            'tickets_sold',
            'image', 
            'ticket_price', 
            'total_tickets', 
            'start_date', 
            'end_date', 
        ]

        start_date  = forms.DateTimeField(
            input_formats=[
            '%Y-%m-%d %H:%M:%S',  # Format: YYYY-MM-DD HH:MM:SS
            '%Y-%m-%d %H:%M',     # Format: YYYY-MM-DD HH:MM
            '%Y-%m-%d',           # Format: YYYY-MM-DD
            ],
            required=False
        )

        end_date  = forms.DateTimeField(
            input_formats=[
            '%Y-%m-%d %H:%M:%S',  # Format: YYYY-MM-DD HH:MM:SS
            '%Y-%m-%d %H:%M',     # Format: YYYY-MM-DD HH:MM
            '%Y-%m-%d',           # Format: YYYY-MM-DD
            ],
            required=False
        )
        

class CompetitionImageForm(forms.ModelForm):
    images = MultiFileField(required=False)

    class Meta:
        model = CompetitionImage
        fields = ['image']


class HolidayCompetitionForm(forms.ModelForm):

    class Meta:
        model = HolidayCompetition
        fields = [
            'name', 
            'description',
            'image',
            'ticket_price', 
            'total_tickets', 
            'start_date', 
            'tickets_sold',
            'end_date',
        ]

    start_date = forms.DateTimeField(
        input_formats=[
            '%Y-%m-%d %H:%M:%S',  # Format: YYYY-MM-DD HH:MM:SS
            '%Y-%m-%d %H:%M',     # Format: YYYY-MM-DD HH:MM
            '%Y-%m-%d',           # Format: YYYY-MM-DD
        ],
        required=False,
        
    )
    end_date = forms.DateTimeField(
        input_formats=[
            '%Y-%m-%d %H:%M:%S',  # Format: YYYY-MM-DD HH:MM:SS
            '%Y-%m-%d %H:%M',     # Format: YYYY-MM-DD HH:MM
            '%Y-%m-%d',           # Format: YYYY-MM-DD
        ],
        required=False,
      
    )


class HoliCompetitionImageForm(forms.ModelForm):
    images = MultiFileField(required=False)

    class Meta:
        model = HoliCompetitionImage
        fields = ['image']