import pyaudio
import wave
import sys
import re
import class_loader
import os
import inspect

from pkgutil import walk_packages
from threading import Thread
from twisted.words.protocols.irc import IRCClient
from twisted.internet.protocol import ReconnectingClientFactory
from twisted.internet import reactor

base_dir = os.path.dirname(__file__)

class BuzzerBot(IRCClient):
    chunk = 1024
    channel = "#rit-foss"
    bot_name = "buzzer_bot"
    lineRate = 1
    p = pyaudio.PyAudio()
    buzzerRegex = re.compile(r'b((z+t)|(uzzer))')

    # import plugins namespace
    plugin = __import__('buzzer_as_a_service')

    modNames = []
        
    # Get a list of plugin module names
    for importer, modName, isPkg in walk_packages(path=plugin.__path__,
                                                  prefix=plugin.__name__+'.',
                                                  onerror=lambda x: None):
        modNames.append(modName)

    # Import each module and create an instance of all of its classes
    extensions = []
    for name in modNames:
        __import__(name)
        pluginExt = getattr(plugin, name.split('.')[1])
        print "loading extension:", name 
        for name, obj in inspect.getmembers(pluginExt):
            if inspect.isclass(obj):
                extensions.append(obj())
 
    print "Extensions Loaded"

    def playBuzzer(self, filePath):
        wf = wave.open(filePath, 'rb')
        stream = self.p.open(format =
                        self.p.get_format_from_width(wf.getsampwidth()),
                        channels = wf.getnchannels(),
                        rate = wf.getframerate(),
                        output = True)

        data = wf.readframes(self.chunk)

        while data != '':
            stream.write(data)
            data = wf.readframes(self.chunk)

        stream.close()

    def signedOn(self):
        self.join(self.factory.channel)
        self.factory.add_bot(self)

    def joined(self, channel):
        print str("Joined " + channel)

    def left(self, channel):
        self.p.terminate()
        print str("Left: " + channel)

    def privmsg(self, user, channel, msg):
       user = user.split("!", 1)[0]
       if channel == self.nickname:
           self.msg(user, "BUZZZ")
       else:
           regexMsg =  self.buzzerRegex.findall(msg.lower())
           if regexMsg and 'kettle' not in user:
               self.buzzer(channel, user, msg)

    def buzzer(self, channel, user, msg):
        for ext in self.extensions:
            ext.buzzer(channel, user, msg)
        task = Thread(target=self.playBuzzer("../../buzzer.wav"))
        task.start()
        self.msg(channel, "Played Buzzer!")

class BuzzerBotFactory(ReconnectingClientFactory):
    active_bot = None

    def __init__(self, protocol=BuzzerBot):
        self.protocol = protocol
        self.channel = protocol.channel
        IRCClient.nickname = protocol.bot_name
        IRCClient.realname = protocol.bot_name

    def add_bot(self, bot):
        self.active_bot = bot

def main():
    f = BuzzerBotFactory()

    reactor.connectTCP("irc.freenode.net", 6667, f)

    reactor.run()

if __name__ == '__main__':
    main()
