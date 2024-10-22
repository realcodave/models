from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import SignUpForm, LoginForm, ModelProfileForm, GalleryForm
from .models import ModelProfile, Gallery, CustomUser
from django.contrib.auth.decorators import login_required

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

@csrf_exempt  # Consider using this carefully in production
def fetch_model_gallery(request, user_id=None):
    # Allow fetching of another user's gallery if user_id is provided
    if user_id:
        user = CustomUser.objects.filter(id=user_id).first()
        if not user:
            return JsonResponse({'error': 'User not found'}, status=404)
    else:
        user = request.user

    # Fetch the gallery images for the specific user
    model_gallery = Gallery.objects.filter(user=user)
    
    if not model_gallery.exists():
        data = {'images': []}  # Return empty list if no images found
    else:
        data = {'images': [gallery.image.url for gallery in model_gallery if gallery.image]}

    return JsonResponse(data)

@login_required
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



def gallery(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)  # Get the user whose gallery we want to display
    
    if request.method == 'POST' and request.user.is_authenticated and request.user == user:
        form = GalleryForm(request.POST, request.FILES)
        if form.is_valid():
            gallery_item = form.save(commit=False)
            gallery_item.user = request.user  # Save with the logged-in user
            gallery_item.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    
    else:
        # Handle GET request
        form = GalleryForm() if request.user == user else None  # Show form only for the gallery owner
        gallery = Gallery.objects.filter(user=user)  # Get the gallery of the requested user
        profile = ModelProfile.objects.filter(user=user).first()
        fullname = None
        image = None
        if profile.image:
            image = profile.image.url
        if profile.fullname: 
            fullname = profile.fullname
        return render(request, 'gallery.html', {
            'form': form,
            'gallery': gallery,
            'owner': user,  # Pass the gallery owner to the template
            'fullname': fullname,
            'image': image,
        })

    
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
@login_required
def userLogout(request):
    logout(request)
    return redirect('login')