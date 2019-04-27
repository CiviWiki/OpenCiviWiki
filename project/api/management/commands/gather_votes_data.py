from django.core.management.base import BaseCommand
from api.models import Bill


class Command(BaseCommand):
    help = 'Gather votes data'

    def handle(self, *args, **options):
        for bill in Bill.objects.filter(is_voted_data_updated=False).iterator():
            bill.update_votes_data()
