# Industrial Metal Sheet Edge Counter (Endüstriyel Metal Sac Kenar Sayım Uygulaması)

## A desktop application developed with Python Kivy for analyzing and counting edges in industrial metal sheets (Python Kivy ile geliştirilmiş, endüstriyel metal sacların kenarlarını analiz eden ve sayan masaüstü uygulaması). The application provides precise ROI (Region of Interest) selection and advanced image processing capabilities using Gabor filters (Uygulama, hassas ROI (İlgi Bölgesi) seçimi ve Gabor filtreleri kullanarak gelişmiş görüntü işleme yetenekleri sunar).

## Features (Özellikler)

### ROI Selection (ROI Seçimi)
- Precise coordinate mapping for accurate edge detection (Hassas kenar tespiti için doğru koordinat eşleme)
- Interactive region selection on the image (Görüntü üzerinde interaktif bölge seçimi)
- Real-time visual feedback (Gerçek zamanlı görsel geri bildirim)

### Image Processing (Görüntü İşleme)
- CLAHE (Contrast Limited Adaptive Histogram Equalization)
- Gaussian Blur (Gaussian Bulanıklaştırma)
- Bilateral Filter (İkili Filtre)
- Gabor Filter (Gabor Filtresi)
- Morphological Operations (Morfolojik İşlemler)

### Analysis (Analiz)
- Metal sheet edge detection and counting (Metal sac kenar tespiti ve sayımı)
- Detailed visual analysis (Detaylı görsel analiz)
- Multiple view comparisons (Çoklu görünüm karşılaştırmaları)
- Performance metrics (Performans metrikleri)-(Eklenebilir)

## Demo Videos (Demo Videoları)

https://github.com/user-attachments/assets/a9c5c428-bb23-4681-beb9-eae2df93801f

https://github.com/user-attachments/assets/4c356446-d3fe-4845-a245-1b3acb0428b0

https://github.com/user-attachments/assets/32ca9c8d-5802-4397-b052-bbb38e398da7


## Requirements (Gereklilikler)

- Python 3.x
- Kivy
- OpenCV
- NumPy
- Matplotlib

## Project Structure (Proje Yapısı)

```
├── assets/                 # Image assets (Görüntü dosyaları)
│   ├── 1.jpg
│   ├── 2.jpg
│   └── 3.jpg
├── src/                   # Source code (Kaynak kod)
│   ├── main.py           # Main application file (Ana uygulama dosyası)
│   ├── set_roi.py        # ROI selection implementation (ROI seçim implementasyonu)
│   └── set_filters.py    # Image processing filters (Görüntü işleme filtreleri)
└── version2/             # Improved version (Geliştirilmiş versiyon)
    ├── assets/           # Image assets for version 2
    │   ├── 1.jpg
    │   ├── 2.jpg
    │   ├── 3.jpg
    │   └── 4.jpg
    └── src/             # Improved source code
        ├── main.py      # Enhanced UI and functionality
        ├── set_roi.py   # Fixed ROI coordinate mapping
        └── set_filters.py
```

## Version Differences (Versiyon Farkları)

### Version 1
- Basic implementation of metal sheet edge counting (Metal sac kenar sayımının temel implementasyonu)
- Initial ROI selection system (İlk ROI seçim sistemi)
- Basic UI design (Temel arayüz tasarımı)

### Version 2
- Improved ROI coordinate mapping (Geliştirilmiş ROI koordinat eşlemesi)
- Enhanced user interface (Geliştirilmiş kullanıcı arayüzü)
- More accurate edge detection (Daha hassas kenar tespiti)

## Getting Started (Başlangıç)

1. Clone the repository (Depoyu klonlayın)
```bash
git clone https://github.com/enescanerkan/industrial-edge-counter-app.git
```

2. Install dependencies (Bağımlılıkları yükleyin)
```bash
pip install -r requirements.txt
```

3. Run the application (Uygulamayı çalıştırın)
```bash
# For version 1 (Versiyon 1 için)
python src/main.py

# For version 2 (Versiyon 2 için)
python version2/src/main.py
```

## Usage (Kullanım)

1. Launch the application (Uygulamayı başlatın)
2. Load your metal sheet image (Metal sac görüntünüzü yükleyin)
3. Select ROI in the "ROI Selection" tab (ROI Seçimi sekmesinde bölge seçin)
4. Process the image in the "Image Processing" tab (Görüntü İşleme sekmesinde görüntüyü işleyin)
5. View detailed edge count analysis and results (Detaylı kenar sayımı analizi ve sonuçlarını görüntüleyin)
