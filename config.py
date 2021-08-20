import os


class Config(object):
    TG_BOT_TOKEN = "1710612658:AAF9MbcpFHrJ-ZLP8XbrtC-U6emqp2Emaeo"
    APP_ID = "2192067"
    API_HASH = "d2e0ba99f1b9cdb632b43633edb76f11"
    AUDIO_THUMBNAIL = os.environ.get("AUDIO_THUMBNAIL", "")
    VIDEO_THUMBNAIL = os.environ.get("VIDEO_THUMBNAIL", "")
    UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", None)



#import os


#class Config(object):
  #  TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")

   # APP_ID = int(os.environ.get("APP_ID", 12345))

   # API_HASH = os.environ.get("API_HASH", "")

  #  AUDIO_THUMBNAIL = os.environ.get("AUDIO_THUMBNAIL", "")

  #  VIDEO_THUMBNAIL = os.environ.get("VIDEO_THUMBNAIL", "")

  #  UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", None)

