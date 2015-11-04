# coding: utf-8


def loadSettings():
    import ConfigParser
    inifile = ConfigParser.SafeConfigParser()
    inifile.read("./settings.ini")
    return {
            'key': inifile.get(u'auth', u'key'),
            'secret': inifile.get(u'auth', u'secret'),
            }

def verifyWriteAuth(flickr):
    flickr.get_request_token(oauth_callback=u'oob')
    authorize_url = flickr.auth_url(perms=u'write')
    webbrowser.open_new_tab(authorize_url)
    verifier = unicode(str(raw_input()))
    print(verifier) 
    flickr.get_access_token(verifier)

def genTimeStamp():
    u'''

        generate timestamp 
        >>> 
        >>>
    '''
    from datetime import datetime
    return unicode(datetime.now().strftime("%y%m/%d_%H:%M:%S"))


def genGallaryName():
    prefix=u'360'
    ts = genTimeStamp()

    return prefix + ts

def createGallary(flickr, title, key):
    return flickr.galleries.create(api_key=key,
                                title=title,
                                description='store')
def uploadPhoto(key, secret, filename):
    flickr = flickrapi.FlickrAPI(key, secret)
    return flickr.upload(filename = u'360.jpg', is_public=0)

if __name__ == "__main__":
    import flickrapi
    import webbrowser
    import picamera
    
    #verify check
    setting = loadSettings()
    print(setting)
    flickr = flickrapi.FlickrAPI(setting['key'], setting['secret'],format='json')
    if not flickr.token_valid(perms=u'write'):
        verifyWriteAuth(flickr)


    #res =  createGallary(flickr, gName, setting['key'])
    #galry_id = res['gallery']['id']
    counter =1000;
    #createGallary
    gName = genGallaryName()
    

    while(counter!=0):
        with picamera.PiCamera() as camera:
            camera.resolution = (2592, 1944)

    # take photo
    path = u'360.jpg'
    res = uploadPhoto(setting['key'], setting['secret'],path)
    #upload photo to created gallary
    # photo add gallary
    

