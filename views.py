from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from authapp.forms import MembershipForm
import stripe
from django.conf import settings
from django.views import View
from .models import Membership
from .forms import MembershipForm
from .models import KickboxingRegistration
from django.shortcuts import get_object_or_404
from .models import ZumbaRegistration
from .models import CrossfitRegistration
from .models import YogaRegistration
from django.contrib.auth.decorators import user_passes_test
from .forms import FreePassRequestForm
from .models import Trainer  
from.models import FreePassRequest
from django.http import HttpResponseRedirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str  
from django.core.mail import send_mail
from django.conf import settings





# Create your views here.
def Home(request):
    return render(request,"index.html")

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        ename = request.POST['ename']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        phone_number = request.POST.get('phone_number')  

        # Check if passwords match
        if pass1 != pass2:
            messages.warning(request, 'Passwords do not match.')

        # Check if phone number is at least 10 digits
        if len(phone_number) < 10:
            messages.warning(request, 'Phone number should be at least 10 digits.')

        # Check if the username or email is already in use
        if User.objects.filter(username=username).exists() or User.objects.filter(email=ename).exists():
            messages.warning(request, 'Username or email is already in use.')

        # Additional checks and processing can be added here

        if pass1 == pass2 and len(phone_number) >= 10 and not (User.objects.filter(username=username).exists() or User.objects.filter(email=ename).exists()):
            # Process registration logic here
            user = User.objects.create_user(username=username, email=ename, password=pass1)
            user.first_name = fname
            user.last_name = lname
            user.save()

            # Redirect to success page or login page
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('/login')

    return render(request, 'signup.html')


def handlelogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = auth.authenticate(username=username, password=pass1)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('/')
        else:
            messages.warning(request, 'Wrong password. Please try again.')
            return redirect('/login')

    return render(request, 'handlelogin.html') 

