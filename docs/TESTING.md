# Test ve Sürüm Akışı

## Günlük geliştirme
- Aktif geliştirme `develop` ve `agent/*` dallarında yürütülür.
- Her push ve pull request'te API lint/type-check/build/test çalışır.
- Flutter analyze ve widget testleri çalışır.
- Flutter web release build oluşturulur.
- Başarılı CI çalışmasında `matbaa-web-preview` artifact'i oluşur.

## Web test paketi
GitHub Actions > ilgili CI çalışması > Artifacts > `matbaa-web-preview` indirilir.
Paket yalnızca `index.html` dosyasından ibaret değildir; Flutter web çıktısındaki tüm dosyalar birlikte tutulmalıdır.

## APK
APK her commit'te üretilmez. Test edilebilir kilometre taşlarında veya final sürümde `Build Android APK` workflow'u manuel çalıştırılır.
Başarılı çalışmada `matbaa-android-apk` artifact'i oluşur.

## Kalite kapıları
Bir sürüm test edilebilir kabul edilmeden önce:
1. API lint başarılı olmalı.
2. API type-check başarılı olmalı.
3. API build başarılı olmalı.
4. API testleri başarılı olmalı.
5. Flutter analyze başarılı olmalı.
6. Flutter widget testleri başarılı olmalı.
7. Flutter web build başarılı olmalı.
8. APK kilometre taşı ise Android release build başarılı olmalı.
