from django.conf.urls import url
from django.urls import path
from story.views import (stepList, storyList, contentInfoByStepId, characterInfo, contentList, register_user_step,
                         users_story_rank, profile_upload, UserAnswerPerformance)

urlpatterns = [
    path('step/list', stepList, name='stepList'),
    path('story/list', storyList, name='storyList'),
    path('contentlist', contentList, name='contentList'),
    path('characterInfo', characterInfo, name='characterInfo'), # duriin medeelel
    path('content', contentInfoByStepId, name='contentInfoByStepId'),
    path('register_user_step', register_user_step, name='register_user_step'),
    path('user_rank', users_story_rank, name='userStoryRank'),
    path('profile_upload', profile_upload, name='profile_upload'),
    path('register_answer', UserAnswerPerformance.register_answer, name='register_answer'),
]
