"""
A simple tool for automatically posting starred items from google reader to delicious.

Based on code from http://peterbouda.blogspot.com/2009/01/how-to-get-google-reader-news-via.html

Example :
    api = GReader2Delicious(reader_id='12345678901234567890', 
                reader_email='john.doe@gmail.com', 
                reader_password='password', 
                delicious_user='john.doe', 
                delicious_password='password')
    api.sync()

greader2delicious is released under the BSD license. See license.txt for details
and the copyright holders.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

""" 

__author__ = "Dave Perrett"
__copyright__ = "(c) 2007-2009 Dave Perrett"
__description__ = "A simple tool for automatically posting starred items from google reader to delicious."
__long_description__ = "greader2delicious allows you to sync starred items in your google reader account to delicious via publicly available APIs."
__email__ = "dev[AT]recurser[DOT]com"
__license__ = "BSD"
__maintainer__ = "David Perrett"
__status__ = "Development"
__url__ = "http://recurser.com/code/p/greader2delicious/"
__version__ = "0.1"

import httplib, logging, urllib

try:
    import feedparser
except:
    print "ERROR: could not import feedparser module"
    print
    print "GReader2Delicious requires the feedparser module."
    print "You can download feedparser at http://www.feedparser.org/"
    print
    raise

try:
    import deliciousapi
except:
    print "ERROR: could not import deliciousapi module"
    print
    print "GReader2Delicious requires the DeliciousAPI module."
    print "You can download deliciousapi at "
    print "http://www.michael-noll.com/wiki/Del.icio.us_Python_API"
    print
    raise

try:
    import pydelicious
except:
    print "ERROR: could not import pydelicious module"
    print
    print "GReader2Delicious requires the pydelicious module."
    print "You can download pydelicious at "
    print "http://code.google.com/p/pydelicious/"
    print
    raise
    
DEFAULT_NUM_TAGS = 15
FROM_GOOGLE_READER_TAG = 'from.google.reader'
UNTAGGED_TAG = 'untagged'
GREADER_DEBUG = True

class GReader2Delicious():
    
    def __init__(self, *args, **kwargs):
        """ 
        Initialise login information
        
        """
        self._reader_id = kwargs.get('reader_id', None)
        self._reader_email = kwargs.get('reader_email', None)
        self._reader_password = kwargs.get('reader_password', None)
        self._delicious_user = kwargs.get('delicious_user', None)
        self._delicious_password = kwargs.get('delicious_password', None)
        self._num_tags = kwargs.get('num_tags', DEFAULT_NUM_TAGS)
        self._cookie = None

    def _get_cookie(self):
        """
        Log into google and get the cookie string needed for requesting feeds
        
        """
        
        if self._cookie:
            return self._cookie
            
        # Login to Google
        conns = httplib.HTTPSConnection("www.google.com")
        params = urllib.urlencode({'Email': self._reader_email, 'Passwd' : self._reader_password, 'service': 'reader', 'source': 'Python Browser 1.0', 'continue': 'http://www.google.com/'})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conns.request("POST", "/accounts/ClientLogin", params, headers)
        response = conns.getresponse()
        if response.status != 200:
            print response.read()
            return 'Error'
        data = response.read()
        conns.close()
        sid = data.split("\n")[0].split("=")[1]
        self._cookie = 'SID="' + sid + '"; $domain=.google.com; $path=/; $expires=1600000000;'
        return self._cookie
    
    def get_starred(self):
        """
        Get the feed of starred items
        
        """
        conn = httplib.HTTPConnection("www.google.com")
        headers = {"Cookie": self._get_cookie(), "Accept": "text/plain"}
        conn.request("GET", "/reader/atom/user/"+ self._reader_id + "/state/com.google/starred", None, headers)
        response = conn.getresponse()
        if response.status != 200:
            print response.read()
            return 'Error'
        data = response.read()
        conn.close()
        return feedparser.parse(data)
        
    def sync(self):
        """
        Sync starred google reader items with delicious
    
        """
        starred_items = self.get_starred()
        api = pydelicious.DeliciousAPI(self._delicious_user, self._delicious_password)
                
        for entry in starred_items.entries:
            
            """ First, check if this entry is already bookmarked """
            post_data = api.request('posts/get?url=%s' % entry.link)
                        
            """ If it's already bookmarked, process the next url. """
            if post_data['posts'] and len(post_data['posts']) > 0:
                self._debug('Post already exists (%s)' % entry.link)
                continue
            
            """ Get the top tags for this post. """
            tags = self._get_tags_for_url(entry.link)
            
            self._debug('Tags: %s' % tags)
            
            """ Add it to delicious. """
            result = api.posts_add(entry.link, entry.title, tags=tags)
            if result and result['result'][0]:
                self._debug('Added post (%s)' % entry.link)
            else:
                self._debug('Error adding post (%s)' % entry.link)
            
    
    def _get_tags_for_url(self, url):
        """ 
        Returns popular tags for this post sorted by popularity, descending.
        
        """
        result = []
        api = deliciousapi.DeliciousAPI()
        post = api.get_url(url)
        
        if post.tags:    
            """ Sort the tags by count descending. """
            from operator import itemgetter
            tags = post.tags.items()
            tags.sort(key = itemgetter(1), reverse=True)
            
            """ Get the first n tags. """
            i = 0
            for tag, count in tags:
                result.append(tag)
                if i == DEFAULT_NUM_TAGS:
                    break
                i += 1
        
        """ If no tags can be found, add an 'untagged' tag so we can easily find these again. """
        if len(result) == 0:
            result.append(UNTAGGED_TAG)
            
        """ Add an 'from google reader' tag so we can easily find these again. """
        result.append(FROM_GOOGLE_READER_TAG)
        
        """ Return as a space-separated string. """
        return ' '.join(result)
    
    def _debug(self, msg):
        """
        Outputs debugging messages if enabled.
        
        """
        if GREADER_DEBUG:
            print msg
            logging.debug(msg)