
"""
Implementation of the Term Frequency Inverse Document Frequency Algorithm
"""

from backend import models
import random
import nltk
import re
from nltk.text import TextCollection
from nltk.corpus import stopwords
import requests  # for dealing with API
import json  # to deal with json inputs/outputs


# Constant that defines the weighting factor for course title in comparison to description
TITLE_WEIGHT = 3
# Constant that defines how many of the best matching courses are displyed
COURSES_TO_DISPLAY = 5
# If there are many courses with the same score, not all are displayed but in total COURSE_MAX
COURSE_MAX = 10

class RM_coursefinder:
    """ Generates DDC-codes for strings and recommends courses and sessions with similar DDC-codes
    """

    def __init__(self):
        pass


    def get_full_ressource(self):
        # The X5GON API is available at:
        PLATFORM_LAM_URL = "http://wp3.x5gon.org/"
        HEADERS = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }
        rid = 44900
        endpoint = "/recommendsystem/v1"
        data = {"resource_id": rid,
                "n_neighbors": 3,
                "model_type": "doc2vec"}
        response = requests.post(PLATFORM_LAM_URL + endpoint,
                                 headers=HEADERS,
                                 data=json.dumps(data))
        rjson = response.json()
        print(rjson.keys())
        print(rjson['output'].keys())
        print(type(rjson['output']['rec_materials']))

    ####################  TF-IDF-Stuff-Start  #################################


    def preprocess(self, s):
        """ This function cleans strings
            - removes special characters from within a string,
            - sets all characters to lower case

        parameters: s(str): single input string.

        return: preprocessed(str): A string with special characters removed
        """
        stripped = re.sub("[^\w\s]", "", s)
        stripped = re.sub("_", "", stripped)

        stripped = re.sub("\s+", " ", stripped)

        stripped = stripped.strip()

        return stripped.lower()

    def calculate_IDFs(self, courses):
        ''' This function calculates inverse term frequencies for each word in courses
        :param courses: Structure containing courses with title and description
        :return: IDFs A Dictionary containing all words as keys with their inverse document frequencies as values
        '''
        mytexts = []
        IDF_scores = {}
        for course in courses:
            # Title und Text zu einem String zusammenfassen, dabei Titel gewichten
            text = course.title + " " + course.description
            text = self.preprocess(text)
            # initialize Dictionary with all accuring words
            text_without_stopwords = ""
            mystopwords = stopwords.words("english") + stopwords.words("german")
            for word in nltk.word_tokenize(text):
                if word not in mystopwords:
                    IDF_scores[word] = 0.0
                    text_without_stopwords = text_without_stopwords + " %s" % word
            mytexts.append(text_without_stopwords)
        myTextCollection = TextCollection(mytexts)
        for word in IDF_scores:
            IDF_scores[word] = myTextCollection.idf(word)
        return IDF_scores

    def calculate_TF_IDF(self, course, IDF_scores, title_weight):
        ''' This function calculates TF_IDF scores for each word that occurs in title and description
            :param course: Structure with title and description representing a course
            :param IDF_scores: Dictionary with words as keys and IDF_scores as values
            :param title_weight: Factor by which the words in the title are weighted
            :return TF_IDF_scores: Dictionary with words as keys and TF-IDF-values as values
        '''
        if course.description == "" or course.description == None or course.title == "" or course.title == None :
            return {}
        text = "%s " % course.title * title_weight + course.description
        text = self.preprocess(text)
        mystopwords = stopwords.words("english") + stopwords.words("german")
        mywords = nltk.word_tokenize(text)
        TF_IDF_scores = {}
        for word in mywords:
            if word not in mystopwords:
                if word in TF_IDF_scores:
                    TF_IDF_scores[word] += 1
                else:
                    TF_IDF_scores[word] = 1
        for word in TF_IDF_scores:
            TF_IDF_scores[word] = TF_IDF_scores[word] * IDF_scores[word]
        return TF_IDF_scores




    ####################  TF-IDF-Stuff-End  #################################

    def process_activity(self, activity, old_state):
        """
        :param activity:  activity
        :param old_state: Old state as dictionary
        :return: True if successful
        """
        return True



    def generate_matching_courses(self,goal):
        """ Creates COURSES_TO_DISPLAY new Courses and recommends them as activities for user
        :param goal Goal to which the courses are recommended"""

        searchstring = self.preprocess(goal.goal)
        wordlist = nltk.word_tokenize(searchstring)
        relevant_words = []
        mystopwords = stopwords.words("english") + stopwords.words("german")
        for word in wordlist:
            if word not in mystopwords:
                relevant_words.append(word)
        # TODO: Activate in production
        # TODO: For testing find workaround to make local courses available for local test systems
        #user_origin = goal.user.origin
        # TODO: The following two lines have to be exchanged to filter courses according to origin
        #courses = models.Course.objects.filter(origin=user_origin)
        courses = models.Course.objects.all()

        matches = {}
        for course in courses:
            if course == None:
                print("Course is None")
            if course.TF_IDF_scores == {}:
                continue
            score = 0.0
            for word in relevant_words:
                if word in course.TF_IDF_scores:
                    if word in course.TF_IDF_scores:
                        score += course.TF_IDF_scores[word]
            if score > 0.0:
                if score in matches.keys():
                    matches[score].append(course)
                else:
                    matches[score] = []
                    matches[score].append(course)
        scores = list(matches.keys())
        scores.sort()

        bestcourses = []

        i = 0
        for score in scores:
            for course in matches[score]:
                bestcourses.append(course)
                i += 1
            if i >= COURSES_TO_DISPLAY:
                break

        if len(bestcourses) == 0:
            a = models.Activity.objects.get_or_create(
                    title="Keine passenden Lehrveranstaltungen",
                    description="Aktuell gibt es zu Ihrem Interesse keine passenden Lehrveranstaltungen. " \
                                "Siddata wird regelmäßig nach neuen passenden Kursen suchen und diese ggf. hier anzeigen. ",
                    type="todo",
                    goal=goal,
                    image="idea.png",
                    status="new"
            )[0]
            a.save()
        i = 0
        for course in bestcourses:

            a = models.Activity.objects.get_or_create(
                    title=course.title,
                    description=course.description,
                    type="course",
                    goal=goal,
                    image="%s.png" %random.choice(["world","idea","library","cat","brainbulb","braincloud","friends"]),
                    course=course,
                    status="new"
            )[0]
            a.save()
            i += 1
            if i == COURSE_MAX:
                break


