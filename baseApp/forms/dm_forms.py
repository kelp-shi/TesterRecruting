from django import forms
from baseApp.db.application.dm_models import DirectMassage

class MessageForm(forms.ModelForm):
    """
    ダイレクトメッセージフォーム
    """
    class Meta:
        model = DirectMassage
        fields = ['Text']
        widgets = {
            'Text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type your message here...'}),
        }