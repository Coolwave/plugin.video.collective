import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os,settings
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
from metahandler import metahandlers
from metahandler import metacontainers
from universal import favorites
from universal import _common as univ_common
from settings import *
import time,datetime


############################################################################################################################################################

icon = 'icon.png'
fanart = 'fanart.png'
fav = favorites.Favorites('plugin.video.collective', sys.argv)
grab = metahandlers.MetaData(preparezip = False)
addon_id = 'plugin.video.collective'
local = xbmcaddon.Addon(id=addon_id)
collectivepath = local.getAddonInfo('path')
addon = Addon(addon_id, sys.argv)
datapath = addon.get_profile()
art = collectivepath+'/art'
net = Net()
#SUBSCRIPTION_FILE = settings.subscription_file()
#SUBSCRIPTIONS_ACTIVATED = settings.subscription_update()
strdomain ="http://www.vidics.ch"
############################################################################################################################################################

base_url = 'http://www.nzbmovieseeker.com'
movie_url = 'http://www.nzbmovieseeker.com/New/'
tv_url = 'http://www.nzbtvseeker.com/'
IMDb_url = 'http://akas.imdb.com'
IMDbIT_url = 'http://akas.imdb.com/movies-in-theaters/?ref_=nb_mv_2_inth'
IMDb250_url = 'http://akas.imdb.com/search/title?groups=top_250&sort=user_rating&my_ratings=exclude'
kidzone_url = 'http://akas.imdb.com/search/title?genres=animation,family&title_type=feature,tv_movie'
kidzonetv_url = 'http://akas.imdb.com/search/title?genres=animation,family&title_type=tv_series,tv_special,mini_series'
onechannel_base = 'http://www.primewire.ag'
onechannel_featured = 'http://www.primewire.ag/index.php?sort=featured'
onechannel_featuredtv = 'http://www.primewire.ag/?tv=&sort=featured'
onechannel_lastest = 'http://www.primewire.ag/?sort=date'
onechannel_lastesttv = 'http://www.primewire.ag/?tv'
onechannel_populartv = 'http://www.primewire.ag/?tv=&sort=views'
onechannel_popular = 'http://www.primewire.ag/?sort=views'
onechannel_ratings = 'http://www.primewire.ag/?sort=ratings'
onechannel_ratingstv = 'http://www.primewire.ag/?tv=&sort=ratings'
onechannel_releasedatetv = 'http://www.primewire.ag/?tv=&sort=release'
onechannel_releasedate = 'http://www.primewire.ag/?sort=release'
allmusic_url = 'http://www.allmusic.com'
allmusic_newrelease = 'http://www.allmusic.com/newreleases'
billboard_url = 'http://www.billboard.com/'
billboard_200 = 'http://www.billboard.com/charts/billboard-200'
IMDBTV_WATCHLIST = settings.imdbtv_watchlist_url()
IMDB_LIST = settings.imdb_list_url()


#Metahandler
def GRABMETA(name,types,year=None):
        type = types
        if year=='': year=None
        EnableMeta = local.getSetting('Enable-Meta')
        #
        if year==None:
                try: year=re.search('\s*\((\d\d\d\d)\)',name).group(1)
                except: year=None
        if year is not None: name=name.replace(' ('+year+')','').replace('('+year+')','')
        #
        if EnableMeta == 'true':
                if 'Movie' in type:
                        ### grab.get_meta(media_type, name, imdb_id='', tmdb_id='', year='', overlay=6)
                        meta = grab.get_meta('movie',name,'',None,year,overlay=6)
                        infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],'plot': meta['plot'],'title': meta['title'],'writer': meta['writer'],'cover_url': meta['cover_url'],'director': meta['director'],'cast': meta['cast'],'backdrop_url': meta['backdrop_url'],'backdrop_url': meta['backdrop_url'],'tmdb_id': meta['tmdb_id'],'year': meta['year']}
                elif 'tvshow' in type:
                        meta = grab.get_meta('tvshow',name,'','',year,overlay=6)
                        infoLabels = {'rating': meta['rating'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],'cast': meta['cast'],'studio': meta['studio'],'banner_url': meta['banner_url'],'backdrop_url': meta['backdrop_url'],'status': meta['status']}
        else: infoLabels=[]
        return infoLabels

def get_html(page_url):

        html = net.http_GET(page_url).content

        import HTMLParser
        h = HTMLParser.HTMLParser()
        html = h.unescape(html)
        return html.encode('utf-8')

def _FixText(t):
        if ("&amp;"  in t): t=t.replace('&amp;'  ,'&')#&amp;#x27;
        if ("&nbsp;" in t): t=t.replace('&nbsp;' ," ")
        if ('&#' in t) and (';' in t):
                t=t.replace("&#8211;",";").replace("&#8216;","'").replace("&#8217;","'").replace('&#8220;','"').replace('&#8221;','"').replace('&#215;' ,'x').replace('&#x27;' ,"'").replace('&#xF4;' ,"o").replace('&#xb7;' ,"-").replace('&#xFB;' ,"u").replace('&#xE0;' ,"a").replace('&#xE9;' ,"e").replace('&#xE2;' ,"a").replace('&#0421;',"")
                if ('&#' in t) and (';' in t):
                        try:            matches=re.compile('&#(.+?);').findall(t)
                        except: matches=''
                        if (matches is not ''):
                                for match in matches:
                                        if (match is not '') and (match is not ' ') and ("&#"+match+";" in t): t=t.replace("&#"+match+";" ,"")
        for i in xrange(127,256): t=t.replace(chr(i),"")
        try: t=t.encode('ascii', 'ignore'); t=t.decode('iso-8859-1')
        except: t=t
        return t



######################################################################################################################################################

 #      addDir(name,url,mode,iconimage,types,favtype) mode is where it tells the plugin where to go scroll to bottom to see where mode is
def CATEGORIES():
        addDir('Movies',onechannel_base,3,art_('Movies','Main Menu'),None,'')
        addDir('TV-Shows',onechannel_base,2,art_('TV Shows','Main Menu'),None,'TV-Shows')
        addDir('Music',onechannel_base,29,art_('music','Main Menu'),None,'')
        fav.add_my_fav_directory(img=art_('Favorites','Main Menu'))
        addDir('Settings','http://',309,art_('Settings','Main Menu'),None,'')
        set_view('list') 
       
       
def TVSHOWScat():
        addDir('Latest Added',onechannel_lastesttv,21,art_('Latest','Sub Menus'),None,'')
        addDir('TV Schedule [COLOR red][B]Not working just yet[/B][/COLOR]',strdomain,57,'',None,'')
        addDir('Featured',onechannel_featuredtv,19,art_('Featured','Sub Menus'),None,'')
        addDir('Popular',onechannel_populartv,23,art_('Popular','Sub Menus'),None,'')
        addDir('Ratings',onechannel_ratingstv,25,art_('Ratings','Sub Menus'),None,'')
        addDir('Release Date',onechannel_releasedatetv,27,art_('Release Date','Sub Menus'),None,'')
        addDir('Genre','http://www.imdb.com/genre',45,art_('Genre','Sub Menus'),None,'')
        addDir('Kids Zone (TV)',kidzonetv_url,50,art_('Kids Zone','Sub Menus'),None,'')
        addDir('IMDb',IMDb_url,53,art_('IMDb','Sub Menus'),None,'')
        addDir('Search',IMDb_url,44,art_('Search','Sub Menus'),None,'')
        set_view('list') 
       
def MOVIEScat():
        addDir('Latest Added',onechannel_lastest,20,art_('Latest','Sub Menus'),None,'')
        addDir('Featured',onechannel_featured,18,art_('Featured','Sub Menus'),None,'')
        addDir('Popular',onechannel_popular,22,art_('Popular','Sub Menus'),None,'')
        addDir('Ratings',onechannel_ratings,24,art_('Ratings','Sub Menus'),None,'')
        addDir('Release Date',onechannel_releasedate,26,art_('Release Date','Sub Menus'),None,'')
        addDir('Genre','http://www.imdb.com/genre',33,art_('Genre','Sub Menus'),None,'')
        addDir('Kids Zone',kidzone_url,49,art_('Kids Zone','Sub Menus'),None,'')
        addDir('IMDb',IMDb_url,13,art_('IMDb','Sub Menus'),None,'')
        addDir('Search',IMDb_url,32,art_('Search','Sub Menus'),None,'')
        set_view('list')

def IMDbcat():
        addDir('In Theaters',IMDbIT_url,15,art_('In Theaters','Sub Menus'),None,'')
        addDir('Top 250',IMDb250_url,17,art_('Top 250','Sub Menus'),None,'')
        addDir('Genre','http://akas.imdb.com/genre',33,art_('Genre','Sub Menus'),None,'')
        addDir('IMDb watchlist','url',13,art_('IMDb watchlist','Sub Menus'),None,'')
        addDir('Search',IMDb_url,32,art_('Search','Sub Menus'),None,'')
        set_view('list')

def IMDbtvcat():
        addDir('Genre','http://www.imdb.com/genre',45,art_('Genre','Sub Menus'),None,'')
        addDir('IMDb watchlist [COLOR red][B]Not working just yet[/B][/COLOR]',IMDb_url,13,art_('IMDb watchlist','Sub Menus'),None,'')
        addDir('Search',IMDb_url,44,art_('Search','Sub Menus'),None,'')
        set_view('list')        

def MUSICcat():
        addDir('Billboard 200','http://www1.billboard.com/charts/billboard-200',39,icon,None,'')
        addDir('Country Albums','http://www1.billboard.com/charts/country-albums',39,icon,None,'')
        addDir('HeatSeeker Albums','http://www1.billboard.com/charts/heatseekers-albums',39,icon,None,'')
        addDir('Independent Albums','http://www1.billboard.com/charts/independent-albums',39,icon,None,'')
        addDir('Catalogue Albums','http://www1.billboard.com/charts/catalog-albums',39,icon,None,'')
        addDir('Folk Albums','http://www1.billboard.com/charts/folk-albums',39,icon,None,'')
        addDir('Digital Albums','http://www1.billboard.com/charts/digital-albums',39,icon,None,'')
        #addDir('Genre','http://www.allmusic.com/genres',41,icon,None,'')
        addDir('New Release',allmusic_newrelease,38,art_('Release Date','Sub Menus'),None,'')
        addDir('Search by Artist','url',43,art_('Search','Sub Menus'),None,'')

def MUSICsearch():
        addDir('Search by Artist',allmusic_url,36,art_('Search','Sub Menus'),None,'')
        addDir('Search by Album',allmusic_url,36,art_('Search','Sub Menus'),None,'')
        addDir('Search by Song',allmusic_url,36,art_('Search','Sub Menus'),None,'')
                                                                          
def MOVIESgene(url):#  cause mode is empty in this one it will go back to first directory
        addDir('Action',movie_url,'',icon,None,'')
                
def TVSHOWSgene(url):#  cause mode is empty in this one it will go back to first directory
        addDir('Action',tv_url,'',icon,None,'')

##############################################################################################################################

def NZBmovie(url):
        html = get_html(url)
        match =  re.compile('<h3> <a href="(.+?)" class="movie-title" title=".+?">(.+?)</a> </h3>.+?<div class="poster">.+?<img src="(.+?)">',re.DOTALL).findall(html)
        for url, name, thumbnail in match:
                addDir(name,url,12,thumbnail,'')
        nextpage = re.compile('<span class="next">.+?<a href="(.+?)">Next</a>',re.DOTALL).findall(html)
        if nextpage:
                addDir('[COLOR blue]Next Page >>[/COLOR]','http://www.nzbmovieseeker.com'+nextpage[0],12,thumbnail,'')

