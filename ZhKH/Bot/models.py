from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models

class TelegramUser(models.Model):
    username = models.CharField("Имя пользователя", max_length=128)
    flatNumber=models.IntegerField("Номер квартиры", blank=True, default=None)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class News(models.Model):
    title = models.CharField("Заголовок", max_length=128)
    text = models.TextField("Основной текст", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Status(models.Model):
    name=models.CharField("Название статуса", max_length=20, blank=True, default=None)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='Статус заказа'
        verbose_name_plural='Статусы'

class Urgency(models.Model):
    name=models.CharField("Наименование категории", max_length=20, blank=True, default=None)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='Категория срочности'
        verbose_name_plural='Категории срочности'


class Proposal(models.Model):
    description = models.TextField("Описание", null=True, blank=True)
    status = models.ForeignKey(Status, blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(TelegramUser, blank=True, null=True, on_delete=models.CASCADE)
    urgency = models.ForeignKey(Urgency, blank=True, null=True, on_delete=models.CASCADE)
    reply = models.TextField("Ответ на предложение", null=True, blank=True, default=None)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return ' № %s Жалоба:%s \n Текущий статус:%s \n Ответ: %s \n '  % (self.id, self.description, self.status, self.reply)

    class Meta:
        verbose_name = 'Жалоба/предложение'
        verbose_name_plural = 'Жалобы/предложения'

class CarType(models.Model):
    name=models.CharField("Тип автомобиля", max_length=20, blank=True, default=None)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='Тип автомобиля'
        verbose_name_plural='Типы автомобилей'

class TimesLimit(models.Model):
    name=models.CharField("Времянной интервал", max_length=20, blank=True, default=None)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='Времянной интервал'
        verbose_name_plural='Времянные интервалы'

class Admission(models.Model):
    user = models.ForeignKey(TelegramUser, blank=True, null=True, on_delete=models.CASCADE)
    carType = models.ForeignKey(CarType, blank=True, null=True, on_delete=models.CASCADE)
    timeLimit = models.ForeignKey(TimesLimit, blank=True, null=True, on_delete=models.CASCADE)
    carNumber = models.CharField("Номер машины", max_length=10, blank=True, null=True)
    fio = models.CharField("ФИО", max_length=100)
    reason = models.TextField("Комментарии", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        if self.carType==None:
            return 'Заказ на пропуск № %s \n для %s в квартиру № %s оформлен' % (self.id, self.fio, self.user.flatNumber)

        else:
            return 'Заказ на пропуск № %s \n ФИО: %s \n квартира № %s \n автомобиль: %s (%s) \n оформлен на срок %s' % (self.id, self.fio, self.user.flatNumber, self.carType, self.carNumber, self.timeLimit)

    class Meta:
        verbose_name = 'Заказ на пропуск'
        verbose_name_plural = 'Заказы на пропуск'


class EmployeeType(models.Model):
    name = models.CharField("Название специальности", max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'

class EmployeeCalling(models.Model):
    user = models.ForeignKey(TelegramUser, blank=True, null=True, on_delete=models.CASCADE)
    employeeType = models.ForeignKey(EmployeeType, blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return 'Оформлен вызов %s в квартиру №%s' % (self.employeeType, self.user.flatNumber)

    class Meta:
        verbose_name = 'Вызов работника ЖКХ'
        verbose_name_plural = 'Вызовы работников ЖКХ'


class CounterValue(models.Model):
    user = models.ForeignKey(TelegramUser, blank=True, null=True, on_delete=models.CASCADE)
    electic = models.IntegerField("Электричество", blank=True, null=True)
    coldWater = models.IntegerField("Холодная вода", blank=True, null=True)
    hotWater = models.IntegerField("Горячая вода", blank=True, null=True)

    def __str__(self):
        return 'Квартира: %s \n Электричество:%s,\n Холодная вода: %s,\n Теплая вода: %s\n\n'\
               % (self.user.flatNumber,  self.electic, self.coldWater, self.hotWater)

    class Meta:
        verbose_name = 'Показание счетчика'
        verbose_name_plural = 'Показания счетчиков'

class Contacts(models.Model):
    fio = models.CharField("ФИО", max_length=100, blank=True, null=True)
    post = models.CharField("Должность", max_length=100)
    phoneNumber=PhoneNumberField("Номер телефона (Например: +79876543210")
    description = models.TextField("Описание")
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return '%s \n%s тел. %s \n \n' % (self.post, self.fio, self.phoneNumber)

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'