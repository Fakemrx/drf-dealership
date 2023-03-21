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

    for dealership in CarDealership.objects.all():  # Goi through every dealership
        if (
            dealership.preferred_cars_list.all()
        ):  # Check if there is a list of preferred cars
            car_prices = search_minimal_price(
                dealership
            )  # Get dict {car: (price, provider)}
            balance_per_car = round(dealership.balance / len(car_prices), 2)
            # Divide balance into equal parts (balance divides according to quantity of found cars)
            if buy_preferred_cars(car_prices, balance_per_car, dealership) == 0:
                # Check is there possibility to buy several cars with such balance per car
                buy_preferred_cars(car_prices, dealership.balance, dealership)
                # Trying to buy several cars using full dealer's balance without dividing it
        else:
            # Logic to buy cars according to specs, not by exact list of preferred cars
            pass


def buy_preferred_cars(car_prices, balance_per_car, dealer):
    """
    Buy cars for exact dealer, according to the best car prices
    and balance per car.
    """
    from dealership.models import CarsInDealershipStock

    cars_bought = 0
    for car, price_and_provider in car_prices.items():
        # Go through every item in a dict {car: (price, provider)}
        price = price_and_provider[0]
        provider = price_and_provider[1]
        for quantity in range(5, 0, -1):  # Try to buy 5, 4, 3, 2, 1 cars
            if price * quantity <= balance_per_car:
                # Check if total price of N cars will be lower than balance per a car
                try:  # Try to get such a car in a dealer's stock
                    dealer_stock = CarsInDealershipStock.objects.get(
                        dealership=dealer, car=car
                    )
                    dealer_stock.quantity += quantity
                    dealer_stock.save()
                    # Add quantity of such a car if it's already exists
                except CarsInDealershipStock.DoesNotExist:
                    CarsInDealershipStock.objects.create(
                        dealership=dealer,
                        car=car,
                        quantity=quantity,
                        price=Decimal(0.00),
                    )
                    # Create new entry in a db about this car in a dealer's stock
                additional_data_entries(dealer, price, quantity, provider, car)
                # Add some more necessary entries into db
                cars_bought += quantity
                break
    return cars_bought


def additional_data_entries(dealer, price, quantity, provider, car):
    """
    Rewrites dealer balance after cars were bought, rewrites quantity of bought
    cars in model for personal discounts, creates an entry in ProviderSales.
    """
    from provider.models import ProviderPersonalDiscounts, ProviderSales

    dealer.balance -= price * quantity
    dealer.save()
    # Reduce a dealer's balance
    try:  # Try to update quantity of all-time bought cars in ProviderPersonalDiscounts
        provider_personal_discount = ProviderPersonalDiscounts.objects.get(
            provider=provider,
            dealership=dealer,
        )
        provider_personal_discount.quantity_of_bought_cars += quantity
        provider_personal_discount.save()
    except ProviderPersonalDiscounts.DoesNotExist:
        # Add new entry into a db about quantity of bought cars in ProviderPersonalDiscounts
        ProviderPersonalDiscounts.objects.create(
            provider=provider,
            dealership=dealer,
            actual_discount=0,
            quantity_of_bought_cars=quantity,
        )
    ProviderSales.objects.create(
        provider=provider,
        dealership=dealer,
        car=car,
        quantity=quantity,
        total_price=price * quantity,
    )
    # Add entry into a db about provider's sale


def search_minimal_price(dealership):
    """Find minimal car prices from a transmitted dealership."""
    from provider.models import CarsInProviderStock, ProviderDiscounts

    car_prices = {}
    for car in dealership.preferred_cars_list.all():  # Go through every car in list
        for provider_stock in CarsInProviderStock.objects.filter(car=car):
            # Go through every provider that have the car we are looking for
            personal_discount = get_personal_discount(
                provider_stock.provider, dealership
            )
            # Get personal discount from cur provider to cur dealer
            try:  # Try to get provider's discount for everyone to cur car
                car_discount = ProviderDiscounts.objects.get(
                    provider=provider_stock.provider, car__car=car
                )
                if (
                    provider_stock.car not in car_prices.keys()
                    or round(
                        car_discount.price_during_discount
                        * Decimal((100 - personal_discount) / 100),
                        2,
                    )
                    < car_prices[car][0]
                ):  # If there is no such a car in dict or price is
                    # lower than existing - add/update dict
                    car_prices[car] = (
                        round(
                            car_discount.price_during_discount
                            * Decimal((100 - personal_discount) / 100),
                            2,
                        ),
                        provider_stock.provider,
                    )
            except ProviderDiscounts.DoesNotExist:
                if (
                    provider_stock.car not in car_prices.keys()
                    or round(
                        provider_stock.price * Decimal((100 - personal_discount) / 100),
                        2,
                    )
                    < car_prices[car][0]
                ):  # If there is no such a car in dict or price is
                    # lower than existing - add/update dict
                    car_prices[car] = (
                        round(
                            provider_stock.price
                            * Decimal((100 - personal_discount) / 100),
                            2,
                        ),
                        provider_stock.provider,
                    )
    return car_prices


def get_personal_discount(provider, dealership):
    """Find if there are any personal discounts for a current dealership."""
    from provider.models import ProviderPersonalDiscounts

    try:  # Try to find any entries in a db about discount percentage
        personal_discount = ProviderPersonalDiscounts.objects.get(
            dealership=dealership, provider=provider
        )
        return personal_discount.actual_discount
        # Return discount percent from a cur provider to a cur dealer
    except ProviderPersonalDiscounts.DoesNotExist:
        return 0
        # Returning 0 as discount percent (price will be full)
