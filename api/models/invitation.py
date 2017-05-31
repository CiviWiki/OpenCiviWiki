"""
Handles beta/website access invitations
"""
from django.db import models
from django.contrib.auth.models import User

class InvitationManager(models.Manager):
    """
    Custom query set manager for the Invitation model
    """
    def get_invitees(self, host_user=None):
        """
        Gets the queryset of invited persons by the host user or all if not specified
        """
        invitation_qs = super(InvitationManager, self).get_queryset()
        if host_user:
            invitees = invitation_qs.filter(host=host_user)
        else:
            invitees = invitation_qs
        return invitees

    def get_registered_invitees(self, host_user=None):
        """
        Gets the queryset of registered invited persons by the host user or all if not specified
        """
        invitation_qs = super(InvitationManager, self).get_queryset()
        if host_user:
            invitees = invitation_qs.filter(host_user=host_user, registered=True)
        else:
            invitees = invitation_qs.filter(registered=True)
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
    #TODO: Invitation type
    #TODO: Invitation limit

    def _get_date_registered(self):
        if self.invitee_user:
            user_instance = User.objects.get(self.invitee_user)
            return user_instance.date_joined
        else:
            return None
    date_registered = property(_get_date_registered)

    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def summarize(self):
        data = {
            'email': self.invitee_email,
            'username': '',
            'date_registered': ''
        }

        if self.invitee_user:
            data['username'] = User.objects.get(self.invitee_user).username
            data['date_registered'] =  self.date_registered

        return data
