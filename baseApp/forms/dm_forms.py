from django import forms
from baseApp.db.application.dm_models import Massage

class MessageForm(forms.ModelForm):
    """
    ダイレクトメッセージフォーム
    """
    class Meta:
        model = Massage
        fields = ['Text']
        widgets = {
            'Text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type your message here...'}),
        }