# main.py → 20.11.2024
from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics.texture import Texture
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.metrics import dp
import cv2
import os
import math
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

from set_roi import ROICanvas
from set_filters import EnhancedGaborDetector


class ImageProcessor:
    """Görüntü işleme yardımcı sınıfı"""

    @staticmethod
    def convert_to_texture(image):
        """OpenCV görüntüsünü Kivy texture'una dönüştürür"""
        if image is None:
            return None

        if len(image.shape) == 2:  # Gri tonlamalı
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        else:  # BGR
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        image_flipped = cv2.flip(image, 0)
        buffer = image_flipped.tobytes()
        texture = Texture.create(size=(image.shape[1], image.shape[0]), colorfmt='rgb')
        texture.blit_buffer(buffer, colorfmt='rgb', bufferfmt='ubyte')
        return texture


class ImageView(Image):
    """Özelleştirilmiş görüntü widget'ı"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.allow_stretch = True
        self.keep_ratio = True


class AnalysisLayout(BoxLayout):
    """Analiz sonuçlarını gösteren layout"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_x = 0.3
        self.padding = dp(10)
        self.spacing = dp(10)

        # Başlık
        self.add_widget(Label(
            text='Analiz Sonuçları',
            size_hint_y=None,
            height=dp(40),
            bold=True
        ))

        # Kenar sayısı etiketi
        self.edge_count_label = Label(
            text='Kenar Sayısı: -',
            size_hint_y=None,
            height=dp(30)
        )
        self.add_widget(self.edge_count_label)

        # ROI boyutları etiketi
        self.roi_size_label = Label(
            text='ROI Boyutları: -',
            size_hint_y=None,
            height=dp(30)
        )
        self.add_widget(self.roi_size_label)

        # Grafik gösterimi için buton
        self.plot_button = Button(
            text='Analiz',
            size_hint_y=None,
            height=dp(40)
        )
        self.add_widget(self.plot_button)


class ROILayout(FloatLayout):
    """ROI seçimi için özel layout"""

    def __init__(self, original_image, **kwargs):
        super().__init__(**kwargs)
        self.original_image = original_image

        # Görüntüyü göster
        self.image = ImageView(texture=ImageProcessor.convert_to_texture(original_image))
        self.add_widget(self.image)

        # ROI canvas'ı ekle
        self.roi_canvas = ROICanvas(original_image=original_image)
        self.add_widget(self.roi_canvas)


