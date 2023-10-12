#import cv2
#import pytesseract
#
#pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
#a = cv2.imread('name_of_gained_item.png', 1)
#
#gray = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
#thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
#invert = 255 - thresh
#acc_name = pytesseract.image_to_string(invert, lang='rus', config='--psm 6').replace('\n\n', ' ').replace('\n', ' ')
#acc_name = ''.join([i for i in acc_name if i != ' ']).replace('.', '').replace(',', '').replace('`', '').replace("'", '')
#
#print(acc_name)




a = set()


a.add(123)
a.add(123)
a.add(123)
a.add(123)
a.add(1232)

print(sorted(a))