def IMDbInTheaters(url):
        EnableMeta = local.getSetting('Enable-Meta')
        html = get_html(url)
        match =  re.compile('<div class=".+?">\n<img class=".+?"\nheight="209"\nwidth="140"\nalt=".+?"\ntitle="(.+?)\(([\d]{4}\))"\nsrc="(.+?)"\nitemprop="image" />\n</div>').findall(html)
        for name, year, thumbnail in match:
                if EnableMeta == 'true':  addDir(name,url,12,'','Movie','Movies')
                if EnableMeta == 'false': addDir(name,url,12,thumbnail,None,'Movies')

def IMDbrate(url):
        EnableMeta = local.getSetting('Enable-Meta')
        html = get_html(url)
        match = re.compile('<a href="(.+?)" title="(.+?)\(([\d]{4}\))"><img src=".+?" height="74" width="54" alt=".+?" title=".+?"></a>').findall(html)
        for url, name, year in match:
                name = str(name).replace('&#xB7;','').replace('&#x27;','').replace('&#x26;','And').replace('&#xE9;','e').replace('&amp;','And').replace('&#x22;','"')
                if EnableMeta == 'true':  addDir(name,url,12,'','Movie','Movies')
                if EnableMeta == 'false': addDir(name,url,12,thumbnail,None,'Movies')
        nextpage = re.compile('<a href="(.+?)">Next.+?</a>').findall(html)
        if nextpage:
                addDir('[COLOR blue]Next Page >>[/COLOR]',' http://akas.imdb.com/'+nextpage[0],17,'',None,'')

def KIDSzone(url):
        EnableMeta = local.getSetting('Enable-Meta')
        html = get_html(url)
        match =  re.compile('<a href="(.+?)" title="(.+?)\(([\d]{4}\))"><img src="(.+?)" height="74" width="54" alt=".+?" title=".+?"></a>').findall(html)
        for url, name, year, thumbnail in match:
                name = str(name).replace('&#xB7;','').replace('&#x27;','').replace('&#x26;','And').replace('&#xE9;','e').replace('&amp;','And').replace('&#x22;','"')
                if EnableMeta == 'true':  addDir(name,url,12,'','Movie','Movies')
                if EnableMeta == 'false': addDir(name,url,12,thumbnail,None,'Movies')
        nextpage = re.compile('<a href="(.+?)">Next.+?</a>').findall(html)
        if nextpage:
                addDir('[COLOR blue]Next Page >>[/COLOR]',' http://akas.imdb.com/'+nextpage[0],49,'',None,'')
                
def KIDSzonetv(url):
        EnableMeta = local.getSetting('Enable-Meta')
        html = get_html(url)
        match =  re.compile('<a href="(.+?)" title="(.+?)\(([\d]{4}\s\TV\s\Series\))"><img src="(.+?)" height="74" width="54" alt=".+?" title=".+?"></a>').findall(html)
        for url, name, year, thumbnail in match:
                name = str(name).replace('USA','US').replace('&#xB7;','').replace('&#x27;','').replace('&#x26;','And').replace('&#xE9;','e').replace('&amp;','And').replace('&#x22;','"')
                if EnableMeta == 'true':  addDir(name,url,30,'','tvshow','TV-Shows')
                if EnableMeta == 'false': addDir(name,url,30,thumbnail,None,'TV-Shows')
        nextpage = re.compile('<a href="(.+?)">Next.+?</a>').findall(html)
        if nextpage:
                addDir('[COLOR blue]Next Page >>[/COLOR]',' http://akas.imdb.com/'+nextpage[0],50,'',None,'')

def onechannelmfeature(url):
        EnableMeta = local.getSetting('Enable-Meta')
        html = get_html(url)
        match =  re.compile('<a href="(.+?)" title="Watch (.+?)(\([\d]{4}\))"><img src="(.+?)" border="0" width="150" height="225" alt=".+?"><h2>.+?</h2></a>').findall(html)
        for url, name, year, thumbnail in match:
                #name = str(name).replace('(2000)','').replace('(2001)','').replace('(2002)','').replace('(2003)','').replace('(2004)','').replace('(2005)','').replace('(2006)','').replace('(2007)','').replace('(2008)','').replace('(2009)','').replace('(2010)','').replace('(2011)','').replace('(2012)','').replace('(2013)','').replace('(2014)','').replace('(2015)','')
                if EnableMeta == 'true':  addDir(name,url,12,'','Movie','Movies')
                if EnableMeta == 'false': addDir(name,url,12,thumbnail,None,'Movies')
        nextpage = re.compile('<div class="pagination">.+?class=current>.+?href="(.+?)">.+?<a href=".+?">.+?</a>.+?<a href=".+?">.+?</div>',re.DOTALL).findall(html)
        if nextpage:
                addDir('[COLOR blue]Next Page >>[/COLOR]','http://www.primewire.ag'+nextpage[0],18,'',None,'')

def onechanneltvfeature(url):
        EnableMeta = local.getSetting('Enable-Meta')
        html = get_html(url)
        match =  re.compile('<a href="(.+?)" title="Watch (.+?)\(([\d]{4}\))"><img src="(.+?)" border="0" width="150" height="225" alt=".+?"><h2>.+?</h2></a>').findall(html)
        for url, name, year, thumbnail in match:
                name = str(name).replace('USA','US')
                #name = str(name).replace('(2000)','').replace('(2001)','').replace('(2002)','').replace('(2003)','').replace('(2004)','').replace('(2005)','').replace('(2006)','').replace('(2007)','').replace('(2008)','').replace('(2009)','').replace('(2010)','').replace('(2011)','').replace('(2012)','').replace('(2013)','').replace('(2014)','').replace('(2015)','')       
                if EnableMeta == 'true': addDir(name,url,30,'','tvshow','TV-Shows')
                if EnableMeta == 'false': addDir(name,url,30,'',None,'TV-Shows')
        nextpage = re.compile('<div class="pagination">.+?class=current>.+?href="(.+?)">.+?<a href=".+?">.+?</a>.+?<a href=".+?">.+?</div>',re.DOTALL).findall(html)
        if nextpage:
                addDir('[COLOR blue]Next Page >>[/COLOR]','http://www.primewire.ag'+nextpage[0],19,'',None,'')
        set_view('tvshows') 

def onechannellastest(url):
        EnableMeta = local.getSetting('Enable-Meta')
        html = get_html(url)
        match =  re.compile('<a href="(.+?)" title="Watch (.+?)\(([\d]{4}\))"><img src="(.+?)" border="0" width="150" height="225" alt=".+?"><h2>.+?</h2></a>').findall(html)
        for url, name, year, thumbnail in match:
                if EnableMeta == 'true':  addDir(name,url,12,'','Movie','Movies')
                if EnableMeta == 'false': addDir(name,url,12,thumbnail,None,'Movies')
        nextpage = re.compile('<div class="pagination">.+?class=current>.+?href="(.+?)">.+?<a href=".+?">.+?</a>.+?<a href=".+?">.+?</div>',re.DOTALL).findall(html)
        if nextpage:
                addDir('[COLOR blue]Next Page >>[/COLOR]','http://www.primewire.ag'+nextpage[0],20,'',None,'')

def onechannellastesttv(url):
        EnableMeta = local.getSetting('Enable-Meta')
        html = get_html(url)
        match =  re.compile('<a href="(.+?)" title="Watch (.+?)\(([\d]{4}\))"><img src="(.+?)" border="0" width="150" height="225" alt=".+?"><h2>.+?</h2></a>').findall(html)
        for url, name, year, thumbnail in match:
                name = str(name).replace('USA','US')
                if EnableMeta == 'true': addDir(name,url,30,'','tvshow','TV-Shows')
                if EnableMeta == 'false': addDir(name,url,30,'',None,'TV-Shows')
        nextpage = re.compile('<div class="pagination">.+?class=current>.+?href="(.+?)">.+?<a href=".+?">.+?</a>.+?<a href=".+?">.+?</div>',re.DOTALL).findall(html)
        if nextpage:
                addDir('[COLOR blue]Next Page >>[/COLOR]','http://www.primewire.ag'+nextpage[0],21,'',None,'')
        set_view('tvshows')

def onechannelmpopular(url):
        EnableMeta = local.getSetting('Enable-Meta')
        html = get_html(url)
        match =  re.compile('<a href="(.+?)" title="Watch (.+?)\(([\d]{4}\))"><img src="(.+?)" border="0" width="150" height="225" alt=".+?"><h2>.+?</h2></a>').findall(html)
        for url, name, year, thumbnail in match:
                if EnableMeta == 'true':  addDir(name,url,12,'','Movie','Movies')
                if EnableMeta == 'false': addDir(name,url,12,thumbnail,None,'Movies')
        nextpage = re.compile('<div class="pagination">.+?class=current>.+?href="(.+?)">.+?<a href=".+?">.+?</a>.+?<a href=".+?">.+?</div>',re.DOTALL).findall(html)
        if nextpage:
                addDir('[COLOR blue]Next Page >>[/COLOR]','http://www.primewire.ag'+nextpage[0],22,'',None,'')

def onechanneltvpopular(url):
        EnableMeta = local.getSetting('Enable-Meta')
        html = get_html(url)
        match =  re.compile('<a href="(.+?)" title="Watch (.+?)\(([\d]{4}\))"><img src="(.+?)" border="0" width="150" height="225" alt=".+?"><h2>.+?</h2></a>').findall(html)
        for url, name, year, thumbnail in match:
                name = str(name).replace('USA','US')
                if EnableMeta == 'true': addDir(name,url,30,'','tvshow','TV-Shows')
                if EnableMeta == 'false': addDir(name,url,30,'',None,'TV-Shows')
        nextpage = re.compile('<div class="pagination">.+?class=current>.+?href="(.+?)">.+?<a href=".+?">.+?</a>.+?<a href=".+?">.+?</div>',re.DOTALL).findall(html)
        if nextpage:
                addDir('[COLOR blue]Next Page >>[/COLOR]','http://www.primewire.ag'+nextpage[0],23,'',None,'')
        set_view('tvshows')

def onechannelmratings(url):
        EnableMeta = local.getSetting('Enable-Meta')
        html = get_html(url)
        match =  re.compile('<a href="(.+?)" title="Watch (.+?)\(([\d]{4}\))"><img src="(.+?)" border="0" width="150" height="225" alt=".+?"><h2>.+?</h2></a>').findall(html)
        for url, name, year, thumbnail in match:
                if EnableMeta == 'true':  addDir(name,url,12,'','Movie','Movies')
                if EnableMeta == 'false': addDir(name,url,12,thumbnail,None,'Movies')
        nextpage = re.compile('<div class="pagination">.+?class=current>.+?href="(.+?)">.+?<a href=".+?">.+?</a>.+?<a href=".+?">.+?</div>',re.DOTALL).findall(html)
        if nextpage:
                addDir('[COLOR blue]Next Page >>[/COLOR]','http://www.primewire.ag'+nextpage[0],24,'',None,'')

