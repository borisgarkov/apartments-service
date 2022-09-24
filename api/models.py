from django.db import models


class Apartment(models.Model):
    id = models.CharField(primary_key=True, max_length=10)

    city = models.CharField(max_length=128)
    street = models.CharField(max_length=128)
    street_number = models.CharField(max_length=16)
    rooms = models.IntegerField()
    floor = models.IntegerField()
    area = models.IntegerField()
    rent = models.IntegerField()

    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)

    description = models.TextField()

    def serialize(self):
        return {
            "id": self.id,
            "street": self.street,
            "street_number": self.street_number,
            "city": self.city,
            "rent": self.rent,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "rooms": self.rooms,
            "area": self.area,
            "description": self.description
        }
