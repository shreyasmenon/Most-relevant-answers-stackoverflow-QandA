
# coding: utf-8

# In[ ]:


import classes
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import csv
import requests
from bs4 import BeautifulSoup
import time

#Required column attributes
columns = ['id','question','question_date','question_desc','answer','answer_date','score','postedby','views','subtags','url']

#initializing chrome driver
driver = webdriver.Chrome(executable_path= 'C:/Users/sarvesh/Downloads/chromedriver_win32/chromedriver')

driver.get("https://stackoverflow.com/")
# Wait 20 seconds for page to load
timeout = 20
try:
    WebDriverWait(driver, timeout)
except TimeoutException:
    print("Timed out waiting for page to load")
    driver.quit()

topic = "six sigma" #similarly we'll have list of other topics
elem = driver.find_element_by_name("q")
elem.clear()
elem.send_keys(topic)
elem.send_keys(Keys.RETURN)
driver.find_element_by_xpath('//*[@title="show 50 items per page"]').click()


list_reviews = []
review_id = 0

while True:    
    links=[]
    list_links = driver.find_elements_by_tag_name('a')
    for i in list_links:
        links.append(i.get_attribute('href'))

    linksf=[]
    for i in range(0,len(links)):
        if type(links[i]) == str:
            linksf.append(links[i])


    ml=[]
    for i in range (0,len(linksf)):
        tokens1=linksf[i].split("/")
        for j in tokens1:
            if j == "questions":
                ml.append(linksf[i])


    no_ques=[]
    for i in range (0,len(ml)):
            tokens1=ml[i].split("/")
            for j in tokens1:
                if j != "tagged" and j == "stackoverflow.com":
                    no_ques.append(ml[i]) # I want

    no_ques2=[]
    for i in range (0,len(no_ques)):
            tokens1=no_ques[i].split("/")
            for j in tokens1:
                if j == "tagged":
                    no_ques2.append(no_ques[i])

    final_url  = [x for x in no_ques if x not in no_ques2]

    no_ques3_final=[]
    for i in range (0,len(final_url)):
            tokens1=final_url[i].split("/")
            if len(tokens1) > 5:
                no_ques3_final.append(final_url[i])

    for i in range (0,len(no_ques3_final)):    
        c=no_ques3_final[i]
        site = requests.get(c);

        if site.status_code is 200:
            soup = BeautifulSoup(site.content, 'html.parser')
        
            #find list of all associated tag links
            tagLinks = soup.find(class_ = 'post-taglist').select('a')

            #incrementing the id
            review_id += 1
         
            #instantiating the class
            review = classes.Review()
        
            #populating review properties
            review.id = review_id
            review.question = soup.find(class_='question-hyperlink').get_text(strip=True)
            review.question_desc = soup.find(class_='post-text').get_text(strip=True)        
            review.url =   soup.find(class_='question-hyperlink').get('href').strip()
            review.views = str(soup.find(class_='module question-stats').findAll('b')[1].get_text(strip=True)).replace('times','')
            review.score = soup.find(class_='vote-count-post ').get_text(strip=True)
            review.subtags  = [ tags.get_text() for tags  in tagLinks ]
        
            review_anchor = (soup.find(class_ = 'user-details').find('a'))
            if(review_anchor is not None ):
                review.postedby = review_anchor.get_text()
        
            review.question_date = (soup.find(class_ = 'user-action-time').select('span')[0])['title']
        
            try:
                review.answer = soup.find("div", class_="answercell post-layout--right").find("div", class_="post-text").get_text(strip=True)
                review.answer_date = (soup.find("div", class_="answercell post-layout--right").find("div", class_="user-action-time").select('span')[0])['title']
            except:
                pass
        
            list_reviews.append(review)
            
    #find next button        
    try:
        next_pagebutton = driver.find_element_by_xpath('//*[@rel="next"]')            
        next_pagebutton.click()                
        #wait for 10 seconds for page to load
        time.sleep(10)
        continue
    except:        
        #break the while loop after all the entries have been appended    
        break
            


#writing the populated list into csv
with open('so-reviews.csv', 'w',encoding="utf-8",newline='',) as file:
      
    print("writing {0} reviews in file so-reviews.csv.. ".format(len(list_reviews)))
    writer = csv.DictWriter(file, fieldnames = columns, delimiter = ',')
    writer.writeheader()
    for row in list_reviews:
        writer.writerow(row.to_dict())


# In[ ]:


from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
import string
from nltk.corpus import stopwords
import nltk
import csv
from nltk.stem.porter import PorterStemmer
import numpy as np
import pandas as pd
from sklearn.preprocessing import normalize
from scipy.spatial import distance


def get_doc_tokens(doc,normalize):
    
    # gets the stop_words
    stop_words = stopwords.words('english')
    porter_stemmer = PorterStemmer()
    if normalize=="stem":
        tokens=[porter_stemmer.stem(token.strip())                 for token in nltk.word_tokenize(doc.lower())                 if token.strip() not in stop_words and                   token.strip() not in string.punctuation]
        
    else:
        tokens=[token.strip()                 for token in nltk.word_tokenize(doc.lower())                 if token.strip() not in stop_words and                   token.strip() not in string.punctuation]
        
    
    
    token_count={token:tokens.count(token) for token in set(tokens)}
    
    
    return token_count

def tfidf(docs,normalize):
    
    #  process all documents to get list of token list
    docs_tokens={idx:get_doc_tokens(doc,normalize)              for idx,doc in enumerate(docs)}

    # get document-term matrix
    dtm=pd.DataFrame.from_dict(docs_tokens, orient="index" )
    dtm=dtm.fillna(0)
      
    # get normalized term frequency (tf) matrix        
    tf=dtm.values
    doc_len=tf.sum(axis=1)
    tf=np.divide(tf.T, doc_len).T
    
    # get idf
    df=np.where(tf>0,1,0)
    
   

    smoothed_idf=np.log(np.divide(len(docs)+1, np.sum(df, axis=0)+1))+1    
    smoothed_tf_idf=tf*smoothed_idf
    
    # finds the similarity among documents
    
    similarity = 1-distance.squareform(distance.pdist(smoothed_tf_idf, 'cosine'))
    similar_docs = np.argsort(similarity)[:,::-1][0,0:7]
    
    #prints top six documents equivalent to the recived indexes
    print(similar_docs)
    
    for idx,doc in enumerate(docs):
        if idx in similar_docs:
            print(idx,doc)
    
    
    return None


# In[ ]:


import nltk
import csv

if __name__ == "__main__":
    docs=[]
    with open("so-reviews.csv","r",encoding="utf-8") as f:
        reader=csv.reader(f)
        
        for line in reader:
            docs.append(line[4])
    print("\n Reviews with Stemming \n ")
    
    tfidf(docs,"stem")

