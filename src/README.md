# Metal Blocks Image Processing Application
Bu uygulama, metal blokların kenar tespiti ve analizi için geliştirilmiş bir Kivy tabanlı görsel arayüz uygulamasıdır. Uygulama, Gabor filtresi ve çeşitli görüntü işleme teknikleri kullanarak metal bloklardaki kenarları tespit eder ve analiz eder.
Proje Yapısı
Proje üç ana Python dosyasından oluşmaktadır:

main.py: Ana uygulama ve kullanıcı arayüzü
set_filters: Görüntü işleme ve Gabor filtresi işlemleri
set_roi.py: ROI (İlgi Alanı) seçimi için gerekli fonksiyonlar

## Gereksinimler
* Python 3.x
* Kivy
* OpenCV (cv2)
* NumPy
* Matplotlib

## Modül Detayları
### * main.py

Ana uygulama modülü, kullanıcı arayüzünü ve temel işlevselliği sağlar.

#### Sınıflar:

#### ImageProcessor: Görüntü işleme yardımcı sınıfı

convert_to_texture(): OpenCV görüntülerini Kivy texture'larına dönüştürür


#### ImageView: Özelleştirilmiş görüntü widget'ı

Görüntüleri esnek ve orantılı şekilde gösterir


#### AnalysisLayout: Analiz sonuçlarını gösteren arayüz bileşeni

Kenar sayısı, ROI boyutları gibi analiz sonuçlarını gösterir
Detaylı analiz grafiklerini gösterme özelliği


#### ROILayout: ROI seçimi için özel arayüz

Orijinal görüntü üzerinde ROI seçimi yapılmasını sağlar


#### MainTabs: Ana uygulama arayüzü

Ana Sayfa, ROI Seçimi ve Görüntü İşleme sekmeleri
Görüntü işleme ve analiz fonksiyonları


#### MainApp: Kivy uygulaması ana sınıfı

### *  set_filters
Görüntü işleme ve filtreleme işlemlerini gerçekleştiren modül.
#### Sınıf: EnhancedGaborDetector
## Ana özellikler ve metodlar:

#### CLAHE uygulama
* Gaussian blur
* Adaptif eşikleme
* Bilateral filtreleme
* Gabor filtresi uygulama
* Morfolojik işlemler

### Önemli metodlar:

* process_image(): Tüm işlemleri sırayla uygular
* apply_roi(): Belirtilen koordinatlarla ROI alır
* get_result(): Son işlem sonucunu döndürür

### * set_roi.py
ROI seçimi için gerekli widget ve fonksiyonları içerir.
* Sınıf: ROICanvas
Özellikler:
* * Fare/dokunmatik girdi ile ROI seçimi
* * Seçilen alanı görsel olarak gösterme
* * Koordinat dönüşümleri
* * ROI'yi kaydetme

### Ana metodlar:

* on_touch_down(): Seçim başlangıcı
* on_touch_move(): Seçim alanı güncelleme
* on_touch_up(): Seçimi tamamlama
* export_roi(): Seçilen ROI'yi dışa aktarma

### Kullanım

* Ana sayfada orijinal görüntüyü görüntüleyin
ROI Seçimi sekmesinde analiz edilecek alanı seçin
Görüntü İşleme sekmesinde:

* "İşle ve Analiz Et" butonuna tıklayın
Sonuçları ve kenar sayısını görüntüleyin
Detaylı analiz için grafikleri inceleyin



### Çıktılar
* Uygulama şu çıktıları sağlar:

* İşlenmiş görüntü
Kenar sayısı
ROI boyutları
Detaylı analiz grafikleri (orijinal görüntü, ROI, işlenmiş görüntü, kenar tespiti)

# Notlar

* Görüntüler "assets" klasöründe saklanmalıdır
ROI seçimi yapılmadan işleme başlatılamaz
İşlem parametreleri set_filters.py içinde özelleştirilebilir.
