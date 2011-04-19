from PMS.Objects import *
from PMS.Shortcuts import *
import re

####################################################################################################

NEISTAT_PREFIX                  = "/video/neistatbros"
NEISTAT_URL                     = "http://www.neistatbrothers.com/"
NEISTAT_RSS_URL                 = "http://ozare.com/xml/xml.php?q=plex"
MEDIA_NAMESPACE                      = {'media':'http://search.yahoo.com/mrss/'}
BLIP_NAMESPACE                       = {'blip':'http://blip.tv/dtd/blip/1.0'}
DEBUG_XML_RESPONSE		     = True
CACHE_INTERVAL                       = 3200

####################################################################################################

def Start():
  Plugin.AddPrefixHandler(NEISTAT_PREFIX, MainMenu, L("neistatbros"), "icon-default.jpg", "art-default.jpg")
  Plugin.AddViewGroup("_InfoList", viewMode="InfoList", mediaType="items")
  MediaContainer.content = 'Items'
  MediaContainer.title1 = 'The Neistat Brothers'
  MediaContainer.art = R("art-default.jpg")
  MediaContainer.viewGroup = "_InfoList"	


def MainMenu():

  # Top level menu
  # Show available episodes

  dir = MediaContainer()

  page = XML.ElementFromURL(NEISTAT_RSS_URL, isHTML=False, cacheTime=CACHE_INTERVAL)

  episodes = page.xpath("//channel/item")

  # We store the episodes into a dictionary so we can reorder it

  episodeDict = dict()

  for episode in episodes:

    title = episode.xpath("./media:title/text()", namespaces=MEDIA_NAMESPACE)[0]
	
    # Find the episode number from the title
    episodeNumber = 1
	
    # Get the description
    try:
		summary = episode.xpath("./media:description/text()", namespaces=MEDIA_NAMESPACE)[0]
		summary = re.sub(r'<[^>]+>','',summary)
    except:
		summary = ''
    
    # Strip out just the first part
    thumb = episode.xpath("./media:thumbnail", namespaces=MEDIA_NAMESPACE)[0].get('url')
    videofile = episode.xpath("./media:content", namespaces=MEDIA_NAMESPACE)[0].get('url')
    durationseconds = episode.xpath("./media:content", namespaces=MEDIA_NAMESPACE)[0].get('length')
    duration = str(int(durationseconds) * 1000)
    subtitle = 'by The Neistat Brothers'
    art = thumb
    # thumb = "http://a.images.blip.tv/Neistat-CarForSale120-465.jpg"
    
    video = VideoItem(videofile, title=title, summary=summary, duration=duration, thumb=thumb, subtitle=subtitle)
	# vidItem = Function(VideoItem(GetVideo, title=title, summary=summary, duration=duration, thumb=thumb, art=art, subtitle=subtitle), url=id)

    # episodeDict[episodeNumber] = video
    dir.Append(video)

  # Now append the videos in a sorted order
  # for key in sorted(episodeDict.keys(), reverse=True):
  # dir.Append(episodeDict[key])


  if DEBUG_XML_RESPONSE:
    PMS.Log(dir.Content())
  return dir


def TidyString(stringToTidy):
  # Function to tidy up strings works ok with unicode, 'strip' seems to have issues in some cases so we use a regex
  if stringToTidy:
    # Strip new lines
    stringToTidy = re.sub(r'\n', r' ', stringToTidy)
    # Strip leading / trailing spaces
    stringSearch = re.search(r'^\s*(\S.*?\S?)\s*$', stringToTidy)
    if stringSearch == None: 
      return ''
    else:
      return stringSearch.group(1)
  else:
    return ''


