from django.contrib import admin
from .models import Booking, NowPlaying, Play


class PlayAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'image',
    )

    ordering = (
        'name',
    )


class NowPlayingAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'play',
        'status',
        'seats',
    )

    ordering = (
        '-date',
    )


class BookingAdmin(admin.ModelAdmin):
    readonly_fields = ('play', 'date')

    fields = ('user_profile', 'amount', 'name', 'email')

    list_display = (
        'user_profile',
        'play',
        'date',
        'amount',
        'name',
        'email',
    )

    ordering = ('play',)


admin.site.register(Play, PlayAdmin)
admin.site.register(NowPlaying, NowPlayingAdmin)
admin.site.register(Booking, BookingAdmin)