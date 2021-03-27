from presidio_image_redactor import ImageRedactorEngine
from presidio_image_redactor.image_analyzer_engine import ImageAnalyzerEngine
from work_strategies.work_base_strategy import WorkerBaseStrategy
from urllib.request import urlopen
import cv2
from PIL import Image, ImageChops
import numpy as np
from mtcnn import MTCNN


class WorkerImageStrategy(WorkerBaseStrategy):
    facial_detector = MTCNN()
    image_analyzer = ImageAnalyzerEngine()
    text_redactor = ImageRedactorEngine()
    scan_for_text = True


    def _fetch(self, task):
        try:
            if task.in_is_local:
                task.data = Image.open(task.in_endpoint).convert('RGB')
            else:
                task.data = Image.open(urlopen(task.in_endpoint)).convert('RGB')
        except Exception:
            print(f'Error reading file from source: {task.in_endpoint}')
        return task

    def _process(self, task):
        try:
            task = self.__anonomize_faces(task)
            if self.scan_for_text:
                task = self.__scan_image_for_text(task)
        except Exception as e:
            print(e)
        return task

    def _push(self, worker, task):
        worker.write_queue.put(task)

    def __anonomize_faces(self, task):
        # note that PIL is RGB and CV2 is BGR
        img = np.array(task.data)
        enhanced_img = self.improve_contrast_image_using_clahe(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        faces = self.facial_detector.detect_faces(enhanced_img)
        task.profile['faces'] = faces
        for face in faces:
            x,y,w,h = face['box']
            cv2.rectangle(img,(x, y),(x+w, y+h),self.REDACT_COLOR,2)
            roi = img[y:y+h,x:x+w]
            blur = cv2.GaussianBlur(roi,(101,101),0)
            img[y:y+h,x:x+w] = blur
        task.data = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        return task

    def __scan_image_for_text(self, task):
        #this is a bit wasteful with memory but Presidio/PIL is not clear how analyze effects the underlying object
        temp = ImageChops.duplicate(task.data)
        image_result = self.image_analyzer.analyze(temp)
        if len(image_result) > 1:
            task.profile['ocr_results_bbox'] = image_result.__dict__
        task.data = self.text_redactor.redact(task.data, self.REDACT_COLOR)
        return task


    def improve_contrast_image_using_clahe(self,img: np.array) -> np.array:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv_planes = cv2.split(hsv)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(16, 16))
        hsv_planes[2] = clahe.apply(hsv_planes[2])
        hsv = cv2.merge(hsv_planes)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)