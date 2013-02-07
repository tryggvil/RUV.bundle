# -*- coding: utf-8 -*-

from scraper import showtree, tabs, get_episodes, get_stream_info, get_latest_episodes, get_podcast_shows, get_podcast_recordings

POD_FEED = "http://feeds.nationalgeographic.com/ng/photography/photo-of-the-day/"
BASE_URL = "http://video.nationalgeographic.com"
#JSON_CAT_URL = "http://video.nationalgeographic.com/video/player/data/mp4/json/main_sections.json"
JSON_CAT_URL = "http://localhost/tabs.dat"
#JSON_CHANNEL_CAT_URL = "http://video.nationalgeographic.com/video/player/data/mp4/json/category_%s.json"
JSON_CHANNEL_CAT_URL = "http://localhost/showtree.dat"
JSON_PLAYLIST_URL = "http://video.nationalgeographic.com/video/player/data/mp4/json/lineup_%s_%s.json"
JSON_VIDEO_URL = "http://video.nationalgeographic.com/video/player/data/mp4/json/video_%s.json"

NAME = L('Title')
RE_DURATION = Regex('(?P<mins>[0-9]+):(?P<secs>[0-9]+)')

# Default artwork and icon(s)
ART = 'art-default.jpg'
ICON = 'icon-default.png'

####################################################################################################
def Start():

	# Set defaults
	MediaContainer.title1 = u'RÚV'

	Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
	Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
	#Plugin.AddViewGroup("Pictures", viewMode="Pictures", mediaType="photos")

	# Set the default ObjectContainer attributes
	ObjectContainer.art = R(ART)
	ObjectContainer.title1 = NAME
	ObjectContainer.view_group = "List"

	# Default icons for DirectoryObject and WebVideoItem
	DirectoryObject.thumb = R(ICON)
	DirectoryObject.art = R(ART)
	VideoClipObject.thumb = R(ICON)
	VideoClipObject.art = R(ART)

	# Set the default cache time
	HTTP.CacheTime = CACHE_1HOUR
	HTTP.Headers['User-Agent'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:15.0) Gecko/20100101 Firefox/15.0.1"

####################################################################################################
@handler('/video/ruv', L('VideoTitle'), art = ART, thumb = ICON)
def VideosMainMenu():

	oc = ObjectContainer()

	# Iterate over all of the available categories and display them to the user.
	categories = JSON.ObjectFromURL(JSON_CAT_URL)
	for category in categories:
		name = category[0]
		catid = category[0]
		oc.add(DirectoryObject(key = Callback(ChannelVideoCategory, id = catid, name = CleanName(name)), title = name))

	oc.add(DirectoryObject(key = Callback(LiveCategory, id = "live", name = u'Beinar Útsendingar'), title = u'Beinar Útsendingar RÚV'))
	#oc.add(DirectoryObject(key = Callback(LiveCategory2, id = "live2", name = u'Beinar Útsendingar RTMP'), title = u'Beinar Útsendingar RÚV RTMP'))

	Log("RUV menu")
	return oc

