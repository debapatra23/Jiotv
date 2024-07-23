
from __future__ import unicode_literals
from xbmcaddon import Addon
from xbmc import executebuiltin
from xbmcgui import Dialog
from codequick import Route, run, Listitem, Resolver, Script
from codequick.script import Settings
from codequick.utils import keyboard
import inputstreamhelper
import urlquick
from uuid import uuid4
from urllib.parse import urlencode
from time import time, sleep
from datetime import datetime, timedelta, date
import json
import m3u8
from .utils import getHeaders, quality_to_enum, strdtnow, notif, daysLeft, hoursLeft, actstatus, expstatus, isLoggedIn, login as ULogin, logout as ULogout, sendOTP, refresh_token
from .constants import filterBy, MAPS, LMAP, CMAP, BMAP, GSET, SSET, CHANNELS_SRC, GET_CHANNEL_URL, CATCHUP_SRC, FEATURED_SRC, M3U_SRC, EPG_SRC, ANM, AID, ICO, IMG, M3U_PATH, runPg, daiurl, daikeys, extraChannels, extUrls
getBool = Settings.get_boolean
channels = urlquick.get(CHANNELS_SRC).json().get("result")
if getBool("extrach"):
    channels.extend(extraChannels)
    daikeys.update(extUrls)
totalCh = len(channels)
fltraL = getBool("filteraddlist")
hdsdch = int(GSET("hdsdch"))
PID = "pvr.iptvsimple"
IID = "inputstream.adaptive"
menu = {"show_listby": filterBy, "catlang_ch": " + ".join([filterBy[1].replace("ies", "y"), filterBy[0][:-1]]), "show_allch": "All " + str(totalCh) + " Channels", "show_featured": "Featured • " + strdtnow[:-12], "show_testch": "Test Channels", "show_settings": "Settings"}
menuLen = len(list(menu))
hasLogo = getBool("chlogo")
art = {"thumb": ICO, "icon": ICO, "fanart": ICO} if hasLogo else {}
tests = ["test", "Test", "TEST"]

@Route.register
def root(plugin):
    mpath = runPg[-20:-1] + ":"
    for f in filterBy:
        yield Listitem.from_dict(**{
            "label": f,
            "art": art,
            "callback": Route.ref(mpath + list(menu)[0]),
            "params": {"by": f}
        })
    menust = 1 if getBool("clmn") else 2
    for g in range(menust, menuLen):
        yield Listitem.from_dict(**{
            "label": list(menu.values())[g],
            "art": art,
            "callback": Route.ref(mpath + list(menu)[g])
        })

@Route.register
def show_listby(plugin, by):
    CONFIG = {}
    for c in range(len(filterBy)):
        OtherKey = list(MAPS[c])[-1] + 1
        MAPS[c].update({OtherKey: "Other " + filterBy[c]})
        CONFIG.update({filterBy[c]: list(MAPS[c].values())})
    for fltr in CONFIG[by]:
        if fltraL:
            if not getBool(fltr):
               continue
        yield Listitem.from_dict(**{
               "label": fltr,
               "art": art,
               "callback": show_channels,
               "params": {"LanCatBro": fltr, "by": by}
           })

def mapId(channel):
    def getmapId(MAP, Id):
        lcbid = channel.get(Id)
        if lcbid not in MAP:
            OtherLCB = "Other " + Id.replace("channel", "").replace("Id", "s").replace("y", "ie").capitalize()
            MAP[lcbid] = OtherLCB
            SSET(OtherLCB, "true")
        return MAP[lcbid]
    Lan = getmapId(LMAP, "channelLanguageId")
    Cat = getmapId(CMAP, "channelCategoryId")
    Bro = getmapId(BMAP, "broadcasterId")
    return Lan, Cat, Bro

def lanCat(channel):
    Cat = CMAP[channel.get("channelCategoryId")]
    Lan = LMAP[channel.get("channelLanguageId")]
    return Lan, Cat

def extUri(channel_id):
    return extUrls[channel_id] if channel_id in extUrls else daiurl % daikeys[channel_id]

def chlogo(channel, channel_id):
    return IMG + channel.get("logoUrl") if channel_id not in daikeys else channel.get("logoUrl")

