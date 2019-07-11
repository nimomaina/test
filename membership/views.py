from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.forms.forms import NON_FIELD_ERRORS
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
import django_pesapal
from django_pesapal.views import PaymentRequestMixin


from .forms import SubscriberForm
# Create your views here.


def home(request):
    return render(request, 'home.html')


def subscriber_new(request, template='registration/signup.html',):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            # Unpack form values
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            # Create the User record
            user = User(username=username, email=email,
                        first_name=first_name, last_name=last_name)
            user.set_password(password)
            user.save()
            success_url = reverse('login')

            def get_pesapal_payment_iframe(self, request):

                '''
                Authenticates with pesapal to get the payment iframe src
                '''
                order_info = {
                    'first_name': request.POST['first_name'],
                    'last_name': request.POST['last_name'],
                    'amount': 1000,
                    'description': 'Annual Subscription',
                    'reference': 2,  # some object id
                    'email': request.POST['email'],
                }

                iframe_src_url = self.get_payment_url(**order_info)
                return iframe_src_url
                    
    else:
        form = SubscriberForm()

    return render(request, template, {'form': form,})

# class PaymentView(PaymentRequestMixin):

#     def get_pesapal_payment_iframe(self, request):

#         '''
#         Authenticates with pesapal to get the payment iframe src
#         '''
#         order_info = {
#             'first_name': request.POST['first_name'],
#             'last_name': request.POST['last_name'],
#             'amount': 1000,
#             'description': 'Annual Subscription',
#             'reference': 2,  # some object id
#             'email': request.POST['email'],
#         }

#         iframe_src_url = self.get_payment_url(**order_info)
#         return iframe_src_url