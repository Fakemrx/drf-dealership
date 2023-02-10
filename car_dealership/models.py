from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class CarDealership(models.Model):
    '''
    Модель автосалона, содержит его название, баланс и локацию.
    '''
    name = models.CharField(max_length=100, verbose_name='Naming')
    # location = models.?
    balance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Car dealerhip's balance")
    is_active = models.BooleanField(verbose_name='Is active')


class CarDealershipDiscounts(models.Model):
    '''
    Модель акций автосалонов, содержит в себе автосалон, который проводит акцию, скидку в процентах, автомобили,
    на которые распространяется скидка и период проведения акции.
    '''
    PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]
    dealership = models.ForeignKey(CarDealership, on_delete=models.CASCADE, verbose_name='Dealership')
    car = models.ForeignKey('cars.Car', on_delete=models.CASCADE, verbose_name='Car')
    discount_dates = models.DurationField(verbose_name='Dates of promotion')
    discount = models.DecimalField(max_digits=3, decimal_places=0, validators=PERCENTAGE_VALIDATOR)
    name = models.CharField(max_length=100, verbose_name='Promotion naming')
    description = models.CharField(max_length=1000, verbose_name='Promotion description')


class DealershipBuyers(models.Model):
    '''
    Модель покупателей автосалонов, содержит автосалон, в котором покупался автомобиль, сам автомобиль, его количество,
    дату продажи, итоговую стоимость и покупателя.
    '''
    dealership = models.ForeignKey(CarDealership, on_delete=models.CASCADE, verbose_name='Dealership')
    buyer = models.ForeignKey('buyer.Buyer', on_delete=models.CASCADE, verbose_name='Buyer')
    car = models.ForeignKey('cars.Car', on_delete=models.CASCADE, verbose_name='Car')
    quantity = models.IntegerField(verbose_name='Quantity of cars')
    total_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Total price')
    sell_date = models.DateTimeField(auto_now=True, verbose_name='Date of sale')


class CarsInDealershipStock(models.Model):
    '''
    Модель наличия автомобилей у автосалона, содержит информацию о дилере,
    автомобиле, стоимости 1 шт. и его количестве "на складе" салона.
    '''
    dealership = models.ForeignKey(CarDealership, on_delete=models.CASCADE, verbose_name='Dealership')
    car = models.ForeignKey('cars.Car', on_delete=models.CASCADE, verbose_name='Car')
    quantity = models.IntegerField(verbose_name='Quantity of cars')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Car price')


class PreferredCars(models.Model):
    '''
    Модель предпочитаемых для автосалона автомобилей, содержит поля выбора по конкретным категориям (CHOICES) отдельных
    характеристик автомобиля, можно задать минимальные и максимальные пороги характеристик авто для фильтрации,
    можно сослаться на конкретный бренд, конкретную модель бренда и на год выпуска автомобиля.
    '''
    TYPE_CHOICES = (
        'SUV',
        'Sedan 4-d',
        'Coupe 2-d',
        'Sportcar',
        'Hypercar',
        'Mini-van',
        'Van',
        'Truck',
        'Wagon',
        'Muscle'
    )
    TANK_CHOICES = (
        'Gasoline',
        'Diesel',
        'Hybrid',
        'Electrocar'
    )
    GEARBOX_CHOICES = (
        'Manual',
        'Automatic',
        'Robotic',
        'Variable',
        'Sequental',
    )
    DRIVETRAIN_CHOICES = (
        'AWD',
        'FWD',
        'RWD',
        '4WD',
    )
    ENGINE_CHOICES = (
        'I3',
        'I4',
        'I5',
        'I6',
        'V6',
        'V8',
        'V10',
        'V12',
        'W10',
        'W12',
        'E',
    )

    dealership = models.ForeignKey(CarDealership, on_delete=models.SET_NULL, verbose_name='Dealership')
    car_brand = models.ForeignKey('cars.Car', to_field='brand')
    car = models.ForeignKey('cars.Car', verbose_name='Certain car')
    car_release_year = models.IntegerField(verbose_name='Release year')

    car_type = models.CharField(null=True, blank=True, CHOICES=TYPE_CHOICES, verbose_name='Car type')
    fuel_type = models.CharField(null=True, blank=True, CHOICES=TANK_CHOICES, verbose_name='Fuel type')
    gearbox_type = models.CharField(null=True, blank=True, CHOICES=GEARBOX_CHOICES, verbose_name='Gearbox type')
    drivetrain_type = models.CharField(null=True, blank=True, CHOICES=DRIVETRAIN_CHOICES,
                                       verbose_name='Drivetrain type')
    engine_type = models.CharField(null=True, blank=True, CHOICES=ENGINE_CHOICES, verbose_name='Engine type')

    min_engine_volume = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Minimal engine volume')
    max_engine_volume = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Maximum engine volume')
    min_hp = models.IntegerField(null=True, blank=True, verbose_name='Minimal engine h.p.')
    max_hp = models.IntegerField(null=True, blank=True, verbose_name='Maximum engine h.p.')
    min_torque = models.IntegerField(null=True, blank=True, verbose_name='Minimal engine torque')
    max_torque = models.IntegerField(null=True, blank=True, verbose_name='Maximum engine torque')
    min_seat_places = models.IntegerField(null=True, blank=True, verbose_name='Minimal seat places')
    max_seat_places = models.IntegerField(null=True, blank=True, verbose_name='Maximum seat places')
