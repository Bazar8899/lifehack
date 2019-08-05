import crypt
import json

from django.contrib.auth.hashers import make_password

from user.models import LHUser, LifeHackOAuthApplication
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

# Create your views here.


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def register_user(request):
    try:
        json_dict = json.loads(request.body.decode('utf-8'))
    except json.decoder.JSONDecodeError:
        data = {
            'response': 'JSON error',
            'status': 101
        }
        return Response(data, content_type='application/json')

    try:
        dob = json_dict['dob']
        gender = json_dict['gender']
        device_id = json_dict['device_id']
        username = json_dict['username']

    except Exception as e:
        data = {
            'response': 'parameter is missing',
            'status': 102,
            'exception' : str(e)
        }
        return Response(data, content_type='application/json')

    if not dob or not username or not gender or not device_id:

        data = {
            'response': 'parameter is missing',
            'status': 102,
            'exception' : str(e)
        }

        return Response(json.dumps(data), content_type='application/json')

    application = True #= LifeHackOAuthApplication.objects.filter(client_id=client_id, client_secret=client_secret).first()

    if not application:

        data = {'status' : 100, 'readable_response' : 'invalid client_id or client_secret'}
        return Response(data, content_type='application/json')

    if application:

        user = LHUser.objects.values().filter(device_id=device_id).first()

        if not user:
            # response = {'status' : 404, 'readable_response': 'user not found'}
            # return HttpResponse(json.dumps(response, default=convert), content_type='application/json')
            user_model = LHUser()
            user_model.device_id = device_id
            user_model.dob = dob
            user_model.gender = gender
            user_model.username = device_id #username
            user_model.password = make_password(device_id, None, 'default')  #crypt.crypt(device_id)
            user_model.save()

            registered_user = LHUser.objects.values().filter(device_id=device_id).first()
            user = new_user_oauth(registered_user['id'])

            data = {'status' : 200, 'readable_response' : 'success', 'userinfo': user}
            return Response(data, content_type='application/json')

        user['status'] = 200
        data = {'status' : 200, 'readable_response' : 'success', 'userinfo': user}
        return Response(data, content_type='application/json')

    else:

        data = {'status' : 100, 'readable_response' : 'invalid application'}
        return Response(data, content_type='application/json')


@api_view(["GET"])
@csrf_exempt
def user_info(request):

    user_values = [
        'id',
        'username',
        'gender',
        'username',
        'last_name',
        'first_name',
        'email',
        'profile_img',
    ]

    user_data = request.user;
    user_data = LHUser.objects.values(*user_values).filter(id=user_data.id).first()
    user_data['stars'] = '10'
    user_data['play_duration'] = '09:10:10'
    user_data['profile_img'] = user_data['profile_img'][7:]

    data = {'status': 200, 'readable_response': 'success', 'userRankList': user_data}

    return Response(data, content_type='application/json')


def new_user_oauth(user_id):

        app = LifeHackOAuthApplication()
        app.user_id = user_id
        app.is_local = 1
        app.client_type = 'public'
        app.authorization_grant_type = 'password'
        app.save()

        values = [
            'id',
            'client_id',
            'client_secret',
        ]

        app = LifeHackOAuthApplication.objects.values(*values).filter(user_id=user_id)

        return app

