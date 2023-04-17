"""Buyer tasks to buy cars from dealerships."""
from datetime import date
from decimal import Decimal
from operator import itemgetter

from celery import shared_task
from celery.utils.log import get_task_logger
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver

logger = get_task_logger(__name__)


@receiver(post_save, sender="buyer.Offer")
def user_buy_car_on_offer_create(sender, instance, created, **kwargs):
    """Celery task that buy's car according to Order information"""
    buy_car(instance)


@shared_task
def buy_queued_cars():
    """
    Celery task that buy cars that were not bought in case of 0
    quantity of car from the offer on dealer's stocks.
    """
    from buyer.models import Offer

    for offer in Offer.objects.filter(is_active=True).select_related("car", "buyer"):
        buy_car(offer)


def buy_car(offer):
    """
    Function that searches for the best prices and tries to buy
    cars according to offer information.
    """
    from dealership.models import CarsInDealershipStock

    dealer_and_price = {}
    for stock in CarsInDealershipStock.objects.filter(
        car=offer.car, quantity__gt=0
    ).select_related("car", "dealership"):
        dealer_and_price[stock.dealership] = calculate_final_price(offer, stock)
    if not dealer_and_price:
        return
    best_dealer_and_price = [
        (k, v)
        for k, v in dealer_and_price.items()
        if v == min(dealer_and_price.values())
    ]
    best_dealer = best_dealer_and_price[0][0]
    best_price = best_dealer_and_price[0][1]
    if offer.max_cost >= best_price and offer.buyer.balance >= best_price:
        data_entries(best_dealer, best_price, offer)


def data_entries(best_dealer, best_price, offer):
    """Creates and updates DB according to processing the offer"""
    from dealership.models import (
        CarsInDealershipStock,
        CarDealership,
        DealerSales,
        DealershipPersonalDiscounts,
    )

    CarsInDealershipStock.objects.filter(dealership=best_dealer, car=offer.car).update(
        quantity=F("quantity") - 1
    )
    CarDealership.objects.filter(id=best_dealer.id).update(
        balance=F("balance") + best_price
    )
    DealerSales.objects.create(
        dealer=best_dealer, buyer=offer.buyer, car=offer.car, total_price=best_price
    )
    dealer_discount, created = DealershipPersonalDiscounts.objects.get_or_create(
        dealer=best_dealer,
        buyer=offer.buyer,
        defaults={"actual_discount": 0, "quantity_of_bought_cars": 1},
    )
    if not created:
        dealer_discount.quantity_of_bought_cars += 1
        dealer_discount.save()
    offer.is_active = False
    offer.save()
    offer.buyer.balance -= best_price
    offer.buyer.save()


def calculate_final_price(offer, stock):
    """Find's personal discount for buyer and discount for everyone"""
    from dealership.models import DealershipPersonalDiscounts, DealershipDiscounts

    pers_discount = DealershipPersonalDiscounts.objects.filter(
        dealer=stock.dealership, buyer=offer.buyer
    ).select_related("dealer", "buyer")
    if pers_discount.exists():
        price_mult = Decimal((100 - pers_discount.first().actual_discount) / 100)
    else:
        price_mult = 1
    car_discount = DealershipDiscounts.objects.filter(
        dealer=stock.dealership,
        car=offer.car,
        discount_date_from__lte=date.today(),
        discount_date_to__gte=date.today(),
    ).select_related("car", "dealer")
    if (
        car_discount.exists()
        and car_discount.first().price_during_discount < stock.price
    ):
        final_price = round(car_discount.first().price_during_discount * price_mult, 2)
    else:
        final_price = round(stock.price * price_mult, 2)
    return final_price