def onechanneltvratings(url):
        EnableMeta = local.getSetting('Enable-Meta')
        html = get_html(url)
        match =  re.compile('<a href="(.+?)" title="Watch (.+?)\(([\d]{4}\))"><img src="(.+?)" border="0" width="150" height="225" alt=".+?"><h2>.+?</h2></a>').findall(html)
        for url, name, year, thumbnail in match:
                name = str(name).replace('USA','US')
                if EnableMeta == 'true': addDir(name,url,30,'','tvshow','TV-Shows')
                if EnableMeta == 'false': addDir(name,url,30,'',None,'TV-Shows')
        nextpage = re.compile('<div class="pagination">.+?class=current>.+?href="(.+?)">.+?<a href=".+?">.+?</a>.+?<a href=".+?">.+?</div>',re.DOTALL).findall(html)
        if nextpage:
                addDir('[COLOR blue]Next Page >>[/COLOR]','http://www.primewire.ag'+nextpage[0],25,'',None,'')
        set_view('tvshows')

def onechannelmreleasedate(url):
        EnableMeta = local.getSetting('Enable-Meta')
        html = get_html(url)
        match =  re.compile('<a href="(.+?)" title="Watch (.+?)\(([\d]{4}\))"><img src="(.+?)" border="0" width="150" height="225" alt=".+?"><h2>.+?</h2></a>').findall(html)
        for url, name, year, thumbnail in match:
                if EnableMeta == 'true':  addDir(name,url,12,'','Movie','Movies')
                if EnableMeta == 'false': addDir(name,url,12,thumbnail,None,'Movies')
        nextpage = re.compile('<div class="pagination">.+?class=current>.+?href="(.+?)">.+?<a href=".+?">.+?</a>.+?<a href=".+?">.+?</div>',re.DOTALL).findall(html)
        if nextpage:
                addDir('[COLOR blue]Next Page >>[/COLOR]','http://www.primewire.ag'+nextpage[0],26,'',None,'')

def onechanneltvreleasedate(url):
        EnableMeta = local.getSetting('Enable-Meta')
        html = get_html(url)
        match =  re.compile('<a href="(.+?)" title="Watch (.+?)\(([\d]{4}\))"><img src="(.+?)" border="0" width="150" height="225" alt=".+?"><h2>.+?</h2></a>').findall(html)
        for url, name, year, thumbnail in match:
                name = str(name).replace('USA','US')
                if EnableMeta == 'true': addDir(name,url,30,'','tvshow','TV-Shows')
                if EnableMeta == 'false': addDir(name,url,30,'',None,'TV-Shows')
        nextpage = re.compile('<div class="pagination">.+?class=current>.+?href="(.+?)">.+?<a href=".+?">.+?</a>.+?<a href=".+?">.+?</div>',re.DOTALL).findall(html)
        if nextpage:
                addDir('[COLOR blue]Next Page >>[/COLOR]','http://www.primewire.ag'+nextpage[0],27,'',None,'')
        set_view('tvshows')
                
def ALLTIMEIMDB(url):
        req = urllib2.Request(url)
        link=OPEN_URL(url)
        match = re.compile('<img src="(.+?)" height="74" width="54" alt=".+?" title="(.+?)\(([\d]{4}\))"></a>\n  </td>\n  <td class="title">\n    \n\n<span class="wlb_wrapper" data-tconst="(.+?)" data-size="small" data-caller-name="search"></span>\n\n    <a href=".+?">.+?</a>\n    <span class="year_type">.+?</span><br>\n<div class="user_rating">\n\n\n<div class="rating rating-list" data-auth=".+?" id=".+?" data-ga-identifier="advsearch"\n title=".+?click stars to rate">\n<span class="rating-bg">&nbsp;</span>\n<span class="rating-imdb" style="width.+?">&nbsp;</span>\n<span class="rating-stars">\n<a href=".+?" title="Register or login to rate this title" rel="nofollow"><span>1</span></a>\n<a href=".+?" title="Register or login to rate this title" rel="nofollow"><span>2</span></a>\n<a href=".+?" title="Register or login to rate this title" rel="nofollow"><span>3</span></a>\n<a href=".+?" title="Register or login to rate this title" rel="nofollow"><span>4</span></a>\n<a href=".+?" title="Register or login to rate this title" rel="nofollow"><span>5</span></a>\n<a href=".+?" title="Register or login to rate this title" rel="nofollow"><span>6</span></a>\n<a href=".+?" title="Register or login to rate this title" rel="nofollow"><span>7</span></a>\n<a href=".+?" title="Register or login to rate this title" rel="nofollow"><span>8</span></a>\n<a href=".+?" title="Register or login to rate this title" rel="nofollow"><span>9</span></a>\n<a href=".+?" title="Register or login to rate this title" rel="nofollow"><span>10</span></a>\n</span>\n<span class="rating-rating"><span class="value">.+?</span><span class="grey">/</span><span class="grey">10</span></span>\n<span class="rating-cancel"><a href=".+?" title="Delete" rel="nofollow"><span>X</span></a></span>\n&nbsp;</div>\n\n</div>\n<span class="outline">(.+?)</span>').findall(link)
        nextp=re.compile('<a href="(.+?)">Next&nbsp;').findall(link)
        try:
                nextp1=nextp[0]
        except:
                pass       
        for iconimage, name,year,url, description in match:
            name = str(name).replace('&#xB7;','').replace('&#x27;','').replace('&#x26;','And').replace('&#xE9;','e').replace('&amp;','And').replace(' TV Series','')
            iconimage1 = iconimage
            url = ' http://akas.imdb.com/title/'+str(url)+'/'
            regex=re.compile('(.+?)_V1.+?.jpg')
            regex1=re.compile('(.+?).gif')
            try:
                    match = regex.search(iconimage1)
                    iconimage= '%s_V1_.SX593_SY799_.jpg'%(match.group(1))
                    fanart= '%s_V1.jpg'%(match.group(1))
            except:
                    pass
            try:    
                    match= regex1.search(iconimage1)
                    iconimage= '%s.gif'%(match.group(1))
                    fanart= '%s_V1.jpg'%(match.group(1))
            except:
                    pass
                    addDir(name,url,12,iconimage,None,description)   
                    set_view('list') 
        try:
                url=' http://akas.imdb.com'+str(nextp1)
                name= '[COLOR blue][B]Next Page >>[/B][/COLOR]'
                addDir(name,url,34,'',None,'')
                set_view('list') 
        except:
                pass
        addDir('[COLOR red][B]<< Return To Main Menu[/B][/COLOR]','url','','',None,'')    
        set_view('list')

def ALLTIMEIMDBTV(url):
        req = urllib2.Request(url)
        link=OPEN_URL(url)
        match = re.compile('<img src="(.+?)" height="74" width="54" alt=".+?" title="(.+?)\(([\d]{4}\s\TV\s\Series\))"></a>\n  </td>\n  <td class="title">\n    \n\n<span class="wlb_wrapper" data-tconst="(.+?)" data-size="small" data-caller-name="search"></span>\n\n    <a href=".+?">.+?</a>\n    <span class="year_type">.+?</span><br>\n<div class="user_rating">\n\n\n<div class="rating rating-list" data-auth=".+?" id=".+?" data-ga-identifier="advsearch"\n title=".+?click stars to rate">\n<span class="rating-bg">&nbsp;</span>\n<span class="rating-imdb" style="width.+?">&nbsp;</span>\n<span class="rating-stars">\n<a href=".+?" title="Register or login to rate this title" rel="nofollow"><span>1</span></a>\n<a href=".+?" title="Register or login to rate this title" rel="nofollow"><span>2</span></a>\n<a href=".+?" title="Register or login to rate this title" rel="nofollow"><span>3</span></a>\n<a href=".+?" title="Register or login to rate this title" rel="nofollow"><span>4</span></a>\n<a href=".+?" title="Register or login to rate this title" rel="nofollow"><span>5</span></a>\n<a href=".+?" title="Register or login to rate this title" rel="nofollow"><span>6</span></a>\n<a href=".+?" title="Register or login to rate this title" rel="nofollow"><span>7</span></a>\n<a href=".+?" title="Register or login to rate this title" rel="nofollow"><span>8</span></a>\n<a href=".+?" title="Register or login to rate this title" rel="nofollow"><span>9</span></a>\n<a href=".+?" title="Register or login to rate this title" rel="nofollow"><span>10</span></a>\n</span>\n<span class="rating-rating"><span class="value">.+?</span><span class="grey">/</span><span class="grey">10</span></span>\n<span class="rating-cancel"><a href=".+?" title="Delete" rel="nofollow"><span>X</span></a></span>\n&nbsp;</div>\n\n</div>\n<span class="outline">(.+?)</span>').findall(link)
        nextp=re.compile('<a href="(.+?)">Next&nbsp;').findall(link)
        try:
                nextp1=nextp[0]
        except:
                pass       
        for iconimage, name, year, url, description in match:
            name = str(name).replace('&#xB7;','').replace('&#x27;','').replace('&#x26;','And').replace('&#xE9;','e').replace('&amp;','And').replace(' TV Series','')
            iconimage1 = iconimage
            url = ' http://akas.imdb.com/title/'+str(url)+'/'
            regex=re.compile('(.+?)_V1.+?.jpg')
            regex1=re.compile('(.+?).gif')
            try:
                    match = regex.search(iconimage1)
                    iconimage= '%s_V1_.SX593_SY799_.jpg'%(match.group(1))
                    fanart= '%s_V1.jpg'%(match.group(1))
            except:
                    pass
            try:    
                    match= regex1.search(iconimage1)
                    iconimage= '%s.gif'%(match.group(1))
                    fanart= '%s_V1.jpg'%(match.group(1))
            except:
                    pass
                    addDir(name,url,30,iconimage,None,description)   
                    set_view('list') 
        try:
                url='http://akas.imdb.com'+str(nextp1)
                name= '[COLOR blue][B]Next Page >>[/B][/COLOR]'
                addDir(name,url,48,'',None,'')
                set_view('list') 
        except:
                pass
        addDir('[COLOR red][B]<< Return To Main Menu[/B][/COLOR]','url','','',None,'')    
        set_view('list')

def IMDBGENRE(url):
        link=OPEN_URL(url)
        match = re.compile('<a href="/genre/(.+?)">(.+?)</a>').findall(link)
        for url1, name, in match:
                url=' http://akas.imdb.com/search/title?genres=%s&title_type=feature&sort=moviemeter,asc'% (url1)
                iconimage=art+url1+'.png'
                addDir(name,url,34,iconimage,None,'')
                set_view('list')

def IMDBGENRETV(url):
        link=OPEN_URL(url)
        match = re.compile('<a href="/genre/(.+?)">(.+?)</a>').findall(link)
        for url1, name, in match:
                url=' http://akas.imdb.com/search/title?genres=%s&title_type=tv_movie,tv_series,tv_special'% (url1)
                iconimage=art+url1+'.png'
                addDir(name,url,48,iconimage,None,'')
                set_view('list')

def onechannelinfo(url):
        url = 'http://www.primewire.ag'
        html = get_html(url)
        match = re.compile('<input type="hidden" name="key" value="(.+?)" />').findall(html)
        return match

def musicnewrelease(url):
        html = get_html(url)
        match =  re.compile('<a class=".+?" href="(.+?)" title="(.+?)" style=".+?" data-tooltip=".+?"><img class="lazy" src=".+?" data-original=".+?"  width="140" height="139" alt=".+?" style=""><noscript><img src="(.+?)" width="140" height="139" alt=".+?" style=""></noscript></a>').findall(html)
        for url, name, thumbnail in match:
                addDir(name,url,40,thumbnail,None,'')
        set_view('list')

