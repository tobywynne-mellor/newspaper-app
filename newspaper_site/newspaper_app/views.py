from django.shortcuts import render
from .forms import ProfileForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

# -----------------------------user's homepage-----------------------


def index(request):
    return render(request, "newspaper_app/base.html")
# -----------------------------user's profile registration and login-----------------------
# user's profile register and login validation


@require_http_methods(["POST"])
@csrf_exempt
def register_validation(request):
    form = UserCreationForm(request.POST)
    registration_form = ProfileForm(request.POST)
    context = {"form": form, "registration_form": registration_form}
    if(form.is_valid() and registration_form.is_valid()):
        context = {"message": True}
        # Save user's name and password
        user = form.save()
        # login user
        login(request, user)
        profile = registration_form.save(False)
        profile.user = user
        # Save user extra info
        profile.save()
        registration_form.save_m2m()
        return redirect("user:base")
    else:
        return render(request, 'newspaper_app/register.html', context)


@require_http_methods(["POST"])
@csrf_exempt
def login_validation(request):
    form = AuthenticationForm(data=request.POST)
    context = {"form": form}
    if(form.is_valid()):
        user = form.get_user()
        login(request, user)
        return redirect("user:base")
    else:
        return render(request, 'newspaper_app/login.html', context)


# user's profile register and login form
@require_http_methods(["GET"])
def register_view(request):
    form = UserCreationForm()
    registration_form = ProfileForm()
    context = {"form": form, "registration_form": registration_form}
    return render(request, 'newspaper_app/register.html', context)


@require_http_methods(["GET"])
def login_view(request):
    form = AuthenticationForm()
    context = {"form": form}
    return render(request, 'newspaper_app/login.html', context)


@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    return redirect("user:base")