class MainTabs(TabbedPanel):
    """Ana uygulama arayüzü"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_default_tab = False

        # Orijinal görüntüyü yükle
        self.original_image = cv2.imread("assets/4.jpg")
        if self.original_image is None:
            raise ValueError("Görüntü yüklenemedi!")

        # Görüntü texture'unu oluştur
        self.image_texture = ImageProcessor.convert_to_texture(self.original_image)

        # Analiz sonuçlarını saklamak için
        self.current_analysis = None

        # Sekmeleri oluştur
        self.home_tab = None
        self.setup_home_tab()
        self.setup_roi_tab()
        self.setup_process_tab()

        # Varsayılan sekme
        self.default_tab = self.home_tab

    def setup_home_tab(self):
        """Ana sayfa sekmesini oluşturur"""
        tab = TabbedPanelItem(text='Ana Sayfa')
        layout = BoxLayout(orientation='vertical')
        image = ImageView(texture=self.image_texture)
        layout.add_widget(image)
        tab.content = layout
        self.home_tab = tab
        self.add_widget(tab)

    def setup_roi_tab(self):
        """ROI seçim sekmesini oluşturur"""
        tab = TabbedPanelItem(text='ROI Seçimi')
        layout = BoxLayout(orientation='vertical')
        roi_layout = ROILayout(self.original_image)
        layout.add_widget(roi_layout)

        save_btn = Button(
            text='ROI Kaydet',
            size_hint=(0, 0),
            on_press=self.save_roi
        )
        layout.add_widget(save_btn)

        self.roi_canvas = roi_layout.roi_canvas
        tab.content = layout
        self.add_widget(tab)


    def setup_process_tab(self):
        """İşleme sekmesini oluşturur"""
        tab = TabbedPanelItem(text='Görüntü İşleme')
        main_layout = BoxLayout(orientation='horizontal')

        # Sol taraf - görüntüler
        images_layout = BoxLayout(orientation='horizontal', size_hint_x=0.7)
        self.original_view = ImageView(texture=self.image_texture)
        self.processed_view = ImageView()
        images_layout.add_widget(self.original_view)
        images_layout.add_widget(self.processed_view)
        main_layout.add_widget(images_layout)

        # Sağ taraf - kontroller ve analiz
        controls_layout = BoxLayout(orientation='vertical', size_hint_x=0.3, padding=10, spacing=10)

        # İşlem butonu
        process_btn = Button(
            text='İşle ve Analiz Et',
            size_hint_y=None,
            height=dp(40),
            on_press=self.process_and_analyze_roi
        )
        controls_layout.add_widget(process_btn)

        # Analiz sonuçları için layout
        self.analysis_layout = AnalysisLayout()
        self.analysis_layout.plot_button.bind(on_press=self.show_detailed_analysis)
        controls_layout.add_widget(self.analysis_layout)

        main_layout.add_widget(controls_layout)
        tab.content = main_layout
        self.add_widget(tab)

    def save_roi(self, instance):
        """ROI'yi kaydeder"""
        roi_image, roi_coords = self.roi_canvas.export_roi()
        if roi_image is not None:
            self.show_info_popup("ROI başarıyla kaydedildi")
        else:
            self.show_error_popup("ROI seçilmedi")

    def process_and_analyze_roi(self, instance):
        """ROI'yi işler ve analiz eder"""
        roi_path = 'assets/roi.jpg'
        if not os.path.exists(roi_path):
            self.show_error_popup("Önce ROI seçin")
            return

        try:
            # Görüntü işleme
            detector = EnhancedGaborDetector(roi_path)
            processed_image = detector.process_image()

            # Canny kenar tespiti
            edges = cv2.Canny(processed_image, 50, 150)

            # Dikey çizgi analizi
            height, width = edges.shape
            vertical_line_x = width // 2
            vertical_edge_count = np.sum(edges[:, vertical_line_x] > 0)
            edge_count = math.ceil(vertical_edge_count / 2)

            # Analiz sonuçlarını sakla
            self.current_analysis = {
                'detector': detector,
                'processed_image': processed_image,
                'edges': edges,
                'edge_count': edge_count,
                'roi_size': (width, height)
            }

            # Sonuçları göster
            self.processed_view.texture = ImageProcessor.convert_to_texture(processed_image)
            self.analysis_layout.edge_count_label.text = f'Kenar Sayısı: {edge_count}'
            self.analysis_layout.roi_size_label.text = f'ROI Boyutları: {width}x{height}'

        except Exception as e:
            self.show_error_popup(f"İşlem hatası: {str(e)}")

    def show_detailed_analysis(self, instance):
        if self.current_analysis is None:
            self.show_error_popup("Önce görüntü işleme yapın")
            return

        try:
            # Matplotlib figure oluştur
            plt.figure(figsize=(18, 6))

            # Orijinal görüntü - ilk görüntü için ROI öncesi tam görüntüyü göster
            plt.subplot(1, 5, 1)
            plt.title("Orijinal Görüntü")
            original_full_image = self.original_image  # Tam orijinal görüntüyü yükle
            plt.imshow(cv2.cvtColor(original_full_image, cv2.COLOR_BGR2RGB))
            plt.axis("off")

            # ROI
            plt.subplot(1, 5, 2)
            plt.title("Seçilen ROI")
            plt.imshow(cv2.cvtColor(self.current_analysis['detector'].original_image, cv2.COLOR_BGR2RGB))
            plt.axis("off")

            # İşlenmiş ROI
            plt.subplot(1, 5, 3)
            plt.title("İşlenmiş ROI")
            plt.imshow(self.current_analysis['processed_image'], cmap="gray")
            plt.axis("off")

            # Canny kenarları
            plt.subplot(1, 5, 4)
            plt.title("Kenar Tespiti")
            plt.imshow(self.current_analysis['edges'], cmap="gray")
            plt.axis("off")

            # Kenar sayımı
            edges_with_line = self.current_analysis['edges'].copy()
            height, width = edges_with_line.shape
            vertical_line_x = width // 2
            cv2.line(edges_with_line, (vertical_line_x, 0), (vertical_line_x, height), 255, 1)

            plt.subplot(1, 5, 5)
            plt.title(f"Kenar Sayımı\n{self.current_analysis['edge_count']} kenar")
            plt.imshow(edges_with_line, cmap="gray")
            plt.axis("off")

            plt.tight_layout()

            # Matplotlib figure'ı bir popup'ta göster
            self.show_plot_popup()

        except Exception as e:
            self.show_error_popup(f"Grafik oluşturma hatası: {str(e)}")

    def show_plot_popup(self):
        """Matplotlib grafiğini popup'ta gösterir"""
        # Matplotlib figure'ı bytesa dönüştür
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        plt.close()
        buf.seek(0)

        # Bytes'ı texture'a dönüştür
        img = ImageView(
            size_hint=(1, 1),
            allow_stretch=True,
            keep_ratio=True
        )
        img.texture = ImageProcessor.convert_to_texture(cv2.imdecode(
            np.frombuffer(buf.read(), np.uint8),
            cv2.IMREAD_COLOR
        ))

        # Popup oluştur ve göster
        popup = Popup(
            title='Detaylı Analiz',
            content=img,
            size_hint=(0.9, 0.9)
        )
        popup.open()

    def show_error_popup(self, message):
        """Hata popup'ı gösterir"""
        Popup(
            title='Hata',
            content=Button(text=message),
            size_hint=(0.8, 0.4)
        ).open()

    def show_info_popup(self, message):
        """Bilgi popup'ı gösterir"""
        Popup(
            title='Bilgi',
            content=Button(text=message),
            size_hint=(0.8, 0.4)
        ).open()


class MainApp(App):
    def build(self):
        return MainTabs()


if __name__ == '__main__':
    MainApp().run()