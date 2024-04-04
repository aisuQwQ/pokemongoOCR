from paddleocr import PaddleOCR
from PIL import Image

import logging
logging.disable(logging.DEBUG)

print('Preparing...')
ocr = PaddleOCR(use_angle_cls=True, use_gpu=False, lang="japan")
print("Ready!")


def readExif(path):
    im=Image.open(path)
    exif=im._getexif()
    if(exif==None or 36867 not in exif):
        return ('-', '-')
    date, time=exif[36867].split(' ')
    date=date.replace(':', '/')
    return (date, time)

def readImg(path):
    result=ocr.ocr(path, cls=True)[0]
    texts = [line[1][0] for line in result]

    targets=['歩いた距離','つかまえたポケモン','訪れたポケストップ','トータルXP','始めた日']
    data={}
    for s in targets:
        if s in texts:
            index=texts.index(s)
            data[s]=texts[index+1]
        else:
            data[s]='-'
    index=texts.index('レベル')
    data['レベル']=texts[index-1]
    data['XP']=texts[index+1]

    print(f"OCR:SUCCESS '{path.split('./')[1]}'")
    data['日付'], data['時刻']=readExif(path)
    return data
