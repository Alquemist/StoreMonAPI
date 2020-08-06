import json
from django.http import JsonResponse
from .models import *
from .serializers import *
from rest_framework import viewsets

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
#from django.db.models import F
from django.db.models import Max

from .myFunctions import *


class InventarViewSet(viewsets.ModelViewSet):
    queryset = Inventar.objects.all()
    serializer_class = InventarSerializer
    @action(methods=['get'], detail=False)
    def searchItem(self, request):
        param = request.GET.get('naziv', default=None)
        try:
            queryset = Inventar.objects.filter(invBr__icontains=int(param))
        except:
            queryset = Inventar.objects.filter(naziv__icontains=param)
        print('queryset: ', queryset)
        #serializer = self.get_serializer(queryset, many=True)
        serializer = InventarSerializer(queryset, many=True)
        data = serializer.data
        print (data)
        return Response(data)

    @action(methods=['delete'], detail=False)
    def deleteItem(self, request):
        itemId = json.loads(request.body.decode('utf-8'))
        Atributi.objects.filter(inventar__id=itemId).delete()
        SpecifikacijeIzrade.objects.filter(inventar__id=itemId).delete()
        Inventar.objects.get(id=itemId).delete()
        return Response()
    
    @action(methods=['get'], detail=False)
    def doesInvExists(self, request):
        invBr = request.GET.get('invBr', default='None')
        return Response(Inventar.objects.filter(invBr=invBr).exists())

    @action(methods=['get'], detail=False)
    def getLastInv(self, request):
        maxInv = Inventar.objects.aggregate(Max('invBr')).values()
        return Response(list(maxInv)[0])

    @action(methods=['get'], detail=False)
    def getAll(self, request):
        inv = Inventar.objects.all()
        serializer = InventarSerializeRelated(inv, many=True)
        return Response(serializer.data)

class AtributiViewSet(viewsets.ModelViewSet):
    #queryset = Inventar.objects.all()
    serializer_class = AtributiSerializer
    
    @action(methods=['get'], detail=False)
    def getattribs(self, request):
        itemID = request.GET.get('itemID')
        print('i am listing for:', itemID)
        queryset = Atributi.objects.filter(inventar__id=itemID)
        serializer = AtributiSerializer(queryset, many=True)
        print(serializer.data)
        return Response(serializer.data)

    @action(methods=['post'], detail=False)
    def addAndLink(self, request):
        data = json.loads(request.body.decode('utf-8'))
        item = filterData(data['item'], ['new','edit'])
        if item.get('id'):
            item = Inventar.objects.get(id=item['id'])
        else:
            item = Inventar.objects.create(**item)

        if isinstance(data['attribs'], (dict, )):
            item.atributi.create(**data) #data['attribs'] ?????
        elif isinstance(data['attribs'], (list,)):
            [item.atributi.create(**filterData(atrib, ['new', 'edited'])) for atrib in data['attribs']]
        return Response(item.id)

    @action(methods=['patch'], detail=False)
    def updateAttribs(self, request):
        attribs = json.loads(request.body.decode('utf-8'))
        [Atributi.objects.filter(id=atrib['id']).update(**atrib) for atrib in attribs]
        return Response()

    @action(methods=['delete'], detail=False)
    def deleteAttribs(self, request):
        atribIds = json.loads(request.body.decode('utf-8'))
        Atributi.objects.filter(id__in=atribIds).delete()
        return Response()


class PrimkaViewSet(viewsets.ViewSet):
    
    @action(methods=['get'], detail=False)
    def getData(self, request):
        print('getPrimka')
        mjesta = Primka.objects.values().distinct().values_list('mjesto', flat=True)
        dobavljaci = Primka.objects.values().distinct().values_list('dobavljac', flat=True)
        placanja = Primka.objects.values().distinct().values_list('nacinPlacanja', flat=True)
        try:
            docBr = Primka.objects.latest('id').docBr
        except Exception:
            docBr = ''
        #print(mjesta, dobavljaci, placanja, docBr)
        return Response({'mjesta': mjesta, 'dobavljaci': dobavljaci, 'placanja':placanja, 'docBr':docBr})

    @action(methods=['post'], detail=False)
    def zaprimanje(self, request):
        data = json.loads(request.body.decode('utf-8'))
        header = data['header']
        zapItems = data['items']
        #print('header:', header)
        primka = Primka.objects.create(**header)
        [insertPrimka(zapItem, primka) for zapItem in zapItems]
        return Response()


