# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 11:25:03 2018

"""

class Review(object):
    
    def __init__(self):
        self.id = 0
        self.question =""
        self.question_date = ""
        self.question_desc = ""
        self.answer = ""
        self.answer_date = ""
        self.score = 0
        self.postedby = ""
        self.views = ""
        self.subtags = []
        self.url = ""
    
    def to_dict(self):  
        return {
        'id': self.id ,
        'question' :self.question,
        'question_date' :self.question_date ,
        "question_desc": self.question_desc,
        'answer': self.answer ,
        'answer_date': self.answer_date ,
        'score' : self.score ,
        'postedby': self.postedby ,
        'views': self.views  ,
        'subtags': self.subtags,
        'url': self.url
        }
    