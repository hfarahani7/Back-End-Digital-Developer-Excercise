from turtle import title
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator
from dateutil import parser
from datetime import timedelta

import requests

categoriesUrl = "https://www.adelphi.edu/wp-json/wp/v2/event_category"
eventUrl = "https://www.adelphi.edu/wp-json/wp/v2/event"

def index(request):
    # eventCategories = getCategoryDict()
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

        # category_str = ""
        # for categoryId in event["event_category"]:
        #     category_str = category_str + eventCategories[categoryId]

        start_parsed = parser.parse(event["start"])
        start_parsed = start_parsed - timedelta(hours=4)
        end_parsed = parser.parse(event["end"])
        end_parsed = end_parsed - timedelta(hours=4)

        event_list.append({
            "categories": category_str,
            "link": event["link"],
            "title": event["title"],
            "startDate": start_parsed.strftime("%B %d"),
            "startTime": start_parsed.strftime("%I %p"),
            "endDate": end_parsed.strftime("%B %d"),
            "endTime": end_parsed.strftime("%I:%M %p"),
            "location": event["location"],
            "description": event["image_alt_text"]
        })

    p = Paginator(event_list, 50)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    return render(request, 'eventPaginator/index.html', {'page_obj': page_obj})

    # template = loader.get_template('eventPaginator/index.html')
    # context = {'event_list': event_list}
    # return HttpResponse(template.render(context, request))

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

# def getCategoryDict():
#     currPage = 1
#     eventCategoryJSON = {}

#     r = requests.get(categoriesUrl + "?page=" + str(currPage))
#     for row in r.json():
#             eventCategoryJSON[row["id"]] = row["name"]
#     pageCount = int(r.headers["X-WP-TotalPages"])

#     while(currPage <= pageCount):
#         currPage += 1
#         r = requests.get(categoriesUrl + "?page=" + str(currPage))
#         for row in r.json():
#             eventCategoryJSON[row["id"]] = row["name"]
#     return(eventCategoryJSON)

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