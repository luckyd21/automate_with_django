from django.core.management import BaseCommand,CommandError
from dataentry.models import Student
import csv
from django.apps import apps

#proposed command 

class Command(BaseCommand):
    help = "Import data from CSV file"

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')
        parser.add_argument('model_name', type=str, help='Name of the model')
    
    def handle(self, *args, **kwargs):
        # logic goes here
        file_path = kwargs['file_path']
        model_name = kwargs['model_name']

        #Search for model across all install app
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label, model_name)
                break #stop searching once model is found
            except LookupError:
                continue #model not found this app, countinue searching next app
        if not model:
            raise CommandError(f'model "{model_name} not found in any')
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            print(reader)
            for row in reader:
                Student.objects.create(**row)

        self.stdout.write(self.style.SUCCESS('Data imported from CSV Successfully'))

