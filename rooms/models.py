from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField
from core import models as core_models
from users import models as user_models

class CommonInfo(core_models.TimeStampedModel):
    name = models.CharField(max_length=80)
    class Meta: abstract = True
    def __str__(self): return self.name

class RoomType(CommonInfo):
    class Meta: verbose_name = "Room Type"; ordering = ["name"]

class Amenity(CommonInfo):
    class Meta: verbose_name_plural = "Amenities"

class Facility(CommonInfo):
    class Meta: verbose_name_plural = "Facilities"

class HouseRule(CommonInfo):
    class Meta: verbose_name = "House Rule"

class Photo(core_models.TimeStampedModel):
    caption = models.CharField(max_length=250, null=True)
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)
    def __str__(self): return self.caption

class Room(core_models.TimeStampedModel):
    name = models.CharField(max_length=60)
    description = models.TextField()
    price = models.IntegerField()
    address = models.CharField(max_length=150)
    country = CountryField()
    city = models.CharField(max_length=80)
    guests = models.IntegerField(help_text="How many people will be staying?")
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_booking = models.BooleanField(default=False)
    host = models.ForeignKey(user_models.User, related_name="rooms", on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, related_name="rooms", blank=True, on_delete=models.SET_NULL, null=True)
    amenities = models.ManyToManyField(Amenity, related_name="rooms", blank=True)
    facilities = models.ManyToManyField(Facility, related_name="rooms", blank=True)
    house_rules = models.ManyToManyField(HouseRule, related_name="rooms", blank=True)

    def __str__(self): return self.name
    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)
    def get_absolute_url(self): return reverse("rooms:detail", kwargs={"pk": self.pk})
    def total_ratings(self):
        all_reviews = self.reviews.all()
        if not all_reviews: return 0
        avg = sum([r.rating_average() for r in all_reviews]) / len(all_reviews)
        return round(avg, 2)
    def first_photo(self):
        photos = self.photos.all()
        return photos[0].file.url if photos else None