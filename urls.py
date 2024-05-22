from django.urls import path, include
from django.contrib import admin
from authapp import views
from .views import signup
from .views import handlelogin, handlelogout
from .views import membership_form
from .views import SelectGymPlanView, PaymentConfirmationView
from django.contrib import admin
from .forms import MembershipForm
from .views import ClassesView
from .views import kickboxing_registration
from .views import kickboxing_receipt
from .views import zumba_registration
from .views import zumba_receipt
from .views import crossfit_registration
from .views import crossfit_receipt
from .views import yoga_registration 
from .views import yoga_receipt
from .views import sunday
from .views import monday
from .views import tuesday
from .views import wednesday
from .views import thursday
from .views import friday
from .views import saturday
from .views import AdminDashboardView
from .views import admin_login
from.views import trainer
from .views import free_pass_request
from .views import fpassr
from .views import add_member
from .views import delete_member
from .views import add_trainer
from .views import delete_trainer
from .views import add_free_pass_request
from .views import delete_free_pass_request
from .views import add_kickboxing_registration
from .views import delete_kickboxing_registration
from .views import add_zumba_registration
from .views import delete_zumba_registration
from .views import add_crossfit_registration
from .views import delete_crossfit_registration
from .views import add_yoga_registration
from .views import delete_yoga_registration
from .views import flyer_view
from .views import about
from .views import photo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home, name="Home"),
    path('signup',views.signup,name="signup"),
    path('login', views.handlelogin, name='handlelogin'),
    path('logout', views.handlelogout, name='handlelogout'),
    path('membership/', membership_form, name='membership_form'),
    path('select_gym_plan/', SelectGymPlanView.as_view(), name='select_gym_plan'),
    path('payment_confirmation/', PaymentConfirmationView.as_view(), name='payment_confirmation'),
    path('classes/', ClassesView.as_view(), name='classes'),
    path('kickboxing_registration/', kickboxing_registration, name='kickboxing_registration'),
    path('kickboxing_receipt/<int:registration_id>/', kickboxing_receipt, name='kickboxing_receipt'),
    path('zumba_registration/', zumba_registration, name='zumba_registration'),
    path('zumba_receipt/<int:registration_id>/', zumba_receipt, name='zumba_receipt'),
    path('crossfit_registration/', crossfit_registration, name='crossfit_registration'),
    path('crossfit_receipt/<int:registration_id>/', crossfit_receipt, name='crossfit_receipt'),
    path('yoga_registration/', yoga_registration, name='yoga_registration'),
    path('yoga_receipt/<int:registration_id>/', yoga_receipt, name='yoga_receipt'),
    path('sunday/', views.sunday, name='sunday'),
    path('monday/', views.monday, name='monday'),
    path('tuesday/', views.tuesday, name='tuesday'),
    path('wednesday/', views.wednesday, name='wednesday'),
    path('thursday/', views.thursday, name='thursday'),
    path('friday/', views.friday, name='friday'),
    path('saturday/', views.saturday, name='saturday'),
    path('admin_dashboard/', AdminDashboardView, name='admin_dashboard'),
    path('admin_login/', admin_login, name='admin_login'),
    path('trainer/', views.trainer, name='trainer'),
    path('free_pass_request/', views.free_pass_request, name='free_pass_request'),
    path('fpassr/', views.fpassr, name='fpassr'),
    path('add-member/', add_member, name='add_member'),
    path('delete_member/<int:member_id>/', delete_member, name='delete_member'),
    path('add_trainer/', views.add_trainer, name='add_trainer'),
    path('delete_trainer/<int:trainer_id>/', views.delete_trainer, name='delete_trainer'),
    path('add_free_pass_request/', views.add_free_pass_request, name='add_free_pass_request'),
    path('delete_free_pass_request/<int:request_id>/', views.delete_free_pass_request, name='delete_free_pass_request'),
    path('add_kickboxing_registration/', views.add_kickboxing_registration, name='add_kickboxing_registration'),
    path('delete_kickboxing_registration/<int:registration_id>/', views.delete_kickboxing_registration, name='delete_kickboxing_registration'),
    path('add_zumba_registration/', views.add_zumba_registration, name='add_zumba_registration'),
    path('delete_zumba_registration/<int:registration_id>/', views.delete_zumba_registration, name='delete_zumba_registration'),
    path('add_crossfit_registration/', views.add_crossfit_registration, name='add_crossfit_registration'),
    path('delete_crossfit_registration/<int:registration_id>/', views.delete_crossfit_registration, name='delete_crossfit_registration'),
    path('add_yoga_registration/', views.add_yoga_registration, name='add_yoga_registration'),
    path('delete_yoga_registration/<int:registration_id>/', views.delete_yoga_registration, name='delete_yoga_registration'),
    path('flyer/', views.flyer_view, name='flyer'),
    path('about/', views.about, name='about'),
    path('photo/', views.photo, name='photo'),

]

    