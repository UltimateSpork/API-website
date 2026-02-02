from django.db import models

# Create your models here.

class LandClass(models.Model):

    name = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.name

class LandCategory(models.Model):

    name = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.name

class State(models.Model):

    name = models.CharField(max_length=2,unique=True)

    def __str__(self):
        return self.name

class County(models.Model):

    name = models.CharField(max_length = 50)
    FIPScode = models.CharField(max_length=10)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("name","state")

    def __str__(self):

        return f"{self.name}, {self.state.name}"

class OffshoreRegion(models.Model):

    name = models.CharField(max_length = 50, unique=True)

    def __str__(self):

        return self.name

class Commodity(models.Model):

    name = models.CharField(max_length = 50)
    unit = models.CharField(max_length = 20)

    class Meta:

        unique_together = ("name","unit")

    def __str__(self):

        return f"{self.name}, ({self.unit})"

class Disposition(models.Model):

    ID = models.AutoField(primary_key = True)
    code = models.IntegerField()
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.description}"

class ProductionRecord(models.Model):

    productionDate = models.DateField()
    volume = models.FloatField()
    landClass = models.ForeignKey(LandClass, on_delete=models.CASCADE)
    landCategory = models.ForeignKey(LandCategory, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True,blank=True)
    county = models.ForeignKey(County, on_delete=models.SET_NULL, null=True,blank=True)
    offshoreRegion = models.ForeignKey(OffshoreRegion, on_delete=models.SET_NULL, null=True,blank=True)
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    disposition = models.ForeignKey(Disposition, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.productionDate} - {self.commodity}"
