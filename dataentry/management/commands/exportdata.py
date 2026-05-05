from django.core.management.base import BaseCommand,CommandError
from dataentry.models import Student
import csv
import datetime
from django.apps import apps
from django.conf import settings
from dataentry.utils import generate_csv_file
class Command(BaseCommand):
    help='Export data in a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('model_name',type=str,help='Model name which exports data')

    def handle(self,*args,**kwargs):

        model_name=kwargs['model_name']

        file_path=generate_csv_file(model_name)

        
        self.stdout.write(self.style.SUCCESS(f'Data from {model_name.split('.')[1]} exported successfully!'))
        

        


