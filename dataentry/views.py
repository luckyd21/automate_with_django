from django.shortcuts import render,redirect
from .utils import get_all_custom_models,check_csv_errors
from uploads.models import Upload
from django.conf import settings
from django.core.management import call_command
from django.contrib import messages
from .tasks import import_data_task, export_data_task



def import_data(request):
    
    if request.method == 'POST':
        file_path = request.FILES.get('file_path')
        model_name = request.POST.get('model_name')
        upload = Upload.objects.create(file=file_path, model_name= model_name)
       

        #construct the full path
        relative_path = upload.file.url
        base_url = str(settings.BASE_DIR)

        file_path = base_url + relative_path
        #check for the csv
        try:
            check_csv_errors(file_path,model_name)
        except Exception as e:
            messages.error(request, str(e))
            return redirect('import_data')

        # handle import data task
        import_data_task.delay(file_path,model_name)

        #show the message to the user
        messages.success(request,'Your data is being imported, you will be notifed once it is done.')
        return redirect('import_data')
    else:
        custom_models = get_all_custom_models()
        
        context = {
            'custom_models': custom_models
        }
        
    return render(request, 'dataentry/importdata.html',context)
def export_data(request):
    if request.method == 'POST':
        model_name = request.POST.get('model_name')
        #call the export data task
        export_data_task.delay(model_name)
         #show the message to the user
        messages.success(request,'Your data is being exported, you will be notifed once it is done.')
        return redirect('export_data')
    else:
        custom_models = get_all_custom_models()
        context ={
            'custom_models': custom_models
        }
    return render(request,'dataentry/exportdata.html',context)

# Create your views here.

