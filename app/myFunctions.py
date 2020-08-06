from app.models import Inventar
from django.db.models import F

def filterData(obj, keysForDel):
    return {key: obj[key] for key in obj.keys() if (key not in keysForDel)}

def updInventar(Inventar, id, promjenaKolicine):
    #print(id, promjenaKolicine)
    item = Inventar.objects.get(id=id)
    #print('227',item.kolicina, promjenaKolicine)
    item.kolicina = F('kolicina') + promjenaKolicine
    item.save()

def insertPrimka(Inventar, zapItem, primka):
    #print(zapItem)
    item = Inventar.objects.get(id=zapItem['id'])
    if zapItem['poUlaznojJM']:
        zapItem['zapKolicina'] = float(zapItem['zapKolicina'])*float(item.JMOdnos)
    zapItem = {
        'item': item,
        'zapKolicina': float(zapItem['zapKolicina'])*float(item.JMOdnos) if zapItem['poUlaznojJM'] else zapItem['zapKolicina'],
        'vrijednost': zapItem['vrijednost'],
        'trosak': zapItem.get('trosak'),
        'rabat': zapItem.get('rabat'),
        'ukupno': zapItem.get('ukupno')
        }
    #print(zapItem)
    try:
        item.kolicina = F('kolicina')+zapItem['zapKolicina']
        item.save()
        primka.zaprimljeno.create(**zapItem)
    except Exception as err:
        print(err.args)

def insertOtpremnica(hdr, otpremnica):
    if not otpremnica['poIzlaznojJM']:
        otpremnica['otprKolicina'] = otpremnica['otprKolicina']*otpremnica['item']['JMOdnos']
    item = Inventar.objects.get(invBr=otpremnica['item']['invBr'])
    item.kolicina = F('kolicina') - otpremnica['otprKolicina']
    item.save()
    otpremnica['item']=item
    try:
        hdr.otpremljeno.create(**filterData(otpremnica, ['poIzlaznojJM']))
    except Exception as err:
        print('Exception:',err.args)
    

def strToFloat(s):
    try:
        return float(s)
    except:
        return(s)


def InventarToRepresentation(self, obj):
    return {
        'id': obj.id,
        'naziv': obj.naziv,
        'invBr': str(obj.invBr),
        'kolicina': float(obj.kolicina),
        'tip': obj.tip,
        'JMIzlaz': obj.JMIzlaz,
        'JMOdnos': float(obj.JMOdnos),
        'JMUlaz': obj.JMUlaz,
    }

def InventarToInternalValue(self, obj):
    return {
        'id': obj['id'],
        'naziv': obj['naziv'],
        'invBr': int(obj['invBr']),
        'kolicina': obj['kolicina'],
        'tip': obj['tip'],
        'JMIzlaz': obj['JMIzlaz'],
        'JMOdnos': obj['JMOdnos'],
        'JMUlaz': obj['JMUlaz']
    }