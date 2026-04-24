from django.apps import apps
from django.core.management.base import CommandError
import csv
from django.db import DataError
from django.core.mail import EmailMessage
from django.conf import settings
import datetime
import os

def get_all_custom_models():
    custom_models=[]

    default_model={'LogEntry','Permission','Group','User','ContentType','Session','Upload'}

    for model in apps.get_models():
        if model.__name__ not in default_model:
            custom_models.append(model.__name__)
    return custom_models


def check_csv_error(file_path,model_name):
    model=None
    for app_config in apps.get_app_configs():
        try:
            model=apps.get_model(app_config.label,model_name)
            break
        except LookupError:
            continue
    if not model:
        raise CommandError(f'The model name: {model_name}, Not found across any of your apps!')
    
    model_fields=[field.name for field in model._meta.fields if field.name!='id']

    try:
        with open(file_path,'r') as file:
            reader=csv.DictReader(file)

            csv_header=reader.fieldnames

            if csv_header != model_fields:
                raise DataError(f'CSV file doesnot match with {model_name} tables!')
    except Exception as e:
        raise e
    
    return model


def send_email_notification(mail_subject,message,to_email,attachment=None):

    try:    
        from_email=settings.DEFAULT_FROM_EMAIL

        mail=EmailMessage(mail_subject,message,from_email,to=to_email)

        if attachment is not None:
            mail.attach_file(attachment)
        mail.content_subtype="html"
        mail.send()

    except Exception as e:
        raise e
    

def generate_csv_file(model_name):
        
        # get the current timestamp
        timestamp=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

        # create a csv file name
        file_name=f'exported_{model_name}_data_{timestamp}.csv'

        # file directory
        path='exported_data'

        # create the full file_path
        file_path=os.path.join(settings.MEDIA_ROOT,path,file_name)

        return file_path
    



    

        