def list_channels(channel):
    channel_id = channel.get("channel_id")
    channel_name = channel.get("channel_name")
    if any(test in channel_name for test in tests):
        Lan, Cat = lanCat(channel)
        channel_name += " (" + Lan + ", " + Cat + ")"
    if getBool("numaddlist"):
        channel_name = "  ".join([str(int(channel.get("channel_order")) + 1), channel_name])
    channel_logo = ""
    if hasLogo:
        channel_logo = chlogo(channel, channel_id)
        art["thumb"] = art["icon"] = art["fanart"] = channel_logo
    listchannels = Listitem.from_dict(**{
            "label": channel_name,
            "art": art,
            "callback": play,
            "params": {
                "channel_id": channel_id
            }
        })        
    if channel.get("isCatchupAvailable") and channel.get("stbCatchup") in [None, True]:
        listchannels.context.container(show_epg, "Catchup", 0, channel_id)
    return listchannels

@Route.register
def show_channels(plugin, LanCatBro, by):
    def fltr(channel):
        Lan, Cat, Bro = mapId(channel)
        LCB = [Lan, Cat, Bro]
        for i in range(len(filterBy)):
            if by == filterBy[i]:
               return LCB[i] == LanCatBro
    for channel in filter(fltr, channels):
        Lan, Cat, Bro = mapId(channel)
        isHD = channel.get("isHD")
        if fltraL:
            if not getBool(Lan):
                continue
            if not getBool(Cat):
                continue
            if not getBool(Bro):
                continue
        if hdsdch == 1 and not isHD:
            continue
        if hdsdch == 2 and isHD:
            continue
        yield list_channels(channel)

@Route.register
def catlang_ch(plugin):
    Cats = list(MAPS[1].values())
    Lans = list(MAPS[0].values())
    CatInd = Dialog().select(filterBy[1], Cats, preselect=0)
    LanInd = Dialog().select(filterBy[0], Lans, preselect=0)
    def fltrcatlang(channel):
        Lan, Cat = lanCat(channel)
        if Cats[CatInd] == Cat and Lans[LanInd] == Lan:
            return True
    for channel in filter(fltrcatlang, channels):
        yield list_channels(channel)

@Route.register
def show_allch(plugin):
    for channel_id, channel in enumerate(channels):
        yield list_channels(channel)

@Route.register
def show_testch(plugin):
    for channel_id, channel in enumerate(channels):
        if any(test in channel.get("channel_name") for test in tests):
            yield list_channels(channel)

@Route.register
def show_featured(plugin, id=None):
    resp = urlquick.get(FEATURED_SRC, headers={"usergroup": "tvYR7NSNn7rymo3F", "os": "android", "devicetype": "phone", "versionCode": "353"}, max_age=-1).json()
    for each in resp.get("featuredNewData", []):
        if id:
             if int(each.get("id", 0)) == int(id):
                data = each.get("data", [])
                for child in data:
                    info_dict = {
                        "art": art,
                        "info": {
                            'originaltitle': child.get("showname"),
                            "tvshowtitle": child.get("showname"),
                            "genre": child.get("showGenre"),
                            "plot": child.get("description"),
                            "episodeguide": child.get("episode_desc"),
                            "episode": 0 if child.get("episode_num") == -1 else child.get("episode_num"),
                            "cast": child.get("starCast", "").split(', '),
                            "director": child.get("director"),
                            "duration": child.get("duration")*60,
                            "tag": child.get("keywords"),
                            "mediatype": "movie" if child.get("channel_category_name") == "Movies" else "episode",
                        }
                    }
                    if child.get("showStatus") == "Now":
                        info_dict["label"] = info_dict["info"]["title"] = child.get(
                            "showname", "") + "[COLOR red] • LIVE[/COLOR]"
                        info_dict["callback"] = play
                        info_dict["params"] = {
                            "channel_id": child.get("channel_id")}
                        yield Listitem.from_dict(**info_dict)
                    elif child.get("showStatus") == "future":
                        timetext = datetime.fromtimestamp(int(child.get("startEpoch", 0)*.001)).strftime(
                            '    [ %I:%M %p -') + datetime.fromtimestamp(int(child.get("endEpoch", 0)*.001)).strftime(' %I:%M %p ]   %a')
                        info_dict["label"] = info_dict["info"]["title"] = child.get(
                            "showname", "") + ("[COLOR green]%s[/COLOR]" % timetext)
                        info_dict["callback"] = ""
                        yield Listitem.from_dict(**info_dict)
                    elif child.get("showStatus") == "catchup":
                        timetext = datetime.fromtimestamp(int(child.get("startEpoch", 0)*.001)).strftime(
                            '    [ %I:%M %p -') + datetime.fromtimestamp(int(child.get("endEpoch", 0)*.001)).strftime(' %I:%M %p ]   %a')
                        info_dict["label"] = info_dict["info"]["title"] = child.get(
                            "showname", "") + ("[COLOR yellow]%s[/COLOR]" % timetext)
                        info_dict["callback"] = play
                        info_dict["params"] = {
                            "channel_id": child.get("channel_id"),
                            "showtime": child.get("showtime", "").replace(":", ""),
                            "srno": datetime.fromtimestamp(int(child.get("startEpoch", 0)*.001)).strftime('%Y%m%d'),
                            "programId":  child.get("srno", ""),
                            "begin":  datetime.fromtimestamp(int(child.get("startEpoch", 0)*.001)).strftime('%Y%m%dT%H%M%S'),
                            "end":  datetime.fromtimestamp(int(child.get("endEpoch", 0)*.001)).strftime('%Y%m%dT%H%M%S')
                        }
                        yield Listitem.from_dict(**info_dict)
        else:
            yield Listitem.from_dict(**{
                "label": each.get("name"),
                "art": art,
                "callback": show_featured,
                "params": {"id": each.get("id")}
            })

