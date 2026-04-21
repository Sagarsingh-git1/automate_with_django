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

        
    
        with open(file_path,'r') as file:
            reader=csv.DictReader(file)

            for row in reader:
                existing=model.objects.filter(roll_no=int(row['roll_no'])).exists()

                if existing:
                    self.stdout.write(self.style.WARNING(f'Student with roll_no {row['roll_no']} already exists!'))   
                else:
                    model.objects.create(**row)

            self.stdout.write(self.style.SUCCESS('Data imported from CSV successfully.'))
