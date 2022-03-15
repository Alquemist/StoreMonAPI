"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.template import RequestContext
from rest_framework.response import Response
from datetime import datetime

from django.views.generic import TemplateView
# from app.models import *

reactRoot = TemplateView.as_view(template_name='index.html')
sw = TemplateView.as_view(template_name='service-worker.js')

# def getAll(request):
#     "Get all data for precaching in Index.db"
#     print('attr:', Inventar.objects.all().prefetch_related('atributi'))
#     return JsonResponse({'data': list(Inventar.objects.all().prefetch_related('atributi').values())}, safe=False)

# def home(request):
#     """Renders the home page."""
#     assert isinstance(request, HttpRequest)
#     return render(
#         request,
#         'app/index.html',
#         {
#             'title':'Home Page',
#             'year':datetime.now().year,
#         }
#     )

# def contact(request):
#     """Renders the contact page."""
#     assert isinstance(request, HttpRequest)
#     return render(
#         request,
#         'app/contact.html',
#         {
#             'title':'Contact',
#             'message':'Your contact page.',
#             'year':datetime.now().year,
#         }
#     )

# def about(request):
#     """Renders the about page."""
#     assert isinstance(request, HttpRequest)
#     return render(
#         request,
#         'app/about.html',
#         {
#             'title':'About',
#             'message':'Your application description page.',
#             'year':datetime.now().year,
#         }
#     )
