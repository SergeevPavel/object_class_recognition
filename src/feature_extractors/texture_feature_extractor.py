import random

from feature_extractor import FeatureExtractor
from texture_feature_extractor_functions import _image_tile_distance, _tile_tile_distance


class TextureFeatureExtractor(FeatureExtractor):
    def __init__(self, image_loader, tile_size=5, tiles_count=1000,
                 images_for_tailing_count=500, delta=0.0, debug=False):
        self.il = image_loader
        self.tile_size = tile_size
        self.tiles_count = tiles_count
        self.images_for_tailing_count = images_for_tailing_count
        self.delta = delta
        self.debug = debug

    def _extract(self, img):
        features =[]
        for tile in self.tiles:
            features.append(_image_tile_distance(img, tile))
        return features

    def _check_same_tile_exist(self, new_tile):
        for tile in self.tiles:
            dst = _tile_tile_distance(tile, new_tile)
            self._debug_print('dst: {}'.format(dst))
            if dst < self.delta:
                return True
        return False

    def generate_tiles(self):
        '''
        generate tiles, and initialize self.tiles
        if images_for_tailing is too low raise exception
        :return:
        '''
        self.tiles = []
        available_images_names = self.il.available_images()
        images_for_tailing_names = random.sample(available_images_names, self.images_for_tailing_count)
        for img_name in images_for_tailing_names:
            img = self.il.load(img_name)
            new_tiles = self._divide_img_by_tiles(img)
            for new_tile in new_tiles:
                if not self._check_same_tile_exist(new_tile):
                    self.tiles.append(new_tile)
                    self._debug_print('tiles count: {}'.format(len(self.tiles)))
                    if len(self.tiles) == self.tiles_count:
                        return
        raise Exception('Tiles not generated')

    def _divide_img_by_tiles(self, img):
        tiles = []
        (height, width) = img.shape[0:2]
        for x in xrange(0, width, self.tile_size):
            for y in xrange(0, height, self.tile_size):
                tiles.append(img[x:(x + self.tile_size), y:(y + self.tile_size)])
        return tiles

    def _debug_print(self, str):
        if self.debug:
            print('TFE debug: {}'.format(str))