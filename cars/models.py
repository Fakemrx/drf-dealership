from django.db import models


class Car(models.Model):
    '''
    Модель автомобиля, содержит поля выбора по конкретным категориям отдельных
    частей автомобиля, а также основные характеристики.
    '''
    TYPE_CHOICES = ('SUV', 'Sedan 4-d', 'Coupe 2-d', 'Sportcar', 'Hypercar',
                    'Mini-van', 'Van', 'Truck', 'Wagon', 'Musclecar'
                    )
    TANK_CHOICES = ('Gasoline', 'Diesel', 'Hybrid', 'Electrocar')
    GEARBOX_CHOICES = ('Manual', 'Automatic', 'Robotic', 'Variable', 'Sequental',)
    DRIVETRAIN_CHOICES = ('AWD', 'FWD', 'RWD', '4WD')
    ENGINE_CHOICES = ('I3', 'I4', 'I5', 'I6', 'V6', 'V8', 'V10', 'V12', 'W10', 'W12', 'E')

    brand = models.CharField(max_length=30, verbose_name='Car brand')
    model = models.CharField(max_length=50, verbose_name='Car model')
    release_year = models.IntegerField(verbose_name='Release year')

    car_type = models.CharField(CHOICES=TYPE_CHOICES, verbose_name='Car type')
    fuel_type = models.CharField(CHOICES=TANK_CHOICES, verbose_name='Fuel type')
    gearbox_type = models.CharField(CHOICES=GEARBOX_CHOICES, verbose_name='Gearbox type')
    drivetrain_type = models.CharField(CHOICES=DRIVETRAIN_CHOICES, verbose_name='Drivetrain type')
    engine_type = models.CharField(CHOICES=ENGINE_CHOICES, verbose_name='Engine type')

    engine_volume = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Engine volume')
    hp = models.IntegerField(null=True, blank=True, verbose_name='Engine horse powers')
    torque = models.IntegerField(null=True, blank=True, verbose_name='Engine torque')
    seat_places = models.IntegerField(null=True, blank=True, verbose_name='Seat places')
    is_active = models.BooleanField(verbose_name='Is active')