####################################################################################################
@route('/video/ruv/live')
def LiveCategory(id, name):

	oc = ObjectContainer()
	#tengipunktur="212.30.206.129"
	tengipunktur="178.19.48.173"
	#key="6532"
	import math
	import random
	ikey=int(math.floor(random.random() * 9999))
	key=str(ikey)
	RTMP_URL="rtmp://"+tengipunktur+"/ruv?key="+key
	PLAYPATH="beint-2"
	swf_url="http://www.ruv.is/files/spilari/player.swf"	
	#url=RTMPVideoURL(url=RTMP_URL, clip=PLAYPATH, swf_url=swf_url, args=(False, PLAYPATH))
	#url=RTMPVideoURL(url=RTMP_URL, clip=PLAYPATH)
	created="2011-03-22 00:56:00"
	duration="00:30:00"
	summary=""
	#image="http://upload.wikimedia.org/wikipedia/en/b/bf/Ruvlogo2011.png"
	
	html5_url="http://"+tengipunktur+":1935/ruv/beint-2/playlist.m3u8?key="+key
	url=html5_url;
	#url="http://178.19.48.173:1935/ruv/beint-2/playlist.m3u8?key=7021"
	title=u'RÚV'
	summary=u'Bein Útsending'
	image=R("ruv-beint.png")
	oc.add(VideoClipObject(
		url = url,
		title = title,
		summary = summary,
		thumb = Resource.ContentsOfURLWithFallback(url=image, fallback=ICON),
		duration = TimeToMs(duration),
		originally_available_at = Datetime.ParseDate(created).date()
	))

	url="http://"+tengipunktur+":1935/ruv/ras1.ruv.is/playlist.m3u8?key="+key
	title=u'Rás 1'
	summary=u'Bein Útsending'
	image=R("ras1-beint.png")
	artist=u'RÚV'
	#oc.add(TrackObject(
	#	url = url,
	#	title = title,
	#	summary = summary,
	#	thumb = Resource.ContentsOfURLWithFallback(url=image, fallback=ICON),
	#	duration = TimeToMs(duration),
	#	originally_available_at = Datetime.ParseDate(created).date()
	#))
	#duration=3600
	rating_key=0
	track = TrackObject(
		key = url,
		title = title,
		artist = artist,
		summary = summary,
		album = summary,
		rating_key = rating_key,
		thumb = image,
		art = image
	)
	media = MediaObject(
		parts = [PartObject(key=Callback(PlayLiveAudio, url=url, ext='mp3'))],
		container = Container.MP3,
		audio_codec = AudioCodec.MP3
	)
	track.add(media)
	oc.add(track)


	url="http://"+tengipunktur+":1935/ruv/ras2.ruv.is/playlist.m3u8?key="+key
	title=u'Rás 2'
	summary=u'Bein Útsending'
	image=R("ras2-beint.png")
	track = TrackObject(
		key = url,
		title = title,
		artist = artist,
		album = summary,
		summary = summary,
		rating_key = rating_key,
		thumb = image,
		art = image
	)
	media = MediaObject(
		parts = [PartObject(key=Callback(PlayLiveAudio, url=url, ext='mp3'))],
		container = Container.MP3,
		audio_codec = AudioCodec.MP3
	)
	track.add(media)
	oc.add(track)
	#oc.add(TrackObject(
	#	url = url,
	#	title = title,
	#	summary = summary,
	#	thumb = Resource.ContentsOfURLWithFallback(url=image, fallback=ICON),
	#	duration = TimeToMs(duration),
	#	originally_available_at = Datetime.ParseDate(created).date()
	#))
        #oc.add(TrackObject(url=url,title=title,summary=summary))

	#see http://forums.plexapp.com/index.php/topic/48486-rtmpvideourl-using-real-rtmp-wont-play-on-ios/
	#see https://github.com/plexinc-plugins/Services.bundle/blob/master/Contents/Service%20Sets/com.plexapp.plugins.blip/URL/Blip/ServiceCode.pys#L155
	#see https://github.com/plexinc-plugins/Services.bundle/blob/master/Contents/Service%20Sets/com.plexapp.plugins.drnu/URL/DRNU/ServiceCode.pys
	return oc



##############
def PlayLiveAudio(url):
	return Redirect(url)


def Lookup():
	return VideoClipObject(title = "MSNBC", summary = "Live MSNBC", thumb ='http://members.fortunecity.com/tvnetworks/nbc/msnbc.jpg' , rating_key="msnbclive://testing/", key=Callback(Lookup),
	items = [MediaObject(
		container = Container.MP4,
		video_codec = VideoCodec.H264,
		audio_codec = AudioCodec.AAC,
		audio_channels = 2,
		optimized_for_streaming = True,
		parts = [PartObject(key = RTMPVideoURL("rtmp://a.cdn.msnbclive.eu/edge playpath=msnbc_live swfUrl=http://msnbclive.eu/player.swf pageUrl=http://blog.livenewschat.tv/rockinroosters/ swfVfy=true live=true", clip = "msnbc_live", live=True, height=467, width=830) )])])

