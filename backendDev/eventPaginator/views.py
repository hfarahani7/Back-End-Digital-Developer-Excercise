from distutils.command.build import build
from turtle import title
from django.shortcuts import render
from django.core.paginator import Paginator
from dateutil import parser
from datetime import timedelta
import requests

categoriesUrl = "https://www.adelphi.edu/wp-json/wp/v2/event_category"
eventUrl = "https://www.adelphi.edu/wp-json/wp/v2/event"

def index(request):
    currPage = request.GET.get('page')
    eventCategories = getCategories()
    events, pageCount = getEvents(currPage)
    event_list = buildEventList(events, eventCategories, currPage, pageCount)

    p = Paginator(range(1, pageCount), 1)
    page_obj = p.get_page(currPage)
    page_obj.event_list = event_list
    return render(request, 'eventPaginator/index.html', {'page_obj': page_obj})

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
# Created dict with {catId:{data}} format to speed up category mapping
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

def getEvents(currPage):
    if(currPage == None):
        r = requests.get(eventUrl)
    else:
        r = requests.get(eventUrl + "?page=" + str(currPage))

    pageCount = int(r.headers["X-WP-TotalPages"])
    return(r.json(), pageCount)

def buildEventList(events, eventCategories, currPage, pageCount):
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
            "description": event["image_alt_text"],
            "number": currPage,
            "num_pages": pageCount
        })
    return(event_list)