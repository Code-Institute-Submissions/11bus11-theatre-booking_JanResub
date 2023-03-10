from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import generic, View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Booking, NowPlaying, Play
from .forms import PlayForm, NowPlayingForm, BookingForm
from useraccount.models import UserProfile


def plays(request):
    """ See all plays available """
    plays = Play.objects.all()

    template = "booking/play_booking.html"
    context = {
        'plays': plays,
    }

    return render(request, template, context)

def play_dates(request, play_id):
    """ See what dates a play is showing """
    play_instance = get_object_or_404(Play, pk=play_id)
    showings = NowPlaying.objects.all()

    template = "booking/date_booking.html"

    context = {
        'play_instance': play_instance,
        'showings': showings,
    }

    return render(request, template, context)

def place_booking(request, nowplaying_id):
    """ Create a booking """
    viewing_instance = get_object_or_404(NowPlaying, pk=nowplaying_id)
    if request.method == 'POST':
        booking_form = BookingForm(request.POST)
        if booking_form.is_valid():
            booking = booking_form.save(commit=False)
            if request.user.is_authenticated:
                profile = UserProfile.objects.get(user=request.user)
                booking.user_profile = profile
            booking_form.save()
            return redirect(reverse('success'))
    else:
        booking_form = BookingForm(instance=viewing_instance)
    


    template = "booking/form_booking.html"
    context = {
        'viewing_instance': viewing_instance,
        'booking_form': booking_form
    }

    return render(request, template, context)


@login_required
def all_bookings(request):
    """ Show all bookings made (admin only) """
    if not request.user.is_superuser:
        return redirect(reverse('home'))
    
    bookings = Booking.objects.all()
    template = 'booking/all_bookings.html'

    context = {
        'bookings': bookings,
    }

    return render(request, template, context)


@login_required
def add_play(request):
    """ Add a play """
    if not request.user.is_superuser:
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = PlayForm(request.POST, request.FILES)
        if form.is_valid():
            play = form.save()
            return redirect(reverse('success'))
    else:
        form = PlayForm()

    template = 'booking/add_play.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_play(request, play_id):
    """ Edit a play"""
    play_instance = get_object_or_404(Play, pk=play_id)
    if not request.user.is_superuser:
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = PlayForm(request.POST, request.FILES, instance=play_instance)
        if form.is_valid():
            form.save()
            return redirect(reverse('success'))
    else:
        form = PlayForm(instance=play_instance)

    template = 'booking/edit_play.html'
    context = {
        'form': form,
        'play_instance': play_instance,
    }

    return render(request, template, context)


@login_required
def delete_play(request, play_id):
    """ Delete a play from the website """
    if not request.user.is_superuser:
        return redirect(reverse('plays'))

    play_instance = get_object_or_404(Play, pk=play_id)
    play_instance.delete()
    return redirect(reverse('success'))

