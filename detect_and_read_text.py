import cv2
from pytesseract import pytesseract
from pytesseract import Output
import pyttsx3

pytesseract.tesseract_cmd = "C:\\Tesseract-OCR\\tesseract.exe" #change path to tesseract.exe location in your machine

class detect_and_read_text:
    def read(self, file_path):
        img = cv2.imread(file_path)

        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        inv = cv2.bitwise_not(img2)

        ret, thresh1 = cv2.threshold(img2, 125, 255, cv2.THRESH_BINARY)

        ret, thresh2 = cv2.threshold(inv, 250, 255, cv2.THRESH_BINARY)

        add_thresh = thresh1|thresh2

        image_data = pytesseract.image_to_data(add_thresh, output_type=Output.DICT)

        sentence = ""
        for i, word in enumerate(image_data['text']):
            if word!="" and not word.isspace():
                x, y, w, h = image_data['left'][i], image_data['top'][i], image_data['width'][i], image_data['height'][i]
                cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 2)
                cv2.putText(img, word, (x,y-3), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,255,0), 1)
                sentence = sentence+" "+word

        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.say(sentence)
        engine.runAndWait()

        cv2.imshow("detected words", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
