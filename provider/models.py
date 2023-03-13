"""Models of provider app."""
from django.db import models


class Provider(models.Model):
    """
    Model of provider, includes name, foundation year, status (active or not).
    """

    name = models.CharField(max_length=100, verbose_name="Naming")
    foundation_year = models.IntegerField(verbose_name="Year of foundation")
    is_active = models.BooleanField(verbose_name="Is active")

    def __str__(self):
        result = f"{self.name} | {self.foundation_year} | "
        if self.is_active is False:
            result += "Inactive"
        else:
            result += "Active"
        return result
        
        
class CarsInProviderStock(models.Model):
    """
    Model of availability cars in providers stock, includes provider referenced to Provider model,
    car referenced to Car model from Car app, price of each vehicle.
    """

    provider = models.ForeignKey(
        Provider, on_delete=models.CASCADE, verbose_name="Dealership"
    )
    car = models.ForeignKey("car.Car", on_delete=models.CASCADE, verbose_name="Car")
    price = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="Car price"
    )

    def __str__(self):
        return f"Provider {self.provider.name} has {self.car}. Price: {self.price}"
