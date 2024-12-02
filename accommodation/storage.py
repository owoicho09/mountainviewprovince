
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
class EmailBackupStorage(FileSystemStorage):
    def save(self, name, content):
        # Save the backup to a temporary file
        filename = os.path.join('/tmp', name)
        with open(filename, 'wb') as f:
            for chunk in content.chunks():
                f.write(chunk)

        # Send the backup as an email attachment
        self.send_backup_by_email(filename)

        return filename

    def send_backup_by_email(self, filename):
        # Send email with backup as attachment
        with open(filename, 'rb') as file:
            send_mail(
                'Database Backup',
                'Please find the attached database backup.',
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],  # Send to the admin email configured above
                fail_silently=False,
                attachments=[(filename, file.read(), 'application/octet-stream')]
            )

# Tell django-dbbackup to use the custom storage backend
