from django import forms
from .models import Review


class ReviewForms(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_description']
