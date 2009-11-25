# Created by Hjalti Jakobsson
# hjalti@hjaltijakobsson.com, modified by Tryggvi Larusson tryggvi.larusson@gmail.com

import re, time, datetime, locale
from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *

PLUGIN_PREFIX   = "/video/ruv"
CACHE_HTML_TIME = 3200
RUV_URL         = "http://dagskra.ruv.is"

################################################################################

def Start():

    # Add the MainMenu prefix handler
    Plugin.AddPrefixHandler(PLUGIN_PREFIX, MainMenu, "RUV", "icon-default.png", "art-default3.jpg")

    # Set up view groups
    Plugin.AddViewGroup("Detail", viewMode = "List", mediaType="items")

    # Set the default cache time
    HTTP.SetCacheTime(14400)

    # Set the default MediaContainer attributes
    MediaContainer.title1 = 'RUV'
    MediaContainer.content = 'List'
    MediaContainer.art = R('art-default3.jpg')

    locale.setlocale(locale.LC_TIME, "is_IS")

def MainMenu():

    dir = DaysList()
    return dir
    
def DaysList():
    
    dir = MediaContainer(art = R('art-default3.jpg'), title2 = "RUV", viewGroup = "List")
    
    page = XML.ElementFromURL(RUV_URL, isHTML = True, cacheTime = CACHE_HTML_TIME)    
    items = page.xpath("//table[@class='dagatal']/tr/td[@class='dagatal_dagar']/a")
    items.reverse()
    today = datetime.date.today()
    
    beintWMVURL="http://dagskra.ruv.is/sjonvarpid/streymi/beint/"
    dir.Append(WindowsMediaVideoItem(beintWMVURL , width=1280, height=720, title = unicode("Sjonvarpid Beint",'utf-8'), subtitle=None, summary=None, duration=None, thumb=None, art=None))
    
    for item in items:
        if item.text != None:
            date = ParseDate(item.attrib["href"])
            if date <= today:
                dayURL = RUV_URL+item.attrib["href"]
                name = date.strftime("%A %d. %B %Y").decode('utf-8')
                
                dir.Append(Function(DirectoryItem(ParseDayPage, title = name.capitalize(), thumb = None), url = dayURL))
    
    return dir
    
def ParseDate(url):
    match = re.search(r'([0-9]{4})/([0-9]{2})/([0-9]{2})', url)
    
    return datetime.date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
        
def ParseDayPage(sender, url):
    
    dir = MediaContainer(art = R('art-default3.jpg'), title2 = None, viewGroup = "List")
    
    #dir.Append(VideoItem("http://skjarinn.is//media/einn/veftivi/video/SMS202.flv", "SMS", subtitle=None, summary=None, duration=None, thumb=None, art=None))
    
    page = XML.ElementFromURL(url, isHTML = True, cacheTime = CACHE_HTML_TIME)
    items = page.xpath("//div[@class='lidur']")
    
    for item in items:
        link = item.xpath("a")
        if(len(link)):
            link = link[0]
            url = link.attrib["href"]
            
            title = item.xpath("strong/a")
            if(len(title)):
                title = title[0].text.encode('Latin-1').decode('utf-8')
                dir.Append(WindowsMediaVideoItem(url , width=1280, height=720, title = title, subtitle=None, summary=None, duration=None, thumb=None, art=None))
                
    return dir