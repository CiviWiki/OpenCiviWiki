# data_loader.py
from django.core.management.base import BaseCommand
from threads.models import Civi, CiviLink, Thread  # Adjust import to your app's name

from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Load dummy data for Civis and CiviLinks"

    def handle(self, *args, **kwargs):
        # Create a thread
        thread, _ = Thread.objects.get_or_create(
            title="Net Neutrality",
        )
        user = User.objects.first()
        # Create dummy Civis
        civi1 = Civi.objects.create(
            title="Civi 1: Importance of Net Neutrality",
            body="Net neutrality ensures that all users have equal access to information and services online.",
            author=user,
            votes_pos=10,
            votes_neg=2,
            thread=thread,
        )

        civi2 = Civi.objects.create(
            title="Civi 2: Risks of Removing Net Neutrality",
            body="Without net neutrality, ISPs could prioritize their own content or the content of those who pay for faster access.",
            author=user,
            votes_pos=15,
            votes_neg=1,
            thread=thread,
        )

        civi3 = Civi.objects.create(
            title="Civi 3: Public Opinion on Net Neutrality",
            body="A significant portion of the public supports net neutrality regulations to protect free internet access.",
            author=user,
            votes_pos=20,
            votes_neg=3,
            thread=thread,
        )

        # Create dummy CiviLinks
        CiviLink.objects.create(
            from_civi=civi1, to_civi=civi2, relation_type="response"
        )

        CiviLink.objects.create(
            from_civi=civi2, to_civi=civi1, relation_type="rebuttal"
        )

        CiviLink.objects.create(from_civi=civi1, to_civi=civi3, relation_type="support")

        CiviLink.objects.create(
            from_civi=civi3, to_civi=civi2, relation_type="challenge"
        )

        self.stdout.write(self.style.SUCCESS("Successfully loaded dummy data"))
