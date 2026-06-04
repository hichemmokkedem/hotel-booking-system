from django.contrib import admin
from .models import Hotel, Room, Reservation

# Inline for managing rooms within hotel admin
class RoomInline(admin.TabularInline):
    model = Room
    extra = 1
    fields = ('room_number', 'room_type', 'price_per_night', 'capacity')

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'rating', 'room_count')
    list_filter = ('rating',)
    search_fields = ('name', 'address')
    inlines = [RoomInline]
    
    def room_count(self, obj):
        return obj.rooms.count()
    room_count.short_description = 'Number of Rooms'

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'hotel', 'room_type', 'price_per_night', 'capacity')
    list_filter = ('room_type', 'hotel')
    search_fields = ('room_number', 'hotel__name')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'room', 'check_in', 'check_out', 'status_badge', 'created_at')
    list_filter = ('check_in', 'check_out', 'created_at')
    search_fields = ('user__username', 'room__room_number', 'room__hotel__name')
    date_hierarchy = 'created_at'
    list_per_page = 20

    def status_badge(self, obj):
        from django.utils.html import format_html
        from datetime import date
        today = date.today()
        
        if obj.check_out < today:
            color = 'gray'
            status = 'Past'
        elif obj.check_in <= today <= obj.check_out:
            color = 'green'
            status = 'Active'
        else:
            color = 'blue'
            status = 'Future'
            
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 10px; font-size: 12px; font-weight: bold;">{}</span>',
            color,
            status
        )
    status_badge.short_description = 'Status'

