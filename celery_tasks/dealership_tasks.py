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

    for dealership in CarDealership.objects.all():  # Running through all dealerships
        if dealership.preferred_cars_list.all():
            # Checking if dealership has list of preferred cars
            car_prices = search_minimal_price(dealership)
            balance_per_car = round(dealership.balance / len(car_prices.keys()), 2)
            # Dividing the balance into equal parts to spend it a bit later
            buy_preferred_cars(car_prices, balance_per_car, dealership)
        else:
            # There will be full scenario for searching suitable cars
            # according to dealership's specs of a car/engine, will
            # be added in next commits
            pass


def buy_preferred_cars(car_prices, balance_per_car, dealer):
    """Buy cars for exact dealer, according to the best car prices
    and balance per car."""
    from dealership.models import CarsInDealershipStock

    for car, price in car_prices.items():
        # Looking for every pair of car instance and it's minimal price
        for quantity in range(5, 0, -1):
            # Trying to buy from 5 to 1 cars (it's made in reverse because it's
            # necessary to buy as many cars as we can)
            if price * quantity <= balance_per_car:
                # Checking if we can buy such a quantity of cars according to
                # minimal price
                try:
                    # Trying to get such an entry in a table
                    dealer_stock = CarsInDealershipStock.objects.get(
                        dealership=dealer, car=car
                    )
                    dealer_stock.quantity = dealer_stock.quantity + quantity
                    dealer_stock.save()
                    # Updating and saving dealer's quantity of a car
                except CarsInDealershipStock.DoesNotExist:
                    # Except a scenario if there is no entries in a table about
                    # this car
                    CarsInDealershipStock.objects.create(
                        dealership=dealer,
                        car=car,
                        quantity=quantity,
                        price=round(price * Decimal(1.1), 2),
                    )
                    # Adding a car to the dealer's stock
                dealer.balance = dealer.balance - price * quantity
                dealer.save()
                # Updating and saving dealer's balance
                break
                # Ending for operation to go to the next car


def search_minimal_price(dealership):
    """Find minimal car prices from a transmitted dealership."""
    from provider.models import CarsInProviderStock, ProviderDiscounts

    car_prices = {}  # Adding dict to view minimal price for each car
    for car in dealership.preferred_cars_list.all():
        # Running through every car in list
        for provider_stock in CarsInProviderStock.objects.filter(car=car):
            # Running through every provider's stock filtering by searchable car
            try:  # Trying to get discounts if they does exist
                car_discount = ProviderDiscounts.objects.get(
                    provider=provider_stock.provider, car__car=car
                )
                if (
                    provider_stock.car not in car_prices.keys()
                    or car_discount.price_during_discount < car_prices[car]
                ):
                    # Checking if there is no data about this car in dict or
                    # if it's price in a current provider less than in previous
                    car_prices[car] = provider_stock.price
            except ProviderDiscounts.DoesNotExist:
                # Except a scenario if there is no discounts for a current car in
                # a current provider's stock
                if (
                    provider_stock.car not in car_prices.keys()
                    or provider_stock.price < car_prices[car]
                ):
                    # Checking if there is no data about this car in dict or
                    # if it's price in a current provider less than in previous
                    car_prices[car] = provider_stock.price
    return car_prices
