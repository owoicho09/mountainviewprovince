from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, StudentProfile

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.create(user=instance)
    else:
        # Update the existing StudentProfile if needed
        profile, created = StudentProfile.objects.get_or_create(user=instance)
        if not created:
            # Perform additional logic for updating the profile if necessary
            profile.save()