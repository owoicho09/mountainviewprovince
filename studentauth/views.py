from django.shortcuts import render,redirect,reverse
from .form import RegistrationForm,UserUpdateForm,ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from .models import CustomUser, StudentProfile
from django.contrib.auth.views import PasswordResetView, PasswordResetCompleteView,PasswordResetConfirmView,PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


# Create your views here.


def register(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in')
        return redirect('studentdashboard:dashboard')
    if request.method == 'POST':
        print(request.POST)
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            email = form.cleaned_data.get('email')

            print('----',email)

            phone = form.cleaned_data.get('phone')
            password = form.cleaned_data.get('password1')


            user = authenticate(email=email,password=password)
            if user is not None:
                login(request,user)
                messages.success(request,'Your Account was created successfully')
                profile, created = StudentProfile.objects.get_or_create(user=request.user)
                phone = profile.phone
                fullname = profile.fullname

                profile.save()
                return redirect('studentdashboard:dashboard')
            else:
                messages.error(request,'Authentication failed,try again')
                return redirect('studentdashboard:register')

    else:
        form = RegistrationForm()
        print('form not valid')

    context = {
        'form':form

    }
    return render(request, 'studentauth/registration.html', context)

def login_page(request):
    if request.user.is_authenticated:
        return redirect('studentdashboard:dashboard')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(f"Email: {email}, Password: {password}")  # Debugging line

        try:
            user = authenticate(request,email=email, password=password)
            print(f"Authenticated User: {user}")  # Debugging line

            if user is not None:
                login(request, user)
                messages.success(request,'Login successful')
                next_url = request.GET.get('next','studentdashboard:dashboard')
                return redirect(next_url)
            else:
                messages.error(request,'Email or Password incorrect')
        except CustomUser.DoesNotExist:
                messages.error(request,'User with Email does not exist')
        except Exception as e:
            messages.error(request,f'An error occurred: {e}')

    return render(request, 'studentauth/login.html')


def profile(request):
    profile = StudentProfile.objects.get(user=request.user)

    # Initialize the forms outside the if block to handle both GET and POST
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile Updated successfully')
            return redirect('studentdashboard:dashboard')
        else:
            # Print form errors to debug validation issues
            print("User form errors:", u_form.errors)
            print("Profile form errors:", p_form.errors)

    context = {
        'profile': profile,
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'studentauth/profile.html', context)


def logout_page(request):
    logout(request)
    return redirect(reverse('studentauth:login'))


def accountsettings(request):

    return render(request,'studentdashboard/accountSettings.html')


@login_required
def password_changed(request):
    return render(request, 'studentdashboard/password_changed.html')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'

    def get_success_url(self):
        # Ensure to use the namespace in the URL name
        return reverse_lazy('studentauth:password_reset_done')


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('studentauth:password_reset_complete')


class CustomPasswordResetComplete(PasswordResetCompleteView):
    template_name = "registration/password_reset_complete.html"


