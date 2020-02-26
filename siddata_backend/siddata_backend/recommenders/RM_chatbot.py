from siddata_backend.recommenders.RM_word_to_vec import RM_word_to_vec
from backend import models

THRESHOLD = 0.5

class RM_chatbot():
    """
    Provides algorighms for a natural language interface.
    """
    def get_chat(self,me, you):
        chat = models.ChatHistory.objects.filter(sender__in=[me,you]).order_by("id")
        chathistory = []
        for message in chat:
            if message.sender == me:
                chathistory.append({"me":message.message})
            else:
                chathistory.append({"you":message.message})
        return chathistory


    def answer(self, question=None, correct_answer=None, given_answer=None, user=None):

        Questions = ["Welcome to your learning playground. May I introduce myself?",
                     "My Name is Sir Data. I am your loyal learning buddy. " \
                     "I will select finest information with love just for you." \
                     "May I ask you how you want to be called?",
                     "May I ask you what kind of resources you prefer for learning? " \
                     "It would help me to make appropriate learning recommendations for you."]

        if correct_answer and given_answer:
            rm = RM_word_to_vec()
            score = rm.check_answer(correct_answer,given_answer)
            if score > THRESHOLD:
                r = "The given answer ist correct, well done!     "
            else:
                r = "Very nice try. "

        # if question is sent, answer with next question
        if question:
            i = 1
            for q in Questions:
                if question == q:
                    r.append(Questions[i])
                else:
                    i += 1

        else:
            user = models.X5gonUser.objects.get(id=1)
            sirdata = models.X5gonUser.objects.get_or_create(x5gon_id=99, name="Sir Data", country="Terra",
                                                             interests="Knowledge and wisdom")[0]
            # get questions that have been asked
            questions = models.ChatHistory.objects.filter(sender=sirdata,receiver=user)

            i = 0
            for question_togo in Questions:
                for question_asked in questions:
                   if question_asked == question_togo:
                         continue
                   else:
                        return question_togo
            return "Well done. All questions have been answered."


            i = 1
            for q in Questions:
                if question == q:
                    r.append(Questions[i])
                else:
                    i += 1


        return(r)

