import win32api
import win32con
import win32gui


def setWallPaper(filepath):
    k = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,
                              "Control Panel\\Desktop", 0,
                              win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(k, "WallpaperStyle", 0, win32con.REG_SZ, "10")
    win32api.RegSetValueEx(k, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER,
                                  filepath, 1 + 2)
