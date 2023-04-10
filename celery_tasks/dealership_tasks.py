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
        cars_list = set()
        if dealership.preferred_cars_list.all():
            cars_list = set(dealership.preferred_cars_list.all())
        cars_list.update(search_suitable_cars(dealership))
        car_prices = search_minimal_price(dealership, cars_list)
        if car_prices:
            balance_per_car = round(dealership.balance / len(car_prices), 2)
            buy_preferred_cars(car_prices, balance_per_car, dealership)


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


def buy_preferred_cars(car_prices, balance_per_car, dealer):
    """
    Buy cars for exact dealer, according to the best car prices
    and balance per car.
    """

    for car, price_and_provider in car_prices.items():
        for quantity in range(5, 0, -1):
            # Try to buy 5 cars, if a dealer does not have enough money
            # (balance_per_car) to buy 5 of them, the quantity will be reduced
            # by 1 and will do that until 2 cases: dealer will buy *quantity*
            # cars or *quantity* will be reduced up to 0.
            success = data_entries(
                dealer, price_and_provider, quantity, car, balance_per_car
            )
            if success:
                break


def data_entries(dealer, price_and_provider, quantity, car, balance_per_car):
    """
    Rewrites dealer balance after cars were bought, rewrites quantity of bought
    cars in model for personal discounts, creates an entry in ProviderSales.
    """
    from provider.models import ProviderPersonalDiscounts, ProviderSales
    from dealership.models import CarsInDealershipStock

    price = price_and_provider[0]
    cur_provider = price_and_provider[1]
    if price * quantity > balance_per_car:
        return False

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
    dealer.balance -= price * quantity
    dealer.save()
    prov_pers_disc, created = ProviderPersonalDiscounts.objects.get_or_create(
        provider=cur_provider,
        dealership=dealer,
        defaults={"actual_discount": 0, "quantity_of_bought_cars": quantity},
    )
    if not created:
        prov_pers_disc.quantity_of_bought_cars += quantity
        prov_pers_disc.save()
    ProviderSales.objects.create(
        provider=cur_provider,
        dealership=dealer,
        car=car,
        quantity=quantity,
        total_price=price * quantity,
    )
    return True


def search_minimal_price(dealership, preferred_cars_list):
    """Find minimal car prices from a transmitted dealership."""
    from provider.models import CarsInProviderStock, ProviderDiscounts

    car_prices = {}
    for car in preferred_cars_list:
        for provider_stock in CarsInProviderStock.objects.filter(car=car):
            personal_discount = get_personal_discount(
                provider_stock.provider, dealership
            )
            car_discount = ProviderDiscounts.objects.filter(
                provider=provider_stock.provider, car__car=car
            )
            price_mult = Decimal((100 - personal_discount) / 100)
            if car_discount.exists():
                price = round(car_discount.price_during_discount * price_mult, 2)
            else:
                price = round(provider_stock.price * price_mult, 2)
            if (
                provider_stock.car not in car_prices.keys()
                or price < car_prices[car][0]
            ):
                car_prices[car] = (price, provider_stock.provider)
    return car_prices


def get_personal_discount(provider, dealership):
    """Find if there are any personal discounts for a current dealership."""
    from provider.models import ProviderPersonalDiscounts

    personal_discount = ProviderPersonalDiscounts.objects.filter(
        dealership=dealership, provider=provider
    )
    if personal_discount.exists():
        return personal_discount.first().actual_discount
    return 0
