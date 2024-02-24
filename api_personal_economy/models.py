from django.db import models
from django.utils import timezone


# Create your models here.
class Account(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey('auth.User', related_name='accounts', on_delete=models.CASCADE)
    balance = models.DecimalField(decimal_places=2, max_digits=15, default=0)
    initial_balance = models.DecimalField(decimal_places=2, max_digits=15, default=0)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        """
        Capitalize the name before saving
        """
        self.name = self.name.capitalize()
        super(Account, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Operation(models.Model):
    INCOME = 'In'
    Expense = 'Exp'
    TYPE_CHOICES = [
        (INCOME, 'Income'),
        (Expense, 'Expense'),
    ]
    type = models.CharField(
        max_length=3,
        choices=TYPE_CHOICES,
        default=Expense,
    )
    account = models.ForeignKey(Account, models.PROTECT, related_name='operations')
    date = models.DateField(default=timezone.now)
    amount = models.DecimalField(decimal_places=2, max_digits=15, default=0)
    description = models.CharField(max_length=250, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f'{self.get_type_display()} of ${self.amount} in account {self.account.name} on {self.date.strftime("%m/%d/%Y")}'
