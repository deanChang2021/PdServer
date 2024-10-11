from typing import Union
import pytesseract
from PIL import Image
from pytesseract import Output


class OCR:

    def ocr(self, imgPath: str, lang: str) -> Union[str, None]:
        print("ocr imgPath: "+ imgPath)
        try:

            # 打开图像文件
            image = Image.open(imgPath)

            # 进行文字识别
            text = pytesseract.image_to_string(image, lang='chi_sim')

            # 打印识别结果
            print("--------text------------")
            print(text)
            return text
        except Exception as e:
            print(e.args)


    def ocr_position(self, imgPath: str, lang: str) -> Union[str, None]:
        print("ocr_position imgPath: " + imgPath)
        try:
            image = Image.open(imgPath)
            print(pytesseract.image_to_boxes(image, output_type=Output.STRING, lang='chi_sim'))
            print("#" * 30)
            print(pytesseract.image_to_data(image, output_type=Output.STRING, lang='chi_sim'))

            # 打印识别结果
            print("--------text------------")

        except Exception as e:
            print(e.args)

    def trans2Black(self, imgPath:str):
        image = Image.open(imgPath)
        grayImage = image.convert("L")
        grayPath = "C:/Users/xdm20058003/Pictures/ocr/gray.jpg"
        grayImage.save(grayPath)
        return grayPath

if __name__ == '__main__':
    #print(pytesseract.get_languages(config=''))
    #OCR().ocr("C:/Users/xdm20058003/Pictures/ocr/test.PNG","chi_sim")

    ocrObj = OCR()
    ocrObj.ocr("C:/Users/xdm20058003/Pictures/ocr/test4.png","chi_sim")
    #grayPath = ocrObj.trans2Black("C:/Users/xdm20058003/Pictures/ocr/test3.jpeg")
    #ocrObj.ocr_position("C:/Users/xdm20058003/Pictures/ocr/test3.jpeg","chi_sim")