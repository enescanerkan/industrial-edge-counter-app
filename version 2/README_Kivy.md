# Kivy Application Setup and Logs Guide

## System Requirements
- Python 3.12.3
- Kivy 2.3.0
- OpenGL compatible graphics card (Currently running on Intel UHD Graphics)

## Dependencies
The application requires the following Kivy dependencies:
- kivy_deps.angle (0.4.0)
- kivy_deps.glew (0.3.1)
- kivy_deps.sdl2 (0.7.0)

## Installation
1. Create a virtual environment (recommended)
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

2. Install required packages
```bash
pip install kivy==2.3.0
```

## Understanding Application Logs

### Log File Location
The application logs are stored at:
```
C:\Users\[Username]\.kivy\logs\kivy_[date].txt
```

### Common Log Messages Explained

#### 1. Initialization Messages
```
[INFO] [Logger] Record log in ...
[INFO] [Kivy] v2.3.0
```
These messages indicate successful initialization of the Kivy framework.

#### 2. Graphics System Information
```
[INFO] [GL] Using the "OpenGL" graphics system
[INFO] [GL] OpenGL version <4.6.0>
```
Indicates the graphics system being used by your application.

#### 3. ROI (Region of Interest) Messages
When you see:
```
ROI kaydedildi. Koordinatlar: (0, 16, 500, 286)
```
This indicates successful saving of a selected region in your application.

### Known Warnings

#### Deprecated Properties Warning
```
[WARNING] Deprecated property "allow_stretch"
[WARNING] Deprecated property "keep_ratio"
```
**Solution**: Update these properties to their newer equivalents in future versions.

## Troubleshooting

### Common Issues and Solutions

1. **OpenGL Related Errors**
   - Ensure your graphics drivers are up to date
   - Check if your GPU supports OpenGL 2.0 or later

2. **Font Loading Issues**
   - Font debug messages are normal during startup
   - No action needed unless you see specific font-related errors

### Debug Mode
To run the application in debug mode:
```python
from kivy.logger import Logger
Logger.setLevel('DEBUG')
```

## Additional Notes

- The application uses matplotlib for certain visualizations
- Various system fonts are automatically detected and loaded
- The application window supports stretching and ratio keeping (though these properties are marked for deprecation)

## Future Updates Needed

1. Update deprecated properties:
   - `allow_stretch`
   - `keep_ratio`

## Support

For issues and questions:
1. Check the Kivy logs at `C:\Users\[Username]\.kivy\logs\`
2. Ensure all dependencies are correctly installed
3. Update graphics drivers if experiencing display issues

---

*Note: This README is based on the application logs and may need updates based on specific application features and requirements.*
------------------------------------------------------------------------------------------
# TÜRKÇESİ :


# Kivy Uygulama Kurulumu ve Log Kılavuzu  
## Sistem Gereksinimleri  
- Python 3.12.3  
- Kivy 2.3.0  
- OpenGL uyumlu bir grafik kartı (Şu an Intel UHD Graphics üzerinde çalışıyor)  
## Bağımlılıklar  
Uygulama, aşağıdaki Kivy bağımlılıklarını gerektirir:  
- `kivy_deps.angle (0.4.0)`  
- `kivy_deps.glew (0.3.1)`  
- `kivy_deps.sdl2 (0.7.0)`  
## Kurulum  
1. Sanal bir ortam oluşturun (önerilir):  
   ```bash  
   python -m venv .venv  
   source .venv/bin/activate  # Windows için: .venv\Scripts\activate  
   ```  
2. Gerekli paketleri yükleyin:  
   ```bash  
   pip install kivy==2.3.0  
   ```  
## Uygulama Loglarının Anlaşılması  
### Log Dosyasının Konumu  
Uygulama logları şu dizinde saklanır:  
```
C:\Users\[KullanıcıAdı]\.kivy\logs\kivy_[tarih].txt  
```  
### Sık Karşılaşılan Log Mesajlarının Açıklamaları  
#### 1. Başlangıç Mesajları  
```
[INFO] [Logger] Record log in ...  
[INFO] [Kivy] v2.3.0  
```  
Bu mesajlar, Kivy framework'ünün başarılı bir şekilde başlatıldığını gösterir.  
#### 2. Grafik Sistemi Bilgileri  
```
[INFO] [GL] Using the "OpenGL" graphics system  
[INFO] [GL] OpenGL version <4.6.0>  
```  
Uygulamanın kullandığı grafik sistemini belirtir.  
#### 3. ROI (İlgi Bölgesi) Mesajları  
Şu mesajı görüyorsanız:  
```
ROI kaydedildi. Koordinatlar: (0, 16, 500, 286)  
```  
Bu, uygulamada seçilen bir bölgenin başarıyla kaydedildiğini gösterir.  
### Bilinen Uyarılar  
#### Kullanımdan Kalkan Özellikler Uyarısı  
```
[WARNING] Deprecated property "allow_stretch"  
[WARNING] Deprecated property "keep_ratio"  
```  
**Çözüm**: Bu özellikleri gelecekteki sürümlerde daha yeni eşdeğerleri ile değiştirin.  
## Sorun Giderme  
### Yaygın Sorunlar ve Çözümleri  
1. **OpenGL ile İlgili Hatalar**  
   - Grafik sürücülerinizin güncel olduğundan emin olun.  
   - GPU’nuzun OpenGL 2.0 veya daha sonraki sürümleri desteklediğini kontrol edin.  
2. **Font Yükleme Sorunları**  
   - Başlangıç sırasında font hata mesajları normaldir.  
   - Fontlarla ilgili özel bir hata görmüyorsanız işlem yapmanıza gerek yoktur.  
### Hata Ayıklama Modu  
Uygulamayı hata ayıklama modunda çalıştırmak için:  
   ```python  
   from kivy.logger import Logger  
   Logger.setLevel('DEBUG')  
   ```  
## Ek Notlar  
- Uygulama, bazı görselleştirmeler için `matplotlib` kullanır.  
- Çeşitli sistem fontları otomatik olarak algılanır ve yüklenir.  
- Uygulama penceresi, esnetme ve oran koruma özelliklerini destekler (ancak bu özellikler kullanım dışı bırakılacak olarak işaretlenmiştir).  
## Gelecek Güncellemeler  
1. Kullanımdan kalkan özelliklerin güncellenmesi:  
   - `allow_stretch`  
   - `keep_ratio`  
## Destek  
Sorunlar ve sorular için:  
1. Kivy loglarını şu dizinde kontrol edin: `C:\Users\[KullanıcıAdı]\.kivy\logs\`  
2. Tüm bağımlılıkların doğru şekilde yüklendiğinden emin olun.  
3. Görüntü sorunları yaşıyorsanız grafik sürücülerinizi güncelleyin.  

