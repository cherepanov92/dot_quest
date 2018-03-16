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