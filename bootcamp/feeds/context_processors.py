from .forms import MultipleInputFileForm

def file_upload_form(request):
  return {'file_form': MultipleInputFileForm()}
