# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 20:19:03 2018
@author: BIA-660 Team 2
"""

import so_scrapper as scrapper



if __name__ == '__main__':
    
    csvfilename = 'so-reviews.csv'
    
    #***Data Preparation***
    #Scrapping data from stackoverflow
    scrapper.scrape_write(csvfilename)
    
    
    
    
    