def billboard200(url):
        html = get_html(url)
        match =  re.compile('<p class="chart_info">.+?<a href="(.+?)" title="(.+?)">.+?</a>.+?<img typeof="foaf:Image" src="(.+?)" alt="(.+?)".+?</div>',re.DOTALL).findall(html)
        for url, name, thumbnail, title in match:
                addDir(name+ ' - ' +title,url,40,thumbnail,None,'')
        nextpage = re.compile('<li class="pager-item"><a href="(.+?)">21 \xe2\x80\x93 40</a></li>').findall(link)
        if nextpage:
                addDir('[COLOR blue]Next Page >>[/COLOR]','http://www.billboard.com/charts/billboard-200'+nextpage[0],39,'',None,'')
        set_view('list')

def BILLBOARD_ALBUM_LISTS(name,url):
        html = get_html(url)
        match = re.compile('"title" : "(.+?)"\r\n.+?"artist" : "(.+?)"\r\n.+?image" : "(.+?)"\r\n.+?"entityId" : ".+?"\r\n.+?"entityUrl" : "(.+?)"').findall(html)
        for name, artist, iconimage, url in match:
            artist=artist.replace('&','And')
            url='http://www1.billboard.com'+url+'#'+url
            if re.search('.gif',iconimage):
                iconimage=icon
            addDir(artist,url,40,iconimage,None,name)    
        set_view('list')

def Music_genre(url):
        html = get_html(url)
        match=re.compile('<a href="/genre(.+?)">\n.+?span>(.+?)</span>').findall(html)
        for url, name in match:
                url=allmusic_url+'/genre'+url
        addDir(name,url,40,'',None,'')
        set_view('list')

def SEASONS(url):
        url1 = 'http://www.primewire.ag'+url
        html = get_html(url1)
        match=re.compile('<h2><a href="(.+?)">(.+?)</a></h2>').findall(html)
        for url,name in match:
                addDir(name,url,56,'',None,'TV-Shows')
        set_view('seasons')

def EPISODES(url):
        EnableMeta = local.getSetting('Enable-Meta')
        url1 = 'http://www.primewire.ag'+url
        html = get_html(url1)
        match = re.compile('<h1 class="titles"><span>\r\n.+?<a href=".+?">(.+?)</a>.+?</span></h1>.+?<div class="tv_episode_item"> <a href="(.+?)">(.+?)                                <span class="tv_episode_name">(.+?)</span>\r\n.+?</a> </div>',re.DOTALL).findall(html)
        for name,url,name1,name2 in match:
                if EnableMeta == 'true':  addDir(name+' - '+name1 + name2,url,30,'','tvshow','TV-Shows')
                if EnableMeta == 'false': addDir(name+' - '+name1 + name2,url,30,thumbnail,None,'TV-Shows')
        set_view('episodes')        
                


####################################################################################################################################################################################                
                         
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    return link


def add_testexecuteaddons(name):
        search = name
        testexecuteaddons = []
    
    
        if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.icefilms'):
                testexecuteaddons.append(('Search Icefilms','XBMC.Container.Update(%s?mode=555&url=%s&search=%s&nextPage=%s)' % (
                        'plugin://plugin.video.icefilms/', 'http://www.icefilms.info/', search, '1')))
    
        if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.projectfreetv'):
                testexecuteaddons.append(('Search projectfreetv', 'XBMC.Container.Update(%s?mode=search&url=url&name=%s)' % (
                        'plugin://plugin.video.projectfreetv/', search)))
    
        if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.tubeplus'):
                testexecuteaddons.append(('Search tubeplus', 'XBMC.Container.Update(%s?mode=130&url=url&name=%s)' % (
                        'plugin://plugin.video.tubeplus/', search)))
    
        if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.alluc'):
                testexecuteaddons.append(('Search alluc', 'XBMC.Container.Update(%s?mode=22&url=url&name=%s)' % (
                        'plugin://plugin.video.alluc/', search)))
    
        if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.movie25'):
                testexecuteaddons.append(('Search Mashup', 'XBMC.Container.Update(%s?mode=4&url=%s)' % (
                        'plugin://plugin.video.movie25/', search)))

        return testexecuteaddons

###########################################################################################################################################################################

def add_executeaddons(name):
        #name = name.replace('([\d]{4}\)','')
        search = name
        addons_name = []
        addons_context = []
        EnableIcefilms = local.getSetting('Enable-Icefilms')
        Enable1channel = local.getSetting('Enable-1channel')
        Enablesimplymovies = local.getSetting('Enable-SimplyMovies')
        EnableMashup = local.getSetting('Enable-Mashup')
        EnableMuchmovies = local.getSetting('Enable-Muchmovies')
        Enablemoviekingdom = local.getSetting('Enable-moviekingdom')
        EnableWhatthefurk = local.getSetting('Enable-Whatthefurk')
        EnableFilmikz = local.getSetting('Enable-Filmikz')
        EnableMegamovieline = local.getSetting('Enable-Megamovieline')
        EnableDailyflix = local.getSetting('Enable-Dailyflix')
        EnableAlluc = local.getSetting('Enable-Alluc')        
        EnableMoviefork = local.getSetting('Enable-Moviefork')
        EnableMerdb = local.getSetting('Enable-Merdb')
        EnableSolarmovie = local.getSetting('Enable-Solarmovie')
        EnableSceper = local.getSetting('Enable-Sceper')        
        EnablereleaseBB = local.getSetting('Enable-releaseBB')        
        Enableoneclickwatch = local.getSetting('Enable-oneclickwatch')
        Enablerlscenter = local.getSetting('Enable-rlscenter')
        Enablescenelog = local.getSetting('Enable-scenelog')
        Enableddlvalley = local.getSetting('Enable-ddlvalley')
        Enableisceners = local.getSetting('Enable-isceners')
        Enable1linkmovies = local.getSetting('Enable-1linkmovies')
        Enablemyvideolinks = local.getSetting('Enable-myvideolinks')
        Enablescenesource = local.getSetting('Enable-scenesource')
        Enablesinglelinkmoviez = local.getSetting('Enable-singlelinkmoviez')
        Enabletheextopia = local.getSetting('Enable-theextopia')
        Enablewrzko = local.getSetting('Enable-wrzko')
        EnableNavix = local.getSetting('Enable-Navix')        
        Enablevidics = local.getSetting('Enable-vidics')
        EnableNewznab = local.getSetting('Enable-Newznab')
        EnableNoobRoom = local.getSetting('Enable-NoobRoom')
        EnableOCM = local.getSetting('Enable-OCM')
        EnableIwatchonline = local.getSetting('Enable-Iwatchonline')
        EnableEasyNews = local.getSetting('Enable-EasyNews')
        Enablexbmctorrenttpb = local.getSetting('Enable-xbmctorrentpbt')
        Enablexbmctorrentka = local.getSetting('Enable-xbmctorrentka')
        Enablexbmctorrentyify = local.getSetting('Enable-xbmctorrentyify')
        if EnableIcefilms == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.icefilms'):
                        addons_name.append('IceFilms')
                        addons_context.append('plugin://plugin.video.icefilms/?mode=555&url=http://www.icefilms.info/&search='+urllib.quote_plus(search)+'&nextPage=1')
                        #addons_context.append('plugin://plugin.video.icefilms/?mode=55&name=Search&url=http%3a%2f%2fwww.icefilms.info%2f='+urllib.quote_plus(search)+'&nextPage=1')
        if Enable1channel == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.1channel'):
                        addons_name.append('1channel (Movies)')
                        addons_context.append('plugin://plugin.video.1channel/?mode=7000&section=&query='+urllib.quote_plus(search)+'=')
        if Enablesimplymovies == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.simplymovies'):
                        addons_name.append('Simplymovies')
                        addons_context.append('plugin://plugin.video.simplymovies/?mode=5&url=url&page=0&search=' + urllib.quote_plus(search))
        if EnableNoobRoom == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.NoobRoom'):
                        addons_name.append('NoobRoom')
                        #searchnb = search.replace(' ','+')
                        addons_context.append('plugin://plugin.video.NoobRoom/?mode=17&name='+urllib.quote_plus(search)+'&url=%2fsearch')
        if EnableMashup == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.movie25'):
                        addons_name.append('Mashup')
                        searchmp = search.replace(' ','%20')
                        addons_context.append('plugin://plugin.video.movie25/?mode=4&url='+urllib.quote_plus(searchmp))
        if EnableMuchmovies == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.muchmovies'):
                        addons_name.append('Muchmovies')
                        addons_context.append('plugin://plugin.video.muchmovies/?mode=7&name='+urllib.quote_plus(search)+'&url=%2fsearch')
        if Enablemoviekingdom == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.moviekingdom'):
                        addons_name.append('MovieKingdom')
                        addons_context.append('plugin://plugin.video.moviekingdom/?mode=200&url='+search+'&imdb=SRO')
        if EnableWhatthefurk == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.whatthefurk'):
                        addons_name.append('WhatTheFurk')
                        addons_context.append('plugin://plugin.video.whatthefurk/?mode=movie dialog menu&url=url&name='+urllib.quote_plus(search))
        if EnableFilmikz == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.filmikz'):
                        addons_name.append('Filmikz')
                        addons_context.append('plugin://plugin.video.filmikz/?mode=7&url=url&name='+urllib.quote_plus(search))
        if EnableMegamovieline == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.mmline'):
                        addons_name.append('Megamovieline')
                        addons_context.append('plugin://plugin.video.mmline/?mode=30&url=url&name='+urllib.quote_plus(search))
        if EnableDailyflix == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.dailyflix'):
                        addons_name.append('Dailyflix')
                        addons_context.append('plugin://plugin.video.dailyflix/?mode=32&url=url&name='+urllib.quote_plus(search))
        if EnableAlluc == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.alluc'):
                        searchalluc = search.replace(' ','%20')
                        addons_name.append('Alluc')
                        addons_context.append('plugin://plugin.video.alluc/?mode=22&url=url&name='+urllib.quote_plus(searchalluc))
        if EnableMoviefork == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.moviefork'):
                        addons_name.append('Moviefork')
                        addons_context.append('plugin://plugin.video.moviefork/?mode=Search&url=url&section=movies&pageno=1&pagecount=1&title='+urllib.quote_plus(search))
        if EnableMerdb == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.merdb'):
                        addons_name.append('Merdb')
                        addons_context.append('plugin://plugin.video.merdb/?mode=Search&section=movies&url='+urllib.quote_plus('http://merdb.ru/')+'&title='+urllib.quote_plus(search))
        if EnableSolarmovie == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.solarmovie.so'):
                        addons_name.append('Solarmovie.so')
                        addons_context.append('plugin://plugin.video.solarmovie.so/?mode=Search&section=movies&title='+urllib.quote_plus(search))
        if EnableSceper == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.sceper'):
                        addons_name.append('Sceper')
                        addons_context.append('plugin://plugin.video.sceper/?mode=Search&section=movies&query='+str(search))
        if EnablereleaseBB == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.releaseBB'):
                        addons_name.append('releaseBB')
                        addons_context.append('plugin://plugin.video.releaseBB/?mode=Search&query='+str(search))
        if Enableoneclickwatch == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.oneclickwatch'):
                        addons_name.append('oneclickwatch')
                        addons_context.append('plugin://plugin.video.oneclickwatch/?mode=Search&query='+str(search))
        if Enablerlscenter == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.rls-center'):
                        addons_name.append('rls-center')
                        addons_context.append('plugin://plugin.video.rls-center/?mode=Search&query='+str(search))
        if Enablescenelog == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.scenelog'):
                        addons_name.append('scenelog')
                        addons_context.append('plugin://plugin.video.rls-center/?mode=Search&query='+str(search))
        if Enableddlvalley == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.ddlvalley'):
                        addons_name.append('ddlvalley')
                        addons_context.append('plugin://plugin.video.ddlvalley/?mode=Search&query='+str(search))
        if Enableisceners == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.isceners'):
                        addons_name.append('isceners')
                        addons_context.append('plugin://plugin.video.isceners/?mode=Search&query='+str(search))
        if Enable1linkmovies == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.1-linkmovies'):
                        addons_name.append('1-linkmovies')
                        addons_context.append('plugin://plugin.video.1-linkmovies/?mode=Search&query='+str(search))
        if Enablemyvideolinks == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.myvideolinks'):
                        addons_name.append('myvideolinks')
                        addons_context.append('plugin://plugin.video.myvideolinks/?mode=Search&query='+str(search))
        if Enablescenesource == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.scene-source'):
                        addons_name.append('scene-source')
                        addons_context.append('plugin://plugin.video.scene-source/?mode=Search&query='+str(search))
        if Enablesinglelinkmoviez == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.singlelinkmoviez'):
                        addons_name.append('singlelinkmoviez')
                        addons_context.append('plugin://plugin.video.singlelinkmoviez/?mode=Search&query='+str(search))
        if Enabletheextopia == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.theextopia'):
                        addons_name.append('theextopia')
                        addons_context.append('plugin://plugin.video.theextopia/?mode=Search&query='+str(search))
        if Enablewrzko == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.wrzko'):
                        addons_name.append('wrzko')
                        addons_context.append('plugin://plugin.video.wrzko/?mode=Search&query='+str(search))                
        if EnableNavix == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.navi-x'):
                        addons_name.append('Navi-x (plugin only) [COLOR blue][B]Keyboard entry only[/B][/COLOR]' )
                        addons_context.append('plugin://plugin.navi-x/?date&mode=0&name='+search+'%20navi-xtreme&processor&type=search&url=http%3a%2f%2fwww.navixtreme.com%2fplaylist%2fsearch%2f')
        if Enablevidics == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.vidics'):
                        addons_name.append('vidics [COLOR blue][B]Keyboard entry only[/B][/COLOR]')
                        #addons_context.append('plugin://plugin.video.vidics/?mode=28&name='+urllib.quote_plus(search)+'&url=%2fsearch')
                        addons_context.append('plugin://plugin.video.vidics/?mode=28&url=movies&searchtext='+urllib.quote_plus(search))
        if EnableNewznab == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.newznab'):
                        addons_name.append('Newznab [COLOR blue][B]Keyboard entry only[/B][/COLOR]')
                        addons_context.append('plugin://plugin.video.newznab/?catid=2000&index=1&mode=newznab&newznab=search&'+search+'=')
        if EnableOCM == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.OCM'):
                        addons_name.append('OCM [COLOR red][B]Not working just yet[/B][/COLOR]')
                        addons_context.append('plugin://plugin.video.OCM/?mode=universalsearch&url='+urllib.quote_plus(search))
        if EnableIwatchonline == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.iwatchonline'):
                        addons_name.append('Iwatchonline [COLOR red][B]Not working just yet[/B][/COLOR]')
                        addons_context.append('plugin://plugin.video.iwatchonline/?mode=search&url=&query'+urllib.quote_plus(search))
        if EnableEasyNews == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.EasyNews'):
                        addons_name.append('EasyNews [COLOR blue][B]Keyboard entry only[/B][/COLOR]')
                        addons_context.append('plugin://plugin.video.EasyNews/?mode=6&name='+urllib.quote_plus(search)+'&url=%2fsearch')
        if Enablexbmctorrenttpb == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.xbmctorrent'):
                        addons_name.append('xbmctorrent (The Pirate Bay)')
                        addons_context.append('plugin://plugin.video.xbmctorrent/tpb/search?%s' % urllib.urlencode({'query': search}))
        if Enablexbmctorrentka == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.xbmctorrent'):
                        addons_name.append('xbmctorrent (Kickass Torrents) [COLOR red][B]Not working just yet[/B][/COLOR]')
                        addons_context.append('plugin://plugin.video.xbmctorrent/kickass/search?%s' % urllib.urlencode({'query': search}))
        if Enablexbmctorrentyify == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.xbmctorrent'):
                        addons_name.append('xbmctorrent (yify) [COLOR red][B]Not working just yet[/B][/COLOR]')
                        addons_context.append('plugin://plugin.video.xbmctorrent/yify/search?%s' % urllib.urlencode({'query': search}))
                
        

        
        dialog = xbmcgui.Dialog()
        ret = dialog.select('Select one of the addons below', addons_name)
        if ret == -1:
                return 
        contextommand = addons_context[ret]
        xbmc.executebuiltin('Container.Update('+contextommand+')')
        

