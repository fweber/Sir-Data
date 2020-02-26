import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'siddata_backend.settings')
django.setup()

import requests # for dealing with API
import json # to deal with json inputs/outputs

from backend.models import X5gonResource, X5gonUser, UserResource
import numpy as np
import scipy.cluster.hierarchy as hcluster


def hierarchical_clustering(data):
    thresh = 1.5
    clusters = hcluster.fclusterdata(data, thresh, criterion="distance")
    print(clusters)

def calculate_difficulty():
    lam_api = "http://wp3.x5gon.org/"
    endpoint = "/difficulty/conpersec/res"
    headers = {'accept': 'application/json', 'Content-Type': 'application/json', }

    user = X5gonUser.objects.get(x5gon_id='3')
    user_resources = UserResource.objects.filter(user=user)
    resource_list = []
    for ur in user_resources:
        resource_list.append(int(ur.resource.x5gon_id))
    data = {"resource_ids": resource_list}

    response = requests.post(lam_api + endpoint,
                             headers=headers,
                             data=json.dumps(data))
    print(response.json())

    rjson = response.json()

    total_score = 0
    i = 0
    for output in rjson['output']:
        total_score += output['value']
        i += 1

    total_score = total_score / i
    print(total_score)

def find_similar_users():
    user = X5gonUser.objects.get(x5gon_id='1')
    user_resources = UserResource.objects.filter(user=user)
    resource_list = []
    for ur in user_resources:
        resource_list.append(int(ur.resource.x5gon_id))
    similar_users = {}
    ordered_users = {}
    print(resource_list)
    for res in resource_list:
        sim_us = UserResource.objects.filter(resource=res.resource)
        for u in sim_us:
            if u.user not in similar_users.keys():
                similar_users[u.user] = [res]
            else:
                similar_users[u].append(res)

    return sorted(similar_users, key=lambda k: len(similar_users[k]), reverse = True)

print(X5gonResource.objects.get(x5gon_id='30289').title)

#
# data = []
# resources = X5gonResource.objects.all()
# keywords = []
# for res in resources:
#      for k in res.keywords:
#          keywords.append(k)
#
# print(len(keywords))
# keywords = list(set(keywords))
# print(len(keywords))
#
# for res in resources:
#     vec = np.zeros(len(keywords))
#     for kw in res.keywords:
#         vec[keywords.index(kw)] = 1
#
#     data.append((res.id, vec))
#
#     # print(res.keywords)
#     # for i, x in enumerate(vec):
#     #     if x==1:
#     #         print(keywords[i])
#     # break
#
# data = np.array(data)
#
# hierarchical_clustering(data)
#


