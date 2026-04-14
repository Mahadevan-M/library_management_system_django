from django import forms
from .models import Book, Wishlist

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'price', 'image']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Title'}),
            'author': forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Author'}),
            'price': forms.NumberInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Price'}),
            'image': forms.FileInput(attrs={'class': 'form-control mb-2'}),
        }