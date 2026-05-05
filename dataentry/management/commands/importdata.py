from django.core.management.base import BaseCommand
import csv
from dataentry.models import Student
from dataentry.utils import check_csv_error

class Command(BaseCommand):
    help='It will import CSV data into the database'

    def add_arguments(self, parser):
        parser.add_argument('file_path',type=str,help='Path to the CSV file')
        parser.add_argument('model_name',type=str,help='The model where data is to be imported.')


    def handle(self, *args, **kwargs):
        file_path=kwargs['file_path']
        model_name=kwargs['model_name']


        # Check the csv errors from the helper function
        model=check_csv_error(file_path,model_name)

        unique_fields = [field.name for field in model._meta.fields if field.name !='id' and field.unique]
        if unique_fields:    
            unique_field=unique_fields[0]
        else:
            unique_field=None
            self.stdout.write(self.style.WARNING(f'There is no unique fields in {model.__name__} table. All data importing!'))
    
        with open(file_path,'r') as file:
            reader=csv.DictReader(file)

            for row in reader:
                if unique_field:

                    existing=model.objects.filter(**{unique_field:row[unique_field]}).exists()

                    if existing:
                        self.stdout.write(self.style.WARNING(f'{model.__name__} with {unique_field} {row[unique_field]} already exists!'))   
                    else:
                        model.objects.create(**row)
                else:
                    model.objects.create(**row)

            self.stdout.write(self.style.SUCCESS('Data imported from CSV successfully.'))
