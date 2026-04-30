from django.shortcuts import render,redirect,get_object_or_404
from .forms import EmailForm
from dataentry.utils import send_email_notification
from django.contrib import messages
from .models import Subscriber,Email,EmailTracking
from .tasks import celery_send_emails
from django.db.models import Sum
from django.http import HttpResponse,HttpResponseRedirect
from django.utils import timezone



# Create your views here.


def send_emails(request):
    if request.method=='POST':
        form=EmailForm(request.POST,request.FILES)
        if form.is_valid():
            email=form.save()
            mail_subject=email.subject
            message=email.body
            email_list=email.email_list
            if email.attachment:    
                attachment=email.attachment.path
            else:
                attachment=None

            # get the subscriber for the email_list
            subscriber=Subscriber.objects.filter(email_list=email_list)

            # Extract the email addresses from the model object
            to_email=[]
            for sub in subscriber:
                to_email.append(sub.email_address)
            
            email_id=email.pk
            
            # handover email sending task to celery
            celery_send_emails.delay(mail_subject,message,to_email,attachment,email_id)
        

            messages.success(request,'Email sent successfully.')
            return redirect('send_emails') 
            

    else:
        form=EmailForm()

        context={
            'form':form,
        }

        return render(request,'emails/send-emails.html',context)
    

def track_dashboard(request):

    emails=Email.objects.all().annotate(total_sent=Sum('sent__total_sent')).order_by('-sent_at')
    context={
        'emails':emails
    }
    return render(request,'emails/track_dashboard.html',context)




def track_stats(request,pk):
    email=get_object_or_404(Email,pk=pk)
    context={
        'email':email,
    }
    return render(request,'emails/track_stats.html',context)

def track_click(request,unique_id):
    url=request.GET.get('url')
    email_track=get_object_or_404(EmailTracking,unique_id=unique_id)
    if email_track.clicked_at is None:
        email_track.clicked_at=timezone.now()
        email_track.save()
        return HttpResponseRedirect(url)
    else:
        return HttpResponseRedirect(url)
    



def track_open(request,unique_id):
    
    email_track=get_object_or_404(EmailTracking,unique_id=unique_id)

    
    if email_track.opened_at is None:
        email_track.opened_at=timezone.now()
        email_track.save()
        return HttpResponse('Open Worked')
    else:
        return HttpResponse('Email already opened')

    
