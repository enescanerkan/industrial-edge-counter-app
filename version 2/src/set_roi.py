# set_roi.py → 22.11.2024
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.image import Image
import cv2
import numpy as np


class ROICanvas(Widget):
    """ROI (Region of Interest) seçimi için canvas widget'ı"""
    width = NumericProperty(0)
    height = NumericProperty(0)

    def __init__(self, original_image=None, **kwargs):
        super().__init__(**kwargs)
        self.original_image = original_image
        self.start_pos = None
        self.end_pos = None
        self.roi_image = None
        self.roi_coords = None

        # Display parameters
        self.display_ratio = 1.0
        self.display_offset = (0, 0)

        # Canvas'ı güncelle
        self.bind(size=self._update_rect, pos=self._update_rect)
        self.setup_display_parameters()

    def _update_rect(self, *args):
        """Canvas boyutlarını güncelle"""
        self.width = self.size[0]
        self.height = self.size[1]
        self.setup_display_parameters()

    def setup_display_parameters(self):
        """Görüntü gösterim parametrelerini hesaplar"""
        if self.original_image is None:
            return

        img_h, img_w = self.original_image.shape[:2]
        widget_ratio = self.width / self.height
        image_ratio = img_w / img_h

        if widget_ratio > image_ratio:
            # Widget daha geniş, yüksekliğe göre ölçekle
            self.display_ratio = self.height / img_h
            scaled_width = img_w * self.display_ratio
            self.display_offset = ((self.width - scaled_width) / 2, 0)
        else:
            # Widget daha dar, genişliğe göre ölçekle
            self.display_ratio = self.width / img_w
            scaled_height = img_h * self.display_ratio
            self.display_offset = (0, (self.height - scaled_height) / 2)

    def get_image_coordinates(self, widget_x, widget_y):
        """Widget koordinatlarını görüntü koordinatlarına dönüştürür"""
        if self.original_image is None:
            return 0, 0

        img_h, img_w = self.original_image.shape[:2]

        # Offset'i çıkar
        rel_x = widget_x - self.display_offset[0]
        rel_y = widget_y - self.display_offset[1]

        # Ölçeklendirmeyi uygula
        img_x = rel_x / self.display_ratio
        img_y = img_h - (rel_y / self.display_ratio)  # Y koordinatını çevir

        # Sınırları kontrol et
        img_x = max(0, min(img_x, img_w))
        img_y = max(0, min(img_y, img_h))

        return int(img_x), int(img_y)

    def get_widget_coordinates(self, img_x, img_y):
        """Görüntü koordinatlarını widget koordinatlarına dönüştürür"""
        if self.original_image is None:
            return 0, 0

        img_h, img_w = self.original_image.shape[:2]

        # Ölçeklendirme ve çevirme uygula
        widget_x = (img_x * self.display_ratio) + self.display_offset[0]
        widget_y = self.height - ((img_h - img_y) * self.display_ratio) - self.display_offset[1]

        return widget_x, widget_y

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
        if not self.start_pos or self.original_image is None:
            return

        self.end_pos = touch.pos

        # Başlangıç ve bitiş koordinatlarını görüntü koordinatlarına dönüştür
        x1, y1 = self.get_image_coordinates(
            min(self.start_pos[0], self.end_pos[0]),
            max(self.start_pos[1], self.end_pos[1])
        )
        x2, y2 = self.get_image_coordinates(
            max(self.start_pos[0], self.end_pos[0]),
            min(self.start_pos[1], self.end_pos[1])
        )

        # Y koordinatlarını sırala
        if y1 > y2:
            y1, y2 = y2, y1

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