from gtts import gTTS
import cv2
import pytesseract
from textblob import TextBlob
import braille

MODE_TEXT = 1
MODE_IMAGE = 2
MODE_RETURN_TTS = 1
MODE_RETURN_BRAILLE = 2
LANG = "ko"
REQUEST_TYPE = MODE_TEXT
RETURN_MODE = MODE_RETURN_BRAILLE

MODE_ERROR = "ERROR"


class Letero:
    def __init__(self, text="Hello, World!", img="images.png", filename="temp", filetype="mp3"):
        self.text = text
        self.img = img
        self.filename = filename
        self.filetype = filetype
        self.useragent = {
            "LeguLeteron": "1.0",
            "RequestType": REQUEST_TYPE,
            "Language": LANG,
            "ReturnMode": RETURN_MODE,
            "Data": ""
        }

    def detect_lang(self):
        lan = TextBlob(self.text)
        return lan.detect_language()

    def image_to_text(self):
        config = ('--tessdata-dir "{dir}" -l {lang}'.format(dir="tessdata", lang=LANG))
        im = cv2.imread(self.img, cv2.IMREAD_COLOR)

        text = pytesseract.image_to_string(im, config=config)
        return text

    def to_tts(self, text):
        tts = gTTS(text=text, lang=LANG)
        tts.save("{name}.{type}".format(name=self.filename, type=self.filetype))

    def to_braille(self, text, quiet=True):
        data = braille.to_braille(text)
        if not quiet:
            braille.print_braille(data)
        else:
            return data
