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
    return unicode(datetime.now().strftime("%y%m%d_%H%M%S"))

def genCaptureName():
    prefix=u'.jpg'
    ts = genTimeStamp()
    return ts+prefix


def genPhotosetName():
    prefix=u'360_'
    ts = genTimeStamp()
    return prefix + ts

def createPhotoSet(flickr, key, title, photoId):
    return flickr.photosets.create(api_key=key,
                                  title=title,
                                  primary_photo_id=photoId)


def addPhoto2Photoset(flickr, key, photoId, photosetId):
    return flickr.photosets.addPhoto(api_key=key,
                                photo_id=photoId,
                                photoset_id=photosetId)
def createGallery(flickr, title, key):
    return flickr.galleries.create(api_key=key,
                                title=title,
                                description='store')
def uploadPhoto(key, secret, filename):
    flickr = flickrapi.FlickrAPI(key, secret)
    return flickr.upload(filename = filename, is_public=0)

if __name__ == "__main__":
    import flickrapi
    import webbrowser
    import picamera
    import sys
    import os

    #verify check
    setting = loadSettings()
    print(setting)
    flickr = flickrapi.FlickrAPI(setting['key'], setting['secret'],format='json')
    if not flickr.token_valid(perms=u'write'):
        verifyWriteAuth(flickr)


    #galry_id = res['gallery']['id']
    counter = int(sys.argv[1]);
    #createGallery
    gName = genPhotosetName()
    res = createPhotoSet(flickr,  setting['key'],gName, u'22738376382')
    import json
    print res
    photosetId = json.loads(res)[u'photoset'][u'id']

    print('XXXXXXXX  '+photosetId)

    for x in range(0,counter):
        capName=genCaptureName()

        with picamera.PiCamera() as camera:
            # take photo
            print camera
            camera.resolution = (2592, 1944)
            print capName
            camera.capture(capName)
            #capName = u'360.jpg'

        res = uploadPhoto(setting['key'], setting['secret'],capName)
        photoid = res[0].text
        print photoid
        res = addPhoto2Photoset(flickr, setting['key'], photoid,photosetId)
        os.remove(capName)

        #upload photo to created gallary
        # photo add gallary
    

