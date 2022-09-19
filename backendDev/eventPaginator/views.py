from turtle import title
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from dateutil import parser

import requests

categoriesUrl = "https://www.adelphi.edu/wp-json/wp/v2/event_category"
eventUrl = "https://www.adelphi.edu/wp-json/wp/v2/event"

def index(request):
    eventCategories = getCategories()
    events = getEvents()
    event_list = []

    for event in events:
        category_str = ""
        for categoryId in event["event_category"]:
            for category in eventCategories:
                if(category["id"] == categoryId):
                    category_str = category_str + category["name"] + ", "
        if(len(category_str) > 0):
            category_str = category_str[:-2]

        start_parsed = parser.parse(event["start"])
        end_parsed = parser.parse(event["end"])

        event_list.append({
            "categories": category_str,
            "link": event["link"],
            "title": event["title"],
            "startDate": start_parsed.strftime("%B %m"),
            # "start-time": 
            "endDate": end_parsed.strftime("%B %m"),
            # "end-time":
            "location": event["location"],
            "description": event["image_alt_text"]
        })

    template = loader.get_template('eventPaginator/index.html')
    context = {'event_list': event_list}
    return HttpResponse(template.render(context, request))

def getCategories():
    currPage = 1
    r = requests.get(categoriesUrl + "?page=" + str(currPage))
    pageCount = int(r.headers["X-WP-TotalPages"])
    eventCategoryJSON = []

    while(currPage <= pageCount):
        currPage += 1
        eventCategoryJSON = eventCategoryJSON + r.json()
        r = requests.get(categoriesUrl + "?page=" + str(currPage))

    return(eventCategoryJSON)

def getCategoryDict():
    #Will replace getCategories()
    #Would be nice to create a dict of event categories here, rather than iterating through every single category
    #when we pass events to the template
    pass

def getEvents():
    currPage = 1
    r = requests.get(eventUrl + "?page=" + str(currPage))
    pageCount = int(r.headers["X-WP-TotalPages"])
    eventJSON = []
    
    while(currPage <= pageCount):
        currPage += 1
        eventJSON = eventJSON + r.json()
        r = requests.get(eventUrl + "?page=" + str(currPage))

    return(eventJSON)