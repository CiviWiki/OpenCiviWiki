from django.db import models
from django.conf import settings
from utils.constants import US_STATES

class RepresentativeManager(models.Manager):
    def get_reps():
        return

class Representative(models.Model):
    first_name = models.CharField(max_length=63, blank=False)
    last_name = models.CharField(max_length=63, blank=False)
    official_full_name = models.CharField(max_length=127, blank=True, null=True)
    about_me = models.CharField(max_length=511, blank=True)

    district = models.CharField(max_length=63, blank=True, null=True)
    
    # junior or senior for senator
    senate_class = models.CharField(max_length=63, blank=True, null=True)
    state = models.CharField(max_length=63)

    level_CHOICES = (
        ('federal', 'Federal'),
        ('state', 'State'),
    )
    level = models.CharField(max_length=31, default='federal', choices=level_CHOICES)

    term_start = models.DateField()
    term_end = models.DateField()

    party = models.CharField(max_length=127)

    bioguideID = models.CharField(max_length=7, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    objects = RepresentativeManager()

    def summarize(self):
        data = {
            "bioguide_id": self.bioguideID,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.official_full_name,
            "about_me": self.about_me,
            "party": self.party,
            "state": '{state}'.format(state=dict(US_STATES).get(self.state)),
            "profile_image": "https://theunitedstates.io/images/congress/225x275/{}.jpg".format(self.bioguideID)
        }
        return data
