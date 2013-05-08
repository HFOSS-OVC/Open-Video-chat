
# External Imports
import logging
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GstVideo, GdkX11


#Define the limitations of the device
# CAPS = "video/x-raw,width=320,height=240,framerate=15/1"
CAPS = "video/x-raw,width=640,height=480,framerate=15/1"

# Define Logger for Logging & DEBUG level for Development
logger = logging.getLogger("ovc-" + __name__)
logger.setLevel(logging.DEBUG)


class GSTStack(object):

    def __init__(self):
        Gst.init(None)
        self._out_pipe = None

    #Build Preview
    def build_preview(self):

        """ Prepare Elements """
        video_source = Gst.ElementFactory.make('autovideosrc', "video-source")
        video_rate = Gst.ElementFactory.make('videorate', None)
        video_caps = Gst.ElementFactory.make("capsfilter", None)
        video_caps.set_property("caps", Gst.caps_from_string(CAPS))
        video_queue = Gst.ElementFactory.make("queue", None)
        video_convert = Gst.ElementFactory.make("videoconvert", None)
        ximage_sink = Gst.ElementFactory.make("ximagesink", "video-output")
        # logger.debug(dir(ximage_sink))

        """ Create Pipeline """
        self.pipe = Gst.Pipeline()

        """ Add Elements to Pipeline """
        self.pipe.add(video_source)
        self.pipe.add(video_rate)
        self.pipe.add(video_caps)
        self.pipe.add(video_queue)
        self.pipe.add(video_convert)
        self.pipe.add(ximage_sink)

        """ Connect Elements """
        video_source.link(video_rate)
        video_rate.link(video_caps)
        video_caps.link(video_queue)
        video_queue.link(video_convert)
        video_convert.link(ximage_sink)

        # Grab the Bus
        bus = self.pipe.get_bus()

        # Listen to signals (messages) on bus
        bus.add_signal_watch()

        # Synchronously handle video transmission messages
        bus.enable_sync_message_emission()

        # Handler for EOS & Errors
        bus.connect('message', self.on_message)

        """ Begin Playing """
        self.pipe.set_state(Gst.State.PLAYING)

        """ Return Pipeline Bus """
        return self.pipe.get_bus()

    # Handle Errors and End of Stream
    def on_message(self, bus, message):
        if message.type == Gst.MessageType.EOS:
            logger.debug("End of Stream, Close Pipeline")
        elif message.type == Gst.MessageType.ERROR:
            try:
                err, debug = message.parse_error()
                logger.debug("Error: %s" % err, debug)
            except Exception:
                logger.debug("Unable to identify message error.")