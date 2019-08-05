import json
import os
import base64
from django.core.files.base import ContentFile
from django.contrib.postgres.search import SearchVector

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def add(request):
  if request.method=='GET':
    data = {}
    # return render(request, 'items/add.html', data)

    response = {'status': 121, 'readable_response' : 'invalid request'}
    return HttpResponse(json.dumps(response), content_type='application/json')

  elif request.method=='POST':

    description = request.POST['description']
    print('Key: %s' % (description) )


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

