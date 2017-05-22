#Import Dependencies
from bs4 import BeautifulSoup
import requests
import re
import operator
import json
from tabulate import tabulate
import sys
from stop_words import get_stop_words


def getWordList(url):
    word_list=[]
    #Raw Data
    source_code=requests.get(url)
    #Convert To Text
    plain_text=source_code.text
    #LXML Format
    soup=BeautifulSoup(plain_text,'lxml')
    #Find Words In Para tag
    for text in soup.findAll('p'):
        if text.text is None:
            continue
        content=text.text
        #Lowercase And Split In Array
        words=content.lower().split()
        
        #For Every Word
        for word in words:
            #Remove NonChars
            clean_word=clean(word)
            #If Still There Is Something There
            if len(clean_word)>0:
                #Add to WordList
                word_list.append(clean_word)
    return word_list

def clean(word):
    clean_word=re.sub('[^A-Za-z]+','',word)
    return clean_word

def createFreqTable(word_list):
    #WordCount
    word_count={}
    for word in word_list:
        if word in word_count:
            word_count[word]+=1
        else:
            word_count[word]=1
    return word_count
    
def remove_stop_words(word_list):
    stop_words=get_stop_words('en')
    temp=[]
    for key,value in word_list:
        if key not in stop_words:
            temp.append([key,value])
    return temp

#Get Data From Wikipedia
wiki_api_link="https://en.wikipedia.org/w/api.php?format=json&action=query&list=search&srsearch="
wiki_link="https://en.wikipedia.org/wiki/"

if len(sys.argv)<2:
    print("Enter Valid String")
    exit()
    
#Get The Search Word
string_query=sys.argv[1]
if len(sys.argv)>2:
    search_mode=True
else:
    search_mode=False

#Create your URL
url=wiki_api_link + string_query
try:
    response=requests.get(url)
    data=json.loads(response.content.decode('utf-8'))
    #Format This Data
    wiki_page_tag=data['query']['search'][0]['title']
    #Create New URL
    url=wiki_link+wiki_page_tag
    page_word_list=getWordList(url)
    #Create Table Of WordCounts
    page_word_count=createFreqTable(page_word_list)
    sorted_freq_list=sorted(page_word_count.items(),key=operator.itemgetter(1),reverse=True)
    #Remove Stop Words
    if search_mode:
        sorted_freq_list=remove_stop_words(sorted_freq_list)
    #Sum the Total Words To Calculate Frequency
    tot_sum=0
    for key,value in sorted_freq_list:
        tot_sum+=value
    #Just Get The Top 20 Words
    if len(sorted_freq_list)>20:
        sorted_freq_list=sorted_freq_list[:20]
    #Create Final List,word+freq+%
    fin_list=[]
    for key,value in sorted_freq_list:
        percent_val=float(value*100)/tot_sum
        fin_list.append([key,value,round(percent_val,4)])
    
    print_headers=['Word','Freq','Percent']
    print(tabulate(fin_list,headers=print_headers,tablefmt='orgtbl'))
except requests.exceptions.Timeout:
    print("Server Didn't Respond ")
    