def add_executeaddonstv(name):
        search = name
        addons_name = []
        addons_context = []
        EnableIcefilmstv = local.getSetting('Enable-Icefilmstv')
        Enable1channeltv = local.getSetting('Enable-1channeltv')
        EnableProjectfreetv = local.getSetting('Enable-Projectfreetv')
        EnableRlsmix = local.getSetting('Enable-Rlsmix')
        EnableTubeplus = local.getSetting('Enable-Tubeplus')
        Enabletvrelease = local.getSetting('Enable-tvrelease')
        Enablesimplymoviestv = local.getSetting('Enable-SimplyMoviestv')
        Enablemoviekingdomtv = local.getSetting('Enable-moviekingdomtv')
        EnableWhatthefurk = local.getSetting('Enable-Whatthefurktv')
        EnableAlluctv = local.getSetting('Enable-Alluctv')        
        EnableMerdbtv = local.getSetting('Enable-Merdbtv')
        EnableSolarmovietv = local.getSetting('Enable-Solarmovietv')
        EnableScepertv = local.getSetting('Enable-Scepertv')        
        EnablereleaseBBtv = local.getSetting('Enable-releaseBBtv')        
        Enableoneclickwatchtv = local.getSetting('Enable-oneclickwatchtv')
        Enablerlscentertv = local.getSetting('Enable-rlscentertv')
        Enablescenelogtv = local.getSetting('Enable-scenelogtv')
        Enableddlvalleytv = local.getSetting('Enable-ddlvalleytv')
        Enableiscenerstv = local.getSetting('Enable-iscenerstv')
        Enablemyvideolinkstv = local.getSetting('Enable-myvideolinkstv')
        Enablescenesourcetv = local.getSetting('Enable-scenesourcetv')
        Enabletheextopiatv = local.getSetting('Enable-theextopiatv')
        Enablewrzkotv = local.getSetting('Enable-wrzkotv')
        EnableNavixtv = local.getSetting('Enable-Navixtv')        
        Enablevidicstv = local.getSetting('Enable-vidicstv')
        EnableNewznabtv = local.getSetting('Enable-Newznabtv')
        EnableOCMtv = local.getSetting('Enable-OCMtv')
        EnableIwatchonlinetv = local.getSetting('Enable-Iwatchonlinetv')
        EnableEasyNewstv = local.getSetting('Enable-EasyNewstv')
        Enablexbmctorrenttpbtv = local.getSetting('Enable-xbmctorrentpbttv')
        Enablexbmctorrentkatv = local.getSetting('Enable-xbmctorrentkatv')
        Enablexbmctorrentyifytv = local.getSetting('Enable-xbmctorrentyifytv')
        if EnableIcefilmstv == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.icefilms'):
                        addons_name.append('IceFilms')
                        addons_context.append('plugin://plugin.video.icefilms/?mode=555&url=http://www.icefilms.info/&search='+search+'&nextPage=1')
        if EnableRlsmix == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.movie25'):
                        addons_name.append('Rlsmix (TV)')
                        searchrm = search.replace(' ','%20')
                        addons_context.append('plugin://plugin.video.movie25/?mode=137&url='+urllib.quote_plus(searchrm))
        if Enable1channeltv == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.1channel'):
                        addons_name.append('1channel (Tv)')
                        addons_context.append('plugin://plugin.video.1channel/?mode=7000&section=tv&query='+urllib.quote_plus(search)+'=')
        if Enablesimplymoviestv == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.simplymovies'):
                        addons_name.append('Simplymovies (TV)')
                        addons_context.append('plugin://plugin.video.simplymovies/?mode=4&url=url&page=0&search=' + urllib.quote_plus(search))
        if EnableAlluctv == 'true':  
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.alluc'):
                        addons_name.append('Alluc')
                        searchmp = search.replace(' ','%20')
                        addons_context.append('plugin://plugin.video.alluc/?mode=22&url=url&name='+searchmp)
        if EnableWhatthefurk == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.whatthefurk'):
                        addons_name.append('WhatTheFurk')
                        addons_context.append('plugin://plugin.video.whatthefurk/?mode=episode dialog menu&url=url&name='+urllib.quote_plus(search))
        if EnableMerdbtv == 'true': 
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.merdb'):
                        addons_name.append('Merdb')
                        addons_context.append('plugin://plugin.video.merdb/?mode=Search&section=tvshows&url='+urllib.quote_plus('http://merdb.ru/')+'&title='+urllib.quote_plus(search))
        if EnableSolarmovietv == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.solarmovie.so'):
                        addons_name.append('Solarmovie.so')
                        addons_context.append('plugin://plugin.video.solarmovie.so/?mode=Search&section=tv&title='+urllib.quote_plus(search))
        if EnableScepertv == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.sceper'):
                        addons_name.append('Sceper')
                        addons_context.append('plugin://plugin.video.sceper/?mode=Search&section=tv-shows&query='+str(search))
        if EnablereleaseBBtv == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.releaseBB'):
                        addons_name.append('releaseBB')
                        addons_context.append('plugin://plugin.video.releaseBB/?mode=Search&query='+str(search))
        if Enableoneclickwatchtv == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.oneclickwatch'):
                        addons_name.append('oneclickwatch')
                        addons_context.append('plugin://plugin.video.oneclickwatch/?mode=Search&query='+str(search))
        if Enablerlscentertv == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.rls-center'):
                        addons_name.append('rls-center')
                        addons_context.append('plugin://plugin.video.rls-center/?mode=Search&query='+str(search))
        if Enablescenelogtv == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.scenelog'):
                        addons_name.append('scenelog')
                        addons_context.append('plugin://plugin.video.rls-center/?mode=Search&query='+str(search))
        if Enableddlvalleytv == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.ddlvalley'):
                        addons_name.append('ddlvalley')
                        addons_context.append('plugin://plugin.video.ddlvalley/?mode=Search&query='+str(search))
        if Enableiscenerstv == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.isceners'):
                        addons_name.append('isceners')
                        addons_context.append('plugin://plugin.video.isceners/?mode=Search&query='+str(search))
        if Enablemyvideolinkstv == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.myvideolinks'):
                        addons_name.append('myvideolinks')
                        addons_context.append('plugin://plugin.video.myvideolinks/?mode=Search&query='+str(search))
        if Enablescenesourcetv == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.scene-source'):
                        addons_name.append('scene-source')
                        addons_context.append('plugin://plugin.video.scene-source/?mode=Search&query='+str(search))
        if Enabletheextopiatv == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.theextopia'):
                       addons_name.append('theextopia')
                       addons_context.append('plugin://plugin.video.theextopia/?mode=Search&query='+str(search))
        if Enablewrzkotv == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.wrzko'):
                        addons_name.append('wrzko')
                        addons_context.append('plugin://plugin.video.wrzko/?mode=Search&query='+str(search))
        if EnableProjectfreetv == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.projectfreetv'):
                        addons_name.append('ProjectFreeTv [COLOR blue][B]Keyboard Only[/B][/COLOR]')
                        searchpft = search.replace(' ','+')
                        addons_context.append('plugin://plugin.video.projectfreetv/?mode=search&section=shows='+urllib.quote_plus(search))
        if EnableNewznabtv == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.newznab'):
                        addons_name.append('Newznab [COLOR blue][B]Keyboard entry only[/B][/COLOR]')
                        addons_context.append('plugin://plugin.video.newznab/?catid=5000&index=1&mode=newznab&newznab=search='+urllib.quote_plus(search))
        if EnableNavixtv == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.navi-x'):
                        addons_name.append('Navi-x (plugin only) [COLOR blue][B]Keyboard entry only[/B][/COLOR]' )
                        addons_context.append('plugin://plugin.navi-x/?date&mode=0&name='+urllib.quote_plus(search)+'%20navi-xtreme&processor&type=search&url=http%3a%2f%2fwww.navixtreme.com%2fplaylist%2fsearch%2f')
        if Enablevidicstv == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.vidics'):
                        addons_name.append('vidics [COLOR blue][B]Keyboard entry only[/B][/COLOR]')
                        addons_context.append('plugin://plugin.video.vidics/?mode=29&name='+urllib.quote_plus(search)+'&url=%2fsearch')
        if EnableIwatchonlinetv == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.iwatchonline'):
                        addons_name.append('IwatchOnline (Tv) [COLOR red][B]Not working just yet[/B][/COLOR]')
                        addons_context.append('plugin://plugin.video.iwatchonline/?mode=Search&query=wentworth&searchin=t')#&searchin=t')
        if EnableTubeplus == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.tubeplus'):
                        addons_name.append('TubePlus [COLOR blue][B]Keyboard entry only[/B][/COLOR]')
                        addons_context.append('plugin://plugin.video.tubeplus/?mode=130&name='+urllib.quote_plus(search)+'TV%20Shows&types=None&url=url')
        if Enabletvrelease == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.tv-release'):
                        addons_name.append('TV-Release (TV) [COLOR red][B]Not working just yet[/B][/COLOR]')
                        addons_context.append('plugin://plugin.video.tv-release/?mode=21&name='+urllib.quote_plus(search)+'&types=None&url=url')
        if EnableEasyNewstv == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.EasyNews'):
                        addons_name.append('EasyNews (TV) [COLOR blue][B]Keyboard entry only[/B][/COLOR]')
                        addons_context.append('plugin://plugin.video.EasyNews/?mode=12&name='+urllib.quote_plus(search)+'&url=%2fsearch')
        if Enablexbmctorrenttpbtv == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.xbmctorrent'):
                        addons_name.append('xbmctorrent (The Pirate Bay)')
                        addons_context.append('plugin://plugin.video.xbmctorrent/tpb/search?%s' % urllib.urlencode({'query': search}))
        if Enablexbmctorrentkatv == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.xbmctorrent'):
                        addons_name.append('xbmctorrent (Kickass Torrents) [COLOR red][B]Not working just yet[/B][/COLOR]')
                        addons_context.append('plugin://plugin.video.xbmctorrent/kickass/search?%s' % urllib.urlencode({'query': search}))
        if Enablexbmctorrentyifytv == 'true':
                if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.xbmctorrent'):
                        addons_name.append('xbmctorrent (yify) [COLOR red][B]Not working just yet[/B][/COLOR]')
                        addons_context.append('plugin://plugin.video.xbmctorrent/yify/search?%s' % urllib.urlencode({'query': search}))
        #if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.hdtv-release'):
                #addons_name.append('HDTV-Release (TV)[COLOR red][B]Not working just yet[/B][/COLOR]')
                #addons_context.append('plugin://plugin.video.hdtv-release/?mode=GetSearchQuery&url='+search)
        

        
        dialog = xbmcgui.Dialog()
        ret = dialog.select('Select one of the addons below', addons_name)
        if ret == -1:
                return
        contextommand = addons_context[ret]
        xbmc.executebuiltin('Container.Update('+contextommand+')')
       

