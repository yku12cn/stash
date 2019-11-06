import urllib.request as urlreq
import urllib.parse as urlparse
import urllib.error as urlerr
import http.cookiejar
from socket import _GLOBAL_DEFAULT_TIMEOUT as GLOBAL_DEF
import time
import ssl
import re
from pathlib import Path
from printLog import printLog

_defaultuserAgent = "\
Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/75.0.3770.142 Safari/537.36"


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
        return self.mylog.logfile()

    def myreq(self, url, postdata="", coder="utf-8",
              attempt=-1, reqtime=GLOBAL_DEF):
        """A simplified web request(post) with cookie
        Post data in the form of {'name':'Eva','age':'20'}
        """
        # Quote url for special characters
        url = urlparse.quote(url, safe=';/:?=')
        # Understand url
        praser = urlparse.urlparse(url)
        if (praser.scheme != '') and (praser.netloc != ''):  # complete url
            pass
        elif (((url[0] == '/') or (url[0:2] == './')) and
              (self.netloc != "")):  # relative url
            praser = praser._replace(scheme=self.scheme, netloc=self.netloc)
        else:  # probably missing http://
            url = "http://" + url
            praser = urlparse.urlparse(url)
        # reset retry flag
        if attempt == -1:
            attempt = self.atpset
        # Try making the request
        try:
            if postdata == "":
                req = urlreq.Request(praser.geturl(), headers=self.fakeHeader)
            else:
                data_parse = urlparse.urlencode(postdata).encode(coder)
                req = urlreq.Request(praser.geturl(), data=data_parse,
                                     headers=self.fakeHeader)
            out = self.cjopener.open(req, timeout=reqtime)
            self.lasturl = urlparse.urlparse(
                out.geturl())  # update last successful req
            return out
        except (urlerr.HTTPError, urlerr.URLError) as error:
            # retry for http error
            self.mylog(error)
            if attempt != 0:
                self.mylog("retry, {} attempts left".format(attempt))
                time.sleep(0.5)
                return self.myreq(url, postdata=postdata, coder=coder,
                                  attempt=attempt - 1, reqtime=reqtime)
            else:
                self.mylog("request fail due to HTTP error")
                return None
        except Exception as error:
            self.mylog(error)
            return None

    def updateNetloc(self, url=""):
        """Force update domain"""
        if url != "":
            if self.myreq(url) is None:
                return False
        self.scheme = self.lasturl.scheme
        self.netloc = self.lasturl.netloc
        return True

    def reqCode(self, url, coder="utf-8", post="",
                postcoder="utf-8", timeout=GLOBAL_DEF):
        """Request for source code"""
        try:
            return self.myreq(url, reqtime=timeout, postdata=post,
                              coder=postcoder).read().decode(coder)
        except Exception as error:
            self.mylog(error)
            return None

    def saveFile(self, url, filename="", timeout=GLOBAL_DEF):
        """Simple download"""
        if filename == "":
            filename = re.findall(r"/([^/]*?)$", url)[0]
        filename = Path(filename)
        if not filename.exists():  # check for conflicts
            try:
                # download data to RAM
                data = self.myreq(url, reqtime=timeout).read()
                downfile = open(filename, "wb")
                downfile.write(data)
                downfile.close()
            except Exception as error:  # clean up mess if fail
                self.mylog(error)
                if filename.exists():
                    filename.unlink()
                return False
        else:
            self.mylog("\"%s\" already exists" %
                       (filename.absolute().as_posix()))
        return True
