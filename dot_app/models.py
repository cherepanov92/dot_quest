from django.db import models

class Historical(models.Model):
    company_alias = models.ForeignKey('Company')
    date = models.DateField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.IntegerField()

    def __str__(self):
        return '{company} | {date}'.format(
            company = str(self.company_alias),
            date = str(self.date)
        )
class Company(models.Model):
    company_name = models.CharField(max_length=40)
    company_alias = models.CharField(max_length=40)

    def __str__(self):
        return f'{self.company_name}'

class Insider(models.Model):
    name = models.CharField(max_length=40)
    relation = models.CharField(max_length=40)

    def __str__(self):
        return f'{self.name}'


class InsiderTrades(models.Model):
    company_alias = models.ForeignKey('Company')
    insider = models.ForeignKey('Insider')
    last_date = models.DateField()
    trans_type = models.CharField(max_length=70)
    owner_type = models.CharField(max_length=40)
    shares_traded = models.FloatField()
    last_price = models.FloatField(blank=True, null=True)
    shares_held = models.IntegerField()

    def __str__(self):
        return '{company} | {insider} | {date}'.format(
            company = str(self.company_alias.company_name),
            insider = str(self.insider.name),
            date=str(self.last_date)
        )
