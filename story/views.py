import json
import random
import string
import base64
from django.core.files.base import ContentFile

from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.db.models import QuerySet
from django.views.decorators.http import require_POST
from rest_framework.views import APIView

from .models import StoryStep, Content, UserStory, Story, Answer
from user.models import CharacterImage, LHUser
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from datetime import datetime, timedelta

from lifeHack.common import clean_data, viewing_step_count, total_step_count, story_lock_status, calc_stars, \
    character_type, get_user_info_by_id, character_image

from rest_framework.decorators import api_view


# Create your views here.


@api_view(["GET"])
@csrf_exempt
def characterInfo(request):

    if not request.GET.__contains__('character_id'):
        data = {'response': 'story id is missing', 'status': 121, 'users' : list()}
        return HttpResponse(json.dumps(data), content_type='application/json')

    character_id = request.GET['character_id']

    if not character_id:
        data = {'response': 'success', 'status': 100, 'users' : list()}
        return Response(data, content_type='application/json')
    
    values = [
        'id',
        'character__name',
        'image_s',
        'image_m',
        'image_l',
        'character__avatar_img_s',
        'character__avatar_img_m',
        'character__avatar_img_l',
        'character__gender',
        'character__age',
        'character__character_type',
    ]

    character_image_list = CharacterImage.objects.values(*values).filter(character_id=character_id)

    for character_info in character_image_list:
        character_info['character_type_text'] = character_type(character_info['character__character_type'])
    
    data = {'status' : 200, 'readable_response': 'success', 'characterInfo': character_image_list}
    return Response(data, content_type='application/json')


@api_view(["GET"])
@csrf_exempt
def contentList(request):

    values = [
        'id',
        'type',
        'position',
        'transition',
        'width',
        'height',
        'direction',
        'bg_color',
        'text_color',
        'bubble_type',
        'step__background',
        'step__story__character__avatar_img_s',
        'step__story__character__avatar_img_m',
        'step__story__character__avatar_img_l',
        'step__story__character__gender',
        'step__story__character__age',
        'content_name',
        'content_image_s',
        'content_image_m',
        'content_image_l',
        'content',
        'question__question',
    ]

    storylist = Content.objects.values(*values)
    
    data = {'status' : 200, 'readable_response': 'success', 'storylist' : storylist}
    return Response(data, content_type='application/json')


@api_view(["GET"])
@csrf_exempt
def storyList(request):

    user = request.user
    user_id = user.id

    customStoryList = list()

    values = [
        'id',
        'character_id',
        'order_num',
        'is_publish',
        'updatedAt',
        'character__name',
        'character__avatar_img_s',
        'character__avatar_img_m',
        'character__avatar_img_l',
        'character__gender',
        'character__age',
        'character__character_type',
    ]

    for story in Story.objects.values(*values).order_by('order_num'):

        story['character_image'] = character_image(story['character_id'])
        story['character_type_text'] = character_type(story['character__character_type'])
        story['viewing_steps'] = viewing_step_count(story['id'], user_id)
        story['totals_steps'] = total_step_count(story['id'])

        if request.GET.__len__() > 0:

            update_date = request.GET['update_date']
            update_date_db = story['updatedAt']
            update_date_db = format(update_date_db)

            if update_date == '':
                customStoryList.append(story)
            else:
                update_date = format(update_date)

                update_date_date = datetime.fromisoformat(update_date)
                update_date_date = update_date_date + timedelta(0,60)
                update_date = str(update_date_date)

                if update_date < update_date_db:
                    customStoryList.append(story)
        else:
            customStoryList.append(story)

    final_custom_story_list = list()

    for story in customStoryList:

        story['total_answers'] = 6
        story['viewing_answers'] = 1

        story['locked'] = story_lock_status(story['id'], user_id)

        if story['viewing_answers'] <= 6:
            story['stars'] = calc_stars(story['viewing_answers'])
        else:
            story['stars'] = calc_stars(0)

        final_custom_story_list.append(story)

    last_updated = Story.objects.latest('updatedAt')
    
    data = {'status': 200, 'update_date': last_updated.updatedAt, 'storylist': customStoryList}
    return Response(data, content_type='application/json')


@api_view(["GET"])
@csrf_exempt
def stepList(request):

    if not request.GET.__contains__('story_id'):
        data = {'response': 'story id is missing', 'status': 121, 'users' : list()}
        return HttpResponse(json.dumps(data), content_type='application/json')

    story_id = request.GET['story_id']

    if not story_id:
        data = {'response': 'success', 'status': 100, 'users' : list()}
        return Response(data, content_type='application/json')

    last_updated = StoryStep.objects.latest('updatedAt')
    
    values = [
        'id',
        'story_id',
        'background',
        'name',
        'updatedAt',
        'order_num',
        'next_step',
        'prev_step',
    ]

    if request.GET.__len__() > 1:
        if request.GET['update_date'] != '':
            update_date_date = datetime.fromisoformat(request.GET['update_date'])
            update_date_date = update_date_date + timedelta(0, 60)
            update_date = str(update_date_date)
            step_list = StoryStep.objects.values(*values).filter(updatedAt__gt=update_date, story_id=story_id)
        else:
            step_list = StoryStep.objects.values(*values).filter(story_id=story_id)
    else:
        step_list = StoryStep.objects.values(*values).filter(story_id=story_id)
    
    step_list = list(step_list)
    custom_story_list = list()

    for story_step in step_list:
        story_step['content'] = contentData(story_step['id'])
        custom_story_list.append(story_step)

    data = {'status' : 200, 'readable_response': 'success', 'update_date': last_updated.updatedAt,'steplist' : custom_story_list}
    return Response(data, content_type='application/json')


