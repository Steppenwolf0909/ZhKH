from django.db import models

from django.db import models
from .views import *

class News(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'



class Status(models.Model):
    name=models.CharField(max_length=20, blank=True, default=None)
    active=models.BooleanField(default=True)

    def __str__(self):
        return ' Статус заказа %s' % self.name


    class Meta:
        verbose_name='Статус заказа'
        verbose_name_plural='Статусы'

class Proposal(models.Model):
    description = models.TextField(null=True, blank=True)
    status = models.ForeignKey(Status, blank=True, null=True, on_delete=models.CASCADE)
    reply = models.TextField(null=True, blank=True, default=None)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return 'Предложение под номером %s' % ( self.id)

    class Meta:
        verbose_name = 'Жалоба/предложение'
        verbose_name_plural = 'Жалобы/предложения'


class Admission(models.Model):
    flat_number = models.IntegerField()
    car_number = models.CharField(max_length=10, blank=True, null=True)
    fio = models.CharField(max_length=100)
    reason = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return 'Заказ на пропуск %s' % (self.id)

    class Meta:
        verbose_name = 'Заказ на пропуск'
        verbose_name_plural = 'Заказы на пропуск'


class EmployeeType(models.Model):
    name = models.IntegerField(blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return (self.id)

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'

class EmployeeCalling(models.Model):
    flat_number = models.IntegerField(blank=True, null=True)
    employee_type = models.ForeignKey(EmployeeType, blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return '%s в квартиру №%s' % (self.employee_type.name, self.flat_number)

    class Meta:
        verbose_name = 'Вызов работника ЖКХ'
        verbose_name_plural = 'Вызовы работников ЖКХ'

class Contacts(models.Model):
    fio = models.CharField(max_length=100, blank=True, null=True)
    post = models.CharField(max_length=100)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return '%s %s' % (self.post, self.fio)

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'