def handlelogout(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('/login')

def membership_form(request):
    
    if request.method == 'POST':
        # Extract form data
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        address = request.POST['address']
        age = request.POST['age']
        gender = request.POST['gender']
        phone_number = request.POST['phone_number']
        date_of_joining = request.POST['date_of_joining']

        if len(phone_number) < 10:
            messages.warning(request, 'Phone number should be at least 10 digits.')
            return render(request, 'membership_form.html')


        request.session['first_name'] = first_name
        request.session['last_name'] = last_name


        membership_instance = Membership.objects.create(
            first_name=first_name,
            last_name=last_name,
            address=address,
            age=age,
            gender=gender,
            phone_number=phone_number,
            date_of_joining=date_of_joining,
        )

        request.session['membership_id'] = membership_instance.id

        messages.success(request, 'Form submitted successfully!')


        return redirect('select_gym_plan')

    return render(request, 'membership_form.html')




class SelectGymPlanView(View):
    template_name = 'select_gym_plan.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        selected_plan = request.POST.get('gym_plan')
        request.session['selected_plan'] = selected_plan

        # Set your Stripe secret key
        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            # Create a PaymentIntent on the server
            amount_in_usd = calculate_amount(selected_plan)
            amount_in_inr = convert_to_inr(amount_in_usd)  # Convert the amount to INR

            intent = stripe.PaymentIntent.create(
                amount=amount_in_inr,
                currency='inr',
            )
            client_secret = intent.client_secret

            context = {
                'client_secret': client_secret,
                'selected_plan': selected_plan,
            }

            return render(request, 'payment_page.html', context)

        except stripe.error.CardError as e:
            # Display error to the user
            messages.error(request, f'Error: {e.error.message}')
            return redirect('select_gym_plan')


def calculate_amount(selected_plan):
    # Implement your logic to calculate the amount based on the selected plan
    # For example, you can use a dictionary to map plans to amounts
    plan_amounts = {'three': 6000, 'six': 12000, 'twelve': 18000}
    return plan_amounts.get(selected_plan, 0)


def convert_to_inr(amount_in_usd):
    # Use the current exchange rate or your preferred rate
    exchange_rate = 74.46  # Replace with the latest exchange rate
    amount_in_inr = int(amount_in_usd * exchange_rate)
    return amount_in_inr

class PaymentConfirmationView(View):
    template_name = 'payment_confirmation.html'

    def get(self, request, *args, **kwargs):
        selected_plan = request.session.get('selected_plan', None)
        first_name = request.session.get('first_name', None)
        last_name = request.session.get('last_name', None)
        amount = None

        if selected_plan == 'three':
            amount = '₹6000'
        elif selected_plan == 'six':
            amount = '₹12000'
        elif selected_plan == 'twelve':
            amount = '₹18000'



        context = {
            'selected_plan': selected_plan,
            'first_name': first_name,
            'last_name': last_name,
            'amount': amount,  
        }

        return render(request, 'payment_confirmation.html', context)
    def post(self, request, *args, **kwargs):
        selected_plan = request.session.get('selected_plan', None)

        # Assuming you have the user's data stored in the session during the membership_form submission
        first_name = request.session.get('first_name', None)
        last_name = request.session.get('last_name', None)
        address = request.session.get('address', None)
        age = request.session.get('age', None)
        gender = request.session.get('gender', None)
        phone_number = request.session.get('phone_number', None)
        date_of_joining = request.session.get('date_of_joining', None)
        selected_plan=selected_plan,

        
        membership_instance = get_object_or_404(Membership, id=membership_id)

        membership_instance.selected_plan = selected_plan
        membership_instance.save()

        return redirect('/')

class ClassesView(View):
    template_name = 'classes.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

def kickboxing_registration(request):
    if request.method == 'POST':
        # Extract form data
        full_name = request.POST.get('full_name')
        date_of_joining = request.POST.get('date_of_joining')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phone_number')
        payment_option = request.POST.get('payment_option')

        if len(phone_number) < 10:
            messages.warning(request, 'Phone number should be at least 10 digits.')
            return render(request, 'kickboxing_registration.html')


        registration_instance = KickboxingRegistration.objects.create(
            full_name=full_name,
            date_of_joining=date_of_joining,
            age=age,
            gender=gender,
            phone_number=phone_number,
            payment_option=payment_option,
        )

        # Redirect or do further processing as needed
        return redirect('kickboxing_receipt', registration_id=registration_instance.id)

        messages.success(request, 'Form submitted successfully!')

    # If it's a GET request, render the form
    return render(request, 'kickboxing_registration.html')

def kickboxing_receipt(request, registration_id):
    # Retrieve the KickboxingRegistration instance using the registration_id
    registration_instance = get_object_or_404(KickboxingRegistration, id=registration_id)

    # Get the necessary details from the instance
    full_name = registration_instance.full_name
    payment_option = registration_instance.payment_option

    if payment_option == '6_months':
        amount = '₹8000'
    elif payment_option == '12_months':
        amount = '₹16000'

    context = {
        'full_name': full_name,
        'payment_option': payment_option,
        'amount': amount,
    }

    return render(request, 'kickboxing_receipt.html', context)

def zumba_registration(request):
    if request.method == 'POST':
        # Extract form data for Zumba registration
        full_name = request.POST.get('full_name')
        date_of_joining = request.POST.get('date_of_joining')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phone_number')
        payment_option = request.POST.get('payment_option')

        if len(phone_number) < 10:
            messages.warning(request, 'Phone number should be at least 10 digits.')
            return render(request, 'zumba_registration.html')


        # Save the registration data in the database
        registration_instance = ZumbaRegistration.objects.create(
            full_name=full_name,
            date_of_joining=date_of_joining,
            age=age,
            gender=gender,
            phone_number=phone_number,
            payment_option=payment_option,
        )

        # Redirect or do further processing as needed
        return redirect('zumba_receipt', registration_id=registration_instance.id)

        messages.success(request, 'Form submitted successfully!')

    # If it's a GET request, render the Zumba registration form
    return render(request, 'zumba_registration.html')

def zumba_receipt(request, registration_id):
    # Retrieve the ZumbaRegistration instance using the registration_id
    registration_instance = get_object_or_404(ZumbaRegistration, id=registration_id)

    # Get the necessary details from the instance
    full_name = registration_instance.full_name
    payment_option = registration_instance.payment_option

    if payment_option == '6_months':
        amount = '₹9000'
    elif payment_option == '12_months':
        amount = '₹18000'

    context = {
        'full_name': full_name,
        'payment_option': payment_option,
        'amount': amount,
    }

    return render(request, 'zumba_receipt.html', context)



def crossfit_registration(request):
    if request.method == 'POST':
        # Extract form data for CrossFit registration
        full_name = request.POST.get('full_name')
        date_of_joining = request.POST.get('date_of_joining')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phone_number')
        payment_option = request.POST.get('payment_option')

        if len(phone_number) < 10:
            messages.warning(request, 'Phone number should be at least 10 digits.')
            return render(request, 'crossfit_registration.html')


        # Save the registration data in the database
        registration_instance = CrossfitRegistration.objects.create(
            full_name=full_name,
            date_of_joining=date_of_joining,
            age=age,
            gender=gender,
            phone_number=phone_number,
            payment_option=payment_option,
        )

        # Redirect or do further processing as needed
        return redirect('crossfit_receipt', registration_id=registration_instance.id)

        messages.success(request, 'Form submitted successfully!')

    # If it's a GET request, render the CrossFit registration form
    return render(request, 'crossfit_registration.html')

def crossfit_receipt(request, registration_id):
    # Retrieve the CrossFitRegistration instance using the registration_id
    registration_instance = get_object_or_404(CrossfitRegistration, id=registration_id)

    # Get the necessary details from the instance
    full_name = registration_instance.full_name
    payment_option = registration_instance.payment_option

    if payment_option == '6_months':
        amount = '₹10000'
    elif payment_option == '12_months':
        amount = '₹20000'


    context = {
        'full_name': full_name,
        'payment_option': payment_option,
        'amount': amount, 
    }

    return render(request, 'crossfit_receipt.html', context)

def yoga_registration(request):
    if request.method == 'POST':
        # Extract form data for Yoga registration
        full_name = request.POST.get('full_name')
        date_of_joining = request.POST.get('date_of_joining')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phone_number')
        payment_option = request.POST.get('payment_option')

        if len(phone_number) < 10:
            messages.warning(request, 'Phone number should be at least 10 digits.')
            return render(request, 'yoga_registration.html')


        # Save the registration data in the database
        registration_instance = YogaRegistration.objects.create(
            full_name=full_name,
            date_of_joining=date_of_joining,
            age=age,
            gender=gender,
            phone_number=phone_number,
            payment_option=payment_option,
        )

        # Redirect or do further processing as needed
        return redirect('yoga_receipt', registration_id=registration_instance.id)

        messages.success(request, 'Form submitted successfully!')

    # If it's a GET request, render the Yoga registration form
    return render(request, 'yoga_registration.html')

def yoga_receipt(request, registration_id):
    # Retrieve the YogaRegistration instance using the registration_id
    registration_instance = get_object_or_404(YogaRegistration, id=registration_id)

    # Get the necessary details from the instance
    full_name = registration_instance.full_name
    payment_option = registration_instance.payment_option

    if payment_option == '6_months':
        amount = '₹7000'
    elif payment_option == '12_months':
        amount = '₹14000'


    context = {
        'full_name': full_name,
        'payment_option': payment_option,
        'amount': amount,
    }

    return render(request, 'yoga_receipt.html', context)

def sunday(request):
    return render(request,"sunday.html")

def monday(request):
    return render(request,"monday.html")

def tuesday(request):
    return render(request,"tuesday.html")

def wednesday(request):
    return render(request,"wednesday.html")

def thursday(request):
    return render(request,"thursday.html")

def friday(request):
    return render(request,"friday.html")

def saturday(request):
    return render(request,"saturday.html")

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        
        if username == 'khushi' and password == 'khushi33':
            
            return redirect('admin_dashboard')
        else:
           
            error_message = 'Invalid username or password.'

    return render(request, 'admin_login.html', locals())


def AdminDashboardView(request):
    
    total_members = Membership.objects.count()
    kickboxing_registrations = KickboxingRegistration.objects.count()
    zumba_registrations = ZumbaRegistration.objects.count()
    crossfit_registrations = CrossfitRegistration.objects.count()
    yoga_registrations = YogaRegistration.objects.count()
    trainers=Trainer.objects.count()
    free_pass=FreePassRequest.objects.count()

   
    all_memberships = Membership.objects.all()
    all_kickboxing_registrations = KickboxingRegistration.objects.all()
    all_zumba_registrations = ZumbaRegistration.objects.all()
    all_crossfit_registrations = CrossfitRegistration.objects.all()
    all_yoga_registrations = YogaRegistration.objects.all()
    all_trainers = Trainer.objects.all()  
    all_free_pass_requests = FreePassRequest.objects.all()


    return render(request, 'admin_dashboard.html', {
        'total_members': total_members,
        'kickboxing_registrations': kickboxing_registrations,
        'zumba_registrations': zumba_registrations,
        'crossfit_registrations': crossfit_registrations,
        'yoga_registrations': yoga_registrations,
        'all_memberships': all_memberships,
        'all_kickboxing_registrations': all_kickboxing_registrations,
        'all_zumba_registrations': all_zumba_registrations,
        'all_crossfit_registrations': all_crossfit_registrations,
        'all_yoga_registrations': all_yoga_registrations,
        'all_trainers': all_trainers,
        'all_free_pass_requests': all_free_pass_requests,

    })

def trainer(request):
    return render(request, 'trainer.html')

def free_pass_request(request):
    if request.method == 'POST':
        form = FreePassRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            # Check if the email or phone number already exists in the database
            if FreePassRequest.objects.filter(email=email).exists() or FreePassRequest.objects.filter(phone_number=phone_number).exists():
                # Display a message indicating that the email or phone number is already used
                messages.error(request, 'Email or phone number is already used for a Free Pass request.')
            elif len(phone_number) != 10:
                # Display a message indicating that the phone number should be 10 digits
                messages.error(request, 'Phone number should be 10 digits.')
            else:
                # Save the form if the email and phone number are not already used and phone number is 10 digits
                form.save()
                messages.success(request, 'Free Pass request submitted successfully!')
                return redirect('fpassr')
        else:
            # Display form errors if form is invalid
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = FreePassRequestForm()
    
    # Get messages and pass them to the template context
    message = None
    storage = messages.get_messages(request)
    for message in storage:
        pass

    return render(request, 'free_pass_request.html', {'form': form, 'message': message})


def fpassr(request):
    return render(request, 'fpassr.html')



def fpassr(request):
    return render(request, 'fpassr.html')

def add_member(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        gender = request.POST.get('gender')
        date_of_joining = request.POST.get('date_of_joining')
        age = request.POST.get('age')
        
        
        membership = Membership.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            gender=gender,
            date_of_joining=date_of_joining,
            age=age
        )
        
        
        return redirect('admin_dashboard')

    return render(request, 'admin_dashboard.html')

def delete_member(request, member_id):
    
    membership = get_object_or_404(Membership, pk=member_id)
   
    membership.delete()
    
    
    messages.success(request, 'Member deleted successfully')
    
    
    return redirect('admin_dashboard')
def add_trainer(request):
    if request.method == 'POST':
        
        full_name = request.POST.get('trainer_full_name')
        age = request.POST.get('trainer_age')
        gender = request.POST.get('trainer_gender')
        email = request.POST.get('trainer_email')
        address = request.POST.get('trainer_address')
        phone_number = request.POST.get('trainer_phone_number')
        
        
        new_trainer = Trainer.objects.create(
            full_name=full_name,
            age=age,
            gender=gender,
            email=email,
            address=address,
            phone_number=phone_number
        )
        
        
        return redirect('admin_dashboard')  
    else:
        
        return render(request, 'add_trainer_form.html')  

def delete_trainer(request, trainer_id):
    
    trainer = get_object_or_404(Trainer, id=trainer_id)
    
    if request.method == 'POST':
        
        trainer.delete()
        
        
        return redirect('admin_dashboard')  
    else:
        
        pass

def add_free_pass_request(request):
    if request.method == 'POST':
        
        full_name = request.POST.get('full_name')
        age = request.POST.get('age')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        trial_date = request.POST.get('trial_date')
        
        
        new_request = FreePassRequest.objects.create(
            full_name=full_name,
            age=age,
            phone_number=phone_number,
            email=email,
            trial_date=trial_date
        )
        
        
        return redirect('admin_dashboard')  
    else:
        
        return render(request, 'add_free_pass_request_form.html')  

def delete_free_pass_request(request, request_id):
    # Retrieve the FreePassRequest object
    request_obj = get_object_or_404(FreePassRequest, id=request_id)
    
    if request.method == 'POST':
        request_obj.delete()
        return redirect('admin_dashboard')  
    else:
        # Handle GET request if needed
        pass

def add_kickboxing_registration(request):
    if request.method == 'POST':
        
        full_name = request.POST.get('full_name')
        date_of_joining = request.POST.get('date_of_joining')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phone_number')
        payment_option = request.POST.get('payment_option')
        
        
        new_registration = KickboxingRegistration.objects.create(
            full_name=full_name,
            date_of_joining=date_of_joining,
            age=age,
            gender=gender,
            phone_number=phone_number,
            payment_option=payment_option
        )
        
       
        return redirect('admin_dashboard')  
    else:
        
        return render(request, 'add_kickboxing_registration_form.html')
def delete_kickboxing_registration(request, registration_id):
   
    registration_obj = get_object_or_404(KickboxingRegistration, id=registration_id)
    
    if request.method == 'POST':
        
        registration_obj.delete()
        
        
        return redirect('admin_dashboard')  
    else:
        
        pass
def add_zumba_registration(request):
    if request.method == 'POST':
       
        full_name = request.POST.get('full_name')
        date_of_joining = request.POST.get('date_of_joining')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phone_number')
        payment_option = request.POST.get('payment_option')
        
        
        new_registration = ZumbaRegistration.objects.create(
            full_name=full_name,
            date_of_joining=date_of_joining,
            age=age,
            gender=gender,
            phone_number=phone_number,
            payment_option=payment_option
        )
        
       
        return redirect('admin_dashboard')  
    else:
        
        return render(request, 'zumba_registration.html')

def delete_zumba_registration(request, registration_id):
   
    registration_obj = get_object_or_404(ZumbaRegistration, id=registration_id)
    
    if request.method == 'POST':
       
        registration_obj.delete()
        
       
        return redirect('admin_dashboard')  
    else:
        
        pass
def add_crossfit_registration(request):
    if request.method == 'POST':
        
        full_name = request.POST.get('full_name')
        date_of_joining = request.POST.get('date_of_joining')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phone_number')
        payment_option = request.POST.get('payment_option')

        
        registration_instance = CrossfitRegistration.objects.create(
            full_name=full_name,
            date_of_joining=date_of_joining,
            age=age,
            gender=gender,
            phone_number=phone_number,
            payment_option=payment_option,
        )

        
        return redirect('admin_dashboard')

    
    return render(request, 'crossfit_registration.html')


def delete_crossfit_registration(request, registration_id):
    
    registration_obj = get_object_or_404(CrossfitRegistration, id=registration_id)
    
    if request.method == 'POST':
        
        registration_obj.delete()
        
        
        return redirect('admin_dashboard')  
    else:
        
        pass

def add_yoga_registration(request):
    if request.method == 'POST':
        
        full_name = request.POST.get('full_name')
        date_of_joining = request.POST.get('date_of_joining')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phone_number')
        payment_option = request.POST.get('payment_option')

        
        registration_instance = YogaRegistration.objects.create(
            full_name=full_name,
            date_of_joining=date_of_joining,
            age=age,
            gender=gender,
            phone_number=phone_number,
            payment_option=payment_option,
        )

        
        return redirect('admin_dashboard')

    
    return render(request, 'add_yoga_registration.html')

def delete_yoga_registration(request, registration_id):
    
    registration_obj = get_object_or_404(YogaRegistration, id=registration_id)
    
    if request.method == 'POST':
        
        registration_obj.delete()
        
    
        return redirect('admin_dashboard')  
    else:
        
        pass

def flyer_view(request):
    return render(request, 'flyer.html')

def about(request):
    return render(request, 'about.html')

def photo(request):
    return render(request, 'photo.html')

