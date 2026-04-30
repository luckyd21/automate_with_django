from django.core.management import BaseCommand,CommandError
from dataentry.models import Student
from django.apps import apps
import csv
import datetime
 
#proposed command = python manage.py exportdata model_name
class Command(BaseCommand):
    help = 'Export data from Student model to a csv file'
    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help='model_name')

    def handle (self, *args, **kwargs):
        #fetch the data from database
        model_name = kwargs['model_name'].capitalize()
        model = None
        print(kwargs)
        for app_config in apps.get_app_configs():
            try:
                model= apps.get_model(app_config.label, model_name)
                break
            except LookupError:
                pass
        if not model:
            self.stdout.write(f'Model {model_name} could not found')
            return
        data = model.objects.all()

                
        
        #generate timestamp of current date and time
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")


        #define the csv file name/path
        file_path = f'exported_students_data{timestamp}.csv'

        # open the csv file and write
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)


            # write the CSV header
            #we want to print the field name of the model that we are trying to expert
            writer.writerow([field.name for field in model._meta.fields])
            #writ the data row
            for dt in data:
                writer.writerow([getattr(dt,field.name) for field in model._meta.fields])
        self.stdout.write(self.style.SUCCESS('data exported successfully'))

