import xbmc, xbmcgui, xbmcaddon, urllib2, json, os

#get actioncodes from https://github.com/xbmc/xbmc/blob/master/xbmc/guilib/Key.h
ACTION_PREVIOUS_MENU = 10
ACTION_NAV_BACK = 92
ACTION_SELECT_ITEM = 7

Settings = xbmcaddon.Addon('script.module.seedboxpy')

_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path').decode('utf-8')

class SeedboxPy_XMBC(xbmcgui.Window):

    server = {  'uri':ur'http://{0}:{1}/server_status.json'.format(Settings.getSetting('server_address'),Settings.getSetting('server_port')),
                'user':Settings.getSetting('username'),
                'passwd':Settings.getSetting('password')
            }

    server_status = None
            
    def __init__(self):

        # Set the application as running
        self.running = True

        xbmcgui.lock()

        # Set the resolution for which the display is meant for
        self.setCoordinateResolution(3)

        self.backgroundImage = xbmcgui.ControlImage(1, 1, 1280, 720, os.path.join(_addon_path, 'resources', 'media', 'background.png'))
        self.backgroundImage.setHeight(self.getHeight())
        self.backgroundImage.setWidth(self.getWidth())
        self.addControl(self.backgroundImage)
        
        self.usedSpace = xbmcgui.ControlLabel(100, 100, 350, 25, 'Used Space:', textColor='0xFF333333')
        self.addControl(self.usedSpace)
        self.usedSpaceStat = xbmcgui.ControlLabel(475, 100, 350, 25, '', textColor='0xFF333333')
        self.addControl(self.usedSpaceStat)
        
        self.downloadsQueued = xbmcgui.ControlLabel(100, 137, 350, 25, 'Downloads Queued:', textColor='0xFF333333')
        self.addControl(self.downloadsQueued)
        self.downloadsQueuedStat = xbmcgui.ControlLabel(475, 137, 350, 25, '', textColor='0xFF333333')
        self.addControl(self.downloadsQueuedStat)
        
        
        self.httpDaemonStatus = xbmcgui.ControlLabel(100, 174, 350, 25, 'Http Daemon Status:', textColor='0xFF333333')
        self.addControl(self.httpDaemonStatus)
        
        self.httpDaemonStatusStatGreen = xbmcgui.ControlLabel(475, 174, 350, 25, 'Online', textColor='0xFF24CD1B')
        self.httpDaemonStatusStatGreen.setVisible(False)
        self.addControl(self.httpDaemonStatusStatGreen)
        
        self.httpDaemonStatusStatRed = xbmcgui.ControlLabel(475, 174, 350, 25, 'Offline', textColor='0xFFCD2D1B')
        self.httpDaemonStatusStatRed.setVisible(False)
        self.addControl(self.httpDaemonStatusStatRed)

        
        self.rssDaemonStatus = xbmcgui.ControlLabel(100, 211, 350, 25, 'RSS Daemon Status:', textColor='0xFF333333')
        self.addControl(self.rssDaemonStatus)        
        
        self.rssDaemonStatusStatGreen = xbmcgui.ControlLabel(475, 211, 350, 25, 'Online', textColor='0xFF24CD1B')
        self.rssDaemonStatusStatGreen.setVisible(False)
        self.addControl(self.rssDaemonStatusStatGreen)
        
        self.rssDaemonStatusStatRed = xbmcgui.ControlLabel(475, 211, 350, 25, 'Offline', textColor='0xFFCD2D1B')
        self.rssDaemonStatusStatRed.setVisible(False)
        self.addControl(self.rssDaemonStatusStatRed)
        
        
        self.queueDaemonStatus = xbmcgui.ControlLabel(100, 248, 350, 25, 'Queue Daemon Status:', textColor='0xFF333333')
        self.addControl(self.queueDaemonStatus)
        
        self.queueDaemonStatusStatGreen = xbmcgui.ControlLabel(475, 248, 350, 25, 'Online', textColor='0xFF24CD1B')
        self.queueDaemonStatusStatGreen.setVisible(False)
        self.addControl(self.queueDaemonStatusStatGreen)
        
        self.queueDaemonStatusStatRed = xbmcgui.ControlLabel(475, 248, 350, 25, 'Offline', textColor='0xFFCD2D1B')
        self.queueDaemonStatusStatRed.setVisible(False)
        self.addControl(self.queueDaemonStatusStatRed)

        self.loadingMessage = xbmcgui.ControlLabel(0,0,150,25, 'Loading...', textColor='0xFF333333')
        self.loadingMessage.setVisible(False)
        self.loadingMessage.setPosition((self.getWidth()-250), (self.getHeight()-125))
        self.addControl(self.loadingMessage)
        
        xbmcgui.unlock()
        
        if self._getData():
            self._loadData()
        
    def _getData(self):
        
        self.loadingMessage.setVisible(True)
        
        try:
            authHandler = urllib2.HTTPBasicAuthHandler()
            authHandler.add_password(
                realm='SeedboxPy',
                uri=self.server['uri'],
                user=self.server['user'],
                passwd=self.server['passwd'],
            )

            urlOpener = urllib2.build_opener(authHandler)
            urllib2.install_opener(urlOpener)
            server_status_json = urllib2.urlopen(self.server['uri']).read()

            self.server_status = json.loads(server_status_json)
            self.loadingMessage.setVisible(False)
            return True
        except:
            self.loadingMessage.setVisible(False)
            self._modal('Download Failed', 'Could not get the Server Status')
            return False
            
    def _loadData(self):
    
        xbmcgui.lock()
        self.usedSpaceStat.setLabel('{0} of {1}'.format(self.server_status['usedSpace'],self.server_status['maxUsedSpace']))
        self.downloadsQueuedStat.setLabel('{0}'.format(self.server_status['downloadsQueued']))
        
        if self.server_status['httpDaemonStatus']:
            self.httpDaemonStatusStatGreen.setVisible(True)
            self.httpDaemonStatusStatRed.setVisible(False)
        else:
            self.httpDaemonStatusStatGreen.setVisible(False)
            self.httpDaemonStatusStatRed.setVisible(True)

        if self.server_status['queueDaemonStatus']:
            self.queueDaemonStatusStatGreen.setVisible(True)
            self.queueDaemonStatusStatRed.setVisible(False)
        else:
            self.queueDaemonStatusStatGreen.setVisible(False)
            self.queueDaemonStatusStatRed.setVisible(True)

        if self.server_status['rssDaemonStatus']:
            self.rssDaemonStatusStatGreen.setVisible(True)
            self.rssDaemonStatusStatRed.setVisible(False)
        else:
            self.rssDaemonStatusStatGreen.setVisible(False)
            self.rssDaemonStatusStatGreen.setVisible(True)
        
        xbmcgui.unlock()

    def doAction(self, action):
        self._modal('button','Code Detected: {0}'.format(action.getButtonCode()))
        if action == ACTION_SELECT_ITEM:
            if self._getData():
                self._loadData()
        
    def _modal(self,title,message):
        modal = xbmcgui.Dialog()
        modal.ok(title,message)

if __name__ == '__main__':
    SeedboxPy = SeedboxPy_XMBC()
    SeedboxPy.doModal()
    del SeedboxPy