@Route.register
def show_epg(plugin, day, channel_id):
    resp = urlquick.get(CATCHUP_SRC.format(day, channel_id), max_age=-1).json()
    epg = sorted(
        resp['epg'], key=lambda show: show['startEpoch'], reverse=True)
    livetext = '[COLOR red] • LIVE[/COLOR]'
    for each in epg:
        current_epoch = int(time()*1000)
        if not each['stbCatchupAvailable'] or each['startEpoch'] > current_epoch:
            continue
        islive = each['startEpoch'] < current_epoch and each['endEpoch'] > current_epoch
        showtime = '   '+livetext if islive else datetime.fromtimestamp(
            int(each['startEpoch']*.001)).strftime(' [ %I:%M %p -') + datetime.fromtimestamp(int(each['endEpoch']*.001)).strftime(' %I:%M %p ] %a')
        yield Listitem.from_dict(**{
            "label": each['showname'] + showtime,
            "art": art,
            "callback": play,
            "info": {
                'title': each['showname'] + showtime,
                'originaltitle': each['showname'],
                "tvshowtitle": each['showname'],
                'genre': each['showGenre'],
                'plot': each['description'],
                "episodeguide": each.get("episode_desc"),
                'episode': 0 if each['episode_num'] == -1 else each['episode_num'],
                'cast': each['starCast'].split(', '),
                'director': each['director'],
                'duration': each['duration']*60,
                'tag': each['keywords'],
                'mediatype': 'episode',
            },
            "params": {
                "channel_id": each.get("channel_id"),
                "showtime": None if islive else each.get("showtime", "").replace(":", ""),
                "srno": None if islive else datetime.fromtimestamp(int(each.get("startEpoch", 0)*.001)).strftime('%Y%m%d'),
                "programId": None if islive else each.get("srno", ""),
                "begin": None if islive else datetime.fromtimestamp(int(each.get("startEpoch", 0)*.001)).strftime('%Y%m%dT%H%M%S'),
                "end": None if islive else datetime.fromtimestamp(int(each.get("endEpoch", 0)*.001)).strftime('%Y%m%dT%H%M%S'),
            }
        })
    if int(day) == 0:
        for i in range(-1, -7, -1):
            label = 'Yesterday' if i == - \
                1 else (date.today() + timedelta(days=i)).strftime('%A %d %B')
            yield Listitem.from_dict(**{
                "label": label,
                "art": art,
                "callback": show_epg,
                "params": {
                    "day": i,
                    "channel_id": channel_id
                }
            })