####################################################################################################
@route('/video/ruv/live2')
def LiveCategory2(id, name):

	oc = MediaContainer(viewGroup='Details', title2=name)
	#oc = ObjectContainer()

	tengipunktur="212.30.206.129"
	#tengipunktur="178.19.48.173"
	#key="6532"
	import math
	import random
	ikey=int(math.floor(random.random() * 9999))
	key=str(ikey)
	RTMP_URL="rtmp://"+tengipunktur+"/ruv?key="+key
	PLAYPATH="beint-2"
	swf_url="http://www.ruv.is/files/spilari/player.swf"	
	#url=RTMPVideoURL(url=RTMP_URL, clip=PLAYPATH, swf_url=swf_url, args=(False, PLAYPATH))
	url=RTMPVideoURL(url=RTMP_URL, clip=PLAYPATH)
	
	html5_url="http://"+tengipunktur+":1935/ruv/beint-2/playlist.m3u8?key="+key
	#url="http://178.19.48.173:1935/ruv/beint-2/playlist.m3u8?key=7021"
	title=u'RÚV'
	summary=u'Bein Útsending'
        oc.Append(VideoItem(url, title=title, summary=summary, thumb=R('ruv-beint.png'))) 

	#oc.add(VideoClipObject(
	#	title=title,
	#	summary=summary,
	#	url=html5_url,
	#	items = [
	#		MediaObject(
	#			video_codec = VideoCodec.H264,
	#			audio_codec = AudioCodec.MP3,
	#			parts = [PartObject(key=html5_url)]
	#		)
	#	]
	#))


	Log("RUV live")

	tengipunktur="212.30.206.129"
	key="6532"
	url="http://"+tengipunktur+":1935/ruv/ras1.ruv.is/playlist.m3u8?key="+key
	title=u'Rás 1'
	summary=u'Bein Útsending'

        oc.Append(TrackItem(url, title, summary=summary, thumb=R('ras1-beint.png'))) # TODO R(thumb_file)
	Log("RUV live Ras1")

	url="http://"+tengipunktur+":1935/ruv/ras2.ruv.is/playlist.m3u8?key="+key
	title=u'Rás 2'
	summary=u'Bein Útsending'

        oc.Append(TrackItem(url, title, summary=summary, thumb=R('ras2-beint.png'))) # TODO R(thumb_file)
	Log("RUV live Ras2")

	return oc



####################################################################################################
@route('/video/ruv/{id}')
def ChannelVideoCategory(id, name):

	oc = ObjectContainer()

	# Iterate over all the subcategories. It's possible that we actually find another sub-sub-category
	# In this case, we will simply recursively call this function again until we find actual playlists.
	categories = JSON.ObjectFromURL(JSON_CHANNEL_CAT_URL)
	stod=""
	if name == u'Sjónvarpsefni':
		stod=u'RÚV'
	elif name == u'Rás 1':
		stod=u'RÁS 1'
	elif name == u'Rás 2':
		stod=u'RÁS 2'
	
	for cat in categories:
		catname = cat['name']
		Log("catname:"+catname)
		Log("stod:"+stod)
		if catname == stod:
			Log("catname matched stod")
			sub_categories = cat['categories']
			for sub_category in sub_categories:
				catname = sub_category['name']
				shows = sub_category['shows']
				catid=catname
				Log("catname:"+catname)
				Log("catid:"+catid)
				oc.add(DirectoryObject(key = Callback(ChannelVideoSubCategory, id = catid, name = CleanName(catname), stod=CleanName(stod)), title = catname))

	#oc.add(DirectoryObject(key = Callback(ChannelVideoCategory, id = "dummy", name = "Dummy"), title = "Dummy"))

	return oc


@route('/video/ruv/category/{id}')
def ChannelVideoSubCategory(id, name, stod):

	oc = ObjectContainer()
	
	categories = JSON.ObjectFromURL(JSON_CHANNEL_CAT_URL)
	for cat in categories:
		catname = cat['name']
		Log("catname:"+catname)
		Log("stod:"+stod)
		if catname == stod:
			Log("catname matched stod")
			sub_categories = cat['categories']
			for sub_category in sub_categories:
				catname = sub_category['name']
				if catname == name:
					shows = sub_category['shows']
					catid="/video/ruv/category/"+catname
					Log("catname:"+catname)
					Log("catid:"+catid)
					for show in shows:
						sname=show[0]
						surl=show[1]
						sid=CleanName(sname)
						oc.add(DirectoryObject(key = Callback(ChannelVideoShowList, id = sid, name = CleanName(sname), url=CleanName(surl)), title = sname))
	return oc


