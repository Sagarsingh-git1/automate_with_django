from django.core.management.base import BaseCommand,CommandError
import csv
from dataentry.models import Student
from django.apps import apps

class Command(BaseCommand):
    help='It will import CSV data into the database'

    def add_arguments(self, parser):
        parser.add_argument('file_path',type=str,help='Path to the CSV file')
        parser.add_argument('model_name',type=str,help='The model where data is to be imported.')


    def handle(self, *args, **kwargs):
        file_path=kwargs['file_path']
        model_name=kwargs['model_name']
        model=None
        for app_config in apps.get_app_configs():
            try:
                model=apps.get_model(app_config.label,model_name)
                break
            except LookupError:
                continue
        if not model:
            raise CommandError(f'The model name: {model_name}, Not found across any of your apps!')
        
    
        with open(file_path,'r') as file:
            reader=csv.DictReader(file)

            for row in reader:
                existing=model.objects.filter(roll_no=int(row['roll_no'])).exists()

                if existing:
                    self.stdout.write(self.style.WARNING(f'The data with roll_no {row['roll_no']} already exists!'))   
                else:
                    model.objects.create(**row)

            self.stdout.write(self.style.SUCCESS('Data imported from CSV successfully.'))
