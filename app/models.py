"""
Definition of models.
"""

from django.db import models
from django.core.validators import MinValueValidator 


class MetaModel(models.Model):

    class Meta:
        abstract = True

    def __str__(self):
        return str([field.name+': '+str(getattr(self, field.name))  for field in self._meta.fields])


#class AttrMeta(MetaModel):

#    new = models.BooleanField(default=False)
#    edited = models.BooleanField(default=False)
#    class Meta:
#        abstract = True

class Atributi(MetaModel):
    id = models.AutoField(primary_key=True)
    naziv = models.CharField(max_length=50)
    vrijednost = models.CharField(max_length=50)
    tip = models.CharField(max_length=10)


class Inventar(MetaModel):
    id = models.AutoField(primary_key=True)
    naziv = models.CharField(max_length=50)
    invBr = models.IntegerField(blank=False, unique=True) 
    kolicina = models.DecimalField(max_digits=16, decimal_places=5, validators=[MinValueValidator(0)]) #[JMIzlaz]
    tip = models.CharField(max_length=24, blank=False)
    JMUlaz = models.CharField(max_length=50, blank=False)
    JMIzlaz = models.CharField(max_length=50, blank=False)
    JMOdnos = models.DecimalField(max_digits=16, decimal_places=5, blank=False)
    atributi = models.ManyToManyField(Atributi)
    izrada = models.ManyToManyField('SpecifikacijeIzrade')


class Primka(MetaModel):
    id = models.AutoField(primary_key=True)
    datum = models.DateField()
    docBr = models.CharField(max_length=50)
    mjesto = models.CharField(max_length=50)
    dobavljac = models.CharField(max_length=50)
    nacinPlacanja = models.CharField(max_length=50)
    napomena = models.CharField(max_length=255)
    zaprimljeno = models.ManyToManyField("Zaprimljeno")


class Zaprimljeno(MetaModel):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Inventar, blank=False, on_delete=models.CASCADE)
    zapKolicina = models.DecimalField(max_digits=16, decimal_places=5, blank=False) #po izlaznoj JM
    vrijednost = models.DecimalField(max_digits=16, decimal_places=5)
    trosak = models.DecimalField(max_digits=16, decimal_places=5)
    rabat = models.DecimalField(max_digits=16, decimal_places=5)
    ukupno = models.DecimalField(max_digits=16, decimal_places=5)


class SpecifikacijeIzrade(MetaModel):
    id = models.AutoField(primary_key=True)
    materijal = models.ForeignKey(Inventar, on_delete=models.CASCADE)
    dimenzije = models.TextField() #'[d1,d2,d3]'
    kolicina = models.DecimalField(max_digits=16, decimal_places=5)
    ostatak = models.DecimalField(max_digits=16, decimal_places=5)
    ukupanUtrosak = models.DecimalField(blank=False, max_digits=16, decimal_places=5)
    napomena = models.CharField(max_length=255, null=True)


class Nalozi(MetaModel):
    id = models.AutoField(primary_key=True)
    proizvod = models.ForeignKey(Inventar, on_delete=models.CASCADE)
    docBr = models.CharField(max_length=50, blank=False, unique=True)
    datum = models.DateField(blank=False)
    kolicina = models.IntegerField(blank=False)
    status = models.CharField(max_length=16, blank=False)
    napomena = models.CharField(max_length=255, null=True)


class Otpremnica(MetaModel):
    id = models.AutoField(primary_key=True)
    datum = models.DateField(blank=False)
    docBr = models.CharField(blank=False, max_length=50, unique=True)
    mjesto = models.CharField(blank=False, max_length=50)
    primaoc = models.CharField(blank=False, max_length=50)
    mjestoPrijema = models.CharField(max_length=50)
    nacinPlacanja = models.CharField(max_length=50)
    napomena = models.CharField(max_length=255)
    otpremljeno = models.ManyToManyField("Otpremljeno")


class Otpremljeno(MetaModel):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Inventar, blank=False, on_delete=models.CASCADE)
    otprKolicina = models.DecimalField(max_digits=16, decimal_places=5, blank=False)
    osnovnaCijena = models.DecimalField(max_digits=16, decimal_places=5, blank=False)
    trosak = models.DecimalField(max_digits=16, decimal_places=5)
    rabat = models.DecimalField(max_digits=16, decimal_places=5)
    ukupno = models.DecimalField(max_digits=16, decimal_places=5, blank=False)


class MPHeader(MetaModel):
    id = models.AutoField(primary_key=True)
    datum = models.DateField(blank=False)
    docBr = models.CharField(blank=False, max_length=50, unique=True)
    mjesto = models.CharField(blank=False, max_length=50)
    kasaId = models.IntegerField(blank=False)
    kasirId = models.CharField(max_length=50)
    nacinPlacanjaOdmah = models.IntegerField() #Pogledaj MPViewSet/getHeaderData
    nacinPlacanjaOstatak = models.IntegerField() #Pogledaj MPViewSet/getHeaderData
    napomena = models.CharField(max_length=255)
    mpItemList = models.ManyToManyField("MPItemList")


class MPItemList(MetaModel):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Inventar, blank=False, on_delete=models.CASCADE)
    otprKolicina = models.DecimalField(max_digits=16, decimal_places=5, blank=False)
    korekcijaG = models.DecimalField(max_digits=16, decimal_places=5) #[%]
    korekcijaZ = models.DecimalField(max_digits=16, decimal_places=5) #[%]
    gotovinski = models.DecimalField(max_digits=16, decimal_places=5) #konacno gotovinski
    ziralno = models.DecimalField(max_digits=16, decimal_places=5)    #konacno ziralno


# Atributi.objects.filter(attmapper__prodID=3).values()
# Atributi.objects.filter(inventar__id=3)      - zahtjeva manytomany polje u inventar tabeli
# Inventar.objects.get(id=3).attmapper_set.all()  - Zahtjeva samo FK u attmapper tabeli prema inventaru
# AttMapper.objects.select_related().filter(id=1) - Zahtjeva samo FK u attmapper tabeli prema inventaru