@Resolver.register
@isLoggedIn
def play(plugin, channel_id, showtime=None, srno=None, programId=None, begin=None, end=None):
    uriToUse = ""
    manifestType = "hls"
    selectionType = GSET("sstype").lower()
    resMax = GSET("resmax")
    resSecMax = GSET("ressecmax")
    props = {
    "IsPlayable": True,
    "inputstream": IID,
    "inputstream.adaptive.manifest_type": manifestType,
    "inputstream.adaptive.stream_selection_type": selectionType,
    "inputstream.adaptive.chooser_resolution_max": resMax,
    "inputstream.adaptive.chooser_resolution_secure_max": resSecMax,
        }
    isExtraCh = getBool("extrach") and channel_id in daikeys
    if isExtraCh:
        uriToUse = extUri(channel_id)
        manifestType = "hls"
        return Listitem().from_dict(**{
        "label": plugin._title,
        "art": art,
        "callback": uriToUse,
        "properties": props
    })
    drm = "com.widevine.alpha"
    is_helper = inputstreamhelper.Helper("mpd", drm)
    hasIs = is_helper.check_inputstream()
    if not hasIs:
        return
    rjson = {
        "channel_id": int(channel_id),
        "stream_type": "Seek"
    }
    if daysLeft <= 0:
        if hoursLeft <= 0:
            refresh_token()
    expstatus()
    actstatus()
    isCatchup = False
    if showtime and srno:
        isCatchup = True
        rjson["showtime"] = showtime
        rjson["srno"] = srno
        rjson["stream_type"] = "Catchup"
        rjson["programId"] = programId
        rjson["begin"] = begin
        rjson["end"] = end
    headers = getHeaders()
#  accesstoken = headers.get("authToken","")
    getUrlHeaders = {"devicetype": "phone", "os": "android", "versioncode": "353", "Content-Type": "application/json"}
# "accesstoken": accesstoken
    headers['channelid'] = str(channel_id)
    headers['srno'] = str(uuid4()) if "srno" not in rjson else rjson["srno"]
    getchannelUrl = GSET("channelurl")
    res = urlquick.post(getchannelUrl, json=rjson, headers=getUrlHeaders, max_age=-1)
    if res.status_code == 419 or res.status_code == 403:
        refresh_token()
    resp = res.json()
    onlyUrl = resp.get("result", "").split("?")[0].split('/')[-1]
    if hasLogo:
        art["thumb"] = art["icon"] = art["fanart"] = IMG + onlyUrl.replace(".m3u8", ".png")
    cookie = "__hdnea__"+resp.get("result", "").split("__hdnea__")[-1]
    headers['cookie'] = cookie
    uriToUse = resp.get("result","")
    mpdArray = resp.get("mpd","")
    isMPD = getBool("usempd")
    mpdMode = isMPD and mpdArray
    if mpdMode:
        manifestType = "mpd"
        uriToUse = mpdArray.get("result", "")
        drmKey = mpdArray.get("key", "")
        license_headers = headers
        license_headers['Content-type'] = 'application/octet-stream'
        manifestHeaders = urlencode(license_headers)
        licenseKey = drmKey + "|" + urlencode(license_headers)
    else:  
        m3u8Headers = {}
        m3u8Headers['user-agent'] = headers['user-agent']
        m3u8Headers['cookie'] = cookie
        m3u8Res = urlquick.get(uriToUse, headers=m3u8Headers, max_age=-1, raise_for_status=True , timeout=9)
        m3u8String = m3u8Res.text
        variant_m3u8 = m3u8.loads(m3u8String)
        isVariant = variant_m3u8.is_variant
        qltyopt = GSET("quality")
        isAdaptiveHLS = GSET("sstype") == "Adaptive" and not isMPD
        if isAdaptiveHLS and isVariant:
            quality = quality_to_enum(qltyopt, len(variant_m3u8.playlists))
            if isCatchup:
                tmpurl = variant_m3u8.playlists[quality].uri
                if "?" in tmpurl:
                    uriToUse = uriToUse.split("?")[0].replace(onlyUrl,tmpurl)
                else:
                    uriToUse = uriToUse.replace(onlyUrl, tmpurl.split("?")[0])
                del headers['cookie']
            else:
                uriToUse = uriToUse.replace(onlyUrl, variant_m3u8.playlists[quality].uri)
        manifestHeaders = urlencode(headers)
        licenseKey = "|" + urlencode(headers)
    props.update({
    "inputstream.adaptive.manifest_type": manifestType,
    "inputstream.adaptive.stream_headers": manifestHeaders,
    "inputstream.adaptive.license_type": drm,
    "inputstream.adaptive.license_key": licenseKey + "|R{SSM}|",
        })
    return Listitem().from_dict(**{
        "label": plugin._title,
        "art": art,
        "callback": uriToUse,
        "properties": props
    })

