from urllib.request import urlopen
import cv2
from PIL import Image
import numpy as np
from mtcnn import MTCNN
np.seterr(divide='ignore', invalid='ignore')


def main():
    img = cv2.cvtColor(cv2.imread("../images/cast.jpg"), cv2.COLOR_BGR2RGB)
    detector = MTCNN()
    faces = detector.detect_faces(img)
    for face in faces:
        x,y,w,h = face['box']
        cv2.rectangle(img,
                      (x, y),
                      (x+w, y+h),
                      (0,155,255),
                      2)
        roi = img[y:y+h,x:x+w]
        blur = cv2.GaussianBlur(roi,(101,101),0)
        img[y:y+h,x:x+w] = blur
    img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
    cv2.imshow("image",img)
    cv2.waitKey(0)


if __name__ == '__main__':
    main()
