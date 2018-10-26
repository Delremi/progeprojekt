import requests
from bs4 import BeautifulSoup
import re
from googletrans import Translator


###########SONGS######################################################

while True:
	artist = raw_input("\033[1m" + "Artist: " + "\033[0m")
	artist_url = artist.replace(" ","").replace(".","").replace("-","").lower()
	songs_index = artist_url[0]
	if not songs_index.isalpha(): songs_index = 19
	songs_url = "https://www.azlyrics.com/%s/%s.html" % (songs_index, artist_url)
	songs_source = requests.get(songs_url).text
	songs_soup = BeautifulSoup(songs_source, "lxml")
	songs_text = songs_soup.get_text().split("\n")
	if not len(songs_text) == 225:
		break
	print("Sellist artisti ei leitud, palun proovi uuesti!")


startline = re.sub(r"\s+", "", "var songlist = [")
endline = re.sub(r"\s+", "", "var res = '<br>';")
status = 0
songs = []
for line in songs_text:
	line_check = re.sub(r'\s+', '', line).strip("\n")
	if line_check == startline:
		status = 1
		continue
	if line_check == endline:
		status = 0
	if status:
		line = line.split(",")[0]
		line = line.strip("{s:").strip('"')
		songs.append(line.encode("utf-8"))

print("\033[1m" + "ANDMEBAASIST LEITUD LOOD:" + "\033[0m")
for item in songs:
	print(item)


#########LYRICS#######################################################

while True:
	title = raw_input("\033[1m" + "Pealkiri: " + "\033[0m")
	title_url = title.replace(" ","").lower()
	lyrics_url = "https://www.azlyrics.com/lyrics/%s/%s.html" % (artist_url, title_url)
	lyrics_source = requests.get(lyrics_url).text
	lyrics_soup = BeautifulSoup(lyrics_source, "lxml")
	lyrics_text = lyrics_soup.get_text().split("\n")
	if not len(lyrics_text) == 225:
		break
	print("Sellist lugu ei leitud, palun proovi uuesti!")

lyrics = []
title_print = ""

startline = '"%s"' % title.lower()
endline = re.sub(r"\s+", "", "if  ( /Android|webOS|iPhone|iPod|iPad|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) )")
status = 0
for line in lyrics_text:
	endline_check  = re.sub(r'\s+', '', line)
	if line.lower() == startline:
		title_print = line
		status = 1
		continue
	if endline_check == endline:
		status = 0
	if status:
		lyrics.append(line.encode('utf-8'))

del lyrics[0:3]
del lyrics[-5:]

print("\n" * 5 + "\033[1m" + title_print + "\033[0m" + "\n" * 2)
for line in lyrics:
	print(line)


#####################################TRANSLATE#####################################
LANGUAGES = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu',
    'fil': 'Filipino',
    'he': 'Hebrew'
}

translator = Translator()

translations = translator.translate(lyrics, dest = "ru")
for i in translations:
	print(i.text)

