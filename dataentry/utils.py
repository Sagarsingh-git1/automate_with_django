from django.apps import apps
from django.core.management.base import CommandError
import csv,time,hashlib
from django.db import DataError
from django.core.mail import EmailMessage
from django.conf import settings
import datetime
import os
from django.shortcuts import get_object_or_404
from emails.models import Email,Sent,Subscriber,EmailTracking
from bs4 import BeautifulSoup


def get_all_custom_models():
    custom_models=[]

    default_model={'LogEntry','Permission','Group','User','ContentType','Session','Upload','List','Subscriber','Email','EmailTracking','ImageCompress','Sent'}

    for model in apps.get_models():
        if model.__name__ not in default_model:
            custom_models.append({'name':model.__name__ , 'label':f'{model._meta.app_label}.{model.__name__}'})
    return custom_models


def check_csv_error(file_path,model_name):
    model=None
    try:
            
        model=apps.get_model(model_name)
    except (LookupError,ValueError):
            raise CommandError(f'The model:{model_name} does not exists!.Use"app_label.ModelName"')
            
    
    model_fields=[field.name for field in model._meta.fields if field.name!='id']

    try:
        with open(file_path,'r') as file:
            reader=csv.DictReader(file)

            csv_header=reader.fieldnames

            if csv_header != model_fields:
                raise DataError(f'CSV file doesnot match with {model.__name__} tables!')
    except Exception as e:
        raise e
    
    return model


def send_email_notification(mail_subject,message,to_email,attachment=None,email_id=None):

    try:    
        from_email=settings.DEFAULT_FROM_EMAIL
        
        for recipeient_mail in to_email:
            if email_id:
                email=Email.objects.get(pk=email_id)
                subscriber=Subscriber.objects.get(email_list=email.email_list,email_address=recipeient_mail)
                timestamp=str(time.time())
                data_to_hash=f'{recipeient_mail}{timestamp}'
                unique_id=hashlib.sha256(data_to_hash.encode()).hexdigest()
                EmailTracking.objects.create(
                    email=email,
                    subscriber=subscriber,
                    unique_id=unique_id

                )
                # Generate the click tracking url and open tracking url
                base_url=settings.BASE_URL
                click_tracking_url=f'{base_url}/emails/track/click/{unique_id}'
                open_tracking_url=f'{base_url}/emails/track/open/{unique_id}'

                # Search for the links in the email body and injecting the url  
                new_message=message
                soup=BeautifulSoup(new_message,'html.parser')
                for link in soup.find_all('a',href=True):
                    url=link['href']
                    tracking_url=f'{click_tracking_url}?url={url}'
                    link ['href']=tracking_url
                new_message=str(soup)
                final_open_tracking_url=f'<img src="{open_tracking_url}" width="1" height="1">'
                new_message+=final_open_tracking_url
            else:
                new_message=message

            mail=EmailMessage(mail_subject,new_message,from_email,to=[recipeient_mail])

            if attachment is not None:
                mail.attach_file(attachment)
            mail.content_subtype="html"
            mail.send()
            # Calculating the total_sent
        if email_id:    
            sent=Sent()
            sent.email=email
            sent.total_sent=email.email_list.count_emails()
            sent.save()

    except Exception as e:
        raise e
    


def generate_csv_file(model_name):
        
        model=None
        try:    
            model=apps.get_model(model_name) 
        except (LookupError,ValueError):
            raise CommandError(f'The model:{model_name} does not exists!.Use"app_label.ModelName"')
        
        obj=model.objects.all()
       
        
        # get the current timestamp
        timestamp=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

        # create a csv file name
        file_name=f'exported_{model.__name__}_data_{timestamp}.csv'

        # file directory
        path=os.path.join(settings.MEDIA_ROOT,'exported_data')

        os.makedirs(path,exist_ok=True)
        
        # create the full file_path
        file_path=os.path.join(path,file_name)
        with open(file_path,'w',newline='')as file:

            writer=csv.writer(file)

            writer.writerow([field.name for field in model._meta.fields])

            for i in obj:    
                writer.writerow([ getattr(i,field.name) for field in model._meta.fields])

        return file_path

    




def run_task(task, *args, **kwargs):
    if settings.USE_CELERY:
        return task.delay(*args, **kwargs)
    else:
        return task(*args, **kwargs)
    



    

        
