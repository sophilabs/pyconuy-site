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
from main.forms import ProposalForm

def index(request):

    return render_to_response('index.html',
    {
        'sponsor_list':Sponsor.objects.order_by('level'),
    }, context_instance=RequestContext(request))


@login_required
def proposal_add(request):

    try:
        speaker = Speaker.objects.get(user=request.user)
    except Speaker.DoesNotExist:
        if request.user.first_name or request.user.last_name:
            name = u'{0} {1}'.format(request.user.first_name, request.user.last_name)
        else:
            name = request.user.username
        speaker = Speaker(user=request.user,
            name = name,
            invite_email = request.user.email,
            invite_token = '')

    if request.method == 'POST':
        form = ProposalForm(request.POST)

        if form.is_valid():

            #save speaker
            speaker.biography = form.cleaned_data['biography']
            speaker.annotation = speaker.annotation or ''
            speaker.save()

            #save proposal
            Proposal.objects.create(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                kind=form.cleaned_data['kind'],
                category=PresentationCategory.objects.get(slug='general'),
                abstract=form.cleaned_data['abstract'],
                audience_level=form.cleaned_data['audience_level'],
                additional_notes=form.cleaned_data['additional_notes'],
                duration=form.cleaned_data['duration'],
                speaker=speaker,
                submitted=datetime.datetime.now(),
                cancelled=False)

            return HttpResponseRedirect('/proposal-sent')
    else:
        form = ProposalForm()

    return render_to_response('proposal_add.html', {
        'form': form,
        }, context_instance=RequestContext(request))

def proposal_sent(request):
    return render_to_response('proposal_sent.html', context_instance=RequestContext(request))

def schedule(request):
    return render_to_response('schedule.html', context_instance=RequestContext(request))
