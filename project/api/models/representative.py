from datetime import datetime
from django.db import models

from core.constants import US_STATES


class RepresentativeManager(models.Manager):
    def create_or_update_from_response(self, response):
        start_date = datetime.strptime(response['start_date'], "%Y-%M-%d")
        end_date = datetime.strptime(response['end_date'], "%Y-%M-%d")
        rep_instance, created = self.get_or_create(bioguide_id=response['bioguide_id'])
        rep_instance.name = response['name']
        rep_instance.district = response['district']
        rep_instance.state = response['state']
        rep_instance.chamber = response['chamber'].lower()
        rep_instance.start_date = start_date
        rep_instance.end_date = end_date
        rep_instance.party = response['party']
        rep_instance.save()
        return rep_instance, created


class Representative(models.Model):
    CHAMBER_CHOICES = [
        ('house', 'House'),
        ('senate', 'Senate')
    ]

    name = models.CharField(max_length=63, blank=False)

    district = models.CharField(max_length=63, blank=True, null=True)
    state = models.CharField(max_length=63)

    chamber = models.CharField(choices=CHAMBER_CHOICES, max_length=200)

    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    party = models.CharField(max_length=127)

    bioguide_id = models.CharField(max_length=10, unique=True)

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    objects = RepresentativeManager()

    def __str__(self):
        return "Rep - {}".format(self.name)

    def summarize(self, account=None):
        from .vote import Vote

        data = {
            "bioguide_id": self.bioguide_id,
            "name": self.name,
            "party": self.party,
            "state": '{state}'.format(state=dict(US_STATES).get(self.state, self.state)),
            "profile_image": "https://theunitedstates.io/images/congress/225x275/{}.jpg".format(self.bioguide_id)
        }
        if account:
            votes = {}
            bills = account.get_voted_bills(serialize=False)
            voted_same_count = Vote.objects.filter(
                bill__in=bills["supported_bills"], representative=self, vote="yes"
            ).count()
            voted_same_count += Vote.objects.filter(
                bill__in=bills["opposed_bills"], representative=self, vote="no"
            ).count()

            voted_different_count = Vote.objects.filter(
                bill__in=bills["supported_bills"], representative=self, vote="no"
            ).count()
            voted_different_count += Vote.objects.filter(
                bill__in=bills["opposed_bills"], representative=self, vote="yes"
            ).count()

            votes["voted_same"] = voted_same_count
            votes["voted_different"] = voted_different_count
            voted_total = float(voted_same_count + voted_different_count)
            votes["compatibility_score"] = voted_same_count / voted_total if voted_total else 0
            votes["compatibility_percentage"] = votes["compatibility_score"] * 100

            data["votes"] = votes

        return data
