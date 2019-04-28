from django.core.management.base import BaseCommand
from api.models import Bill


class Command(BaseCommand):
    help = 'Gather votes data'

    def handle(self, *args, **options):
        for bill in Bill.objects.filter(vote_data_last_updated=None).iterator():
            bill.update_votes_data()
