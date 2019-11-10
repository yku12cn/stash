"""A simplified web interface
Copyright 2019 Yang Kaiyu yku12cn@gmail.com
"""

import urllib.request as urlreq
import urllib.parse as urlparse
import urllib.error as urlerr
import http.cookiejar
from socket import _GLOBAL_DEFAULT_TIMEOUT as GLOBAL_DEF
import time
import ssl
from pathlib import Path
from printLog import printLog

_defaultuserAgent = "\
Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/75.0.3770.142 Safari/537.36"


def _transFile(source, target, buffer):
    """A helper function for file transferring"""
    Totle = source.length
    last = 0
    while True:
        now = round((1 - source.length/Totle)*20)
        if last != now:
            print("=" * (now - last), sep="", end="", flush=True)
            last = now
        pack = source.read(buffer)
        if not pack:
            break
        target.write(pack)
    print("")


class SimpleWeb():
    """A simplified web interface"""

    def __init__(self, log="", setattempt=2, userAgent=_defaultuserAgent):
        # set the limit for HTTP retry attempts
        self.atpset = setattempt
        # Fake Header
        self.fakeHeader = {}
        self.fakeHeader["User-Agent"] = userAgent
        # Create cookie jar
        self.cjopener = urlreq.build_opener(
            urlreq.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        # Bypassing SSL check
        ssl._create_default_https_context = ssl._create_unverified_context
        self.scheme = "http"
        self.netloc = ""
        self.lasturl = urlparse.urlparse("")
        self.mylog = printLog(log)  # rename logging function

    def logfile(self):
        """get the logfile handler"""
        return self.mylog.logfile()

    def _completeUrl(self, url):
        """Fix incomplete url"""
        parser = urlparse.urlparse(url)
        if parser.scheme and parser.netloc:  # complete url
            pass
        elif parser.netloc:  # missing scheme only
            if self.scheme:
                parser = parser._replace(scheme=self.scheme)
            else:
                parser = parser._replace(scheme="http")
        elif parser.scheme:  # have scheme, don't have netloc
            self.mylog("invalid address:", url)
            return None
        elif (((parser.path[0] == '/') or (parser.path[0:2] == './')) and
              (self.netloc != "")):  # relative url
            parser = parser._replace(scheme=self.scheme, netloc=self.netloc)
        else:  # probably missing http://
            if self.scheme:
                url = "%s://%s" % (self.scheme, url)
            else:
                url = "http://%s" % url
            parser = urlparse.urlparse(url)
        return parser.geturl()

    def myreq(self, url, postdata=None, coder="utf-8",
              attempt=-1, reqtime=GLOBAL_DEF):
        """A simplified web request(post) with cookie
        Post data in the form of {'name':'Eva','age':'20'}
        """
        # Quote url for special characters
        url = urlparse.quote(url, safe=':/?#[]@!$&\'()*+,;=%')
        # Understand url
        url = self._completeUrl(url)
        # reset retry flag
        if attempt == -1:
            attempt = self.atpset
        # Try making the request
        try:
            if postdata:
                data_parse = urlparse.urlencode(postdata).encode(coder)
                req = urlreq.Request(url, data=data_parse,
                                     headers=self.fakeHeader)
            else:
                req = urlreq.Request(url, headers=self.fakeHeader)
            out = self.cjopener.open(req, timeout=reqtime)
            self.lasturl = urlparse.urlparse(
                out.geturl())  # update last successful req
            return out
        except urlerr.URLError as error:
            # retry for all net error
            self.mylog(error)
            if attempt != 0:
                self.mylog("retry request,", attempt, "attempts left")
                time.sleep(0.5)
                return self.myreq(url, postdata=postdata, coder=coder,
                                  attempt=attempt - 1, reqtime=reqtime)
            return None

    def updateNetloc(self, url=None):
        """Force update domain"""
        if url:
            if not self.myreq(url):
                return False
        self.scheme = self.lasturl.scheme
        self.netloc = self.lasturl.netloc
        return True

    def reqCode(self, url, coder="utf-8", post=None, postcoder="utf-8",
                attempt=-1, timeout=GLOBAL_DEF):
        """Request for source code"""
        # reset retry flag
        if attempt == -1:
            attempt = self.atpset
        # Try fetching data
        while attempt >= 0:
            # Try to connect target
            handle = self.myreq(url, reqtime=timeout, attempt=0,
                                postdata=post, coder=postcoder)
            if handle:
                try:
                    # Try fetching data
                    data = handle.read()
                except OSError as error:
                    # Handle connection issues
                    self.mylog(error)
                    if attempt == 0:
                        return None
                    self.mylog("re-loading data,", attempt, "attempts left")
                    time.sleep(0.5)
                    attempt = attempt - 1
                    continue
                try:
                    # Try decode
                    return data.decode(coder)
                except ValueError as error:
                    self.mylog("Codec error:", error)
                    return None
            else:
                # Handle connection failure
                if attempt == 0:
                    return None
                self.mylog("retry request,", attempt, "attempts left")
                time.sleep(0.5)
                attempt = attempt - 1

    def saveFile(self, url, filename=None, buffer=64000,
                 attempt=-1, timeout=GLOBAL_DEF):
        """Simple download"""
        if not filename:
            filename = Path(url).name
        filename = Path(filename)
        if filename.exists():  # check for conflicts
            self.mylog(filename.absolute().as_posix(), "already exists")
            return True
        # reset retry flag
        if attempt == -1:
            attempt = self.atpset
        # Try fetching data
        while attempt >= 0:
            # Try to connect target
            handle = self.myreq(url, reqtime=timeout, attempt=0)
            if handle:
                downfile = open(filename, "wb")
                try:
                    # Try to download data
                    _transFile(handle, downfile, buffer)
                    downfile.close()
                    return True
                except OSError as error:
                    # Handle transfer error
                    self.mylog(error)
                    downfile.close()
                    if filename.exists():
                        filename.unlink()
                    if attempt == 0:
                        return False
                    self.mylog("re-transfer,", attempt, "attempts left")
                    time.sleep(0.5)
                    attempt = attempt - 1
            else:
                # Handle connection failure
                if attempt == 0:
                    return False
                self.mylog("retry request,", attempt, "attempts left")
                time.sleep(0.5)
                attempt = attempt - 1
