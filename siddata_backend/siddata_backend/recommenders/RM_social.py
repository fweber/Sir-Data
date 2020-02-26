from backend.models import X5gonUser, UserResource
import requests
import json
import copy

class RM_social():
    """
    This class contains user recommender functions for other users.
    """

    def __init__(self):
        """
        Initializes a SocialRecommender.
        """

        self.lam_api = "http://wp3.x5gon.org/"
        self.headers = {'accept': 'application/json', 'Content-Type': 'application/json', }


    def find_similar_users(self, user):

        resource_list = UserResource.objects.filter(user=user).values('resource')

        similar_users = {}
        for res in resource_list:
            sim_us = UserResource.objects.filter(resource=res['resource']).values('user')
            for u in sim_us:
                if u['user'] not in similar_users.keys():
                    similar_users[u['user']] = [res['resource']]
                else:
                    similar_users[u['user']].append(res['resource'])

        return sorted(similar_users, key=lambda k: len(similar_users[k]), reverse=True)


    def find_users_knn(self, resource, k=3):
        endpoint = "/recommendsystem/v1"

        data = {"resource_id": resource,
                "n_neighbors": k,
                "model_type": "doc2vec"}

        response = requests.post(self.lam_api + endpoint,
                                 headers=self.headers,
                                 data=json.dumps(data))
        rjson = response.json()

        knn_resources = rjson['output']['rec_materials']

        potential_users = UserResource.objects.filter(resource=resource)
        users = potential_users.copy()

        for u in potential_users:
            for res in knn_resources:
                if not UserResource.objects.filter(user=u, resource=res).exists():
                    users.remove(u)

        return users


    def calculate_score(self, user):
        endpoint = "/difficulty/conpersec/res"

        user_resources = UserResource.objects.filter(user=user)
        resource_list = []
        for ur in user_resources:
            resource_list.append(int(ur.resource.x5gon_id))
        data = {"resource_ids": resource_list}

        response = requests.post(self.lam_api + endpoint,
                                 headers=self.headers,
                                 data=json.dumps(data))

        rjson = response.json()

        total_score = 0
        i = 0
        for output in rjson['output']:
            total_score += output['value']
            i += 1

        total_score = total_score / i

        return total_score


    def find_experts_on_resource(self, resource):
        experts = UserResource.objects.filter(resource=resource, expert_on=True).values('user')
        return experts




