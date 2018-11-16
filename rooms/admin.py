from django.contrib    import admin
from django.utils.html import mark_safe

from .                 import models

@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "used_by",
    )

    def used_by(self, obj):
        return obj.rooms.count()

class PhotoInline(admin.TabularInline):

    model = models.Photo

@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    inlines = (PhotoInline,)
    fieldsets = (
        (
            "Basic info",
            {"fields": ("name", "description", "price", "country", "city", "address")}
        ),
        (
            "Times",
            {"fields":("check_in", "check_out", "instant_booking")}
        ),
        (
            "Spaces",
            {"fields":("guests", "beds", "bedrooms", "bathrooms")}
        ),
        (
            "More About the Space",
            {
                "classes": ("collapse",),
                "fields" : ("amenities", "facilities", "house_rules"),
            },
        ),
        (
            "Last Details",
            {"fields": ("host",)}
        ),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "bathrooms",
        "check_in",
        "check_out",
        "instant_booking",
        "count_amenities",
        "count_photos",
        "total_ratings",
    )

    list_filter = ("instant_booking",
                    "host__superhost",
                    'room_type',
                    'amenities',
                    'facilities',
                    'house_rules',
                    'city',
                    'country',)

    raw_id_fields = ("host",)

    search_fields = ("^city", "^host__username")

    filter_horizontal = ("amenities", "facilities", "house_rules")

    def count_amenities(self, obj):
        return obj.amenities.count()

    count_amenities.short_description = "Amenity Count"

    def count_photos(self, obj):
        return obj.photos.count()

    count_photos.short_description = "Photo Count"

@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="80px" src="{obj.file.url}" />')

    get_thumbnail.short_description = "Thumbnail"

