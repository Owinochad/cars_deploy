from django.contrib import admin
from .models import *

class CompetitionImageInline(admin.TabularInline):
    model = CompetitionImage
    extra = 1  # Number of extra forms to display for adding new images

class HoliCompetitionImageInline(admin.TabularInline):
    model = HoliCompetitionImage
    extra = 1  # Number of extra forms to display for adding new images

class CompetitionAdmin(admin.ModelAdmin):
    inlines = [CompetitionImageInline]
    list_display = ['car_model', 'index_display', 'priority', 'start_date', 'end_date']
    list_editable = ['index_display', 'priority']
    ordering = ['priority']

    def save_model(self, request, obj, form, change):
        if obj.index_display and obj.priority:
            # Enforce unique priority if index_display is set to True
            Competition.objects.filter(priority=obj.priority).exclude(id=obj.id).update(priority=None)
        elif not obj.index_display:
            obj.priority = None  # Reset priority if index_display is False
        super().save_model(request, obj, form, change)

class HoliCompetitionAdmin(admin.ModelAdmin):
    inlines = [HoliCompetitionImageInline]
    list_display = ['name', 'index_display', 'priority', 'start_date', 'end_date']
    list_editable = ['index_display', 'priority']
    ordering = ['priority']

    def save_model(self, request, obj, form, change):
        if obj.index_display and obj.priority:
            # Enforce unique priority if index_display is set to True
            HolidayCompetition.objects.filter(priority=obj.priority).exclude(id=obj.id).update(priority=None)
        elif not obj.index_display:
            obj.priority = None  # Reset priority if index_display is False
        super().save_model(request, obj, form, change)

# Register the admin classes
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(HolidayCompetition, HoliCompetitionAdmin)

# Register other models
admin.site.register(Entry)
admin.site.register(Winner)
admin.site.register(BasketItem)
admin.site.register(MpesaTransaction)
admin.site.register(Ticket)
admin.site.register(CompetitionImage)
admin.site.register(HoliCompetitionImage)
