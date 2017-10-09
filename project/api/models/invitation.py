"""
Handles beta/website access invitations
"""
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import formats

class InvitationManager(models.Manager):
    """
    Custom query set manager for the Invitation model
    """
    def filter_by_host(self, host_user=None):
        """
        Gets the queryset of invited persons by the host user or all if not specified
        """

        # Get invitations queryset from parent class
        invitations = super(InvitationManager, self).get_queryset()

        if host_user:
            invitees = invitations.filter(host_user=host_user)
        else:
            invitees = invitations

        return invitees

    def get_registered_invitees(self, host_user=None):
        """
        Gets the queryset of registered invited persons by the host user or all if not specified
        """

        # Get invitations queryset from parent class
        invitations = super(InvitationManager, self).get_queryset()

        if host_user:
            invitees = invitations.filter(host_user=host_user, registered=True)
        else:
            invitees = invitations.filter(registered=True)

        return invitees


class Invitation(models.Model):
    """
    Keeps track of invitations and registration status of invitees
    """

    objects = InvitationManager()

    host_user = models.ForeignKey(User, default=None, null=True, related_name="hosts")
    invitee_email = models.EmailField(default=None, null=False)
    verification_code = models.CharField(max_length=31, null=False)
    invitee_user = models.ForeignKey(User, default=None, null=True, related_name="invitees")

    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    #TODO: Invitation type
    #TODO: Invitation limit

    def _get_date_registered(self):
        if self.invitee_user:
            # user_instance = User.objects.get(self.invitee_user)
            return self.invitee_user.date_joined
        else:
            return None

    date_registered = property(_get_date_registered)

    def summarize(self):
        data = {
            'email': self.invitee_email,
            'username': '',
            'date_registered': '',
            'date_invited': str(self.date_created),
            'date_recent_activity': '',
        }

        if self.invitee_user:
            data['status'] = 'registered'
            data['username'] = self.invitee_user.username
            data['date_registered'] = str(self.date_registered)
        else:
            data['status'] = 'sent'

        return data