class SpecifikacijeViewSet(viewsets.ViewSet):

    @action(methods=['get'], detail=False)
    def getSpecs(self, request):
        itemId = request.GET.get('itemId')
        queryset = SpecifikacijeIzrade.objects.filter(inventar__id=itemId)
        serializer = SpecifikacijeSerializer(queryset, many=True)
        data = [
            {**{key: strToFloat(val) for (key, val) in lst.items()},
            **{'materijal':Inventar.objects.get(id=lst['materijal']).naziv, 'materijalId': lst['materijal']}}
            for lst in serializer.data
            ]
        return Response(data)

    @action(methods=['post'], detail=False)
    def saveSpecs(self, request):
        data = json.loads(request.body.decode('utf-8'))
        itemId = data['itemId']
        specs = data['specs']
        delSpecs = data['delSpecs']
        #print(delSpecs, data)
        item = Inventar.objects.get(id=itemId)
        try:
            [item.izrada.create(**filterData({**spec, **{'materijal': Inventar.objects.get(id=spec['materijalId'])}}, ['materijalId', 'new', 'JM'])) for spec in specs]
            SpecifikacijeIzrade.objects.filter(id__in=delSpecs).delete()
        except Exception as err:
            print(itemId, specs)
            print(err)
        return Response()


class NaloziViewSet(viewsets.ModelViewSet):
    @action(methods=['post'], detail=False)
    def saveNalog(self, request):
        data = json.loads(request.body.decode('utf-8'))
        itemId = data['itemId']
        item = Inventar.objects.get(id=itemId)
        nalog = data['nalog']
        nalog.update({'proizvod': item})
        #print(itemId, nalog)
        try:
            Nalozi.objects.create(**nalog)
            return Response()
        except Exception as err:
            response = Response(err.args, status=status.HTTP_400_BAD_REQUEST)
            if err.args[0]==1062:
                response = Response('Nalog sa Br: {} već postoji!'.format(nalog['docBr']), status=status.HTTP_409_CONFLICT)
            return response
    
    @action(methods=['get'], detail=False)
    def getNalogList(self, request):
        queryData = json.loads(request.query_params.get("queryData"))
        statusDict = {0:"Izrađen", 1:"Odobren", 2:"U proizvodnji", 3:"Završeno"}
        print('nalozilist', queryData)
        
        def searchByItem(param):
            return Nalozi.objects.filter(proizvod__invBr=int(param))
            
        def searchByDates(dates):
            return  Nalozi.objects.filter(datum__gte=dates[0]).filter(datum__lte=dates[1])
        
        if len(queryData):
            switch = {"item": searchByItem, "dates": searchByDates}
            queryset = switch.get(list(queryData.keys())[0])(list(queryData.values())[0])
            #print(queryset)
            serializer = NaloziSerializer(queryset, many=True)
            return Response({'naloziList': serializer.data, 'statusDict': statusDict})
        else:
            return Response({'naloziList': [], 'statusDict': statusDict})
    
    @action(methods=['patch'], detail=False)
    def updateNalog(self, request):                                 #statusList = {"Izrađen":0, "Odobren":1, "U proizvodnji":2, "Završeno":3}
        data = json.loads(request.body.decode('utf-8'))
        nalog = Nalozi.objects.get(id=data['id'])
        #print('status naloga', data['status'])
        def updNalog():
            nalog.status = int(data['status'])
            nalog.save()
        if int(data['status']) < 2:
            updNalog()
        if int(data['status']) == 2:
            #print('u proizvodnji')
            specs = nalog.proizvod.izrada.values_list('materijal_id', 'ukupanUtrosak')
            [updInventar(id, -utrosak*nalog.kolicina) for id, utrosak in specs]
            updNalog()
        if int(data['status']) == 3:
            #print('zavrseno')
            updInventar(nalog.proizvod_id, nalog.kolicina)
            updNalog()

        return Response()

        
