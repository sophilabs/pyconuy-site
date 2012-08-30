import datetime
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from symposion.speakers.models import Speaker
from symposion.proposals.models import Proposal
from django.template import RequestContext
from symposion.sponsors_pro.models import Sponsor
from symposion.proposals.models import PresentationCategory
from main.forms import SpeakerForm, ProposalForm

def index(request):
    return render_to_response('index.html',
    {
        'sponsor_list':Sponsor.objects.order_by('level'),
    }, context_instance=RequestContext(request))

def about(request):
    return render_to_response('about.html', context_instance=RequestContext(request))

@login_required
def proposal_add(request):
    if request.method == 'POST': # If the form has been submitted...
        form_proposal = ProposalForm(request.POST) # A form bound to the POST data
        form_speaker = SpeakerForm(request.POST)
        try:
            Speaker.objects.get(user=request.user)
            speaker = Speaker.objects.get(user=request.user)
        except Speaker.DoesNotExist:
            if form_speaker.is_valid():
                    speaker = Speaker.objects.create(
                        user=request.user,
                        name='{0} {1}'.format(request.user.first_name, request.user.last_name),
                        biography=form_speaker.cleaned_data['biography'],
                        annotation=form_speaker.cleaned_data['annotation'],
                        invite_email=request.user.email,
                        invite_token="")
            else:
                return render_to_response('proposal_add.html', {
                    'form_proposal':form_proposal, 'form_speaker':form_speaker
                }, context_instance=RequestContext(request))

        if form_proposal.is_valid():
            Proposal.objects.create(
                title=form_proposal.cleaned_data['title'],
                description=form_proposal.cleaned_data['description'],
                kind=form_proposal.cleaned_data['kind'],
                category=PresentationCategory.objects.get(slug='general'),
                abstract=form_proposal.cleaned_data['abstract'],
                audience_level=form_proposal.cleaned_data['audience_level'],
                additional_notes=form_proposal.cleaned_data['additional_notes'],
                duration=form_proposal.cleaned_data['duration'],
                speaker=speaker,
                submitted=datetime.datetime.now(),
                cancelled=False)
            return HttpResponseRedirect('/proposal_sent') # Redirect after POST
    else:
        try:
            Speaker.objects.get(user=request.user)
            form_speaker = ""
        except Speaker.DoesNotExist:
            form_speaker = SpeakerForm()
        form_proposal = ProposalForm()

    return render_to_response('proposal_add.html', {
        'form_proposal':form_proposal, 'form_speaker':form_speaker
        }, context_instance=RequestContext(request))

def proposal_info(request):
    return render_to_response('proposal_info.html', context_instance=RequestContext(request))

def proposal_sent(request):
    return render_to_response('proposal_sent.html', context_instance=RequestContext(request))

def schedule(request):
    return render_to_response('schedule.html', context_instance=RequestContext(request))
