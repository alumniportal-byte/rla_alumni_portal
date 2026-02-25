from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from dashboard.models import DistinguishedAlumni

class Command(BaseCommand):

    def handle(self,*args,**kwargs):

        limit = timezone.now() - timedelta(days=0)

        DistinguishedAlumni.objects.filter(
            is_deleted=True,
            deleted_at__lt=limit
        ).delete()