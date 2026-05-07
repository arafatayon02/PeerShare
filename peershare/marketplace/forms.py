from django import forms
from .models import Item, Review, Booking


class ItemForm(forms.ModelForm):
    class Meta:
        model  = Item
        fields = ['title', 'description', 'price', 'category', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'e.g. Scientific Calculator'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Describe your item in detail...'
            }),
            'price': forms.NumberInput(attrs={
                'placeholder': 'Enter price in ৳',
                'min': 1,
            }),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model  = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Share your experience...'
            }),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model  = Booking
        fields = ['days']
        widgets = {
            'days': forms.NumberInput(attrs={
                'placeholder': 'How many days?',
                'min': 1,
                'max': 365,
            }),
        }


class ChatForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 2,
            'placeholder': 'Type your message...'
        })
    )