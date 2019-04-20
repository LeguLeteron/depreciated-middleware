from gtts import gTTS
import cv2
import pytesseract
from textblob import TextBlob

USERAGENT = "LeguLeteron/1.0 RequestType/"
MODE_TEXT = 1
MODE_IMAGE = 2
MODE_ERROR = "ERROR"

class Letero:
    def __init__(self, text="Hello, World!", img="images.png", filename="temp", filetype="mp3"):
        self.text = text
        self.img = img
        self.filename = filename
        self.filetype = filetype

    def detect_lang(self):
        lan = TextBlob(self.text)
        return lan.detect_language()

    def image_to_text(self):
        config = ('--tessdata-dir "{dir}" -l {lang}'.format(dir="tessdata", lang="ko"))
        im = cv2.imread(self.img, cv2.IMREAD_COLOR)

        text = pytesseract.image_to_string(im, config=config)
        return text

    def to_tts(self, text, language="ko"):
        tts = gTTS(text=text, lang=language)
        tts.save("{name}.{type}".format(name=self.filename, type=self.filetype))
