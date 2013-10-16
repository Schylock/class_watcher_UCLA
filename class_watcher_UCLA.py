import urllib
import urllib2
from time import sleep
from HTMLParser import HTMLParser

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def init(self, targets):
        targets.sort()
        self.targets = targets
        self.state = 2
        self.current = None
        self.available = []
        
    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if self.state == 0:
                if attr[1] == 'opengreen' or attr[1] == 'waitpurple':
                    self.state = 1
                elif attr[1] == 'closedred':
                    self.state = 2
            elif self.state == 1 and self.current != None:
                if attr[1] == 'opengreen' or attr[1] == 'waitpurple':
                    self.available.append(self.current)
                    self.current = None
                elif attr[1] == 'closedred':
                    self.crrent = None
    def handle_data(self, data):
        if (self.state == 2 or self.state == 1) and 'LEC ' in data:
            self.state = 0
            self.current = None
            #print 'lec', self.state
        elif self.state == 1 and data in self.targets and self.current == None:
            self.current = data
           # print 'class', self.current

def send(message = "None"):
    number = "8313926314" #put your number here
    prov = '41'   #this is ur provider code, google it 
    url = 'http://www.onlinetextmessage.com/send.php'
    values = {'code' : '',
              'number' : number,
              'from' : 'schyock11@gmail.com',
              'remember' : 'n',
              'subject' : 'Add Now',
              'carrier' : prov,
              'quicktext' : '',
              'message' : message,
              's' : 'Send Message'}
    data = urllib.urlencode(values)  ##text sender
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()
    print "Message Successfully Sent"

def tent( src = 'to add.txt'):
    src = open(src, 'r') # line form:  "classurl classname" no quotes obv
    classes = []
    for line in src:
        line = line.split()
        classes.append(line)
    while True:
        for c in classes:
            response = urllib2.urlopen(c[0])
            response = response.read()
            if len(c) == 2:
                if 'opengreen' in response or 'waitpurple' in response:
                    send(c[1])
                    print c[1]
                    classes.remove(c)
            else:
                parser = MyHTMLParser()
                parser.init(c[2:len(c)])
                parser.feed(response)
                if len(parser.available) != 0:
                    print parser.available
                    send(parser.available[0])
                    classes.remove(c)
        sleep(60)

tent()
