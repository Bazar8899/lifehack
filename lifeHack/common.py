import json
from rest_framework.response import Response

from story.models import UserStory, StoryStep
from user.models import CharacterImage


def clean_data(request, required_keys):

    try:
        json_dict = json.loads(request.body.decode('utf-8'))
    except json.decoder.JSONDecodeError:
        data = {
            'response': 'JSON error',
            'status': 101
        }
        return Response(json.dumps(data), content_type='application/json')

    for key in required_keys:

        if key not in json_dict:

            return Response({
                'status': 121,
                'readable_response' : key + ' key is missing'
            })

    return json_dict


def story_lock_status(story, user):
    values = [
        'id',
    ]

    datalist = UserStory.objects.values(*values).filter(story_id=story, user_id=user)
    data_count = len(datalist)
    return data_count


def viewing_step_count(story, user):

    values = [
        'id',
        'user_id',
        'story_id',
        'step_id',
    ]

    datalist = UserStory.objects.values(*values).filter(story_id=story, user_id=user)
    data_count = len(datalist)
    return data_count


def total_step_count(story):
    values = [
        'id',
    ]

    datalist = StoryStep.objects.values(*values).filter(story_id=story)
    data_count = len(datalist)
    return data_count


def calc_stars(answer_count):
    if answer_count == 0 or answer_count is None:
        return 0
    elif answer_count == 1 or answer_count == 2:
        return 1
    elif answer_count == 3 or answer_count == 4:
        return 2
    elif answer_count == 5 or answer_count == 6:
        return 3


def character_type(type):
    if type == 0:
        return 'Straight'
    elif type == 1:
        return 'Lesbian'
    elif type == 2:
        return 'Gay'
    elif type == 3:
        return 'Transgender'


def get_user_info_by_id(step_id, user_id):
    values = [
        'id',
        'story_id',
        'user_id',
        'step_id',
        'answer_id',
        'type',
    ]

    return UserStory.objects.values(*values).filter(step_id=step_id, user_id=user_id).first()


def character_image(character_id):
    values = [
        'image_s',
        'image_m',
        'image_l'
    ]

    images = CharacterImage.objects.values(*values).filter(character_id=character_id)
    return images[0]['image_l']





