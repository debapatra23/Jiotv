
import xbmcaddon
from xbmcvfs import translatePath

ADD = xbmcaddon.Addon()
AIN = ADD.getAddonInfo
AID = AIN("id")
ANM = AIN("name")
PRO = AIN("profile")
ICO = AIN("icon")
GSET = ADD.getSetting
SSET = ADD.setSetting
runPg = "RunPlugin(plugin://" + AID + "/resources/lib/main/"
filterBy = ["Languages", "Categories", "Broadcasters"]
LMAP = {1: "Hindi", 2: "Marathi", 3: "Punjabi", 4: "Urdu", 5: "Bengali", 6: "English", 7: "Malayalam", 8: "Tamil", 9: "Gujarati", 10: "Odia", 11: "Telugu", 12: "Bhojpuri", 13: "Kannada", 14: "Assamese", 15: "Nepali", 16: "French"}
CMAP = {5: "Entertainment", 6: "Movies", 7: "Kids", 8: "Sports", 9: "Lifestyle", 10: "Infotainment", 12: "News", 13: "Music", 15: "Devotional", 16: "Business News", 17: "Educational", 18: "Shopping"}
BMAP = {1: "General", 3: "Viacom18 Media", 4: "Times Network", 5: "Zee Entertainment", 6: "Sony Pictures Network", 7: "Warner Bros", 8: "TV Today Network", 9: "Sun Network", 10: "Discovery Network", 11: "NDTV Network", 14: "9X Media", 15: "ABP Group", 16: "B4U Network", 18: "Doordarshan", 20: "Jio Sports Events", 22: "Raj Network", 23: "Republic Network", 24: "Sahara Network", 25: "TravelFoodxp Network", 26: "Fyi Media Group", 27: "Jio Cinema", 28: "Shemaroo Jio Live", 30: "BAG Network", 32: "ETV Network", 33: "Enterr10 Network", 34: "Education Network", 35: "Independent News Service", 36: "Malayala Manorama", 38: "Jaya TV Network", 41: "PTC Network", 44: "TV9 Network", 45: "Tseries Hungama", 46: "Merchant Records", 47: "Desi Punjabi Bhojpuri", 48: "Saregama", 49: "KC Global Media", 50: "Wild Earth", 51: "Zee News Media", 52: "Seven Colors Broadcasting", 53: "QYOU Media", 54: "PowerKids Entertainment", 55: "Asianet News Network", 56: "Brit Asia TV Network", 57: "ITV News Network", 58: "Hare Krsna Content Broadcast", 59: "MH One TV Network", 60: "News Nation Network", 61: "SAB Network", 62: "Kalaignar TV Pvt Ltd", 64: "Sidharth TV Network", 65: "Insight Media City", 66: "Fashion India", 67: "Brave TV", 68: "Narikaa Digital", 69: "Red Bull Media", 70: "RS Bharat", 71: "NH Studioz", 73: "INH News Janta TV", 74: "Channel Divya", 75: "Pitaara TV", 76: "Coke Studio India", 77: "Janam Multimedia", 78: "Navsarjan Sanskruti", 79: "Bollywood Masala", 80: "Bharat Nation", 81: "India Superfast", 82: "NK Media Ventures"}
MAPS = [LMAP, CMAP, BMAP]
CHANNELS_SRC = GSET("channelssource") if bool(GSET("channelssource")) else SSET("channelssource", "https://jiotvapi.cdn.jio.com/apis/v1.4/getMobileChannelList/get/?os=android&devicetype=phone&usertype=tvYR7NSNn7rymo3F")
GET_CHANNEL_URL = GSET("channelurl") if bool(GSET("channelurl")) else SSET("channelurl", "https://tv.media.jio.com/apis/v2.0/getchannelurl/getchannelurl?langId=6&userLanguages=All")
CATCHUP_SRC = GSET("catchupsource") if bool(GSET("catchupsource")) else SSET("catchupsource", "https://jiotvapi.cdn.jio.com/apis/v1.3/getepg/get?offset={0}&channel_id={1}&langId=6")
FEATURED_SRC = GSET("featuredsource") if bool(GSET("featuredsource")) else SSET("featuredsource", "https://tv.media.jio.com/apis/v1.6/getdata/featurednew?start=0&limit=30&langId=6")
M3U_PATH = GSET("m3ufolder") if bool(GSET("m3ufolder")) else SSET("m3ufolder", translatePath(PRO))
M3U_FILE = (GSET("m3ufile") if bool(GSET("m3ufile")) else SSET("m3ufile", "playlist")) + ".m3u"
EPG_SRC = GSET("epgsource") if bool(GSET("epgsource")) else SSET("epgsource", "https://tobalan.github.io/epg.xml.gz")
M3U_SRC = str(M3U_PATH) + str(M3U_FILE)
master = "/master.m3u8"
#daiurl = "https://dai.google.com/linear/hls/event/%s" + master
daiurl = "https://dai.google.com/ssai/event/%s" + master
epicon = "https://epiconvh.s.llnwi.net/%s" + master
pubads = "https://pubads.g.doubleclick.net/ssai/event/%s" + master
yuppfta = "https://yuppftalive.akamaized.net/080823/%s/playlist.m3u8"
sofast = "https://streams2.sofast.tv/ptnr-yupptv/title-%s-ENG_YuppTV/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/%s/manifest.m3u8"
IMG = "https://jiotvimages.cdn.jio.com/dare_images/images/%s/-/" % GSET("logosize")
yuppImg = "https://d229kpbsb5jevy.cloudfront.net/tv/150/150/bnw/"
epiconimg = "https://www.epicon.in/img/"

