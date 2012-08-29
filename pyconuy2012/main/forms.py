from django import forms
from symposion.proposals.models import PresentationCategory, PresentationKind, Proposal
from symposion.speakers.models import Speaker
from bootstrap.forms import BootstrapForm
from django.utils.translation import ugettext_lazy as _

class SpeakerForm(BootstrapForm):

    biography = forms.CharField(widget=forms.Textarea)
    annotation = forms.CharField(widget=forms.Textarea)

class ProposalForm(BootstrapForm):

    title = forms.CharField(max_length=100,
        help_text=_(''))
    abstract = forms.CharField(widget=forms.Textarea,
        help_text=_(''))
    description = forms.CharField(widget=forms.Textarea,
        help_text=_(''))
    kind = forms.ModelChoiceField(PresentationKind.objects.all().order_by('name'),
        help_text=_(''))
    duration = forms.ChoiceField(choices=Proposal.DURATION_CHOICES,
        help_text=_(''))
    audience_level = forms.ChoiceField(choices=Proposal.AUDIENCE_LEVELS,
        help_text=_(''))
    additional_notes = forms.CharField(widget=forms.Textarea(), required=False,
        help_text=_(''))