def add_executeaddonsmusic(name):
        search = name
        addons_name = []
        addons_context = []
        if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.icefilms'):
                addons_name.append('IceFilms')
                addons_context.append('plugin://plugin.video.icefilms/?mode=555&url=http://www.icefilms.info/&search='+search+'&nextPage=1')
        if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.audio.xbmchubmusic'):
                addons_name.append('xbmchubmusic [COLOR red][B]Not working just yet[/B][/COLOR]')
                addons_context.append('plugin://plugin.audio.xbmchubmusic/?mode=216&name='+urllib.quote_plus(search)+'%20Search&url=url')
        if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.audio.searchmp3mobi-master'):
                addons_name.append('searchmp3mobi [COLOR red][B]Not working just yet[/B][/COLOR]')
                addons_context.append('plugin://plugin.audio.searchmp3mobi/?mode=Search&url=url&name='+name)
        if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.vevo'):
                addons_name.append('vevo [COLOR red][B]Not working just yet[/B][/COLOR]')
                addons_context.append('plugin://plugin.video.vevo/?mode=searchArtists&url=url&name='+name)
        
        
        dialog = xbmcgui.Dialog()
        ret = dialog.select('Search For "'+search.title()+'" At The Addons Below', addons_name)
        if ret == -1:
                return
        contextommand = addons_context[ret]
        xbmc.executebuiltin('Container.Update('+contextommand+')')

##############################################################################################################################################################################

