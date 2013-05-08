
# External
from gettext import gettext as _
import logging

# Sugar
from sugar3.activity.activity import Activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityButton
from sugar3.activity.widgets import TitleEntry
from sugar3.activity.widgets import StopButton
from sugar3.activity.widgets import ShareButton
from sugar3.activity.widgets import DescriptionItem

# GStreamer
from gi.repository import Gtk
from gst_stack import GSTStack

# Create Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class TestWindow(Activity):

    def __init__(self, handler):
	Activity.__init__(self, handler)
	self.max_participants = 1
	self.setup_toolbar()

        # Create Drawing Area
        self.draw = Gtk.DrawingArea()
        self.draw.show()

        # Apply Canvas
        self.set_canvas(self.draw)

        # Add signal for realized
        self.get_canvas().connect('realize', self.setup_gstreamer)

    def setup_gstreamer(self, sender):

        # Create GStreamer for Testing
        self.gst = GSTStack()

        # Get Video Bus
        self.bus = self.gst.build_preview()

        # Attach to Preview
        self.bus.connect("sync-message::element", self.draw_preview)

    def draw_preview(self, bus, message):
        if message.get_structure() is None:
            return

        # Capture the new GStreamer handle request
        if message.get_structure().get_name() == "prepare-window-handle":
            message.src.set_window_handle(self.draw.get_window().get_xid())

        # # Size DrawingArea to Fit
        # self.draw.set_size_request(
        #         self.draw.get_parent().get_parent().get_allocation().width,
        #         self.draw.get_parent().get_parent().get_allocation().height)


    def setup_toolbar(self):
        toolbar_box = ToolbarBox()
        activity_button = ActivityButton(self)
        toolbar_box.toolbar.insert(activity_button, 0)
        activity_button.show()
        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()
        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()
        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

