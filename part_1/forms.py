from django import forms
# from uploads.core.models import Document
from .models import Document, AppKeys
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('document', )


class AppKeysForm(forms.ModelForm):
	class Meta:
		model = AppKeys
		fields = ('CustomerKey', 'CustomerSecretKey', 'AccessTokenKey', 'AccessTokenSecret', )
