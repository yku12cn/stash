import sys
from pathlib import Path
from io import StringIO
from time import time, strftime, localtime


def _timestamp(ftime):
        """Generate a time stamp from seconds"""
        return "[%s.%03d] " % (strftime("%Y/%b/%d %H:%M:%S", localtime(ftime)),
                               ftime * 1000 % 1000)


class printLog():
    """Logging while Printing!"""

    def __init__(self, log=""):
        if log == "":
            self._logfile = None
        else:
            self.logfile(log)
            # self.logfile = open(Path(log), "a")

    def logfile(self, log, mkdirF=True):
        """Assign or re-assign the log file
        usage: logfile(log="path of your logfile", mkdirF=True)
        if mkdirF is set to be True, logfile() will create
        the directory if it does not exists.
        """
        if hasattr(self, "_logfile"):
            # check if logfile() is called by __init__
            if self._logfile is not None:
                # if a file instance already exists, close the instance
                self._logfile.close()

        logpath = Path(log)
        if mkdirF:
            if not logpath.parent.exists():
                Path.mkdir(logpath.parent, parents=True)
        self._logfile = open(logpath, "a")

    def printL(self, *args, t=False, redirect=False, file=None, **kwargs):
        """A wrap of python built-in print()
        use it as you normally using print()
        if self._logfile is defined the result
        of print() will also be logged

        if [redirect] is True, the print() will be muted and
        its results will be returned

        if [t] is Set, each log will started with a time stamp
        """
        if self._logfile:
            # print to log
            if t:  # Print time stamp
                print(_timestamp(time()), end="", file=self._logfile)
            print(*args, file=self._logfile, **kwargs)

        if redirect:
            # handle redirect flag
            temp = StringIO()
            print(*args, file=temp, **kwargs)
            return temp.getvalue()

        if not file:
            file = sys.stdout
        print(*args, file=file, **kwargs)


if __name__ == "__main__":
    # This is a short demo
    from time import sleep
    a = printLog("test.log")
    printL = a.printL
    for i in range(10):
        printL("hello from iter", i, t=True, end="")
        printL(" balabala?")
        sleep(0.1)
