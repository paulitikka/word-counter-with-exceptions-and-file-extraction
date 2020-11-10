# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 14:16:40 2020

@author: pauli
"""
# Task 1.

# Extract the following journal peer review data for each (available) article from 
# BMJ, PLOS Medicine, and BMC between January 15 2019 and January 14 2020, and use also google searches: 

(fyi, this file may be excessive)

#(1) The quality of preventive care for pre-school aged children in Australian general practice
#(2) Louise K. Willes
#(3) 6.12.2019
#(4) 3 reviewers
#(5) Dagmar Haller 
#(6) (366 words), 
#(7a optional) MD PhD, University of Geneva
#(8) Lena Sanci 
#(9) (621 words), 
#(9a optional) Prof., Director, University of Melbourne
#(10) Lisa Whitehead 
#(11) (77 words), 
#(11a optional)Prof., Dean, Edith Cowan University Western Australia

#%%
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
import pandas as pd #for importing files
# https://pandas.pydata.org/pandas-docs/version/0.18.1/generated/pandas.DataFrame.html
import numpy as np  #for calculations, array manipulations, and fun :)
import matplotlib.pyplot as plt #for scientifical plots
import os
#%%https://developers.google.com/edu/python/regular-expressions
#https://docs.python.org/3/library/urllib.request.html
#https://bmcmedicine.biomedcentral.com/articles?tab=keyword&searchType=journalSearch&sort=PubDateAscending&volume=17&page=1
    
urln_all='https://bmcmedicine.biomedcentral.com/articles?tab=\
keyword&searchType=journalSearch&sort=PubDateAscending&volume=17&page=1'
urln_all2='https://bmcmedicine.biomedcentral.com/articles?tab=\
keyword&searchType=journalSearch&sort=PubDateAscending&volume=17&page=2'
urln_all3='https://bmcmedicine.biomedcentral.com/articles?tab=\
keyword&searchType=journalSearch&sort=PubDateAscending&volume=17&page=3'
urln_all4='https://bmcmedicine.biomedcentral.com/articles?tab=\
keyword&searchType=journalSearch&sort=PubDateAscending&volume=17&page=4'
urln_all5='https://bmcmedicine.biomedcentral.com/articles?tab=\
keyword&searchType=journalSearch&sort=PubDateAscending&volume=17&page=5'

#%Here all combined..
utot=[urln_all,urln_all2,urln_all3,urln_all4,urln_all5]
soupn=[]
responsen=[]
one_a_tagn=[]
for i in range(0,len(utot)):
    responsen = requests.get(utot[i])
    soupn = BeautifulSoup(responsen.text, 'html.parser')
    one_a_tagn.append(soupn.findAll('a')) #ok

mylistn=[]
for j in range(0,len(one_a_tagn)):   
#https://stackoverflow.com/questions/13187778/convert-pandas-dataframe-to-numpy-array
    for i in range(0, len(one_a_tagn[j])):
        mylistn.append((one_a_tagn[j][i]['href'])) #this has all

#%First) Goal would to print all the all articles' peerrieview sigths
#It is every third that we want to print from the list..starting from the first
inda=[]
for i in range(0, len(mylistn)):  
    str = mylistn[i]
    match = re.search(r'track/pdf/10.', str)
# If-statement after search() tests if it succeeded
    if match:
#        print('found', match.group()) ## 'found word:cat'
        inda.append(i-2)
        print(i-2)  #this is ok
     
thelistn=pd.DataFrame(mylistn)
thelistn=thelistn.ix[inda]    
pr='/open-peer-review'

#%The first level for all one article's reviews:this is ist
download_url = 'https://bmcmedicine.biomedcentral.com'+ thelistn+pr  
#the download has the links to all reviews of single paper, but need to fethc one by one  
#%download_url had comhttps that need to go
inda=[]
for i in range(0, len(download_url)):  
    str = download_url.iloc[i][0]
    match = re.search(r'comhttp', str)
# If-statement after search() tests if it succeeded
    if match:
        inda.append(i) 
        print(i)  #this is ok
#%
download_url=download_url.drop(download_url.index[inda],axis=0) 
#https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.drop_duplicates.html
download_url=download_url.drop_duplicates() #the number is 227, while yesterday it was 226...    
#%%This loop seem to be working below (24.1.2020), This takes 10 min, before enter, check if you already have what you need
for i in range(0,len(download_url.index)):
    url=[]
    url=download_url.ix[download_url.index[i],0]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    one_a_tag = soup.findAll('a')
    link=[]
    for i in range(0,len(one_a_tag)):
        link.append(one_a_tag[i]['href'])

    ind=[]
    for i in range(0, len(link)):  
        str = link[i]
        match = re.search(r'Report_V0', str)
        if match:
            ind.append(i)

    linka=pd.DataFrame(link)
    for i in range(0,len(ind)):
        urllib.request.urlretrieve(linka.ix[ind[i],0], filename='C:\\python\\BMC\\'+linka.ix[ind[i]][0][-40:])
#        time.sleep(1)

#%%There are two ways to do this. Either converge all the files as one, or import them separately as a big pands frame.
# The method one:
#%% Read all files with pdf to word and compress program, e.g.WPS PDF to Word
#the change the compressed doc to csv:
#https://convertio.co/de/docx-csv/
#https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
#https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.dropna.html
#https://stackoverflow.com/questions/22765313/when-import-docx-in-python3-3-i-have-error-importerror-no-module-named-excepti
directory="C:\python\BMC\merge.csv"
dataframes = pd.read_csv(directory, header=None)
dataframes=dataframes.dropna()
#https://chrisalbon.com/python/data_wrangling/pandas_list_unique_values_in_column/   
#https://www.guru99.com/python-regular-expressions-complete-tutorial.html#3

#The method two: 
#%%Now I need to do I loop for all files, and save the results
directory="C:\python\BMC\*.docx"
import glob
dataframes = []
all_files2=(glob.glob(directory))
# Create the list for the three DataFrames you want to create:
#%%
for filename in all_files2:
    dataframes.append(pd.read_csv(filename))
#% Scaling to experimental frame (Combes et al. 2016)
#% In case column names are misplaces (during calculations)
#%%
#% This is how I import docx files:
import docx2txt
result=[]
result = docx2txt.process(all_files2[451])
#% Scaling to experimental frame (Combes et al.
#%This worked:
#https://stackoverflow.com/questions/13169725/how-to-convert-a-string-that-has-newline-characters-in-it-into-a-list-in-python
#%
r2=[]
r2=result.splitlines()
#https://stackoverflow.com/questions/4842956/python-how-to-remove-empty-lists-from-a-list
list2 =[]
list2 = [e for e in r2 if e] 
list2=[x.split("\t") for x in list2]
list2 = [e for e in list2 if e]
#%
#% This is how you delete lists:
#https://www.geeksforgeeks.org/list-methods-in-python-set-2-del-remove-sort-insert-pop-extend/
for i in range(len(list2)):
    if list2[i][0] == '':
        del list2[i][0]
for i in range(len(list2)):
    if list2[i][0] == '':
        del list2[i][0]
#% The pandas are better to handle data (in functions) than list of lists (according to my experience):
df=pd.DataFrame(list2)

#%%Once you have the dataframe well extracted, the below function it should work:
def words2(df):
    #%
    io=[]
    xx=[]
    for i in range(0, len(df)):
        str = (df.iloc[i])
        match1 = re.search(r'Reviewer\'s report:', str)
        match2 = re.search(r'Are the methods appropriate and well described?', str)
        match3 = re.search(r'https://', str)
        match4 = re.search(r'Does the work include the necessary controls?', str)
        match5 = re.search(r'Are the conclusions drawn adequately supported by the data shown?', str)
        match6 = re.search(r'Are you able to assess any statistics in the \
                      manuscript or would you recommend an additional statistical review?', str)
        match7 = re.search(r'I am able to assess the statistics', str)
        match8 = re.search(r'Quality of written English', str)
        match8b = re.search(r'Acceptable', str)
        match9 = re.search(r'Declaration of competing interests', str)
        match10 = re.search(r'I declare that I have no competing interests.', str)  
        if match1:
            io.append(i)
        elif match2:
            io.append(i)
        elif match3:
            io.append(i*100000)
            #%
        elif match4:
            io.append(i)
        elif match5:
            io.append(i)
        elif match6:
            io.append(i)
        elif match7:
            io.append(i)
        elif match8:
            io.append(i)
        elif match8b:
            io.append(i)
        elif match9:
            io.append(i)
        elif match10:
            io.append(i)
    io.append(len(df))
            #%
    for i in range(0,len(io)):
        if io[i]>100000:
            io[i]=io[i]/100000
    dx= [0]
#    https://stackoverflow.com/questions/3525953/check-if-all-values-of-iterable-are-zero
    #%
    for i in range(0,len(io)):
        if isinstance(io[i], float):
           dx.append(io[i])
           #%
    io3=[]
    for i in range(len(io)):
        if not isinstance(io[i], float):
           io3.append(io[i])
     
    io2=list(tuple(range(io3[0]+1, io3[1])))
#https://www.geeksforgeeks.org/python-program-to-count-words-in-a-sentence/    
#res = len(re.findall(r'\w+', 'how many words are here'))  
    res=[]
#https://stackoverflow.com/questions/44284297/python-regex-keep-alphanumeric-but-remove-numeric
#'https://onlinelibrary.wiley.com/doi/full/10.1002/sim.7992 https://onlinelibrary.wiley.com/doi/full/10.1002/sim.7993'
    for i in io2:
        res.append(len(re.findall(r'\w+', re.sub(r'\b[0-9]+\b', '', df.iloc[i]))))
#%
    return  np.sum(res)

#%%The loop:
def file_count(all_files2): 
    #%%
    count=[]  
    df=[]
    result=[]
    r2=[]
    list2=[]
    list3=[]
    list4=[]
    a=[]
    b=[]
    for i in range(len(all_files2)):
        result.append(docx2txt.process(all_files2[i]))
        r2.append(result[i].splitlines())
        #%
        list2.append([e for e in r2[i] if e]) 
        list3.append([x.split("\t") for x in list2[i]])
        list4.append([e for e in list3[i] if e])
        

    #%
    for i in range(len(list4)):
        for j in range(len(list4[i])):
            if shape(list4[i][j])>(1,):
                list4[i][j][0]=(" ".join([e for e in list4[i][j] if e]))

               
    df=[]
    for i in range(len(list4)):
        df.append(pd.DataFrame(list4[i])) 
    #%
    for i in range(len(df)):
        df[i]=df[i].ix[:,0]  
        #%%
    count=[]
    ff=[]
    count1=[]
    count2=[]
    count3=[]
    for i in range(len(df)):
#        ff.append(pd.DataFrame(df[i]))
        count.append(words2(df[i])) #Yes!! Got it!!
        count1.append(df[i][1])
        count2.append(df[i][2])
        count3.append(df[i][3])
        #%%df.iloc[i][0]
#        words2(df.iloc[55,:])
         words2(df[99])
         
#%% Finally save the data:
count=pd.DataFrame(count) 
count1=pd.DataFrame(count1)     
count2=pd.DataFrame(count2)
count3=pd.DataFrame(count3)             
count.to_csv('comparison1.csv', index=False,header=None)
count1.to_csv('comparison2.csv', index=False,header=None)
count2.to_csv('comparison3.csv', index=False,header=None)
count3.to_csv('comparison4.csv', index=False,header=None)
