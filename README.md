# Sir Data - Your Personal Education Butler
This project was developed and prototyped at the X5gon Hackathon for the Good in Paris in February of 2020 by Saskia Bruhn, Marisa Wodrich and Felix Weber. The task was to develop Artificial Intelligence (AI) based technical solutions to unlock Open Educational Resources (OER) to progress towards the 17 Sustainability Goals as defined by the United Nations https://sdgs.un.org/goals.

## 1. Technical prerequisites 
In siddata_backend the code of our django (python) project is located. To make it run on your machine, you need to install
- Python 3.7
- the packages listed in requirements.txt
- download the english google word2vec model at https://github.com/mmihaltz/word2vec-GoogleNews-vectors

## 2. You can install Sir Data locally
1. Set up a Python Environment with Python 3.7.
2. Install the packages in requirements.py
3. Set up a postgreSQL database 
   database: sirdata
       user: sirdata
   password: sirdata
4. Call the manage.py script with the following parameters:
   - python manage.py makemigrations
   - python manage.py migrate
   - python manage.py runserver 0.0.0.0:8000
5. Open your browser and enter http://localhost:8000/sirdata/show_oer 

## 3. Online access
Theoretically Sir Data waits for you in your browser at
[pinky.siddata.de](pinky.siddata.de)
Practically it is quite late in the night now and we need some rest for the pitch...


