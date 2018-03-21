
# coding: utf-8

# In[4]:


import csv
import requests
from bs4 import BeautifulSoup
dict_list=[]
site = requests.get('https://stackoverflow.com/');
if site.status_code is 200:
    content = BeautifulSoup(site.content, 'html.parser')
    questions = content.find_all(class_='question-summary')
    for question in questions:
        topic = question.find(class_='question-hyperlink').get_text()
        url =   question.find(class_='question-hyperlink').get('href')
        views = question.find(class_='views').find(class_='mini-counts').find('span').get_text()
        answers = question.find(class_='status').find(class_='mini-counts').find('span').get_text()
        votes = question.find(class_='votes').find(class_='mini-counts').find('span').get_text()
        updated_data = {"topic": topic, "url": url, "views": views, "answers":answers, "votes":votes}
        dict_list.append(updated_data)
    with open ('find.csv','w') as file:
        writer = csv.DictWriter(file, fieldnames = ["topic", "url", "views", "answers", "votes"], delimiter = ',')
        writer.writeheader()
        for row in dict_list:
            writer.writerow(row) 

