#-*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.functional import cached_property
from django.db.models import Count
from django.db.models import Sum


class Company(models.Model):
    name = models.CharField(max_length=150)
    bic = models.CharField(max_length=150, blank=True)

    # no need to use it
    def get_order_count(self):
        return self.orders.count()

    # though I improved the query here, but it still need lots of time to load
    def get_order_sum(self):
        total_sum = self.contacts.annotate(order_total=Sum('orders__total')).aggregate(Sum('order_total'))['order_total__sum']
        return total_sum

    # I did this one which will save loading time
    def get_order_breakdown(self):
        contacts = self.contacts.annotate(order_total=Sum('orders__total'), order_count=Count('orders__total'))
        sum_val = sum(list(contacts.values_list("order_total", flat=True)))
        order_count = sum(list(contacts.values_list("order_count", flat=True)))
        data_dict = {
            "order_count": order_count,
            "sum_val": sum_val,
            "contacts": contacts
        }
        return data_dict


class Contact(models.Model):
    company = models.ForeignKey(
        Company, related_name="contacts", on_delete=models.PROTECT)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField()

    def get_order_count(self):
        return self.orders.count()


@python_2_unicode_compatible
class Order(models.Model):
    order_number = models.CharField(max_length=150)
    company = models.ForeignKey(Company, related_name="orders")
    contact = models.ForeignKey(Contact, related_name="orders")
    total = models.DecimalField(max_digits=18, decimal_places=9)
    order_date = models.DateTimeField(null=True, blank=True)
    # for internal use only
    added_date = models.DateTimeField(auto_now_add=True)
    # for internal use only
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % self.order_number