daikeys = {
        154: "UI4QFJ_uRk6aLxIcADqa_A", # Sony SAB
        155: "DD7fA-HgSUaLyZp9AjRYxQ", # Sony TEN 5 HD
        162: "yeYP86THQ4yl7US8Zx5eug", # Sony TEN 1 HD
        289: "oJ-TGgVFSgSMBUoTkauvFQ", # Sony MAX SD
        291: "HgaB-u6rSpGx3mo4Xu3sLw", # SET HD
        471: "UI4QFJ_uRk6aLxIcADqa_A", # Sony SAB HD
        474: "rPzF28qORbKZkhci_04fdQ", # Sony PAL
        476: "Qyqz40bSQriqSuAC7R8_Fw", # Sony MAX HD
        483: "4Jcu195QTpCNBXGnpw2I6g", # Sony MAX2
        514: "", # Sony TEN 1
        523: "", # Sony TEN 2
        524: "", # Sony TEN 3
        525: "", # Sony TEN 5
        697: "pSVzGmMpQR6jdmwwJg87OQ", # Sony AATH
        762: "8FR5Q-WfRWCkbMq_GxZ77w", # Sony PIX HD
        852: "V73ovbgASP-xGvQQOukwTQ", # Sony BBC Earth HD English
        872: "40H5HfwWTZadFGYkBTqagg", # Sony YAY Hindi
        873: "40H5HfwWTZadFGYkBTqagg", # Sony YAY Tamil
        874: "40H5HfwWTZadFGYkBTqagg", # Sony YAY Telugu
        891: "Syu8F41-R1y_JmQ7x0oNxQ", # Sony TEN 2 HD
        892: "", # Sony TEN 3 HD Hindi
        1146: "-_w3Jbq3QoW-mFCM2YIzxA", # Sony Marathi SD
        1393: "H_ZvXWqHRGKpHcdDE5RcDA", # Sony WAH
        1396: "HgaB-u6rSpGx3mo4Xu3sLw", # SET SD
        1772: "", # Sony TEN 4 HD Tamil
        1773: "", # Sony TEN 4 HD Telugu
        1774: "", # Sony TEN 4 Tamil
        1775: "", # Sony TEN 4 Telugu
        2861: "", # Sony TEN 3 HD Marathi

        3000: "IoTNl-GQShWKit_KdZNY_A", # NDTV Rajasthan
        3001: "sXGilpLZQeWCygKyNIyQig", # NDTV MP Chhattisgarh
    }
