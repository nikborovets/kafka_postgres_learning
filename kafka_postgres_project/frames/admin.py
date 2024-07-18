from django.contrib import admin
from .models import Frame

class FrameAdmin(admin.ModelAdmin):
    list_display = ('frame_id', 'get_formatted_timestamp')

    def get_formatted_timestamp(self, obj):
        return obj.get_formatted_timestamp()
    get_formatted_timestamp.short_description = 'Timestamp'

admin.site.register(Frame, FrameAdmin)
