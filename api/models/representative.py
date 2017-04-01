from django.db import models
from account import Account

class RepresentativeManager(models.Manager):
    def summarize(self, representative):
        a = Account.objects.get(user=representative.account)
        data = {
            "first_name": a.first_name,
            "last_name": a.last_name,
            "about_me": a.about_me,
            "location": a.get_location(),
            "history": [Civi.objects.serialize(c) for c in Civi.objects.filter(author_id=account.id).order_by('-created')],
            "profile_image": "https://theunitedstates.io/images/congress/225x275/{bioguide_id}.jpg".format(bioguide_id=representative.bioguideID),
            "followers": self.followers(a),
            "following": self.following(a),
        }
        return data

class Representative(models.Model):
    account = models.ForeignKey(Account, default=None, null=True)

    first_name = models.CharField(max_length=63, blank=False)
    last_name = models.CharField(max_length=63, blank=False)
    about_me = models.CharField(max_length=511, blank=True)

    district = models.CharField(max_length=63, blank=True, null=True)
    senate_class = models.CharField(max_length=63, blank=True, null=True) # junior or senior for senator
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
