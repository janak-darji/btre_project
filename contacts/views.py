from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.mail import send_mail
from . models import Contact
# Create your views here.
def contact(request):
    if request.method == 'POST':
        listing_id =  request.POST['listing_id']
        listing =  request.POST['listing']
        name =  request.POST['name']
        email =  request.POST['email']
        phone =  request.POST['phone']
        message =  request.POST['message']
        user_id =  request.POST['user_id']
        realtor_email =  request.POST['realtor_email']

        if request.user.is_authenticated:
            user_id= request.user.id
            has_contacted =  Contact.objects.all().filter(listing_id=listing_id,user_id = user_id)
            if has_contacted:
                messages.error(request,'You have already made inquiry for this property')
                return redirect('/listings/' + listing_id)

        contact =  Contact(listing=listing, listing_id=listing_id,name=name, email= email, phone= phone, message=message, user_id = user_id)
        contact.save()
        send_mail(
            'Property listing inquery',
            'There has been inquery for ' + listing +  '. Sign in to admin panel for more details',
            'janak.n.darji@gmail.com',
            [realtor_email,'janak.n.darji@gmail.com'],            
            fail_silently=False
        )

        messages.success(request,'Your request submitted succecssfully')
        return redirect('/listings/' + listing_id)
