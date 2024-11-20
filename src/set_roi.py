# set_roi.py → 20.11.2024
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.image import Image
import cv2
import numpy as np


class ROICanvas(Widget):
    """ROI (Region of Interest) seçimi için canvas widget'ı"""
    # Widget'ın boyutlarını tutacak özellikler
    width = NumericProperty(0)
    height = NumericProperty(0)

    def __init__(self, original_image=None, **kwargs):
        super().__init__(**kwargs)
        self.original_image = original_image
        self.start_pos = None
        self.end_pos = None
        self.roi_image = None
        self.roi_coords = None

        # Canvas'ı güncelle
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, *args):
        """Canvas boyutlarını güncelle"""
        self.width = self.size[0]
        self.height = self.size[1]

    def on_touch_down(self, touch):
        """Dokunma başladığında çağrılır"""
        if not self.collide_point(*touch.pos):
            return

        # Önceki çizimleri temizle
        self.canvas.after.clear()
        self.start_pos = touch.pos

        with self.canvas.after:
            Color(1, 0, 0, 0.5)  # Kırmızı, yarı saydam
            self.rect_draw = Rectangle(pos=touch.pos, size=(0, 0))

    def on_touch_move(self, touch):
        """Dokunma hareket ettiğinde çağrılır"""
        if not self.start_pos:
            return

        x = min(touch.pos[0], self.start_pos[0])
        y = min(touch.pos[1], self.start_pos[1])
        w = abs(touch.pos[0] - self.start_pos[0])
        h = abs(touch.pos[1] - self.start_pos[1])

        self.rect_draw.pos = (x, y)
        self.rect_draw.size = (w, h)

    def on_touch_up(self, touch):
        """Dokunma bittiğinde çağrılır"""
        if not self.start_pos or not self.original_image is not None:
            return

        self.end_pos = touch.pos

        # Görüntü koordinatlarına dönüştür
        img_h, img_w = self.original_image.shape[:2]
        scale_x = img_w / float(self.width)
        scale_y = img_h / float(self.height)

        x1 = int(min(self.start_pos[0], self.end_pos[0]) * scale_x)
        y1 = int(min(self.start_pos[1], self.end_pos[1]) * scale_y)
        x2 = int(max(self.start_pos[0], self.end_pos[0]) * scale_x)
        y2 = int(max(self.start_pos[1], self.end_pos[1]) * scale_y)

        # Sınırları kontrol et
        x1 = max(0, min(x1, img_w))
        y1 = max(0, min(y1, img_h))
        x2 = max(0, min(x2, img_w))
        y2 = max(0, min(y2, img_h))

        # ROI'yi kaydet
        self.roi_coords = (x1, y1, x2, y2)
        self.roi_image = self.original_image[y1:y2, x1:x2].copy()

    def export_roi(self):
        """ROI'yi dışa aktarır"""
        if self.roi_image is not None:
            cv2.imwrite("assets/roi.jpg", self.roi_image)
            print(f"ROI kaydedildi. Koordinatlar: {self.roi_coords}")
            return self.roi_image, self.roi_coords
        return None, None

