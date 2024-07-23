
from __future__ import unicode_literals
import urlquick
import time
import base64
import json
from xbmc import executebuiltin
from uuid import uuid4
from codequick.storage import PersistentDict
from codequick import Script
from codequick.script import Settings
from functools import wraps
from datetime import datetime, timedelta
from .constants import ANM, GSET, SSET, runPg

dtnow = datetime.now()
strdtnow = str(dtnow.strftime(" on %a, %d %b %Y at %I:%M %p"))
sesTime = 1728000

def secLeft():
    with PersistentDict("headers") as db:
        exp = db.get("exp", 0)
    return int(exp - time.time())

decdaysLeft = secLeft() / 86400
daysLeft = int(decdaysLeft)
hoursLeft =  int(decdaysLeft * 24)

def actstatus():
    strdaysLeft = str(daysLeft) + (" day" if daysLeft == 1 else " days")
    strhoursLeft = str(hoursLeft) + (" hour" if hoursLeft == 1 else " hours")
    strtimeLeft = strhoursLeft if daysLeft < 1 else strdaysLeft
    actdt = ("Active" + strdtnow + ". Auto-login after " + strtimeLeft)
    SSET("astatus", actdt)

def expstatus():
    expdate = dtnow + timedelta(days=daysLeft)
    SSET("estatus", "Session till " + expdate.strftime("%a, %d %b %Y ") + GSET("exptime"))

def getHeaders():
    with PersistentDict("headers") as db:
        return db.get("headers", False)

def quality_to_enum(quality_str, arr_len):
    mapping = {
        'Best': arr_len-1,
        'High': max(arr_len-2, arr_len-3),
        'Medium+': max(arr_len-3, arr_len-4),
        'Medium': max(2, arr_len-3),
        'Low': min(2, arr_len-3),
        'Lower': 1,
        'Lowest': 0,
    }
    if quality_str in mapping:
        return min(mapping[quality_str], arr_len-1)
    return 0

def notif(msg):
    Script.notify(msg, ANM)

def logstatus(io):
    Logio = "Logged " + io
    tf = "true" if io == "in" else "false"
    SSET("lstatus", Logio + strdtnow)
    SSET("isloggedin", tf)
    notif(Logio)

def isLoggedIn(func):
    @wraps(func)
    def login_wrapper(*args, **kwargs):
        with PersistentDict("headers") as db:
            headers = db.get("headers")
            exp = db.get("exp", 0)
        if headers and exp > time.time():
            SSET("isloggedin", "true")
            return func(*args, **kwargs)
        elif headers and exp < time.time():
            refresh_token()
            return False
        else:
            SSET("isloggedin", "false")
            notif("Login please")
            executebuiltin(runPg + "login/)")
            return False
    return login_wrapper

def refresh_token():
    headers = getHeaders()
    accesstoken = headers.get("authToken","")
    refreshToken = headers.get("refreshToken","")
    if not headers:
        return
    url = "https://auth.media.jio.com/tokenservice/apis/v1/refreshtoken?langId=6"
    refresh_headers = {
        "accesstoken": accesstoken,
        "uniqueid": headers.get("uniqueId",""),
        "devicetype":"phone",
        "os":"android",
        "user-agent":"okhttp/4.2.2",
        "versioncode": "353",
    }
    body = {
        "appName": "RJIL_JioTV",
        "deviceId": headers.get("deviceId",""),
        "refreshToken": refreshToken
    }
    resp = urlquick.post(url, json=body, headers=refresh_headers, max_age=-1, verify=False, raise_for_status=False).json()
    if resp.get("authToken", "") != "":
        headers["authToken"] = resp.get("authToken")
    if resp.get("ssoToken", "") != "":
        headers["ssotoken"] = resp.get("ssoToken")
        with PersistentDict("headers") as db:
                db["headers"] = headers
                db["exp"] = time.time() + sesTime
        SSET("tokreftime", "Token refreshed" + strdtnow)
        notif("Token refreshed")
    return None

def login(mobile, otp):
    resp = None
    mobile = "+91" + mobile
    otpbody = {
            "number": base64.b64encode(mobile.encode("ascii")).decode("ascii"),
            "otp": otp,
            "deviceInfo": {
                "consumptionDeviceName": "ZUK Z1",
                "info": {
                    "type": "android",
                    "platform": {
                        "name": "ham"
                    },
                    "androidId": str(uuid4())
                }
            }
        }
    resp = urlquick.post("https://jiotvapi.media.jio.com/userservice/apis/v1/loginotp/verify", json=otpbody, headers={"User-Agent": "okhttp/4.2.2", "devicetype": "phone", "os": "android", "appname": "RJIL_JioTV"}, max_age=-1, verify=False, raise_for_status=False).json()
    if resp.get("ssoToken", "") != "":
        _CREDS = {
            "authToken": resp.get("authToken"),
            "refreshToken": resp.get("refreshToken"),
            "jToken": resp.get("jToken"),
            "ssotoken": resp.get("ssoToken"),
            "userid": resp.get("sessionAttributes", {}).get("user", {}).get("uid"),
            "uniqueid": resp.get("sessionAttributes", {}).get("user", {}).get("unique"),
            "crmid": resp.get("sessionAttributes", {}).get("user", {}).get("subscriberId"),
            "subscriberid": resp.get("sessionAttributes", {}).get("user", {}).get("subscriberId"),
        }
        headers = {
            "deviceId": str(uuid4()),
            "devicetype": "phone",
            "os": "android",
            "osversion": "9",
            "user-agent": "plaYtv/7.1.5 (Linux;Android 9) ExoPlayerLib/2.11.7",
            "usergroup": "tvYR7NSNn7rymo3F",
            "versioncode": "353",
            "dm": "ZUK ZUK Z1"
        }
        headers.update(_CREDS)
        with PersistentDict("headers") as db:
            db["headers"] = headers
            db["exp"] = time.time() + sesTime
        SSET("exptime", dtnow.strftime("at %I:%M %p"))
        logstatus("in")        
        return None
    else:
        msg = resp.get("message", ANM)
        SSET("isloggedin", "false")
        notif("Login Failed " + msg)
        return msg

def sendOTP(mobile):
    mobile = "+91" + mobile
    body = {"number": base64.b64encode(mobile.encode("ascii")).decode("ascii")}
    resp = urlquick.post("https://jiotvapi.media.jio.com/userservice/apis/v1/loginotp/send", json=body, headers={"user-agent": "okhttp/4.2.2", "os": "android", "host": "jiotvapi.media.jio.com", "devicetype": "phone", "appname": "RJIL_JioTV"}, max_age=-1, verify=False, raise_for_status=False)
    if resp.status_code != 204:
        return resp.json().get("errors", [{}])[-1].get("message")
    return None

def logout():
    with PersistentDict("headers") as db:
        del db["headers"]
    logstatus("out")
