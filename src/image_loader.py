__author__ = 'Andrey Lazarevich'
import cv2
import os


class ImageLoader:

    def __init__(self, cut_size=250, image_dir_path=os.getcwd(), haarcascade_path='haarcascade_eye.xml'):
        self.separator = os.sep
        self.haarcascade_name = haarcascade_path
        self.cascade = []
        self.init_haar()
        assert isinstance(cut_size, int)
        self.cut_size = cut_size
        self.image_ext = [".jpg", ".png", ".bmp"]
        self.dir_path = image_dir_path
        self.image_dir = os.listdir(image_dir_path)

    def init_haar(self):
        try:
            self.cascade = cv2.CascadeClassifier(self.haarcascade_name)
        except Exception:
            self.cascade = []

    def load(self, image_name):
        full_path = self.dir_path + self.separator + image_name
        image = cv2.imread(full_path)
        if not self.cascade:
            cutted_image = self.__simple_cut(image)
        else:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            eyes = self.cascade.detectMultiScale(gray)
            try:
                x_local = eyes[0][0]
                y_local = eyes[0][1]
                cutted_image = self.__smart_cut(x_local, y_local, image)
            except IndexError:
                cutted_image = self.__simple_cut(image)
        return cv2.resize(cutted_image, (self.cut_size, self.cut_size))

    def __smart_cut(self, x_local, y_local, image):
        height = image.shape[0]
        width = image.shape[1]
        if height < width:
            diff = height / 2
            right_space = width - x_local
            if right_space < diff:
                left_adjust = 2 * diff - right_space
                cutted_image = image[0:height, x_local - left_adjust:width]
            else:
                right_adjust = 2 * diff - x_local
                cutted_image = image[0:height, 0:x_local + right_adjust]
        else:
            diff = width / 2
            top_space = height - y_local
            if top_space < diff:
                bot_adjust = 2 * diff - top_space
                cutted_image = image[y_local - bot_adjust:height, 0:width]
            elif y_local < diff:
                top_adjust = 2 * diff - y_local
                cutted_image = image[0:y_local + top_adjust, 0:width]
        return cutted_image

    def __simple_cut(self, image):
        height = image.shape[0]
        width = image.shape[1]
        x_local = width / 2
        y_local = height / 2
        if height < width:
            diff = height / 2
            cutted_image = image[0:height, x_local - diff:x_local + diff]
        else:
            diff = width/2
            cutted_image = image[y_local - diff:y_local + diff, 0:width]
        return cutted_image

    def available_images(self):
        image_names = []
        for some_file in self.image_dir:
            filext = os.path.splitext(some_file)[1]
            if filext in self.image_ext:
                image_names.append(some_file)
        return image_names






