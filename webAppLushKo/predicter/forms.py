from .models import Documents
from django.forms import ModelForm, TextInput, FileInput


class DocumentsForm(ModelForm):
    class Meta:
        model = Documents
        fields = ['id_uniq', 'title', 'document']

        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название документа'
            }),

            "document": FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Загрузите документ',
            })
        }