@csrf_exempt
@api_view(["GET"])
def contentInfoByStepId(request):

    if not request.GET.__contains__('step_id'):
        data = {'response': 'story id is missing', 'status': 121, 'users' : list()}
        return Response(data, content_type='application/json')

    step_id = request.GET['step_id']

    if not step_id:
        data = {'response': 'success', 'status': 100, 'users' : list()}
        return Response(data, content_type='application/json')
    
    # values = [
    #     'id',
    #     'story_id',
    #     'background',
    #     'name',
    #     'next_step',
    #     'prev_step',
    # ]

    content = Content.objects.values().filter(step_id=step_id)
    
    content = list(content)
    
    if len(content) == 0:
        data = {'status' : 100, 'readable_response': 'success', 'content' : content}
    else:
        data = {'status' : 200, 'readable_response': 'success', 'content' : content}
    return Response(data, content_type='application/json')


def contentData(step_id):
    values = [
        'id',
        'type',
        'position',
        'transition',
        'width',
        'height',
        'direction',
        'bg_color',
        'text_color',
        'bubble_type',
        'step__background',
        'step__story__character__avatar_img_s',
        'step__story__character__avatar_img_m',
        'step__story__character__avatar_img_l',
        'step__story__character__gender',
        'step__story__character__age',
        'content_name',
        'content_image_s',
        'content_image_m',
        'content_image_l',
        'content',
        'question__question',
        'question_id',
    ]

    content_list = list()

    data = Content.objects.values(*values).filter(step_id=step_id)
    for question in data:
        question['answer'] = answer_by_question(question['question_id'])
        content_list.append(question)
    return data


def answer_by_question(question_id):
    values = [
        'id',
        'answer',
        'step_id',
    ]

    data = Answer.objects.values(*values).filter(question_id=question_id)
    return data


@require_POST
@login_required
@csrf_exempt
def register_user_step(request):

    try:
        # user = request.user
        json_dict = json.loads(request.body.decode('utf-8'))
        user_id = json_dict['user_id']
        story_id = json_dict['story_id']
        step_id = json_dict['step_id']
        answer_id = json_dict['answer_id']

    except Exception as e:
        data = {
            'response': 'parameter is missing',
            'status': 102,
            'exception' : str(e)
        }
        return Response(data, content_type='application/json')

    if not step_id or not story_id or not step_id:

        data = {
            'response': 'parameter is missing',
            'status': 102,
            'exception' : str(e)
        }
        
        return Response(json.dumps(data), content_type='application/json')

    user_story = UserStory()

    user_story.user_id = user_id
    user_story.story_id = story_id
    user_story.step_id = step_id
    user_story.answer_id = answer_id
    user_story.save()

    step_user = get_user_info_by_id(step_id, user_id)

    data = {'status': 200, 'readable_response': 'success', 'step_user': step_user}
    # return Response(data)
    return HttpResponse(json.dumps(data), content_type='application/json')


@api_view(["GET"])
@csrf_exempt
def users_story_rank(request):
    values = [
        'id',
        'user_id',
        'story_id',
    ]

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

    top_user_list = list()
    user_story_list = UserStory.objects.values(*values).order_by('user_id')[:10]
    for user in user_story_list:
        user_info = LHUser.objects.values(*user_values).filter(id=user['user_id'])

        if len(user_info) > 0:
            user['username'] = user_info[0]['username']
            user['last_name'] = user_info[0]['last_name']
            user['first_name'] = user_info[0]['first_name']
            user['email'] = user_info[0]['email']
            if user_info[0]['profile_img'][7:] == "":
                temp_url = "media/character/avatar_l/Group_1991.png"
            else:
                temp_url = user_info[0]['profile_img'][7:]
            user['profile_uri'] = temp_url
            user['rank'] = 35
            top_user_list.append(user)

    data = {'status': 200, 'readable_response': 'success', 'count': len(top_user_list), 'userRankList': top_user_list}

    return Response(data, content_type='application/json')


@require_POST
@login_required
@csrf_exempt
def profile_upload(request):

    json_dict = json.loads(request.body.decode('utf-8'))
    image_string = json_dict['profile_img']
    ext = image_string.split('/')[-1]

    data_image = ContentFile(base64.b64decode(image_string), name='temp.' + ext)

    profile_img = data_image
    fs = FileSystemStorage()
    filename = fs.save("media/profile/" + random_string(30) + ".png", profile_img)
    user_data_value = request.user
    user_data_value.profile_img = fs.url(filename)
    user_data_value.save()
    data = {'status': 200, 'readable_response': 'success'}

    return HttpResponse(data, content_type='application/json')


def random_string(string_length=30):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


class UserAnswerPerformance(APIView):

    @csrf_exempt
    def register_answer(request):
        user_id = request.user.id
        # user_id = request.GET.get('user')
        story_id = request.GET.get('story')
        data_type = int(request.GET.get('type'))

        if data_type == 1:
            step_id = request.GET.get('step')
            answer_id = None
        elif data_type == 2:
            step_id = None
            answer_id = request.GET.get('answer')

        UserStory.objects.create(
            user_id=user_id,
            story_id=story_id,
            step_id=step_id,
            answer_id=answer_id,
            type=data_type,)

        return HttpResponse(status=200, content_type='application/json')



