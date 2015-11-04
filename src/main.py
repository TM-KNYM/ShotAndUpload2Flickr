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

def genCaptureName():
    prefix=u'.jpg'
    ts = genTimeStamp()
    return ts+prefix


def genGallaryName():
    prefix=u'360'
    ts = genTimeStamp()
    return prefix + ts

def addPhoto2Gallary(flickr, key, photoId, galleryId):
    return flickr.galleries.addPhoto(api_key=key,
                                gallery_id=galleryId,
                                photo_id=photoId)
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
    #import picamera
    import sys

    #verify check
    setting = loadSettings()
    print(setting)
    flickr = flickrapi.FlickrAPI(setting['key'], setting['secret'],format='json')
    if not flickr.token_valid(perms=u'write'):
        verifyWriteAuth(flickr)


    #galry_id = res['gallery']['id']
    counter = int(sys.argv[1]);
    #createGallary
    gName = genGallaryName()
    res = createGallary(flickr, gName, setting['key'])
    import json
    print res
    galleryid = json.loads(res)[u'gallery'][u'id']

    for x in range(0,counter):
        #with picamera.PiCamera() as camera:
            # take photo
            #camera.resolution = (2592, 1944)
            #capName=genCaptureName()
            #camera.capture(capName)
            capName = u'360.jpg'
            res = uploadPhoto(setting['key'], setting['secret'],capName)
            photoid = int(res[0].text)
            res = addPhoto2Gallary(flickr, setting['key'], photoid,galleryid)
            print res
            #upload photo to created gallary
            # photo add gallary
    

