"""Main tasks of all project."""
from decimal import Decimal

from celery import shared_task
from celery.utils.log import get_task_logger
from django.db.models import Q

logger = get_task_logger(__name__)


@shared_task
def dealership_buys_preferred_cars():
    """
    Celery task, tries to find suitable cars for dealerships according to the
    car specs that was set in dealerships params. It tries to find providers
    according to exact car models/brands, if there is an empty setting it tries
    to find cars according to release year, car type, engine fuel type.
    """
    from dealership.models import CarDealership

    for dealership in CarDealership.objects.all():
        cars_list = set(dealership.preferred_cars_list.all())
        cars_list.update(search_suitable_cars(dealership))
        cars_prices_prov = search_minimal_price(dealership, cars_list)
        if cars_prices_prov:
            balance_per_car = round(dealership.balance / len(cars_prices_prov), 2)
            buy_preferred_cars(cars_prices_prov, balance_per_car, dealership)


def search_suitable_cars(dealership):
    """Search suitable cars according to car specs."""
    from car.models import Car

    query_conditions = Q()
    if dealership.preferred_car_release_year_from:
        query_conditions &= Q(
            release_year__gte=dealership.preferred_car_release_year_from
        )
    if dealership.preferred_car_release_year_to:
        query_conditions &= Q(
            release_year__lte=dealership.preferred_car_release_year_to
        )
    if dealership.preferred_car_type:
        query_conditions &= Q(car_type=dealership.preferred_car_type)
    if dealership.preferred_fuel_type:
        query_conditions &= Q(engine__fuel_type=dealership.preferred_fuel_type)
    suitable_cars = set(Car.objects.filter(query_conditions))
    return suitable_cars


def buy_preferred_cars(cars_prices_prov, balance_per_car, dealer):
    """
    Buy cars for exact dealer, according to the best car prices
    and balance per car.
    """
    actual_balance, cars_quantity_to_buy = calculate_buy_request(
        dealer, cars_prices_prov, balance_per_car
    )
    for car, price_and_provider in cars_prices_prov.items():
        if car in cars_quantity_to_buy.keys():
            data_entries(dealer, price_and_provider, cars_quantity_to_buy[car], car)
    dealer.balance = actual_balance
    dealer.save()


def calculate_buy_request(dealer, cars_prices_prov, balance_per_car):
    """
    Calculates possible buy request that tries to buy every car
    at least one time.
    """
    cars_quantity_to_buy = {}
    balance_left_free = dealer.balance
    total_quantity = 0
    while True:
        quantity_on_start = total_quantity
        not_bought_list = []
        for car, price_and_provider in cars_prices_prov.items():
            car_price = price_and_provider[0]
            if car_price <= balance_per_car and balance_left_free - car_price >= 0:
                balance_left_free -= car_price
                total_quantity += 1
                if car in cars_quantity_to_buy.keys():
                    cars_quantity_to_buy[car] += 1
                else:
                    cars_quantity_to_buy[car] = 1
            else:
                not_bought_list.append(car)
        if not_bought_list:
            for car in not_bought_list:
                if balance_left_free > cars_prices_prov[car][0]:
                    total_quantity += 1
                    cars_quantity_to_buy[car] = 1
                    balance_left_free -= cars_prices_prov[car][0]
        if quantity_on_start == total_quantity:
            break
    return balance_left_free, cars_quantity_to_buy


def data_entries(dealer, price_and_provider, quantity, car):
    """
    Rewrites dealer balance after cars were bought, rewrites quantity of bought
    cars in model for personal discounts, creates an entry in ProviderSales.
    """
    from provider.models import ProviderPersonalDiscounts, ProviderSales
    from dealership.models import CarsInDealershipStock

    dealer_stock, created = CarsInDealershipStock.objects.get_or_create(
        dealership=dealer,
        car=car,
        defaults={
            "quantity": quantity,
            "price": Decimal(0.00),
        },
    )
    if not created:
        dealer_stock.quantity += quantity
        dealer_stock.save()

    prov_pers_disc, created = ProviderPersonalDiscounts.objects.get_or_create(
        provider=price_and_provider[1],
        dealership=dealer,
        defaults={"actual_discount": 0, "quantity_of_bought_cars": quantity},
    )
    if not created:
        prov_pers_disc.quantity_of_bought_cars += quantity
        prov_pers_disc.save()

    ProviderSales.objects.create(
        provider=price_and_provider[1],
        dealership=dealer,
        car=car,
        quantity=quantity,
        total_price=price_and_provider[0] * quantity,
    )


def search_minimal_price(dealership, preferred_cars_list):
    """Find minimal car prices from a transmitted dealership."""
    from provider.models import CarsInProviderStock, ProviderDiscounts
    from provider.models import ProviderPersonalDiscounts

    cars_prices_prov = {}
    for car in preferred_cars_list:
        for provider_stock in CarsInProviderStock.objects.filter(car=car):
            personal_discount = 0
            discount = ProviderPersonalDiscounts.objects.filter(
                dealership=dealership, provider=provider_stock.provider
            )
            if discount.exists():
                personal_discount = discount.first().actual_discount
            car_discount = ProviderDiscounts.objects.filter(
                provider=provider_stock.provider, car__car=car
            )
            price_mult = Decimal((100 - personal_discount) / 100)
            if car_discount.exists():
                price = round(
                    car_discount.first().price_during_discount * price_mult, 2
                )
            else:
                price = round(provider_stock.price * price_mult, 2)
            if (
                provider_stock.car not in cars_prices_prov.keys()
                or price < cars_prices_prov[car][0]
            ):
                cars_prices_prov[car] = (price, provider_stock.provider)
    return cars_prices_prov
