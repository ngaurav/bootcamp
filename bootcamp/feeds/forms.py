from django_file_form.forms import UploadedFileField, MultipleUploadedFileField, FileFormMixin
from django import forms

class MultipleInputFileForm(FileFormMixin, forms.Form):
    input_file = MultipleUploadedFileField()
