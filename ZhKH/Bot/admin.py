from django.contrib import admin
from .models import *

class TelegramUserAdmin(admin.ModelAdmin):
    class Meta:
        model=TelegramUser

admin.site.register(TelegramUser, TelegramUserAdmin)

class NewsAdmin(admin.ModelAdmin):
    class Meta:
        model=News

admin.site.register(News, NewsAdmin)


class StatusAdmin(admin.ModelAdmin):
    class Meta:
        model=Status

admin.site.register(Status,StatusAdmin)



class ProposalAdmin(admin.ModelAdmin):
    class Meta:
        model=Proposal

admin.site.register(Proposal,ProposalAdmin)


class AdmissionAdmin(admin.ModelAdmin):
    class Meta:
        model = Admission

admin.site.register(Admission, AdmissionAdmin)

class EmployeeTypeAdmin(admin.ModelAdmin):
    class Meta:
        model = EmployeeType

admin.site.register(EmployeeType, EmployeeTypeAdmin)

class EmployeeCallingAdmin(admin.ModelAdmin):
    class Meta:
        model = EmployeeCalling

admin.site.register(EmployeeCalling, EmployeeCallingAdmin)

class ContactsAdmin(admin.ModelAdmin):
    class Meta:
        model = Contacts

admin.site.register(Contacts, ContactsAdmin)

class CounterValueAdmin(admin.ModelAdmin):
    class Meta:
        model = CounterValue

admin.site.register(CounterValue, CounterValueAdmin)

class TimesLimitAdmin(admin.ModelAdmin):
    class Meta:
        model = TimesLimit

admin.site.register(TimesLimit, TimesLimitAdmin)

class CarTypeAdmin(admin.ModelAdmin):
    class Meta:
        model = CarType

admin.site.register(CarType, CarTypeAdmin)

class UrgencyAdmin(admin.ModelAdmin):
    class Meta:
        model = Urgency

admin.site.register(Urgency, UrgencyAdmin)