class OtpremniceViewSet(viewsets.ViewSet):
    @action(methods=['get'], detail=False)
    def getData(self, request):
        mjesta = Otpremnica.objects.values().distinct().values_list('mjesto', flat=True)
        primaoci = Otpremnica.objects.values().distinct().values_list('primaoc', flat=True)
        placanja = Otpremnica.objects.values().distinct().values_list('nacinPlacanja', flat=True)
        mjestaPrijema = Otpremnica.objects.values().distinct().values_list('mjestoPrijema', flat=True)
        try:
            docBr = Otpremnica.objects.latest('id').docBr
        except Exception:
            docBr = ''
        #print({'mjesta': mjesta, 'primaoci': primaoci, 'placanja':placanja, 'mjestaPrijema': mjestaPrijema, 'docBr':docBr})
        responseObj = {
            'mjesto': mjesta.latest('datum') if len(mjesta) else '',
            'mjesta': mjesta if len(mjesta) else [],
            'docBr': docBr,
            'primaoc': primaoci.latest('datum') if len(primaoci) else '',
            'primaoci': primaoci if len(primaoci) else [],
            'mjestoPrijema': mjestaPrijema.latest('datum') if len(mjestaPrijema) else '',
            'mjestaPrijema': mjestaPrijema if len(mjestaPrijema) else [],
            'nacinPlacanja': placanja.latest('datum') if len(placanja) else '',
            'naciniPlacanja': placanja if len(placanja) else [],
            }
        return Response(responseObj)
    
    @action(methods=['post'], detail=False)
    def saveData(self, request):
        data = json.loads(request.body.decode('utf-8'))
        hdrData = data['hdrData']
        otpremnice = data['otpremnice']
        #print(otpremnice)
        try:
            hdr = Otpremnica.objects.create(**hdrData)
            [insertOtpremnica(hdr, otpremnica) for otpremnica in otpremnice]
            return Response()
        except Exception as err:
            if err.args[0]==1062:
                response = Response('Doc sa tim brojem već postoji!', status=status.HTTP_409_CONFLICT)
            else:
                response = Response(err.args, status=status.HTTP_406_NOT_ACCEPTABLE)
            print(response)
            return response

    @action(methods=['get'], detail=False)
    def searchData(self, request):
        params = json.loads(request.query_params.get("params"))
        itemId = params['item']
        dates = params['dates']
        print('params', params)
        qs = Otpremnica.objects.all()
        if itemId:
            qs = qs.filter(otpremljeno__item_id=itemId)
        if dates[0]:
            qs = qs.filter(datum__gte=dates[0])
        if dates[0]:
            qs = qs.filter(datum__lte=dates[1])
        #print(qs)
        serializer = OtpremnicaSerializer(qs, many=True)
        return Response(serializer.data)
    
    @action(methods=['get'], detail=False)
    def getDetails(self, request):
        id = json.loads(request.query_params.get("id"))
        qs = Otpremljeno.objects.filter(otpremnica__id=id)
        serializer = OtpremljenoSerializer(qs, many=True)
        return Response(serializer.data)


class MPViewSet(viewsets.ViewSet):
    placanja = {
            'odmah': {0: 'Gotovinski', 2:'Kartično', 3: 'Žiralno'},
            'ostatak': {0: 'Žiralno', 1: 'Odloženo', 2: 'Ostalo'}
        }
    @action(methods=['get'], detail=False)
    def getHeaderData(self, request):
        try:
            kasaId = json.loads(request.query_params.get("kasaId"))
            lastEntry = MPHeader.objects.filter(kasaid=kasaId).latest(id)
            lastEntry = MPHeaderSerializer(lastEntry).data()
        except Exception:
            lastEntry = {'mjesto': '', 'docBr': '', 'nacinPlacanjaOdmah': 0, 'nacinPlacanjaOstatak': 0, 'naciniPlacanja': self.placanja, 'kasaId': ''}
        return Response(lastEntry)
    
    @action(methods=['post'], detail=False)
    def saveMPData(self, request):
        hdrData = json.loads(request.query_params.get("hdrData"))
        MPItemList = json.loads(request.query_params.get("MPList"))
        hdr = MPHeader.objects.create(**hdrData)
        [hdr.mpItemList.create(**item) for item in MPItemList]
        return Response()


# class PreFetchingViewSet(viewsets.ViewSet):
    
#     @action(methods=['get'], detail=False)
#     def preFetchAll(self, request):
#         inv = Inventar.objects.all()#Inventar.objects.all().prefetch_related('atributi')#Inventar.objects.all()
#         serializer = InventarSerializeRelated(inv, many=True)
#         print(serializer)
#         return Response(serializer.data)