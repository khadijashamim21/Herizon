from django.db import models
from django.contrib.auth.models import User

# ---------------------------
# User Profile Model
# ---------------------------

GENDER_CHOICES = [
    ('F', 'Female'),
    ('M', 'Male'),
    ('O', 'Other'),
]

BATCH_CHOICES = [
    ('A', 'Batch A'),
    ('B', 'Batch B'),
    ('C', 'Batch C'),
]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='F')
    bio = models.TextField(blank=True)
    skills = models.CharField(max_length=200, blank=True)
    linkedin = models.URLField(blank=True)
    verified = models.BooleanField(default=False)
    batch = models.CharField(max_length=1, choices=BATCH_CHOICES, blank=True, null=True)
    saved_jobs = models.ManyToManyField('Job', blank=True)
    saved_materials = models.ManyToManyField('Material', blank=True)

    def __str__(self):
        return self.user.username


# ---------------------------
# Post Model
# ---------------------------

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('job', 'Job'),
        ('material', 'Material'),
        ('update', 'Update'),
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    tags = models.CharField(max_length=200, blank=True)  # comma-separated tags

    def __str__(self):
        return f"{self.author.username} - {self.category}"


# ---------------------------
# Comment Model
# ---------------------------

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.id}"


# ---------------------------
# Job Model
# ---------------------------

class Job(models.Model):
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    link = models.URLField()
    image_url = models.URLField(blank=True)  # Optional image for card
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company}"


# ---------------------------
# Material Model
# ---------------------------

class Material(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True)
    file = models.FileField(upload_to='materials/', blank=True, null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ---------------------------
# Badge Model
# ---------------------------

class Badge(models.Model):
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=10)  # emoji or icon
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.icon} {self.name} - {self.user.user.username}"
