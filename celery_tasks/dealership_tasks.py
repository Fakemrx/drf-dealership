"""Celery tasks for a dealership."""
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
                dealership, dealership.preferred_cars_list.all()
            )  # Get dict {car: (price, provider)}
        else:
            # Logic to buy cars according to specs, not by exact list of preferred cars
            cars_list = search_suitable_cars(dealership)
            car_prices = search_minimal_price(
                dealership, cars_list
            )  # Get dict {car: (price, provider)}
        if car_prices:
            balance_per_car = round(dealership.balance / len(car_prices), 2)
            # Divide balance into equal parts (balance divides according to quantity of found cars)
            if buy_preferred_cars(car_prices, balance_per_car, dealership) == 0:
                # Check is there possibility to buy several cars with such balance per car
                buy_preferred_cars(car_prices, dealership.balance, dealership)
                # Trying to buy several cars using full dealer's balance without dividing it


def search_suitable_cars(dealership):
    """Search suitable cars according to car specs."""
    from car.models import Car

    cars_suitable_by_specs = []  # List for every car that fits local spec
    num_of_specs = 0
    if dealership.preferred_car_release_year_from:
        num_of_specs += 1
        for car in Car.objects.filter(
            release_year__gte=dealership.preferred_car_release_year_from
        ):
            cars_suitable_by_specs.append(car)
            # Add a car to the list if it's year greater than in spec or equals
    if dealership.preferred_car_release_year_to:
        num_of_specs += 1
        for car in Car.objects.filter(
            release_year__lte=dealership.preferred_car_release_year_to
        ):
            cars_suitable_by_specs.append(car)
            # Add a car to the list if it's year less than in spec or equals
    if dealership.preferred_car_type:
        num_of_specs += 1
        for car in Car.objects.filter(car_type=dealership.preferred_car_type):
            cars_suitable_by_specs.append(car)
            # Add a car to the list if it's car type equals to the spec
    if dealership.preferred_fuel_type:
        num_of_specs += 1
        for car in Car.objects.filter(engine__fuel_type=dealership.preferred_fuel_type):
            cars_suitable_by_specs.append(car)
            # Add a car to the list if it's engine's fuel type equals to the spec
    suitable_cars = suitable_cars_list_filter(cars_suitable_by_specs, num_of_specs)
    # List for cars that matches every specified spec
    return suitable_cars


def suitable_cars_list_filter(
    cars_suitable_by_specs,
    num_of_specs,
):
    """
    Filters only cars that match final search.
    """
    suitable_cars = []
    for car in cars_suitable_by_specs:
        if (
            cars_suitable_by_specs.count(car) == num_of_specs
            and car not in suitable_cars
        ):
            suitable_cars.append(car)
            # Add every single car if it matches with all conditions
    return suitable_cars


def buy_preferred_cars(car_prices, balance_per_car, dealer):
    """
    Buy cars for exact dealer, according to the best car prices
    and balance per car.
    """

    cars_bought = 0
    for car, price_and_provider in car_prices.items():
        # Go through every item in a dict {car: (price, provider)}
        for quantity in range(5, 0, -1):  # Try to buy 5, 4, 3, 2, 1 cars
            success = data_entries(
                dealer, price_and_provider, quantity, car, balance_per_car
            )
            # Add some more necessary entries into db
            cars_bought += quantity
            if success:
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
    # Create new entry in a db about this car in a dealer's stock
    if price * quantity <= balance_per_car:
        # Check if total price of N cars will be lower than balance per a car
        try:  # Try to get such a car in a dealer's stock
            dealer_stock = CarsInDealershipStock.objects.get(dealership=dealer, car=car)
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
        dealer.balance -= price * quantity
        dealer.save()
        # Reduce a dealer's balance
        try:  # Try to update quantity of all-time bought cars in ProviderPersonalDiscounts
            provider_personal_discount = ProviderPersonalDiscounts.objects.get(
                provider=cur_provider,
                dealership=dealer,
            )
            provider_personal_discount.quantity_of_bought_cars += quantity
            provider_personal_discount.save()
        except ProviderPersonalDiscounts.DoesNotExist:
            # Add new entry into a db about quantity of bought cars in ProviderPersonalDiscounts
            ProviderPersonalDiscounts.objects.create(
                provider=cur_provider,
                dealership=dealer,
                actual_discount=0,
                quantity_of_bought_cars=quantity,
            )
        ProviderSales.objects.create(
            provider=cur_provider,
            dealership=dealer,
            car=car,
            quantity=quantity,
            total_price=price * quantity,
        )
        # Add entry into a db about provider's sale
        return True
    return False


def search_minimal_price(dealership, preferred_cars_list):
    """Find minimal car prices from a transmitted dealership."""
    from provider.models import CarsInProviderStock, ProviderDiscounts

    car_prices = {}
    for car in preferred_cars_list:  # Go through every car in list
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
