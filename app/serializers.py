from rest_framework import serializers
from .models import *
from .myFunctions import InventarToInternalValue, InventarToRepresentation
from django.forms.models import model_to_dict


class InventarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Inventar
        fields = (
            'id',
            'naziv',
            'invBr',
            'tip',
            'kolicina',
            'JMIzlaz',
            'JMOdnos',
            'JMUlaz',
        )

    to_representation = InventarToRepresentation
    to_internal_value = InventarToInternalValue

    # def to_representation(self, obj):
    #     return {
    #         'id': obj.id,
    #         'naziv': obj.naziv,
    #         'invBr': str(obj.invBr),
    #         'kolicina': float(obj.kolicina),
    #         'tip': obj.tip,
    #         'JMIzlaz': obj.JMIzlaz,
    #         'JMOdnos': float(obj.JMOdnos),
    #         'JMUlaz': obj.JMUlaz,
    #     }

    # def to_internal_value(self, obj):
    #     print('to internal: ', obj)
    #     return {
    #         'id': obj['id'],
    #         'naziv': obj['naziv'],
    #         'invBr': int(obj['invBr']),
    #         'kolicina': obj['kolicina'],
    #         'tip': obj['tip'],
    #         'JMIzlaz': obj['JMIzlaz'],
    #         'JMOdnos': obj['JMOdnos'],
    #         'JMUlaz': obj['JMUlaz']
    #     }

class AtributiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atributi

        fields = (
        'id',
        'naziv',
        'vrijednost',
        'tip',
        )
    

class SpecifikacijeSerializer(serializers.ModelSerializer):
    JM = serializers.CharField(source='materijal.JMIzlaz')
    class Meta:
        model = SpecifikacijeIzrade
        fields = (
            'id',
            'materijal',
            'dimenzije',
            'JM',
            'kolicina',
            'ostatak',
            'ukupanUtrosak',
            'napomena'
        )


class InventarSerializeRelated(serializers.ModelSerializer):
    atributi = AtributiSerializer(many=True, read_only=True)
    izrada = SpecifikacijeSerializer(many=True, read_only=True)
    class Meta:
        model = Inventar

        fields = (
            'id',
            'naziv',
            'invBr',
            'tip',
            'gotovinaMP',
            'ziralMP',
            'gotovinaVP',
            'ziralVP',
            'pdvStopa',
            'kolicina',
            'JMIzlaz',
            'JMOdnos',
            'JMUlaz',
            'atributi',
            'izrada'
        )

        to_representation = InventarToRepresentation

class PrimkaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Primka

        fields = (
            'mjesto',
            'docBr',
            'datum',
            'dobavljac',
            'nacinPlacanja',
            'napomena'
            )


class NaloziSerializer(serializers.ModelSerializer):

    naziv = serializers.CharField(source='proizvod.naziv')
    #statusDict = serializers.SerializerMethodField()

    class Meta:
        model = Nalozi
        fields = (
            'id',
            'docBr',
            'datum', 
            'kolicina',
            'napomena',
            'naziv',
            'status',
        )


class OtpremnicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otpremnica
        fields = (
            'id',
            'datum',
            'docBr',
            'mjesto',
            'primaoc',
            'mjestoPrijema',
            'nacinPlacanja',
            'napomena',
            )


class OtpremljenoSerializer(serializers.ModelSerializer):
    item = serializers.CharField(source='item.naziv')
    class Meta:
        model = Otpremljeno
        fields = (
            'item',
            'otprKolicina',
            'osnovnaCijena',
            'trosak',
            'rabat',
            'ukupno'
        )


class MPHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model =  MPHeader
        fields = (
            'id',
            'datum',
            'docBr',
            'mjesto',
            'kasaId',
            'Kasir',
            'nacinPlacanjaOdmah',
            'nacinPlacanjaOstatak',
            'napomena',
            )


class MPItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MPItemList
        fields = (
            'item',
            'otprKolicina',
            'korekcijaG',
            'korekcijaZ',
            'gotovinski',
            'ziralno',
        )