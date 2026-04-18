from django.core.management.base import BaseCommand,CommandError
from dataentry.models import Student
import csv
import datetime
from django.apps import apps

class Command(BaseCommand):
    help='Export data in a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('model_name',type=str,help='Model name which exports data')

    def handle(self,*args,**kwargs):

        model_name=kwargs['model_name'].capitalize()

        # fetch the data
        model=None
        for app_config in apps.get_app_configs():
            try:
                model=apps.get_model(app_config.label,model_name)
                
                break
            except LookupError:
                continue
        
        if not model:
            raise CommandError(f'The model:{model_name} does not exists!')
        
        obj=model.objects.all()

        

        # get the current timestamp
        timestamp=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')




        # create a csv file name

        file_path=f'exported_{model_name}_data_{timestamp}.csv'

        

        # write the data in the file
        with open(file_path,'w',newline='')as file:
            writer=csv.writer(file)

            writer.writerow([i.name for i in model._meta.fields])

            for i in obj:    
                writer.writerow([ getattr(i,field.name) for field in model._meta.fields])

        self.stdout.write(self.style.SUCCESS(f'Data from {model_name} exported successfully!'))
        