def getSchedule(sched_date): 
        url="http://www.vidics.ch/calendar/"+sched_date+ ".html"
        print "selected_date|" + url
        html = get_html(url)
        newlink = ''.join(html.splitlines()).replace('\t','')
        listcontent=re.compile('<div class="indexClanedarDay left" id="date_'+sched_date+'">(.+?)</div>').findall(newlink)
        print 
        if(len(listcontent)>0):
                latestepi=re.compile('<h3 itemscope itemtype="http://schema.org/TVSeries" class="CalTvshow" title="(.+?)">(.+?)</h3>').findall(listcontent[0])
                for vtmp,vcontent in latestepi:
                        (sUrl,stmp,sName)=re.compile('<a itemprop="url" class="CalTVshowName pukeGreen" href="(.+?)" title="(.+?)">(.+?)</a>').findall(vcontent)[0]
                        (eUrl,eName)=re.compile('<a itemprop="url" class="CalTVshowEpisode blue" href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(vcontent)[0]
                        addDirContext(RemoveHTML(sName),strdomain+sUrl,57,"","","tv")
                        addDirsehedule("  --"+RemoveHTML(eName),strdomain+eUrl,57,"")  
def List4Days():
        sched_date=str(datetime.date.today())
        date_name=time.strftime("%A", time.strptime(sched_date, "%Y-%m-%d"))
        addDir("Today's ("+sched_date+") TV Schedule "+sched_date,'',58,'',None,'')
        sched_date=str(datetime.date.today()-datetime.timedelta(days=1))
        date_name=time.strftime("%A", time.strptime(sched_date, "%Y-%m-%d"))
        addDir(date_name+"'s ("+sched_date+") TV Schedule "+sched_date,'',58,'',None,'')
        sched_date=str(datetime.date.today()-datetime.timedelta(days=2))
        date_name=time.strftime("%A", time.strptime(sched_date, "%Y-%m-%d"))
        addDir(date_name+"'s ("+sched_date+") TV Schedule "+sched_date,'',58,'',None,'')
        sched_date=str(datetime.date.today()-datetime.timedelta(days=3))
        date_name=time.strftime("%A", time.strptime(sched_date, "%Y-%m-%d"))
        addDir(date_name+"'s ("+sched_date+") TV Schedule "+sched_date,'',58,'',None,'')
        sched_date=str(datetime.date.today()-datetime.timedelta(days=4))
        date_name=time.strftime("%A", time.strptime(sched_date, "%Y-%m-%d"))
        addDir(date_name+"'s ("+sched_date+") TV Schedule "+sched_date,'',58,'',None,'')
        sched_date=str(datetime.date.today()-datetime.timedelta(days=5))
        date_name=time.strftime("%A", time.strptime(sched_date, "%Y-%m-%d"))
        addDir(date_name+"'s ("+sched_date+") TV Schedule "+sched_date,'',58,'',None,'')
        sched_date=str(datetime.date.today()-datetime.timedelta(days=6))
        date_name=time.strftime("%A", time.strptime(sched_date, "%Y-%m-%d"))
        addDir(date_name+"'s ("+sched_date+") TV Schedule "+sched_date,'',58,'',None,'')

##############################################################################################################################################################################

def IMDB_LISTS(url):
        addDir('IMDb watchlist',IMDBTV_WATCHLIST,14,art_('Watchlist','Sub Menus'),None,'')
        addDir('In Theaters',IMDbIT_url,15,art_('In Theaters','Sub Menus'),None,'')
        addDir('Top 250',IMDb250_url,17,art_('Top 250','Sub Menus'),None,'')
        addDir('Genre','http://akas.imdb.com/genre',33,art_('Genre','Sub Menus'),None,'')
        addDir('Search',IMDb_url,32,art_('Search','Sub Menus'),None,'')
        if local.getSetting('imdb_user') == 'ur********':
                xbmcgui.Dialog().ok('The Collective Information','You Need To Input Your IMDb Number Into ','Addon Settings')
        if local.getSetting('message') == 'false':
                xbmcgui.Dialog().ok('The Collective Information','            For Full Support For This Plugin Please Visit','                    [COLOR yellow][B]WWW.XBMCHUB.COM[/B][/COLOR]','Please Turn Off Message in Addon Settings')
        #url=IMDB_LIST
        #link=OPEN_URL(url)
        #match = re.compile('<div class="list_name"><b><a    onclick=".+?"     href="(.+?)"    >(.+?)</a>').findall(link)
        #for url, name in match:
                #url='http://www.imdb.com'+str(url)+'?start=1&view=grid&sort=listorian:asc&defaults=1'
                #addDir(name,url,35,art_('IMDb','Sub Menus'),None,'')
                #set_view('list')

def IMDB_LISTSTV(url):
        addDir('IMDb watchlist',IMDBTV_WATCHLIST,14,art_('Watchlist','Sub Menus'),None,'')
        addDir('Genre','http://akas.imdb.com/genre',45,art_('Genre','Sub Menus'),None,'')
        addDir('Search',IMDb_url,44,art_('Search','Sub Menus'),None,'')
        set_view('list')
        if local.getSetting('imdb_user') == 'ur********':
                xbmcgui.Dialog().ok('The Collective Information','You Need To Input Your IMDb Number Into ','Addon Settings')
        if local.getSetting('message') == 'false':
                xbmcgui.Dialog().ok('The Collective Information','            For Full Support For This Plugin Please Visit','                    [COLOR yellow][B]WWW.XBMCHUB.COM[/B][/COLOR]','Please Turn Off Message in Addon Settings')
        #url=IMDB_LIST

           
def WATCH_TV_LIST(url):
        link=OPEN_URL(url)
        link=str(link).replace('\n','').replace('src="http://i.media-imdb.com/images/SFaa265aa19162c9e4f3781fbae59f856d/nopicture/medium/film.png" ','')
        link=link.split('<div class="list grid">')[1]
        link=link.split('<div class="see-more">')[0]
        match=re.compile('''src="(.+?)".+?<a href="(.+?)">(.+?)</a>''').findall(link)
        for iconimage, url, name in match:
                if re.search('V1', iconimage, re.IGNORECASE):
                        regex=re.compile('(.+?)_V1.+?.jpg')
                        match = regex.search(iconimage)
                        iconimage='%s_V1_.SX593_SY799_.jpg'%(match.group(1))
                        fanart=str(iconimage).replace('_.SX593_SY799_','')
                else:
                        fanart='None'
                url = 'http://akas.imdb.com'+str(url)
                name=str(name).replace('&#xB7;','').replace('&#x27;','').replace('&#x26;','And').replace(':','')
                series=str(name)
                description=''
                addDir(name,url,35,iconimage,None,'')
        url=IMDB_LIST
        nextpage = re.compile('<div class="pagination">\n.+?\n.+?\n.+?<a href="(.+?)">Next&nbsp;&raquo;</a>\n\n.+?</div>',re.DOTALL).findall(link)
        if nextpage:
                addDir('[COLOR blue]Next Page >>[/COLOR]',IMDBTV_WATCHLIST+'/watchlist'+nextpage[0],14,'',None,'')
                set_view('list')

def WATCH_MOVIE_LIST(url):
        link=OPEN_URL(url)
        link=str(link).replace('\n','').replace('src="http://i.media-imdb.com/images/SFaa265aa19162c9e4f3781fbae59f856d/nopicture/medium/film.png" ','')
        link=link.split('<div class="list grid">')[1]
        link=link.split('<div class="see-more">')[0]
        match=re.compile('''src="(.+?)".+?<a href="(.+?)">(.+?)\(([\d]{4}\))</a>''').findall(link)
        for iconimage, url, name, year in match:
                if re.search('V1', iconimage, re.IGNORECASE):
                        regex=re.compile('(.+?)_V1.+?.jpg')
                        match = regex.search(iconimage)
                        iconimage='%s_V1_.SX593_SY799_.jpg'%(match.group(1))
                        fanart=str(iconimage).replace('_.SX593_SY799_','')
                else:
                        fanart='None'
                url = 'http://akas.imdb.com'+str(url)
                name=str(name).replace('&#xB7;','').replace('&#x27;','').replace('&#x26;','And').replace(':','')
                series=str(name)
                description=''
                addDir(name,url,12,iconimage,None,'')
                set_view('list') 
                        
def WATCH_LIST_SEARCH(name,url):
        series = str(name)
        dialog = xbmcgui.Dialog()
        if dialog.yesno("Please Select Correct Type", "", "[COLOR blue]               Please Select If Item Is A Movie Or Tv Series[/COLOR]", '', "MOVIE", "TV"): 
                        add_executeaddonstv(name)
        else:
                        add_executeaddons(name)

    
################################################################################################################################################################
        
def Supersearch(url):
        EnableMeta = local.getSetting('Enable-Meta')
        searchStr = ''
        keyboard = xbmc.Keyboard(searchStr, "Search The Collective")
        keyboard.doModal()
        if (keyboard.isConfirmed() == False):
                return
        searchstring = keyboard.getText()
        if len(searchstring) == 0:
                return
        newStr = searchstring.replace(' ','%20')
        mashup = 'http://www.movie25.so'
        IMDb_url = 'http://akas.imdb.com'
        tv_release = 'http://tv-release.net'
        ochannel = 'http://www.primewire.ag'
        mashuplinks = re.compile('<input type="hidden" name="key" value="(.+?)" />').findall(mashup)
        tv_releaselinks = re.compile('<input type="hidden" name="key" value="(.+?)" />').findall(tv_release)
        ochannellinks = re.compile('<input type="hidden" name="key" value="(.+?)" />').findall(ochannel)
        newStr1 = str(ochannellinks)
        newStr2 = str(tv_releaselinks)
        newStr3 = str(mashuplinks)
        ochannellink = OPEN_URL(ochannel+'/index.php?search_keywords=&key='+newStr3+'&search_section=1')
        tv_releaselink = OPEN_URL(tv_release+'/index.php?search_keywords=&key='+newStr2+'&search_section=1')
        mashuplink = OPEN_URL(mashup+'/index.php?search_keywords=&key='+newStr3+'&search_section=1')
        match =  re.compile('<a href="(.+?)" title="Watch (.+?)"><img src="(.+?)" border="0" width="150" height="225" alt=".+?"><h2>.+?</h2></a>').findall(mashup)
        match1 =  re.compile('<a href="(.+?)" title="Watch (.+?)"><img src="(.+?)" border="0" width="150" height="225" alt=".+?"><h2>.+?</h2></a>').findall(tv_release)
        match2 =  re.compile('<a href="(.+?)" title="Watch (.+?)"><img src="(.+?)" border="0" width="150" height="225" alt=".+?"><h2>.+?</h2></a>').findall(ochannel)
        for url, name, thumbnail in match:
                if ochannellist == 'true':  addDir(name.encode('UTF-8','ignore'),url,12,'','Movie','Movies')
        for url, name, thumbnail in match1:
                if mashuplist == 'true': addDir(name.encode('UTF-8','ignore'),url,12,'','Movie','Movies')
        for url, name, thumbnail in match2:
                if tv_releaelist == 'true': addDir(name.encode('UTF-8','ignore'),url,12,'','Movie','Movies')
                
        set_view('list')

def Searchtvshows(url):
        EnableMeta = local.getSetting('Enable-Meta')
        searchStr = ''
        keyboard = xbmc.Keyboard(searchStr, "Search")
        keyboard.doModal()
        if (keyboard.isConfirmed() == False):
                return
        searchstring = keyboard.getText()
        if len(searchstring) == 0:
                return
        newStr = searchstring.replace(' ','%20')
        link = OPEN_URL(url+'/index.php?search_keywords='+newStr+'&key=(.+?)&search_section=2')
        match =  re.compile('<a href="(.+?)" title="Watch (.+?)"><img src="(.+?)" border="0" width="150" height="225" alt=".+?"><h2>.+?</h2></a>').findall(link)
        for url, name, thumbnail in match:
                if EnableMeta == 'true': addDir(name.encode('UTF-8','ignore'),url,30,'','tvshow','TV-Shows')
                if EnableMeta == 'false': addDir(name.encode('UTF-8','ignore'),url,30,'',None,'TV-Shows')
        set_view('list')

def IMDB_SEARCH(url):
        EnableMeta = local.getSetting('Enable-Meta')
        searchStr = ''
        keyboard = xbmc.Keyboard(searchStr, "Search")
        keyboard.doModal()
        if (keyboard.isConfirmed() == False):
                return
        searchstring = keyboard.getText()
        if len(searchstring) == 0:
                return
        newStr = searchstring.replace(' ','%20')
        #http://www.imdb.com/find?q='+newStr+'&s=all'
        html = get_html(url+'/search/title?title='+newStr+'&title_type=feature,tv_movie,documentary,video')
        
        match =  re.compile('<a href="(.+?)" title="(.+?)\(([\d]{4}\))"><img src="(.+?)" height="74" width="54" alt=".+?" title=".+?"></a>').findall(html)
        for url, name, year, thumbnail in match:
                name = str(name).replace('&#xB7;','').replace('&#x27;','').replace('&#x26;','And').replace('&#xE9;','e').replace('&amp;','And').replace('&#x22;','"')
                if EnableMeta == 'true':  addDir(name,url,12,'','Movie','Movies')
                if EnableMeta == 'false': addDir(name,url,12,thumbnail,None,'Movies')
        set_view('list')

def IMDB_SEARCHTV(url):
        EnableMeta = local.getSetting('Enable-Meta')
        searchStr = ''
        keyboard = xbmc.Keyboard(searchStr, "Search")
        keyboard.doModal()
        if (keyboard.isConfirmed() == False):
                return
        searchstring = keyboard.getText()
        if len(searchstring) == 0:
                return
        newStr = searchstring.replace(' ','%20')
        #http://www.imdb.com/find?q='+newStr+'&s=all'
        html = get_html(url+'/search/title?title='+newStr+'&title_type=tv_movie,tv_series,tv_episode,tv_special,mini_series')
        
        match =  re.compile('<a href="(.+?)" title="(.+?)\(([\d]{4}\s\TV\s\Series\))"><img src="(.+?)" height="74" width="54" alt=".+?" title=".+?"></a>').findall(html)
        for url, name, year, thumbnail in match:
                name = str(name).replace('&#xB7;','').replace('&#x27;','').replace('&#x26;','And').replace('&#xE9;','e').replace('&amp;','And').replace(' TV Series','').replace('&#x22;','"')
                if EnableMeta == 'true':  addDir(name,url,30,'','tvshow','TV-Shows')
                if EnableMeta == 'false': addDir(name,url,30,thumbnail,None,'TV-Shows')
        set_view('list')

def UNIVERSALSEARCH(name):
        EnableMeta = local.getSetting('Enable-Meta')
        newStr = name.replace(' ','%20')
        #http://www.imdb.com/find?q='+newStr+'&s=all'
        html = get_html(' http://akas.imdb.com/search/title?title='+newStr+'&title_type=feature,tv_movie,documentary,video')
        
        match =  re.compile('<a href="(.+?)" title="(.+?)\(([\d]{4}\))"><img src="(.+?)" height="74" width="54" alt=".+?" title=".+?"></a>').findall(html)
        for url, name, year, thumbnail in match:
                name = str(name).replace('&#xB7;','').replace('&#x27;','').replace('&#x26;','And').replace('&#xE9;','e').replace('&amp;','And').replace('&#x22;','"')
                if EnableMeta == 'true':  addDir(name,url,12,'','Movie','Movies')
                if EnableMeta == 'false': addDir(name,url,12,thumbnail,None,'Movies')
        set_view('list')

def UNIVERSALSEARCHTV(name):
        EnableMeta = local.getSetting('Enable-Meta')
        newStr = name.replace(' ','%20')
        #http://www.imdb.com/find?q='+newStr+'&s=all'
        html = get_html(' http://akas.imdb.com/search/title?title='+newStr+'&title_type=tv_movie,tv_series,tv_episode,tv_special,mini_series')
        
        match =  re.compile('<a href="(.+?)" title="(.+?)\(([\d]{4}\s\TV\s\Series\))"><img src="(.+?)" height="74" width="54" alt=".+?" title=".+?"></a>').findall(html)
        for url, name, year, thumbnail in match:
                name = str(name).replace('&#xB7;','').replace('&#x27;','').replace('&#x26;','And').replace('&#xE9;','e').replace('&amp;','And').replace(' TV Series','').replace('&#x22;','"')
                if EnableMeta == 'true':  addDir(name,url,12,'','tvshow','TV-Shows')
                if EnableMeta == 'false': addDir(name,url,12,thumbnail,None,'TV-Shows')
        set_view('list')

def TVDBSearch(url):
        EnableMeta = local.getSetting('Enable-Meta')
        searchStr = ''
        keyboard = xbmc.Keyboard(searchStr, "Search")
        keyboard.doModal()
        if (keyboard.isConfirmed() == False):
                return
        searchstring = keyboard.getText()
        if len(searchstring) == 0:
                return
        newStr = searchstring.replace(' ','%20')
        link = OPEN_URL(url+'/index.php?search_keywords='+newStr+'&key=fdd6063da4415536&search_section=2')
        match =  re.compile('<a href="(.+?)" title="Watch (.+?)"><img src="(.+?)" border="0" width="150" height="225" alt=".+?"><h2>.+?</h2></a>').findall(link)
        for url, name, thumbnail in match:
                if EnableMeta == 'true':  addDir(name.encode('UTF-8','ignore'),url,30,'','tvshow','TV-Shows')
                if EnableMeta == 'false': addDir(name.encode('UTF-8','ignore'),url,30,thumbnail,None,'TV-Shows')
        setView('movies', 'default')

def SearchMusicArtist(url):
        searchStr = ''
        keyboard = xbmc.Keyboard(searchStr, "Search")
        keyboard.doModal()
        if (keyboard.isConfirmed() == False):
                return
        searchstring = keyboard.getText()
        if len(searchstring) == 0:
                return
        newStr = searchstring.replace(' ','%20')
        html = get_html(url+'/search/all/'+newStr)
        match = re.compile('<a href="(.+?)" data-tooltip=".+?">\n                <img src="(.+?)" height="100" alt="(.+?)">\n            </a>').findall(html)
        for url, thumbnail, name in match:
                addDir(name,url,30,thumbnail,None,'')
        set_view('list')

def artist_search(url):
        do_artist_search(SEARCH())
                
def do_artist_search(search_entered):
        name=str(search_entered).replace('+','')
        #fanart=get_fanart(name)
        html = get_html('http://www.allmusic.com/search/artists/'+search_entered)

        match=re.compile('<div class="photo">\n.+?a href="(.+?)" data-tooltip=".+?">\n.+?img src="(.+?).jpg.+?" height=".+?" alt="(.+?)">').findall(html)
        for url,iconimage,artist in match:
                url=allmusic_url+url+'/discography'
                iconimage=iconimage.replace('JPG_170','JPG_400')+'.jpg'
                addDir(artist,url,40,iconimage,None,artist)
                set_view('list')

                

def SEARCH():
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, 'Search Music...XBMCHUB.COM')
        keyboard.doModal()
        if keyboard.isConfirmed():
                search_entered = keyboard.getText() .replace(' ','+')  # sometimes you need to replace spaces with + or %20
                if search_entered == None:
                        return False
        return search_entered 

