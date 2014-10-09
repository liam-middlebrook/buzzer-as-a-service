import pyaudio
import wave
import sys
import re

from threading import Thread
from twisted.words.protocols.irc import IRCClient
from twisted.internet.protocol import ReconnectingClientFactory
from twisted.internet import reactor

class BuzzerBot(IRCClient):
    
    chunk = 1024
    channel = "#rit-foss"
    bot_name = "buzzer_bot"
    lineRate = 1
    p = pyaudio.PyAudio()
    buzzerRegex = re.compile(r'b((z+t)|(uzzer))')

    def playBuzzer(self):
        wf = wave.open("../../buzzer.wav", 'rb')
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
               task = Thread(target=self.playBuzzer())
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

if __name__ == '__main__':
    f = BuzzerBotFactory()

    reactor.connectTCP("irc.freenode.net", 6667, f)

    reactor.run()
