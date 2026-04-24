from awd_main.celery import app
from django.core.management import call_command
from .utils import send_email_notification,generate_csv_file
from django.conf import settings



@app.task
def celery_import_data(file_path,model_name):
    try:
        call_command('importdata',file_path,model_name)
        mail_subject= 'Import Data'
        message='Your data has been successfully imported !'
        to_email=settings.DEFAULT_TO_EMAIL
        send_email_notification(mail_subject,message,to_email)
        return 'Imported sucessfully'
        
    except Exception as e:
        raise e
    

@app.task  
def celery_export_data(model_name):
    try:    
        call_command('exportdata',model_name)
        mail_subject='Export Data'
        message='Your data has been exported successfully! Please find the attachment.'
        to_email=settings.DEFAULT_TO_EMAIL
        attachment=generate_csv_file(model_name)

        send_email_notification(mail_subject,message,to_email,attachment)
        return "Exported Successfully"
    
    except Exception as e:
        raise e
    

 
    
    







    
