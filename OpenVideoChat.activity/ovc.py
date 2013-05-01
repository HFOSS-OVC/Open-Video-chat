#    This file is part of OpenVideoChat.
#
#    OpenVideoChat is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    OpenVideoChat is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with OpenVideoChat.  If not, see <http://www.gnu.org/licenses/>.
"""
:mod: `OpenVideoChat/OpenVideoChat.activity/ovc` -- Open Video Chat
=======================================================================

.. moduleauthor:: Justin Lewis <jlew.blackout@gmail.com>
.. moduleauthor:: Taylor Rose <tjr1351@rit.edu>
.. moduleauthor:: Fran Rogers <fran@dumetella.net>
.. moduleauthor:: Remy DeCausemaker <remyd@civx.us>
.. moduleauthor:: Luke Macken <lmacken@redhat.com>
.. moduleauthor:: Casey DeLorme <cxd4280@rit.edu>
"""


#External Imports
import logging
from gettext import gettext as _
from sugar3.presence import presenceservice
from sugar3.graphics.alert import NotifyAlert
from sugar3.activity.activity import Activity


# Slated for possible removal
# import fcntl
# import array
# import socket
# import struct
# from sugar3 import profile
# from gi.repository import GObject


#Local Imports
from gui import Gui
from gst_stack import GSTStack
from network_stack import NetworkStack


# Constants
SUGAR_MAX_PARTICIPANTS = 2


# Define Logger for Logging & DEBUG level for Development
logger = logging.getLogger("ovc-" + __name__)
logger.setLevel(logging.DEBUG)


class OpenVideoChatActivity(Activity):

    def __init__(self, handle):
        Activity.__init__(self, handle)

        # Self-Enforced max_participants
        self.max_participants = SUGAR_MAX_PARTICIPANTS


        """ Setup GUI """
        logger.debug("Preparing GUI")
        self.set_canvas(Gui(self))


        """ Setup GSTStack """
        logger.debug("Setting up GSTStack")
        # self.gststack = GSTStack(self.get_canvas().render_preview, self.get_canvas().render_incoming)
        # self.gststack.build_preview()
        # self.gststack.build_incoming_pipeline()
        # GObject.idle_add(self.gststack.start_stop_incoming_pipeline, True)

        # self.get_canvas().set_gstreamer_stack(self.gstreamer_stack);


        """ Setup Network Stack """
        logger.debug("Preparing Network Stack")
        self.network_stack = NetworkStack()
        self.establish_activity_sharing()
        # self.get_canvas().set_network_stack(self.network_stack)

    # Modularly apply single sharing handler, can be recalled on disconnect to re-establish event handling
    def establish_activity_sharing(self):
        if self.shared_activity:
            if self.get_shared():
                self.network_stack.setup(self)
            else:
                self.sharing_handler = self.connect('joined', self.network_stack.joined_cb)
        else:
            self.sharing_handler = self.connect('shared', self.network_stack.shared_cb)

    # Automate Tear-Down of OVC Components
    def can_close(self):
        logger.debug("Shutting down Network and GST")
        # self.gststack.start_stop_incoming_pipeline(False)
        # self.gststack.start_stop_outgoing_pipeline(False)
        return True


    """ Automated Alert Handling """

    def alert(self, title, text=None, timeout=5):
        if text != None:
            alert = NotifyAlert(timeout=timeout)
            alert.props.title = title
            alert.props.msg = text
            self.add_alert(alert)
            alert.connect('response', self.alert_cancel_cb)
            alert.show()

    def alert_cancel_cb(self, alert, response_id):
        self.remove_alert(alert)


    """ Journal Save and Restore """

    def write_file(self, file_path):
        file = open(file_path, 'w')
        try:
            file.write(self.get_canvas().get_history())
        finally:
            file.close()

    def read_file(self, file_path):
        file = open(file_path, 'r')
        try:
            for line in file:
                self.get_canvas().chat_write_line(line)
        finally:
            file.close()


    """ Old Code To Be Removed """

    # def net_cb(self, src, args):
    #     """
    #     Callback for network commands
    #     """

    #     # new chat message
    #     if src == "chat":
    #         message, sender = args
    #         self.get_canvas().receive_message(message)

    #     # join request
    #     elif src == "join":
    #         handle = self.netstack.get_tube_handle()
    #         if handle and self.sent_ip > 0:
    #             # http://code.activestate.com/recipes/439094-get-the-ip-address
    #             # -associated-with-a-network-inter/

    #             def get_ip_address(ifname):
    #                 s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #                 return socket.inet_ntoa(fcntl.ioctl(
    #                         s.fileno(),
    #                         0x8915,  # SIOCGIFADDR
    #                         struct.pack('256s', ifname[:15]))[20:24])

    #             # http://code.activestate.com/recipes/439093-get-names-of-all-
    #             # up-network-interfaces-linux-only/

    #             def all_interfaces():
    #                 max_possible = 128  # arbitrary. raise if needed.
    #                 bytes = max_possible * 32
    #                 s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #                 names = array.array('B', '\0' * bytes)
    #                 outbytes = struct.unpack('iL', fcntl.ioctl(
    #                     s.fileno(),
    #                     0x8912,  # SIOCGIFCONF
    #                     struct.pack('iL', bytes, names.buffer_info()[0])))[0]
    #                 namestr = names.tostring()
    #                 return [namestr[i:i + 32].split('\0', 1)[0] for i in range
    #                                                 (0, outbytes, 32)]


    #             for interface in all_interfaces():
    #                 if interface != 'lo':
    #                     try:
    #                         ip = get_ip_address(interface)
    #                         self.sent_ip = self.sent_ip - 1
    #                         handle.announce_ip(ip)
    #                         break
    #                     except:
    #                         print "Interface %s did not give ip" % interface
    #             else:
    #                 print "Could not find ip address"

    #     elif src == "ip":

    #         # fixme: Store ip with user so we can make user lists to switch
    #         # between later on

    #         if not hasattr(self, 'out'):
    #                 #~ s1,s2,s3 = self.out.get_state()
    #                 #~ if s2 == gst.STATE_PLAYING:
    #                 #~ print args,"has sent its ip, ignoring as we are already
    #                 #              streaming"
    #                 #~ else:

    #             self.gststack.build_outgoing_pipeline(args)

    #             # FIXME
    #             GObject.timeout_add(5000, self.gststack.start_stop_outgoing_pipeline)

    #         else:
    #             print args, "has sent its ip, ignoring as we are already \
    #                         streaming"

    #     elif src == "buddy_add":
    #         self.get_canvas().receive_message(_("%s has joined the chat") % args)

    #     elif src == "buddy_rem":
    #         self.get_canvas().receive_message(_("%s has left the chat") % args)

    # # Send new chat message
    # def send_message(self, text):
    #     handle = self.netstack.get_tube_handle()
    #     prof = profile.get_nick_name()

    #     if handle:
    #         handle.receive_message("<%s> %s" % (prof, text))

