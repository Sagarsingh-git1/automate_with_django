from django.shortcuts import render,redirect
from .forms import EmailForm
from dataentry.utils import send_email_notification
from django.contrib import messages
from .models import Subscriber
from .tasks import celery_send_emails

# Create your views here.


def send_emails(request):
    if request.method=='POST':
        form=EmailForm(request.POST,request.FILES)
        if form.is_valid():
            email_form=form.save()
            mail_subject=email_form.subject
            message=email_form.body
            email_list=email_form.email_list
            if email_form.attachment:    
                attachment=email_form.attachment.path
            else:
                attachment=None

            # get the subscriber for the email_list
            subscriber=Subscriber.objects.filter(email_list=email_list)

            # Extract the email addresses from the model
            to_email=[]
            for email in subscriber:
                to_email.append(email.email_address)
            
            # handover email sending task to celery
            
            celery_send_emails.delay(mail_subject,message,to_email,attachment)
        

            messages.success(request,'Email sent successfully.')
            return redirect('send_emails') 
            

    else:
        form=EmailForm()

        context={
            'form':form,
        }

        return render(request,'emails/send-emails.html',context)
