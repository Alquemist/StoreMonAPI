from .viewSets import *
from rest_framework import routers


router = routers.DefaultRouter()
router.register(prefix='inventar', viewset=InventarViewSet, basename='Inventar')
router.register(prefix='atributi', viewset=AtributiViewSet, basename='Atributi')
router.register(prefix='primka', viewset=PrimkaViewSet, basename='Primka')
router.register(prefix='specs', viewset=SpecifikacijeViewSet, basename='SpecifikacijeIzrade')
router.register(prefix='nalozi', viewset=NaloziViewSet, basename='Nalozi')
router.register(prefix='otpremnice', viewset=OtpremniceViewSet, basename='Otpremnica')
router.register(prefix='MP', viewset=MPViewSet, basename='MPHeader')
# router.register(prefix='preFetch', viewset=PreFetchingViewSet, basename='Inventar')

