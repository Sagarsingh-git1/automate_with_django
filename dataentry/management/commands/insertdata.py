from django.core.management.base import BaseCommand
from dataentry.models import Student

class Command(BaseCommand):
    help='It will insert datas into the database'


    def handle(self, *args, **kwargs):

        dataset=[
                {'roll_no':1001,'name':'Sagar','age':25},
                {'roll_no':1002,'name':'Vijay','age':29},
                {'roll_no':1003,'name':'John','age':23},
                {'roll_no':1004,'name':'Carl','age':25},
        ]
        for data in dataset:
            existing_record=Student.objects.filter(roll_no=data['roll_no']).exists()
            if existing_record:
                self.stdout.write(self.style.WARNING(f'Data with roll_no {data['roll_no']} already exists in the database.'))
            else:
                Student.objects.create(roll_no=data['roll_no'],name=data['name'],age=data['age'])
        self.stdout.write(self.style.SUCCESS('Data inserted successfully!'))

