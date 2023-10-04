from django import forms

from mass_upload.models import StgProduct

class UploadFileForm(forms.ModelForm):
     class Meta :
        model = StgProduct
        fields = ['file_name']

    #     image = forms.FileField(widget=forms.FileInput(attrs={
    #     'accept':'.jpg,.png,.jpeg',
    #     'class' : 'btn btn-info', })
    #    )
        
        file_name = forms.FileField(widget=forms.FileInput(attrs={
        'class' : 'btn btn-info'}),
       )