extUrls = {
        4000: epicon % "epic",
        4001: epicon % "gubbare", 
        4002: epicon % "ishaara",
        4003: epicon % "nazara",
        4004: epicon % "showbox",
        4005: epicon % "filamchi",
        4019: sofast % ("CARTOON-TV-CLASSICS", "d5543c06-5122-49a7-9662-32187f48aa2c"),
        4020: sofast % ("BABYFIRST", "c8d16110-566c-4e95-a1df-55d175e9e201"),
        4021: sofast % ("KIDDO", "5bcf9d24-04f2-401d-a93f-7af54f29461a"),
        4022: sofast % ("BEANI-KIDS-TV", "ae504cae-b81f-49e6-8b40-71d7c0843589"),
        4023: sofast % ("HD-TRAVEL-TV", "e58c3999-b5e1-4322-8d73-db8ebd8acb32"),
        4024: sofast % ("HERITAGE", "e4523706-f2a8-4b0f-b081-40fe59a46f81"),
        4025: sofast % ("HERITAGE-TOURISM-TV", "cff3309e-ded1-40dd-a6dc-e3a6d0a92d72"),
        4026: sofast % ("ENCORE", "390efe7e-4a1a-4f9f-8266-b4d90ab7121a"),
        4028: "https://anjantvevent.pc.cdn.bitgravity.com/anjantv/live/amlst:event_anjan_,b400,b800,b1024,b1200,b1500,b4000,.smil/playlist.m3u8",
        4030: "https://web-ndtv-marathi.akamaized.net/hls/live/2110470/ndtvmarathi/master_1.m3u8"
}

