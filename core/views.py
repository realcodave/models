from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import SignUpForm, LoginForm, ModelProfileForm
from .models import ModelProfile

# Create your views here.
def index(request):
    models = ModelProfile.objects.all()
    return render(request, 'index.html', {'models':models})

def aboutUs(request):
    return render(request, 'about.html', {})

def casting(request):
    return render(request, 'casting.html', {})

def model_dashboard(request):
    return render(request,'model-dashboard.html', {})


@csrf_exempt  # Use this for API-style endpoints, but consider CSRF protection for production
def fetch_model_profile(request):
    model_profile = get_object_or_404(ModelProfile, user=request.user)
    data = {
        'fullname': model_profile.fullname,
        'height': model_profile.height,
        'hobby': model_profile.hobby,
        'gender': model_profile.gender,
        'occuption': model_profile.occuption,
        'nationality': model_profile.nationality,
        'language': model_profile.language,
        'location': model_profile.location,
        'address': model_profile.address,
        'dob': model_profile.dob,
        'bio': model_profile.bio,
        'phone_number': model_profile.phone_number,
        'twitter': model_profile.x,  # Ensure these fields exist
        'facebook': model_profile.facebook,
        'instagram': model_profile.instagram,
        'linkedin': model_profile.linkedin,
        'image': model_profile.image.url if model_profile.image else '',  # Ensure to handle if no image
    }
    return JsonResponse(data)

def model_profile(request):
    if request.method == 'POST':
        model_profile = get_object_or_404(ModelProfile, user=request.user)
        form = ModelProfileForm(request.POST, request.FILES, instance=model_profile)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        # Handle GET request: create or retrieve the profile instance
        model_profile, created = ModelProfile.objects.get_or_create(user=request.user)
        form = ModelProfileForm(instance=model_profile)
        
        # Render the profile page with the form
        return render(request, 'model-profile.html', {'form': form})
    

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Save the new user
            user = form.save()

            # Authenticate the user (using email and password)
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')

            user = authenticate(request, email=email, password=raw_password)

            if user is not None:
                # Log the user in
                login(request, user)
                
                # Return the role in the JSON response
                return redirect('home')
            else:
                return JsonResponse({'errors': 'Authentication failed'}, status=400)
        else:
            return JsonResponse({'errors': form.errors}, status=400)

    return render(request, 'register.html', {'form': SignUpForm()})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Authenticate user
            user = authenticate(request, email=email, password=password)
            if user is not None:
                # Log the user in
                login(request, user)
                # Redirect based on user role
                
                return redirect('profile')
                
            else:
                return JsonResponse({'error': 'Invalid email or password'}, status=400)
        else:
            return JsonResponse({'errors': form.errors}, status=400)

    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def userLogout(request):
    logout(request)
    return redirect('login')