import urllib,urllib2,re,xbmcplugin,xbmcgui,urlresolver,xbmc,xbmcplugin,xbmcgui,xbmcaddon,os,sys
from metahandler import metahandlers
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
from universal import favorites
from universal import _common as univ_common

###############################################################################################################

addon_id = 'plugin.video.collective'
local = xbmcaddon.Addon(id=addon_id)
collectivepath = local.getAddonInfo('path')
addon = Addon(addon_id, sys.argv)
datapath = addon.get_profile()
art = collectivepath+'/art'
net = Net()
fav = favorites.Favorites('plugin.video.collective', sys.argv)
artRadio='http://www.thedarewall.com/mp3/images/bgcont.png'


##### Common Functions #####
def eod(): addon.end_of_directory()
def addst(r,s=''): return addon.get_setting(r)   ## Get Addon Settings
def addpr(r,s=''): return addon.queries.get(r,s) ## Get Addon Params
def tfalse(r,d=False): ## Get True / False
	if   (r.lower()=='true' ): return True
	elif (r.lower()=='false'): return False
	else: return d
def set_view(content='none',view_mode=50):
	h=int(sys.argv[1])
	if (content is not 'none'): xbmcplugin.setContent(h, content) ### set content type so library shows more views and info
	if (tfalse(addst('auto-view'))==True):
		if (content=='movies'):					view_mode=addst('movies-view')
		elif (content=='tvshows'):			view_mode=addst('tvshows-view')
		elif (content=='seasons'):			view_mode=addst('season-view')
		elif (content=='episodes'):			view_mode=addst('episode-view')
		elif (content=='links'):				view_mode=addst('links-view')
		elif (content=='list'):					view_mode=addst('default-view')
		else:														view_mode=addst('default-view')
		xbmc.executebuiltin("Container.SetViewMode(%s)" % view_mode)
_artPath=xbmc.translatePath(os.path.join(collectivepath,'art'))
def art_(f,fo='',fe='.png'): 
	if (fo is not ''): return xbmc.translatePath(os.path.join(os.path.join(_artPath,fo),f+fe))
	else: return xbmc.translatePath(os.path.join(_artPath,f+fe))
##### /\ ##### Common Functions #####

def imdbtv_watchlist_url():
        return "http://www.imdb.com/user/" + local.getSetting('imdb_user') + "/watchlist?start=1&view=grid&sort=listorian:asc&defaults=1"
    
def imdb_list_url():
        return 'http://www.imdb.com/user/' + local.getSetting('imdb_user') + '/lists?tab=public'


