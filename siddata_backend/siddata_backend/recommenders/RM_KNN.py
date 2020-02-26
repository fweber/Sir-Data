import plotly.io as pio
pio.renderers.default = "colab"

import cufflinks as cf # to directly bind pandas and plotly

import requests # for dealing with API
import json # to deal with json inputs/outputs


cf.go_offline() # set plotly to offline mode

class KNNRecommender():

    def __init__(self):
        self.lam_api = "http://wp3.x5gon.org/"
        self.endpoint = "/recommendsystem/v1"
        self.headers = {'accept': 'application/json', 'Content-Type': 'application/json',}


    def KNN(self, resource_id, k):
        data = 	{"resource_id": resource_id,
                   "n_neighbors": k,
                   "model_type": "doc2vec"}

        response = requests.post(self.lam_api + self.endpoint,
                                 headers=self.headers,
                                 data=json.dumps(data))
        rjson = response.json()

        return rjson['output']['rec_materials']





