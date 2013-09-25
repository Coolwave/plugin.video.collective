import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,sys

TITLE='Coolwave'    
    
def removefolder():   
    import glob
    super = xbmc.translatePath(os.path.join('special://home/addons','*superrepo*'))
    for infile in glob.glob(super):
	    for root, dirs, files in os.walk(infile):
	        for f in files:
	            try:
	                os.unlink(os.path.join(root, f))
	            except:
	                pass
	        for d in dirs:
	            try:
	                os.unlink(os.path.join(root, d))
	            except:
	                pass
	    
	    os.rmdir(infile)
	    
	    

    
    
def EXIT():
        dialog = xbmcgui.Dialog()
        dialog.ok(TITLE, "Sorry non of my plugins support super repo","if you want to carry on using my plugins", "then i suggest uninstalling super repo")
        if dialog.yesno(TITLE, "","Would you like me to unistall it now ??", ""):
            removefolder()
        else:
            xbmc.executebuiltin("XBMC.Container.Update(path,replace)")
            xbmc.executebuiltin("XBMC.ActivateWindow(Home)")
    
def GetFile():
     import glob
     super = xbmc.translatePath(os.path.join('special://home/addons','*superrepo*'))
     for infile in glob.glob(super):
         File=infile
         print infile
     try:
         return File
     except:
         return 'ALL OK'
         
         
         
         
if 'superrepo' in GetFile():
    EXIT()
