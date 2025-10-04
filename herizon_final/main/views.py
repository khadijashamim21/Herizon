from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db.models import Count
from .models import Post, Job, Material, UserProfile, Badge

# ---------------------------
# AUTHENTICATION VIEWS
# ---------------------------

def signup(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        gender = request.POST.get('gender')

        if User.objects.filter(username=username).exists():
            error = 'Username already taken.'
        elif gender != 'F':
            error = 'Only female users can register.'
        else:
            user = User.objects.create_user(username=username, password=password)
            profile, created = UserProfile.objects.get_or_create(user=user)
            if created:
                profile.gender = gender
                profile.save()
            return redirect('login')

    return render(request, 'signup.html', {'error': error})


def user_login(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            profile, created = UserProfile.objects.get_or_create(user=user)
            if created:
                profile.gender = 'F'
                profile.save()
            return redirect('feed')
        else:
            error = "Invalid username or password."
    return render(request, 'login.html', {'error': error})


def user_logout(request):
    logout(request)
    return redirect('login')


# ---------------------------
# MAIN APP VIEWS
# ---------------------------

@login_required
def feed(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    skills = user_profile.skills.split(",") if user_profile.skills else []

    personalized_posts = Post.objects.none()
    if skills:
        # Filter posts containing any of the user's skills
        from django.db.models import Q
        q_filter = Q()
        for skill in skills:
            q_filter |= Q(content__icontains=skill.strip())
        personalized_posts = Post.objects.filter(q_filter).order_by('-created_at')

    trending_posts = Post.objects.annotate(like_count=Count('likes')).order_by('-like_count')[:5]
    all_posts = Post.objects.all().order_by('-created_at')

    return render(request, 'feed.html', {
        'posts': all_posts,
        'personalized_posts': personalized_posts,
        'trending_posts': trending_posts,
    })


@login_required
def jobs(request):
    jobs_list = Job.objects.all().order_by('-created_at')
    return render(request, 'jobs.html', {'jobs': jobs_list})


@login_required
def materials(request):
    materials_list = Material.objects.all().order_by('-created_at')
    return render(request, 'materials.html', {'materials': materials_list})


@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        category = request.POST.get('category')
        Post.objects.create(author=request.user, content=content, category=category)
        return redirect('feed')
    return render(request, 'create_post.html')


# ---------------------------
# BADGES
# ---------------------------

def assign_verified_badge(user_profile):
    if user_profile.verified:
        Badge.objects.get_or_create(
            user=user_profile,
            name="Verified",
            icon="🌸"
        )


# ---------------------------
# SAVE JOBS & MATERIALS
# ---------------------------

@login_required
def save_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    profile.saved_jobs.add(job)
    return redirect('/jobs/')


@login_required
def save_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    profile.saved_materials.add(material)
    return redirect('/materials/')


# ---------------------------
# SEARCH POSTS
# ---------------------------

@login_required
def search_posts(request):
    query = request.GET.get('q', '')
    filtered_posts = Post.objects.filter(content__icontains=query)
    return render(request, 'feed.html', {'posts': filtered_posts, 'query': query})


# ---------------------------
# USER PROFILE
# ---------------------------

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    user_profile, _ = UserProfile.objects.get_or_create(user=user)
    posts = Post.objects.filter(author=user).order_by('-created_at')
    badges = Badge.objects.filter(user=user_profile)
    return render(request, 'profile.html', {'user_profile': user_profile, 'posts': posts, 'badges': badges})