extraChannels = [
{"channel_id": 762, "channel_order": "2000", "channel_name": "Sony Pix HD", "channelCategoryId": 6, "channelLanguageId": 6, "isHD": True, "isCatchupAvailable": False, "broadcasterId": 6, "logoUrl": IMG+"Sony_Pix_HD.png"},
{"channel_id": 852, "channel_order": "2001", "channel_name": "Sony BBC Earth HD", "channelCategoryId": 10, "channelLanguageId": 6, "isHD": True, "isCatchupAvailable": False, "broadcasterId": 6, "logoUrl": IMG+"Sony_BBC_Earth_HD_English.png"},

{"channel_id": 3000, "channel_order": "2002", "channel_name": "NDTV Rajasthan", "channelCategoryId": 12, "channelLanguageId": 1, "isHD": False, "isCatchupAvailable": False, "broadcasterId": 11, "logoUrl": "https://yt3.googleusercontent.com/T5ltIUteczA2n9OJfjCEAYU1PZ_Mqbr3BkUrcgj7IvvkU5w8w3-wieb_KPCk--ZRNfNmesqXGg=s400"},
{"channel_id": 3001, "channel_order": "2003", "channel_name": "NDTV MP Chhattisgarh", "channelCategoryId": 12, "channelLanguageId": 1, "isHD": False, "isCatchupAvailable": False, "broadcasterId": 11, "logoUrl": "https://yt3.googleusercontent.com/qATXIkOUNcKSPZ4GYYpyDR1AaKmBjLKT2ITlIYtCNGThB9FLs-LuGwsnztgQzJarcNgG0Kgdg3k=s400"},
{"channel_id": 4030, "channel_order": "2004", "channel_name": "NDTV Marathi", "channelCategoryId": 12, "channelLanguageId": 2, "isHD": False, "isCatchupAvailable": False, "broadcasterId": 11, "logoUrl": "https://drop.ndtv.com/ndtv/ndtvcms/images/marathi/MH-512x512.jpg"},

{"channel_id": 4000, "channel_order": "2010", "channel_name": "Epic", "channelCategoryId": 9, "channelLanguageId": 1, "isHD": True, "isCatchupAvailable": False, "broadcasterId": 1, "logoUrl": epiconimg+"epic-tv.png"},
{"channel_id": 4001, "channel_order": "2017", "channel_name": "Gubbare", "channelCategoryId": 7, "channelLanguageId": 1, "isHD": True, "isCatchupAvailable": False, "broadcasterId": 1, "logoUrl": epiconimg+"gubbare-logo.png"},
{"channel_id": 4002, "channel_order": "2018", "channel_name": "Ishaara", "channelCategoryId": 5, "channelLanguageId": 1, "isHD": True, "isCatchupAvailable": False, "broadcasterId": 1, "logoUrl": epiconimg+"ishara-logo.png"},
{"channel_id": 4003, "channel_order": "2019", "channel_name": "Nazaara", "channelCategoryId": 5, "channelLanguageId": 1, "isHD": True, "isCatchupAvailable": False, "broadcasterId": 1, "logoUrl": epiconimg+"nazara-logo.png"},
{"channel_id": 4004, "channel_order": "2020", "channel_name": "Showbox", "channelCategoryId": 13, "channelLanguageId": 1, "isHD": True, "isCatchupAvailable": False, "broadcasterId": 1, "logoUrl": epiconimg+"new-show-box-logo.png"},
{"channel_id": 4005, "channel_order": "2021", "channel_name": "Filamchi Bhojpuri", "channelCategoryId": 6, "channelLanguageId": 12, "isHD": True, "isCatchupAvailable": False, "broadcasterId": 1, "logoUrl": epiconimg+"new_filamchi_logo.png"},
{"channel_id": 4019, "channel_order": "2022", "channel_name": "Cartoon TV Classics", "channelCategoryId": 7, "channelLanguageId": 6, "isHD": True, "isCatchupAvailable": False, "broadcasterId": 1, "logoUrl": yuppImg+"cartoon_classics_512X512_balck.png"},
{"channel_id": 4020, "channel_order": "2023", "channel_name": "Baby First", "channelCategoryId": 7, "channelLanguageId": 6, "isHD": True, "isCatchupAvailable": False, "broadcasterId": 1, "logoUrl": yuppImg+"BabyFirstTV_black.png"},
{"channel_id": 4021, "channel_order": "2024", "channel_name": "Kiddo", "channelCategoryId": 7, "channelLanguageId": 6, "isHD": True, "isCatchupAvailable": False, "broadcasterId": 1, "logoUrl": yuppImg+"Kiddo512X512_blackz1.png"},
{"channel_id": 4022, "channel_order": "2025", "channel_name": "Beani Kids TV", "channelCategoryId": 7, "channelLanguageId": 6, "isHD": True, "isCatchupAvailable": False, "broadcasterId": 1, "logoUrl": yuppImg+"Beani-Kids-TV_black.png"},
{"channel_id": 4023, "channel_order": "2026", "channel_name": "HD Travel TV", "channelCategoryId": 9, "channelLanguageId": 6, "isHD": True, "isCatchupAvailable": False, "broadcasterId": 1, "logoUrl": yuppImg+"HD-Travel_TV_black.png"},
{"channel_id": 4024, "channel_order": "2027", "channel_name": "Heritage", "channelCategoryId": 9, "channelLanguageId": 6, "isHD": True, "isCatchupAvailable": False, "broadcasterId": 1, "logoUrl": yuppImg+"Heritage_TV_black.png"},
{"channel_id": 4025, "channel_order": "2028", "channel_name": "Heritage Tourism TV", "channelCategoryId": 9, "channelLanguageId": 6, "isHD": True, "isCatchupAvailable": False, "broadcasterId": 1, "logoUrl": yuppImg+"heritage_tourism_512X512_balck.png"},
{"channel_id": 4026, "channel_order": "2029", "channel_name": "Encore", "channelCategoryId": 9, "channelLanguageId": 6, "isHD": True, "isCatchupAvailable": False, "broadcasterId": 1, "logoUrl": yuppImg+"512X512Encore.png"},
{"channel_id": 4028, "channel_order": "2030", "channel_name": "Anjan TV", "channelCategoryId": 13, "channelLanguageId": 1, "isHD": True, "isCatchupAvailable": False, "broadcasterId": 1, "logoUrl": "https://anjan.tv/sites/default/files/logo_0.png"}
]
