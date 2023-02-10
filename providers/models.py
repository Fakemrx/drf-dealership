from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Provider(models.Model):
    '''
    Модель поставщика, содержит название компании, год основания.
    '''
    name = models.CharField(max_length=100, verbose_name='Naming')
    foundation_year = models.IntegerField(verbose_name='Year of foundation')
    is_active = models.BooleanField(verbose_name='Is active')


class ProviderDiscounts(models.Model):
    '''
    Модель акций поставщиков, содержит в себе поставщика, который проводит акцию, скидку в процентах, автомобили,
    на которые распространяется скидка и период проведения акции.
    '''
    PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, verbose_name='Provider')
    car = models.ForeignKey('cars.Car', on_delete=models.CASCADE, verbose_name='Car')
    discount_dates = models.DurationField(verbose_name='Dates of promotion')
    discount = models.DecimalField(max_digits=3, decimal_places=0, validators=PERCENTAGE_VALIDATOR)
    name = models.CharField(max_length=100, verbose_name='Promotion naming')
    discription = models.CharField(max_length=1000, verbose_name='Promotion discription')


class ProviderBuyers(models.Model):
    '''
    Модель покупателей поставщиков, содержит автосалон, в котором покупался автомобиль, сам автомобиль, его количество,
    дату продажи и покупателя.
    '''
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, verbose_name='Provider')
    dealership = models.ForeignKey('car_dealership.CarDealership', on_delete=models.CASCADE, verbose_name='Dealership')
    car = models.ForeignKey('cars.Car', on_delete=models.CASCADE, verbose_name='Car')
    quantity = models.IntegerField(verbose_name='Quantity of cars')
    total_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Total price')
    sell_date = models.DateTimeField(auto_now=True, verbose_name='Date of sale')


class CarsInProviderStock(models.Model):
    '''
    Модель наличия автомобилей у поставщика, содержит информацию о поставщике,
    автомобиле и цене.
    '''
    provider = models.ForeignKey('car_dealership.CarDealership', on_delete=models.CASCADE, verbose_name='Dealership')
    car = models.ForeignKey('cars.Car', on_delete=models.CASCADE, verbose_name='Car')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Car price')