@Script.register
def m3ugen(plugin):
    PLAY_URL = runPg[10:] + "play/?"
    M3U_CHANNEL = "\n#EXTINF:0 tvg-id=\"{tvg_id}\" tvg-name=\"{channel_name}\" group-title=\"{group_title}\" tvg-chno=\"{tvg_chno}\" tvg-logo=\"{tvg_logo}\"{catchup},{channel_name}\n{play_url}"
    m3ustr = "#EXTM3U"
    if getBool("chepg"):
        m3ustr += " x-tvg-url=\"%s\"" % EPG_SRC
    for i, channel in enumerate(channels):
        Lan, Cat, Bro = mapId(channel)
        if getBool("filterplaylist"):
            if not getBool(Lan):
               continue 
            if not getBool(Cat):
               continue                  
            if not getBool(Bro):
               continue
        isHD = channel.get("isHD")
        if hdsdch == 1 and not isHD:
            continue
        if hdsdch == 2 and isHD:
            continue
        channel_id = channel.get("channel_id")
        channel_logo = chlogo(channel, channel_id)
        group = Lan + ";" + Cat
        _play_url = extUri(channel_id) if getBool("extrach") and channel_id in daikeys else PLAY_URL + "channel_id={0}".format(channel_id)
        catchup = ""
        if channel.get("isCatchupAvailable"):
            catchup = ' catchup="vod" catchup-source="{0}channel_id={1}&showtime={{H}}{{M}}{{S}}&srno={{Y}}{{m}}{{d}}&programId={{catchup-id}}" catchup-days="7"'.format(PLAY_URL, channel_id)
        m3ustr += M3U_CHANNEL.format(
            tvg_id=channel_id,
            channel_name=channel.get("channel_name"),
            group_title=group,
            tvg_chno=int(channel.get("channel_order", i)) + 1,
            tvg_logo=channel_logo,
            catchup=catchup,
            play_url=_play_url,
        )
    with open(M3U_SRC, "w+") as f:
        f.write(m3ustr.replace(u'\xa0', ' ').encode('utf-8').decode('utf-8'))
    urlquick.cache_cleanup(-1)
    notif("Playlist Updated. Restart")

@Route.register
def show_settings(plugin):
    def lab(id):
       Ai = Addon(id).getAddonInfo
       return str(Ai("name") + " " + list(menu.values())[menuLen-1])
    for id in [AID, PID, IID]:
        yield Listitem.from_dict(**{
            "label": lab(id),
            "art": art,
            "callback": open_settings,
            "params": {"id": id}
        })
    tasks = ["Update " + lab(PID)[:-8] + "Playlist", "Clear " + ANM + " Cache"]
    for t in tasks:
        yield Listitem.from_dict(**{
            "label": t,
            "art": art,
            "callback": m3ugen if t == tasks[0] else cleanup
        })

@Script.register 
def open_settings(plugin, id):
    Addon(id).openSettings()

@Script.register
def cleanup(plugin):
    urlquick.cache_cleanup(-1)
    notif("Cache cleared")

@Script.register
def login(plugin):
    headers = getHeaders()
    if headers:
        refresh_token()
        return
    if GSET("mobile") != "": 
        mobile = GSET("mobile")
    else:
        mobile = Dialog().numeric(0, "Enter " + ANM[:-2] + " number")
        SSET("mobile", mobile)
    error = sendOTP(mobile)
    if error:
        notif("Login Error " + error)
        return
    otp = Dialog().numeric(0, "Enter " + ANM + " OTP")
    ULogin(mobile, otp)

@Script.register
def logout(plugin):
    urlquick.cache_cleanup(-1)
    ULogout()
