from django.db import models


class Buyer(models.Model):
    '''
    Модель покупателя, содержит в себе ФИО покупателя, баланс.
    '''
    GENDER_CHOICES = ('Men', 'Women')
    full_name = models.CharField(max_length=100, verbose_name='Full name')
    age = models.IntegerField(verbose_name='Age')
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES, verbose_name='Gender')
    balance = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Buyer's balance")
    is_active = models.BooleanField(verbose_name='Is active')


class Offer(models.Model):
    '''
    Модель запроса на покупку, содержит в себе покупателя, максимальную цену покупки, автомобиль и их количество.
    '''
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, verbose_name='Buyer')
    car = models.ForeignKey('cars.Car', on_delete=models.CASCADE, verbose_name='Car')
    max_cost = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Maximum cost')
    quantity = models.IntegerField(verbose_name='Quantity of cars')