#######################################################################################################################################################################

def get_subscriptions():
    try:
        content = read_from_file(SUBSCRIPTION_FILE)
        lines = content.split('\n')
        
        for line in lines:
            data = line.split('\t')
            if len(data) == 2:
                if data[1].startswith('tt'):
                    tv_show_name = clean_file_name(data[0].split('(')[0][:-1])
                    tv_show_imdb = data[1]
                    tv_show_mode = "strm tv show dialog"
                    create_tv_show_strm_files(tv_show_name, tv_show_imdb, tv_show_mode, TV_SHOWS_PATH)
                else:
                    mode = data[1]
                    items = get_menu_items(name, mode, "", "")
                    
                    for (url, li, isFolder) in items:
                        paramstring = url.replace(sys.argv[0], '')
                        params = get_params(paramstring)
                        movie_name = urllib.unquote_plus(params["name"])
                        movie_data = urllib.unquote_plus(params["name"])
                        movie_imdb = urllib.unquote_plus(params["imdb_id"])
                        movie_mode = "strm movie dialog"
                        create_strm_file(movie_name, movie_data, movie_imdb, movie_mode, MOVIES_PATH)
        xbmc.executebuiltin('UpdateLibrary(video)')
                    
    except:
        xbmc.log("[Failed to fetch subscription")

def subscription_index(name, mode):
    try:
        content = read_from_file(SUBSCRIPTION_FILE)
        line = str(name) + '\t' + str(mode)
        lines = content.split('\n')
        index = lines.index(line)
        return index
    except:
        return -1 #Not subscribed

def subscribe(name, mode):
    if subscription_index(name, mode) >= 0:
        return
    content = str(name) + '\t' + str(mode) + '\n'
    write_to_file(SUBSCRIPTION_FILE, content, append=True)
    
def unsubscribe(name, mode):
    index = subscription_index(name, mode)
    if index >= 0:
        content = read_from_file(SUBSCRIPTION_FILE)
        lines = content.split('\n')
        lines.pop(index)
        s = ''
        for line in lines:
            if len(line) > 0:
                s = s + line + '\n'
        
        if len(s) == 0:
            os.remove(SUBSCRIPTION_FILE)
        else:
            write_to_file(SUBSCRIPTION_FILE, s)

def create_strm_file(name, data, imdb_id, mode, dir_path):
    try:
        strm_string = create_url(name, mode, data=data, imdb_id=imdb_id)
        filename = clean_file_name("%s.strm" % name)
        path = os.path.join(dir_path, filename)
        stream_file = open(path, 'w')
        stream_file.write(strm_string)
        stream_file.close()
    except:
        xbmc.log("Error while creating strm file for : " + name)

def remove_strm_file(name, dir_path):
    try:
        filename = "%s.strm" % (clean_file_name(name, use_blanks=False))
        path = os.path.join(dir_path, filename)
        os.remove(path)
    except:
        xbmc.log("[Was unable to remove movie: %s" % (name)) 

#######################################################################################################################################################################

def smart_unicode(s):
        """credit : sfaxman"""
        if not s:
                return ''
        try:
                if not isinstance(s, basestring):
                        if hasattr(s, '__unicode__'):
                                s = unicode(s)
                        else:
                                s = unicode(str(s), 'UTF-8')
                elif not isinstance(s, unicode):
                        s = unicode(s, 'UTF-8')
        except:
                if not isinstance(s, basestring):
                        if hasattr(s, '__unicode__'):
                                s = unicode(s)
                        else:
                                s = unicode(str(s), 'ISO-8859-1')
                elif not isinstance(s, unicode):
                        s = unicode(s, 'ISO-8859-1')
        return s

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'): params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2: param[splitparams[0]]=splitparams[1]
        return param

def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok

def RemoveHTML(strhtml):
            html_re = re.compile(r'<[^>]+>')
            strhtml=html_re.sub('', strhtml)
            return strhtml

def addDirContext(name,url,mode,iconimage,plot="",vidtype="", cm=[]):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&vidtype="+vidtype
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot": plot} )
        if(len(cm)==0):
                contextMenuItems = AddFavContext(vidtype, url, name, iconimage)
        else:
                contextMenuItems=cm
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDirsehedule(name,url,mode,iconimage,plot=""):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot": plot} )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


def addDir(name,url,mode,iconimage,types,favtype):
        ok=True
        type = types
        if type != None: infoLabels = GRABMETA(name,types)
        else: infoLabels = {'title':name}
        try: img = infoLabels['cover_url']
        except: img= iconimage
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=img)
        liz.setInfo( type="Video", infoLabels= infoLabels)
        try: liz.setProperty( "Fanart_Image", infoLabels['backdrop_url'] )
        except: t=''
        contextMenuItems = []
        contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        #Universal Favorites
        if 'Movies' in favtype:
                contextMenuItems.append(('Add to Favorites', fav.add_directory(name, u, section_title='Movies')))
                liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        elif 'TV-Shows' in favtype:
                contextMenuItems.append(('Add to Favorites', fav.add_directory(name, u, section_title='TV-Shows')))
                liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        else:
                contextMenuItems.append(('Add to Favorites', fav.add_directory(name, u, section_title='Other Favorites')))
                liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        
#####################################################################################################################################################################
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

params=get_params()
url=None; name=None; mode=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass

print "Mode: "+str(mode); print "URL: "+str(url); print "Name: "+str(name)
   
        
#these are the modes which tells the plugin where to go
if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        NZBmovie(url)

elif mode==2:
        print ""+url
        TVSHOWScat()
        
elif mode==3:
        print ""+url
        MOVIEScat()

elif mode==4:
        print ""+url
        MOVIESgene(url)

elif mode==5:
        print ""+url
        TVSHOWSgene(url)

elif mode==6:
        print ""+url
        OPEN_URL(url)

elif mode==7:
        print ""+url
        getTorrents(url, page)
                
elif mode==8:
        print ""+url
        Download(url)

elif mode==9:
        print ""+url
        Searchmovies(url)

elif mode==10:
        print ""+url
        OPEN_playercorefactory()

elif mode==11:
        print ''+url
        OPEN_URL(url)

elif mode==12:
        print ''+url
        add_executeaddons(name)

elif mode==13:
        print ''+url
        IMDB_LISTS(url)

elif mode==14:
        print ''+url
        WATCH_TV_LIST(url)

elif mode==15:
        print ''+url
        IMDbInTheaters(url)

elif mode==16:
        print ''+url
        IMDbcat()

elif mode==17:
        print ''+url
        IMDbrate(url)

elif mode==18:
        print ''+url
        onechannelmfeature(url)

elif mode==19:
        print ''+url
        onechanneltvfeature(url)

elif mode==20:
        print ''+url
        onechannellastest(url)

elif mode==21:
        print ''+url
        onechannellastesttv(url)

elif mode==22:
        print ''+url
        onechannelmpopular(url)

elif mode==23:
        print ''+url
        onechanneltvpopular(url)

elif mode==24:
        print ''+url
        onechannelmratings(url)

elif mode==25:
        print ''+url
        onechanneltvratings(url)

elif mode==26:
        print ''+url
        onechannelmreleasedate(url)

elif mode==27:
        print ''+url
        onechanneltvreleasedate(url)

elif mode==28:
        print ''+url
        Searchtvshows(url)

elif mode==29:
        print ''+url
        MUSICcat()

elif mode==30:
        print ''+url
        add_executeaddonstv(name)

elif mode==31:
        print ''+url
        TVDBSearch(url)

elif mode==32:
        print ''+url
        IMDB_SEARCH(url)
                
elif mode==33:
        print ''+url
        IMDBGENRE(url)

elif mode==34:
        print ''+url
        ALLTIMEIMDB(url)

elif mode==35:
        print ''+url
        WATCH_LIST_SEARCH(name,url)

elif mode==36:
        print ''+url
        SearchMusicArtist(url)

elif mode==37:
        print ''+url
        MUSICsearch()

elif mode==38:
        print ''+url
        musicnewrelease(url)

elif mode==39:
        print ''+url
        BILLBOARD_ALBUM_LISTS(name,url)

elif mode==40:
        print ''+url
        add_executeaddonsmusic(name)

elif mode==41:
        print ''+url
        Music_genre(url)

elif mode==42:
        print ''+url
        do_artist_search(search_entered)

elif mode==43:
        print ''+url
        artist_search(url)

elif mode==44:
        print ''+url
        IMDB_SEARCHTV(url)

elif mode==45:
        print ''+url
        IMDBGENRETV(url)

elif mode==46:
        print ''+url
        IMDbtvcat()

elif mode==47:
        print ''+url
        WATCH_MOVIE_LIST(url)

elif mode==48:
        print ''+url
        ALLTIMEIMDBTV(url)

elif mode==49:
        print ''+url
        KIDSzone(url)

elif mode==50:
        print ''+url
        KIDSzonetv(url)

elif mode==51:
        print ''+url
        UNIVERSALSEARCH(name)

elif mode==52:
        print ''+url
        UNIVERSALSEARCHTV(name)

elif mode==53:
        print ''+url
        IMDB_LISTSTV(url)

elif mode==54:
        print ''+url
        add_testexecuteaddons(name)

elif mode==55:
        print ''+url
        SEASONS(url)

elif mode==56:
        print ''+url
        EPISODES(url)

elif mode==57:
        print ''+url
        List4Days()

elif mode==58:
        print ''+url
        getSchedule(sched_date)
                
elif mode==309:
        print ''+url
        addon.addon.openSettings()

                
xbmcplugin.endOfDirectory(int(sys.argv[1]))
