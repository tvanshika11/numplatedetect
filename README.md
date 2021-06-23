Number plate detection using pytesseract.
Libraries installed:
1. open cv
2. pytesseract
3. imutils

prior requirements :
you need to install tesseract.exe file(approx 50.7MB) from tesseract-OCR and copy its path

We have used Canny edge detection algo for detecting edges.
And finally we have used pytesseract.image_to_string function for extracting the number .