@route('/video/ruv/show/{id}')
def ChannelVideoShowList(id, name, url):
	
	oc = MediaContainer(title2=name)
	#oc = ObjectContainer()
	episodes = get_episodes(url)
	for episode in episodes:
		sname, surl = episode
		Log("sname:"+sname)
		Log("surl:"+surl)
		title=sname
		summary=""
		media_info=get_stream_info(surl)
		Log("media_info:"+str(media_info))
		media_type=media_info['media_type']
		if media_type == "mp3":
			html5_url=media_info['html5_url']
			Log("html5_url:"+html5_url)
        		oc.Append(TrackItem(html5_url, title, summary=summary, thumb=R('ras1-beint.png'))) # TODO R(thumb_file)
		else:
			RTMP_URL=media_info['rtmp_url']
			PLAYPATH=media_info['playpath']
			html5_url=media_info['html5_url']
			media_url=RTMPVideoURL(url=RTMP_URL, clip=PLAYPATH)
			#media_url=html5_url
			#oc.Append(TrackItem(media_url, title, summary=summary, thumb=R('ras2-beint.png')))
			#oc.add(VideoClipObject(url=media_url, title=title, summary=summary, thumb=R('ruv-beint.png')))
	        	oc.Append(VideoItem(media_url, title=title, summary=summary, thumb=R('ruv-beint.png'))) 
	return oc


####################################################################################################
@route('/video/ruv/playlist/{id}', allow_sync = True)
def ChannelVideoPlaylist(id, name, surl):

	oc = ObjectContainer(view_group="InfoList")

	# Iterate over all the available playlist and extract the available information.
	playlist = JSON.ObjectFromURL(JSON_PLAYLIST_URL % (id, str(0)))
	for video in playlist['lineup']['video']:
		name = video['title'].replace('&#45;', '-')
		summary = video['caption']

		duration_text = video['time']
		try:
			duration_dict = RE_DURATION.match(duration_text).groupdict()
			mins = int(duration_dict['mins'])
			secs = int(duration_dict['secs'])
			duration = ((mins * 60) + secs) * 1000
		except:
			 duration = 0

		# In order to obtain the actual url, we need to call the specific JSON page. This will also
		# include a high resolution thumbnail that can be used. We've found a small number of JSON
		# pages which don't actually include the URL link. We should try and detect these and simply
		# skip them.
		video_details = JSON.ObjectFromURL(JSON_VIDEO_URL % video['id'])
		url = BASE_URL + video_details['video']['url']
		if url == "http://video.nationalgeographic.com/video/player/":
			continue

		thumb = video_details['video']['still']
		if thumb.startswith("http://") == False:
			thumb = BASE_URL + thumb
		
		oc.add(VideoClipObject(
			url = url, 
			title = CleanName(name), 
			summary = String.StripTags(summary.strip()), 
			thumb = thumb,
			duration = duration))

	# It's possible that there is actually no vidoes are available for the ipad. Unfortunately, they
	# still provide us with empty containers...
	if len(oc) == 0:
		return MessageContainer(name, "There are no titles available for the requested item.")
	
	return oc

####################################################################################################
def CleanName(name):

	# Function cleans up HTML ascii stuff	
	remove = [('&amp;','&'),('&quot;','"'),('&#233;','e'),('&#8212;',' - '),('&#39;','\''),('&#46;','.'),('&#58;',':'), ('&#8482;','')]
	for trash, crap in remove:
		name = name.replace(trash,crap)

	return name.strip()

###################################################################################################
def TimeToMs(timecode):

	seconds  = 0
	duration = timecode.split(':')
	duration.reverse()

	for i in range(0, len(duration)):
		seconds += int(duration[i]) * (60**i)

	return seconds * 1000

