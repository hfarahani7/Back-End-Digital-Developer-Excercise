from django.shortcuts import render
from django.http import HttpResponse
import requests
import json

eventCategories = [{}]
events = [[{}]]
categoriesUrl = "https://www.adelphi.edu/wp-json/wp/v2/event_category"
eventUrl = "https://www.adelphi.edu/wp-json/wp/v2/event"

def index(request):
    # return HttpResponse("Test")
    categoryJSON = getCategories()
    return HttpResponse(categoryJSON)
    

def getCategories():
    try:
        r = requests.get(categoriesUrl)
    except:
        return("502 please try again later")
    #for category in r.json() do something
    return(r.json())

def getEvents():
