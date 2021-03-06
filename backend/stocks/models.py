from django.db import models


# Create your models here.
# class TimestampedModel(models.Model):
#     created_at =
#     pass
#     class Meta:
#         abstract=True

class SIC(models.Model):
    sic = models.CharField(max_length=4,primary_key=True)
    industry = models.CharField(max_length=61)

class Firm(models.Model):
    cik = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    sic = models.ForeignKey(SIC, on_delete=models.SET_NULL,null=True)
    country = models.CharField(max_length=30,blank=True)


class Insider(models.Model):
    cik = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    firm = models.ForeignKey(Firm, on_delete=models.SET_NULL, null=True)
    amount = models.IntegerField()


class Stock(models.Model):
    EXCHANGE_CHOICES = [('NASDAQ', 'Nasdaq'), ('NYSE', 'NYSE')]
    ticker = models.CharField(max_length=5,primary_key=True)
    firm = models.ForeignKey(Firm, on_delete=models.CASCADE,null=True)
    exchange = models.CharField(max_length=6, choices=EXCHANGE_CHOICES)
    IPO_year = models.CharField(max_length=4, null=True)
    is_active = models.BooleanField(null=True)
    volume = models.IntegerField(null=True)



class File(models.Model):
    SECURITY_TITLES = [('CS','Common Stock'),('SO','Stock Option')]
    ACTION_CHOICES = [('A','Acquired'),('D','Disposed of')]
    accNumber = models.IntegerField(primary_key=True)
    firm = models.ForeignKey(Firm, on_delete=models.SET_NULL, null=True)
    transaction_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    price = models.FloatField()
    title = models.CharField(max_length=2,choices=SECURITY_TITLES)
    action = models.CharField(max_length=1,choices=ACTION_CHOICES)
