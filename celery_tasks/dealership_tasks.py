"""Main tasks of all project."""
from decimal import Decimal

from celery import shared_task
from celery.utils.log import get_task_logger

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
        if dealership.preferred_cars_list.all():
            car_prices = search_minimal_price(
                dealership, dealership.preferred_cars_list.all()
            )
        else:
            cars_list = search_suitable_cars(dealership)
            car_prices = search_minimal_price(dealership, cars_list)
        if car_prices:
            balance_per_car = round(dealership.balance / len(car_prices), 2)
            if buy_preferred_cars(car_prices, balance_per_car, dealership) == 0:
                buy_preferred_cars(car_prices, dealership.balance, dealership)


def search_suitable_cars(dealership):
    """Search suitable cars according to car specs."""
    from car.models import Car

    cars_suitable_by_specs = []
    num_of_specs = 0
    if dealership.preferred_car_release_year_from:
        num_of_specs += 1
        for car in Car.objects.filter(
            release_year__gte=dealership.preferred_car_release_year_from
        ):
            cars_suitable_by_specs.append(car)
    if dealership.preferred_car_release_year_to:
        num_of_specs += 1
        for car in Car.objects.filter(
            release_year__lte=dealership.preferred_car_release_year_to
        ):
            cars_suitable_by_specs.append(car)
    if dealership.preferred_car_type:
        num_of_specs += 1
        for car in Car.objects.filter(car_type=dealership.preferred_car_type):
            cars_suitable_by_specs.append(car)
    if dealership.preferred_fuel_type:
        num_of_specs += 1
        for car in Car.objects.filter(engine__fuel_type=dealership.preferred_fuel_type):
            cars_suitable_by_specs.append(car)
    suitable_cars = suitable_cars_list_filter(cars_suitable_by_specs, num_of_specs)
    return suitable_cars


def suitable_cars_list_filter(
    cars_suitable_by_specs,
    num_of_specs,
):
    """
    Filters only cars that match final search.
    Function looks at quantity of exact car in cars_suitable_by_specs and
    compares it to the num_of_specs, if it equals - the car matches all
    the specified parameters, if it's quantity lower than needed - this car
    does not suit our "filters" and will not be added to the final list.
    Args:
    cars_suitable_by_specs - list of filtered cars
    num_of_specs - total quantity of specs
    """
    suitable_cars = []
    for car in cars_suitable_by_specs:
        if (
            cars_suitable_by_specs.count(car) == num_of_specs
            and car not in suitable_cars
        ):
            suitable_cars.append(car)
    return suitable_cars


def buy_preferred_cars(car_prices, balance_per_car, dealer):
    """
    Buy cars for exact dealer, according to the best car prices
    and balance per car.
    """

    cars_bought = 0
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
                cars_bought += quantity
                break
    return cars_bought


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
