import pygame


class spritesheet(object):
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert_alpha()

    def image_at(self, rectangle, size=1, colorkey=None): #colorkey 是看背景的顏色
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        image = pygame.transform.scale(
            image, (image.get_size()[0] * size, image.get_size()[1] * size))
        return image

    def images_at(self, rects, size, colorkey=None):
        return [self.image_at(rect, size, colorkey)
                for rect in rects]  #前面的rect由後面的for迴圈決定 (整體是一個list)

    #第一張的rect
    def load_strip(self, rect, image_count, size, colorkey=None):
        #[(0, 0, 40, 50), (40, 0, 40, 50)]
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, size, colorkey)


class Animation:
    def __init__(self,
                 filename,
                 rect,
                 count,
                 size=1,
                 colorkey=None,
                 loop=False,
                 frames=1):
        self.filename = filename
        ss = spritesheet(filename)
        self.count=count
        self.imagesR = ss.load_strip(rect, count, size, colorkey)
        self.imagesL = [
            pygame.transform.flip(image, True, False) for image in self.imagesR
        ]
        self.times = 0
        self.now_picture_index = 0  #現在在地幾張 圖片
        self.loop = loop
        self.frames_needed_to_do_next = frames
        self.frames_now = 0  #現在在第幾幀

    def iter(self):
        self.now_picture_index = 0
        self.frames_now = 0

    def next(self, direction):
        if self.now_picture_index >= len(self.imagesR):
            if self.loop:
                self.now_picture_index = 0
                self.times += 1

        image = self.imagesR[self.now_picture_index] if direction == 1 else self.imagesL[self.now_picture_index]
        #??? = 如果if成立的值  if condition else 如果if不成立的值
        self.frames_now += 1
        if self.frames_now == self.frames_needed_to_do_next:
            self.now_picture_index += 1
            self.frames_now = 0
        return image

    def __add__(self, ss):
        self.images.extend(ss.images)
        return self
