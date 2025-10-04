# main/signals.py
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, Badge

# -----------------------------
# UserProfile creation signals
# -----------------------------
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

# -----------------------------
# Automatic Badge Assignment
# -----------------------------

# Award "Job Hunter" badge when user saves 5+ jobs
@receiver(m2m_changed, sender=UserProfile.saved_jobs.through)
def award_job_hunter_badge(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        if instance.saved_jobs.count() >= 5:
            Badge.objects.get_or_create(user=instance, name="Job Hunter", icon="🏆")
        else:
            Badge.objects.filter(user=instance, name="Job Hunter").delete()

# Award "Material Collector" badge when user saves 5+ materials
@receiver(m2m_changed, sender=UserProfile.saved_materials.through)
def award_material_collector_badge(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        if instance.saved_materials.count() >= 5:
            Badge.objects.get_or_create(user=instance, name="Material Collector", icon="📚")
        else:
            Badge.objects.filter(user=instance, name="Material Collector").delete()
