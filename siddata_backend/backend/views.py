from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.db.models import Count
from .models import X5gonResource
from backend import models
from backend.models import UserResource, X5gonResource, X5gonUser, ChatHistory
from siddata_backend.recommenders.RM_social import RM_social
from siddata_backend.recommenders.RM_chatbot import RM_chatbot
import requests


def home(request):
    """Start page.

    :param request The view's request object."""

    page = 'home'  # for highlighting navbar entry
    return render(request, "backend/home.html")




def show_oer(request):
    """Display OER interface

    :param request The view's request object.
    :returns renderable response from form template
    """
    page = 'show OER'

    # Incoming stuff
    requestDIC=request.POST

    #message = requestDIC.get("message")

    user = models.X5gonUser.objects.get(id=1)
    usrimage = "/static/images/profile1.png"

    sirdata = models.X5gonUser.objects.get_or_create(x5gon_id=99, name="Sir Data", country="Terra", interests="Knowledge and wisdom")[0]
    sirdata.save()
    # if message:
    #     m = models.ChatHistory.objects.get_or_create(sender=user,receiver=sirdata,message=message)[0]
    #     m.save()
    #
    # rm = RM_chatbot()
    # answer = rm.answer()

    # m = models.ChatHistory.objects.get_or_create(sender=sirdata, receiver=user, message=answer)[0]
    # m.save()


    chatpartners = [user,sirdata]

    if len(models.ChatHistory.objects.filter(sender__in=chatpartners))>0:
        pass
        #print("chat history for user not empty")
    else:
        startmessage = models.ChatHistory.objects.get_or_create(
            sender=sirdata,
            receiver=user,
            message="Welcome to your learning playground. May I introduce myself?"
        )[0]
        startmessage.save()
    rm = RM_chatbot()
    Chat_History = rm.get_chat(me=user, you=sirdata)


    Chat_History = [
        {"you":"Welcome to your learning playground. May I introduce myself?"\
              "My Name is Sir Data. I am your loyal learning buddy. "\
              "May I ask you how you want to be called?"},
        {"me":"My name ist Amal Kumar"},
        {"you": "May I ask you what kind of resources you prefer for learning? Texts or Videos or...?" \
                "It would help me to make appropriate learning recommendations for you."}
    ]
    return render(request,"backend/oer_interface.html",locals())


def learning_content(request):

    user = X5gonUser.objects.get(id=1)

    PLATFORM_URL = "https://platform.x5gon.org/api/v1"
    get_materials_endpoint = "/oer_materials/"


    OER = []
    resources = UserResource.objects.filter(user=user).values('resource')
    # print(resources)
    for res in resources:
        r = X5gonResource.objects.get(id=res['resource'])
        x5gon_id = r.x5gon_id
        response = requests.get(PLATFORM_URL + get_materials_endpoint + x5gon_id)
        r_json = response.json()
        description = str(r_json['oer_materials']['description'])
        url = r_json['oer_materials']['url']
        crown = UserResource.objects.get(user=user, resource=r).crown
        OER.append({'title': r.title,
                    'description' : description,
                    'type': r.type,
                    'language': r.language,
                    'crown:': crown,
                    'url': url})




    return render(request,"backend/learning_content.html",locals())




def backend_js(request):
    return render(request, "backend/backend.js", locals())

def learning_buddies(request):
    mentor = False
    interests = False
    requestDict  =request.POST
    social_rec = RM_social()
    user = X5gonUser.objects.get(id=1)
    users_resources = UserResource.objects.filter(user=user)
    resources = []
    for ur in users_resources:
        resources.append(ur.resource)

    similar_interest_users = social_rec.find_similar_users(user)
    similar_interest_users.remove(user.id)

    Buddies = []

    if not requestDict.keys():
        mentor = False
    elif 'interests' in requestDict.keys():
        interests = True
        mentor = False
        title='Find people with similar interests'
        for i in similar_interest_users:
            user = X5gonUser.objects.get(id=i)
            score = int(social_rec.calculate_score(user)*100)
            Buddies.append({'name': user.name,
                            'country': user.country,
                            'interests': user.interests,
                            'score': score,
                            'image': '/static/images/profile'+str(int(user.id))+'.png'})
            Buddies.reverse()
    elif 'mentor' or 'dropdown' in requestDict.keys():
        mentor = True
        title = 'Find a new Mentor'

        if 'dropdown' in requestDict.keys():
            resource = X5gonResource.objects.get(id=int(requestDict['dropdown']))
            experts = social_rec.find_experts_on_resource(resource)[:3]

            if user.id in experts.values():
                experts.remove({'user': user.id})

            for i in experts:
                if i['user'] != user.id:
                    exp = X5gonUser.objects.get(id=i['user'])
                    score = int(social_rec.calculate_score(exp) * 100)
                    Buddies.append({'name': exp.name,
                                     'country': exp.country,
                                     'interests': exp.interests,
                                     'score': score,
                                     'image': '/static/images/profile' + str(int(exp.id)) + '.png'})

    return render(request, "backend/learning_buddies.html", locals())


def profile(request):
    social_rec = RM_social()
    user = X5gonUser.objects.get(id=1)
    usrimage = "/static/images/profile1.png"
    score = int(social_rec.calculate_score(user) * 100)

    usrres = UserResource.objects.get(user=user, crown=True)

    Badges = []

    Badges = [
              {"name": "Introduction to Mechanics for Robotics", },
              {"name": "Mechatronics and its Discontents", },
              ]

    return render(request, "backend/profile.html", locals())

def learning_playground(request):


    Chat_History = [
        {"you":"Here comes your first question: "\
              'By which physical concept can the pendulum be described?'},
        {"me":'Harmonic Oscillator'},
        {"you": "This answer is absolutely correct!"},
        {"you": 'Please provide the formula for the force constant.'}
        ]

    return render(request, "backend/learning_playground.html", locals())
