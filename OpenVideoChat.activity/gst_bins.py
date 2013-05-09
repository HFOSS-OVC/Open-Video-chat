#    This fileis part of OpenVideoChat.
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
:mod: `OpenVideoChat/OpenVideoChat.activity/gst_bins` --
        Open Video Chat GStreamer Bins
=======================================================================
.. moduleauthor:: Caleb Coffie <CalebCoffie@gmail.com>
.. moduleauthor:: Casey DeLorme <cxd4280@rit.edu>
"""


# External Imports
import logging
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst


# Define Logger for Logging & DEBUG level for Development
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Define caps for RTP Streams
# Theora requires this ugly base64-encoded information.
# TODO: Make this human-readable, and translate using a python base64 library.

VIDEO_RTP_CAPS = "video/x-theora, streamheader=(buffer)< 807468656f72610302010014000f0001400000f000000000000f000000010000010000010000c35000c0, 817468656f72612b000000586970682e4f7267206c69627468656f726120312e312032303039303832322028546875736e656c64612900000000, 827468656f7261becd28f7b9cd6b18b5a9494a10739ce6318c5294a42108318c62108421084000000000000000000011f4e1642e5549b47612f570b4986b95a2a9409648a1d047d399b8d66430174b2552912c94462210078391c0d06431168b05628130944621100783a1c0c8602c1509848220f0683014fb9917d69555541412d2d19190504f0f0dcdcc8c8b4b4b4a0a0a08c8c8c787878786464646450505050503c3c3c3c3c3c3c28282828282828281414141414141402100b0a101828333d0c0c0e131a3a3c370e0d1018283945380e11161d3357503e1216253a446d674d182337405168715c31404e5767797865485c5f62706467631112182f6363636312151a4263636363181a3863636363632f42636363636363636363636363636363636363636363636363636363636363636363636363636310101014181c2028101014181c2028301014181c2028304014181c2028304040181c2028304040401c20283040404060202830404040608028304040406080803e2fcb7d00d3313be428de0ea89bdb96622dd471be03f7289225ee0d8c97d6aa91a665762ec4204e460f68ea64be730dad586c655295e7dbb87e49dc434ccaec5d88217c8a3c355a836325e3f3977312ba3da3c9384fbaaa420c57354fbaaa457634119ca6941ed1e75dc90e0656b31b7ce1fc5785e0979dbfe138ed30f68f3a9226301756b3329a835df0c9690a3fb40bd0a78d8e65d91a077283da3ceb94db6bbd82b829546045f127fc5a2d63907dc221dcdaff710b48d8662cad01ba72572287bb79d497aaa4a84799c274ad66c171bc508aec0d240e4f143ddbaefffb263796c1483d9e05a759dc7162b3187c065472346a26964daffea52dcec8e2c3e0f93826964da3c16f019f5740b2b022d31e4caffea52dc84d68f5e76036a22ff81ec7cbe84dcc2767d2db056b8134b26ba6280f32777aaa440126bf5ee5ea7134bb506e759b0896a1b8595869fe28f23bf3855494a02e8ceb26251afc2cac5e4e4d2ed23cedc398843b8f7360ff4b6a29404573862f5aca2cac7922fedbb909b6a3ecc4661d09ffd325b0d452811c22cacdd79f6a4f33f6d42225cd8742d327ba705cc7c48e7ba8aa916562f943ef7c06d44ffebd33c23114832e18a6e6d171de9bc3005f5acd440750f0dbe5d50a715adcf393b447a4aa26923fcd32309f30be7576043f9d3b8b6c573e8053534b438728c2695ed1279ae461be60d5cc37b49caec637011edfb83b88133da2593ceaa539993e816b0dc079d9b05137b2c913586f6f395e2b33072ea3d325c7fc7c554ad61007d7b1809f26e35ed174e611656b980f095b144dec91e85acdff0aa914be2379dfe4ee334160aee6ec0352636a3d96489a745ac9cc2637d42aa465c9d6709fe370708c26286dafb2e9dd8aed20dcbe7093c8b0f841529237785a1fb149e56b1c4e3975121b9b8660d286dafb34b95ff0a5c4e3166d11232426976d6e39bcefdf07d6acac144387fb8cba82a15521db404d2ed26b47370ce1be01f5a7e7a8e2eac2b3cc276e658f029112806d34bac9a42bfa383dcbc5a61df23eb1598b38ff204f737a82caea53b84f7118266dacba49942e0bfdf07428cf0ed6fc726317f00aa9391264c31f2037707b15a3af90bb9c46500db59b4973bd77eb2b155242b5ecfb90387d18f177eb2b3a2f93b7230c41a36d66ce5519442aa5b80cda36d72c65bbe8481c3c2f60a26fc4562b49d9d2d7b3a3e441529703d188db564d33a30bfbb0dd0ab5a9ee2345d0f25904dffdc83879aee9ef3139226d443033ac594aac8b9a1d3b09a593d8ff3ec2d0f887ce18de65b9f9da3d799c595ae347488134bb49ed1814d46705a2d5f01f38fdbce068a09095b4dafbe6170238bbe72acb2a52c59ba843e65852a8fdd4300b98f0deb2cb4bc095336d64d23cf93c7689ed1387d752a8e5906895336d64f637f783b44a33f0eb0e16d85703731867103e7fca9a85a8671d9ed0331a4cdb5964c9d5f5962ef0e0c70451ee3727fd77282a290321b6a99a672d0c70edd4559621f8f119ec97b8b46e8568bd40c9a666dae2c269fb40aec29a845f1d49c8fc97dba379c0aa91d5fc2730c791f5a10d1dfe80668836d52269748f2f4b2b2ef3714ee79c2df808b286e80e578482695b6ba671e0fddb1a0b2b277bd54297c31241b6a95a4d9e5442ddc3af43f308d15fe2bb04fcad5dda0a86f529803b5d1705bd3ef4425e48666daa569364c70ffc394ea235958dea5287808fa122f60c590db54cd3397ff601ca75d416fd5bc588bb1e52a9c1217a56036d4ca6699e3727b4428b9807af947eb2b2377d6e3ca948b7e91cfa4085656460bc99934cd81b6b8ddff510ed3a5a38dc4672174c5e60cb134cdb6b45bec8aa0291d7762b4a4fffc42e226fe0a47b09a51d404ec383fcbe1bdc62cf9acb02224256d36b1f7e5eb6a15525c65df81182695b6ba499a2a2ff83f75eb8618a0dcb6c5643cce2aa42324253499b6b9d17b963810f9f03b6517f68f7ae3713dd62b800518dffa7e605350b57780906669336d65cb0891f7615a17bd1c7db8dce8626498d336dacaa30497a3e54d44079f56584fdbdb8b783f8a11b89e4f9cc4aa920427bfda5958efa8dc0501b6ac9a678b0997cb778371fa75c0d336da9850cb1be692340727b2fd0955222796d6b0efae04091c4a42e4ebfef72aa4b2b22139f0db550c2f5c658b4cfd99e5b183af78a553eb41401b6a95a4d2671e3c90df7207eed832884fe58af714d481c3a84789f957602f8eef96a8302412b498db5cf2c626ef5dfe29a877f3ab601e91c5cacacf37217e5e918311b6b29334cf2b89e8e02cac8ba854d411be5c5e194cd33946dae3848e56d101e6ef47f3f7c046e523e9fd5548dfc8084a3b88e2c5617255e34cdb6a61332c7fb7a0de2f416bffbbe3c2cac12ae1962d3336d5330be7a3949d102385552528cdddf51101238b0adc9285d330bff1b6a658b4cfe50b67f0f61a8aa940462cac71bf64ae44ca2736d5ffc32c5a665d6b0bfaf489e490881e5aa6a086e73f939812099a666dacb963dd857b8511a2bfe70ebd075fa72406da994cd33958e17dd5298078e7e14456ee58e3d56771c229a887d2de7c202350909434cdb6a61332c6fbb70ffbe2c564ff3a882300cb16999b6a9985f74bfa7fb9595a9a843e406e89228b5eb875d8f4e4a169fcc1962d3336d5730be7ef741514bc71611ab7497e428a41bc6490c440381d063833c8b675f7267c6ba3fdb951dfa595bc95552378c9218880703a0c7067916cebee4cf8d747fb72a3bf4b2b792aaa46f192431100e07418e0cf22d9d7dc99f1ae8ff6e5477e9656f255548aa9384fd4008978266999b6b2e5231c21f16562de5f7a2eec8e8ff705b1c35297ae5fd02cae03cdc2e4860c465334ccdb596f9f83bf917407f3f3e52a96560fa88bd6f0a038242f4a34cdb6a4ccb1c2eed1ade82cace56be9fc237093b6fe90213a3f4a184ccb15e699b6d6ea22535149e440fa7a3b71cfa15d91c037169f8cb16999330bcdb5ba5ea486a10a27ab2ba55201bc8f00f932fba75a35d1fec63833ca5e5db851d46408519204a2eb585e4ca273be9ffd62b06dab9e0cb1699efef912aa4aa940462cac71bf64ae44ca2736d5ffc32c5a665d6b0bfaf489e49080 >, width=(int)320, height=(int)240, pixel-aspect-ratio=(fraction)1/1, framerate=(fraction)15/1"
AUDIO_RTP_CAPS = "audio/x-speex, rate=(int)44100, channels=(int)1, streamheader=(buffer)< 5370656578202020312e327263310000000000000000000000000000010000005000000044ac0000020000000400000001000000ffffffff800200000000000001000000000000000000000000000000, 1f000000456e636f6465642077697468204753747265616d6572205370656578656e630000000001 >"


class VideoOutBin(Gst.Bin):
    def __init__(self):
        super(VideoOutBin, self).__init__(ip)

		# Set IP
        self.ip = ip

        # Add theora Encoder
        video_enc = Gst.ElementFactory.make("theoraenc", None)
        video_enc.set_property("bitrate", 50)
        video_enc.set_property("speed-level", 2)
        self.add(video_enc)

        # Add rtptheorapay
        video_rtp_theora_pay = Gst.ElementFactory.make("rtptheorapay", None)
        self.add(video_rtp_theora_pay)

        # Add udpsink
        udp_sink = Gst.ElementFactory.make("udpsink", None)
        udp_sink.set_property("host", self.ip)
        udp_sink.set_property("port", 5004)
        self.add(udp_sink)

        # Link Elements
        video_tee.link(video_enc)
        video_enc.link(video_rtp_theora_pay)
        video_rtp_theora_pay.link(udp_sink)


##############
# AudioOutBin
##############
class AudioOutBin(Gst.Bin):
    def __init__(self):
        super(AudioOutBin, self).__init__()

        self.ip = None

        # Audio Source
        audio_src = Gst.ElementFactory.make("autoaudiosrc", None)
        self.add(audio_src)

        # Opus Audio Encoding
        audio_enc = Gst.ElementFactory.make("speexenc", None)
        self.add(audio_enc)

        # RTP Opus Pay
        audio_rtp = Gst.ElementFactory.make("rtpspeexpay", None)
        self.add(audio_rtp)

        # Audio UDP Sink
        udp_sink = Gst.ElementFactory.make("udpsink", None)
        udp_sink.set_property("host", self.ip)
        udp_sink.set_property("port", 5005)
        self.add(udp_sink)

        # Link Elements
        audio_src.link(audio_enc)
        audio_enc.link(audio_rtp)
        audio_rtp.link(udp_sink)


#############
# VideoInBin
#############
class VideoInBin(Gst.Bin):
    def __init__(self):
        super(VideoInBin, self).__init__()

        # Video Source
        video_src = Gst.ElementFactory.make("udpsrc", None)
        video_src.set_property("port", 5004)
        video_src.set_property("caps", Gst.caps_from_string(VIDEO_RTP_CAPS))
        self.add(video_src)

        # RTP Theora Depay
        video_rtp_theora_depay = Gst.ElementFactory.make("rtptheoradepay", None)
        self.add(video_rtp_theora_depay)

        # Video decode
        video_decode = Gst.ElementFactory.make("theoradec", None)
        self.add(video_decode)
        video_rtp_theora_depay.link(video_decode)

        # Change colorspace for xvimagesink
        video_convert = Gst.ElementFactory.make("videoconvert", None)
        self.add(video_convert)

        # Send video to xviamgesink
        xvimage_sink = Gst.ElementFactory.make("autovideosink", None)
        self.add(xvimage_sink)

        # Link Elements
        video_src.link(video_rtp_theora_depay)
        video_decode.link(video_convert)
        video_convert.link(xvimage_sink)


#############
# AudioInBin
#############
class AudioInBin(Gst.Bin):
    def __init__(self):
        super(AudioInBin, self).__init__()

        # Audio Source
        audio_src = Gst.ElementFactory.make("udpsrc", None)
        audio_src.set_property("port", 5005)
        audio_src.set_property("caps", Gst.caps_from_string(AUDIO_RTP_CAPS))
        self.add(audio_src)

        # RTP Opus Depay
        audio_rtp = Gst.ElementFactory.make("rtpspeexdepay", None)
        self.add(audio_rtp)

        # Opus Audio Decoding
        audio_dec = Gst.ElementFactory.make("speexdec", None)
        self.add(audio_dec)

        # Audio Sink
        audio_sink = Gst.ElementFactory.make("autoaudiosink", None)
        self.add(audio_sink)

        # Link Elements
        audio_src.link(audio_rtp)
        audio_rtp.link(audio_dec)
        audio_dec.link(audio_sink)
