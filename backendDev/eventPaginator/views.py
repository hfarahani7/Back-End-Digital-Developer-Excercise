from turtle import title
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

import requests
import json

eventCategories = [{}]
events = [{}]
event_list = [{}]
categoriesUrl = "https://www.adelphi.edu/wp-json/wp/v2/event_category"
eventUrl = "https://www.adelphi.edu/wp-json/wp/v2/event"

def index(request):
    eventCategories = getCategories()
    events = getEvents()

    for event in events:
        event_list.append({
            "link": event.link,
            "title": event.title,
            "category": event.category,
            "start": event.start,
            "end": event.end,
            "location": event.location
        })

    context = {'event_list': event_list}
    template = loader.get_template('eventPaginator/index.html')
    return HttpResponse(template.render(context, request))
    

def getCategories():
    # #returns list of raw json from WP event categories endpoint
    currPage = 1
    r = requests.get(eventUrl + "?page=" + currPage)
    pageCount = r.header()["X-WP-TotalPages"]
    eventCategoryJSON = [{}]

    while(currPage <= pageCount):
        currPage += 1
        eventCategoryJSON.append(r.json())
        r = requests.get(categoriesUrl + "?page=" + currPage)

    return(eventCategoryJSON)

def getEvents():
    #returns list of raw json from WP events endpoint
    currPage = 1
    r = requests.get(eventUrl + "?page=" + currPage)
    pageCount = r.header()["X-WP-TotalPages"]
    eventJSON = [{}]
    
    while(currPage <= pageCount):
        currPage += 1
        eventJSON.append(r.json())
        r = requests.get(eventUrl + "?page=" + currPage)

    return(eventJSON)
