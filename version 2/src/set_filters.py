# set_filters.py → 20.11.2024
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math


class EnhancedGaborDetector:
    def __init__(self, image_path):
        self.original_image = cv2.imread(image_path, cv2.IMREAD_COLOR)  # Renkli olarak yükle
        if self.original_image is None:
            raise ValueError("Görüntü yüklenemedi")

        self.original_image_rgb = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)  # RGB'ye çevir
        self.image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)  # İşleme için gri tonlama
        self.filtered_image = None

    def apply_clahe(self, clip_limit=2.0, tile_grid_size=(8, 8)):
        """Görüntüye CLAHE uygular."""
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
        self.image = clahe.apply(self.image)
        return self.image

    def apply_blur(self, kernel_size=(7, 7)):
        """Görüntüye Gaussian blur uygular."""
        self.image = cv2.GaussianBlur(self.image, kernel_size, 0)
        return self.image

    def apply_adaptive_threshold(self, max_value=255, adaptive_method=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 threshold_type=cv2.THRESH_BINARY, block_size=21, C=1):
        """Adaptif eşikleme uygular."""
        self.image = cv2.adaptiveThreshold(
            self.image, max_value, adaptive_method, threshold_type, block_size, C
        )
        return self.image

    def apply_bilateral_filter(self, d=9, sigma_color=75, sigma_space=75):
        """Görüntüye bilateral filtre uygular."""
        self.image = cv2.bilateralFilter(self.image, d, sigma_color, sigma_space)
        return self.image

    def apply_gabor_filter(self, ksize=21, sigma=8.0, theta=np.pi / 4, lambd=10.0, gamma=0.5, psi=0):
        """Görüntüye Gabor filtresi uygular."""
        kernel = cv2.getGaborKernel(
            (ksize, ksize),
            sigma,
            theta,
            lambd,
            gamma,
            psi,
            ktype=cv2.CV_32F
        )
        self.filtered_image = cv2.filter2D(self.image, cv2.CV_8UC3, kernel)
        return self.filtered_image

    def apply_morphological_operations(self, erosion_kernel=3, erosion_iter=1,
                                       dilation_kernel=3, dilation_iter=1):
        """Erozyon ve genişletme işlemleri uygular."""
        kernel = np.ones((erosion_kernel, erosion_kernel), np.uint8)
        self.filtered_image = cv2.erode(self.filtered_image, kernel, iterations=erosion_iter)

        kernel = np.ones((dilation_kernel, dilation_kernel), np.uint8)
        self.filtered_image = cv2.dilate(self.filtered_image, kernel, iterations=dilation_iter)

        return self.filtered_image

    def process_image(self, clahe_params=None, blur_params=None, bilateral_params=None, gabor_params=None,
                      morphological_params=None):
        """Tüm işlemleri sırayla uygular."""
        # İşleme parametreleri
        default_clahe = {'clip_limit': 2.0, 'tile_grid_size': (8, 8)}
        default_blur = {'kernel_size': (11, 11)}
        default_bilateral = {'d': 9, 'sigma_color': 75, 'sigma_space': 75}
        default_gabor = {
            'ksize': 10,
            'sigma': 5.7,
            'theta': 2 * (np.pi) / 4,
            'lambd': 10.0,
            'gamma': 0.5,
            'psi': 0
        }
        default_morphological = {
            'erosion_kernel': 3,
            'erosion_iter': 1,
            'dilation_kernel': 5,
            'dilation_iter': 1
        }

        clahe_params = clahe_params or default_clahe
        blur_params = blur_params or default_blur
        bilateral_params = bilateral_params or default_bilateral
        gabor_params = gabor_params or default_gabor
        morphological_params = morphological_params or default_morphological

        # İşlem sırası
        self.apply_clahe(**clahe_params)
        self.apply_blur(**blur_params)
        self.apply_bilateral_filter(**bilateral_params)
        self.apply_gabor_filter(**gabor_params)
        self.apply_morphological_operations(**morphological_params)

        return self.filtered_image

    def get_result(self):
        """Son işlem sonucunu döndürür."""
        if self.filtered_image is None:
            raise ValueError("Henüz işlem yapılmadı")
        return self.filtered_image

    def apply_roi(self, roi_coordinates):
        """Belirtilen koordinatlarla ROI alır."""
        x1, y1, x2, y2 = roi_coordinates
        roi = self.original_image[y1:y2, x1:x2]
        return roi


def display_image_processing(image_path, roi_coordinates, canny_low=50, canny_high=150):
    detector = EnhancedGaborDetector(image_path)

    # ROI uygulama
    roi_image = detector.apply_roi(roi_coordinates)

    # ROI üzerinde filtre işlemlerini uygulama
    detector.image = cv2.cvtColor(roi_image, cv2.COLOR_BGR2GRAY)
    processed_roi = detector.process_image()

    # Canny Kenar Algılama
    edges = cv2.Canny(processed_roi, canny_low, canny_high)

    # Çizgi ve kenar sayma işlemleri
    image_height, image_width = edges.shape
    vertical_line_x = image_width // 2

    # Dikey çizgi çizimi
    edges_with_line = edges.copy()
    cv2.line(edges_with_line, (vertical_line_x, 0), (vertical_line_x, image_height), 255, 1)

    # Çizginin geçtiği kenarları sayma
    vertical_edge_count = np.sum(edges[:, vertical_line_x] > 0)

    # Matplotlib ile görselleştirme
    plt.figure(figsize=(18, 6))

    plt.subplot(1, 5, 1)
    plt.title("Orijinal Görüntü (Renkli)")
    plt.imshow(detector.original_image_rgb)
    plt.axis("off")

    plt.subplot(1, 5, 2)
    plt.title("Seçilen ROI (Orijinal Görüntü)")
    plt.imshow(cv2.cvtColor(roi_image, cv2.COLOR_BGR2RGB))
    plt.axis("off")

    plt.subplot(1, 5, 3)
    plt.title("İşlenmiş ROI (Gabor ve CLAHE)")
    plt.imshow(processed_roi, cmap="gray")
    plt.axis("off")

    plt.subplot(1, 5, 4)
    plt.title("Canny Uygulanan Görüntü")
    plt.imshow(edges, cmap="gray")
    plt.axis("off")

    plt.subplot(1, 5, 5)
    plt.title(f"Çizgi ve Kenar Sayımı\nKenar Sayısı: {math.ceil(vertical_edge_count / 2)}")
    plt.imshow(edges_with_line, cmap="gray")
    plt.axis("off")

    plt.tight_layout()
    plt.show()

# Bu scripti test etmek için :
# Filtre ayarından sonra
if __name__ == "__main__":
    image_path = "assets/1.jpg"
    roi_coordinates = (337, 386, 445, 1173)
    display_image_processing(image_path, roi_coordinates)