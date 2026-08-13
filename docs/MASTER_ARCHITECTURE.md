# Matbaa Yönetim Sistemi — Master Mimari v0.1

## 1. Sistem mimarisi
Başlangıç mimarisi **modüler monolit + offline-first mobil istemci** olacaktır. Tek API ve tek PostgreSQL veritabanı işletme maliyetini düşük tutar; domain modülleri kod içinde kesin sınırlarla ayrılır. Erken mikroservis kullanılmaz. Dosya, bildirim, raporlama ve makine telemetrisi ileride ayrı servise çıkarılabilecek sözleşmelerle tasarlanır.

Katmanlar: Flutter istemci -> API/uygulama servisleri -> domain kuralları -> repository/Prisma -> PostgreSQL. Dosyalar nesne depolamada, cihaz önbelleği yerel veritabanında tutulur. Komuta Merkezi ve raporlar için işlem tablolarından ayrı okuma modelleri/projection kullanılır.

## 2. Ana modüller
Kullanıcı arayüzünde 9 ana iş alanı vardır: Platform, Ticari, Ürün Mühendisliği, Üretim, Kalite, Varlık Yönetimi, Tedarik Zinciri, Maliyet, Yönetim. Bu gruplama 40 ayrı menü yerine iş akışını temel alır.

## 3. Alt modüller
Platform: kullanıcı, rol/yetki, sistem ayarları, sözlükler, audit, cihaz/sync, dosya, bildirim.
Ticari: müşteri, teklif, sipariş.
Ürün: ürün revizyonu, teknik özellikler, rota/reçete, teknik dosyalar.
Üretim: iş emri, planlama, vardiya, makine atama, canlı üretim, duruş, fire, paketleme.
Kalite: kontrol şablonu, kontrol planı, kontrol sonucu, uygunsuzluk, müşteri şikayeti.
Varlık: makine, sayaç, arıza, bakım planı, bakım emri, yedek parça.
Tedarik: malzeme, depo/raf/lot, stok hareketi, rezervasyon, tedarikçi, satın alma, mal kabul, sevkiyat.
Maliyet: tahmini maliyet, gerçekleşen maliyet, fark analizi.
Yönetim: Komuta Merkezi, KPI/OEE, raporlar, karar destek.

## 4. Modüller arası veri akışı
Müşteri -> Sipariş -> İş Emri -> Ürün Revizyonu -> Üretim Rotası -> Plan -> Operasyon Emri -> Makine + Personel -> Üretim Olayları -> Kalite + Fire + Duruş -> Paketleme -> Sevkiyat -> Maliyet Kapanışı.

Stok iş emrinde rezervasyon oluşturur; üretim tüketimleri stok hareketine dönüşür. Arıza üretimi durdurabilir; kullanılan parça stoktan düşer. Kalite onayı sevkiyat kapısıdır. Tüm kritik hareketler audit ve bildirim motoruna olay üretir.

## 5. Kullanıcı rolleri
Sistem yöneticisi, fabrika müdürü, üretim müdürü, vardiya amiri, planlama, operatör, operatör yardımcısı, kalite, bakım, depo, satın alma, sevkiyat, muhasebe ve izleyici başlangıç rol setidir. Roller sabit kod değildir; yönetici yeni rol oluşturabilir.

## 6. Yetki modeli
RBAC + bağlamsal iş kuralı kullanılır. Yetki kodu `modul.eylem` biçimindedir: `production.start`, `quality.approve`, `shipment.complete`, `audit.read` gibi. Rol yalnızca yetki paketidir. Örneğin kullanıcıda `shipment.complete` olsa bile kalite onayı yoksa domain kuralı sevkiyatı engeller. Silme, düzeltme, onay ve geri alma ayrı izinlerdir.

## 7. Veritabanı tabloları
Platform: organization, facility, user, role, permission, user_role, role_permission, app_setting, system_dictionary, system_dictionary_item, audit_log, device, sync_mutation, notification_rule, notification, file_asset, entity_file.
İnsan: employee, employee_skill, machine_qualification, training, certificate, leave_record, absence_record, shift_definition, shift_instance, shift_assignment, shift_handover.
Ticari/ürün: customer, customer_contact, customer_instruction, quotation, sales_order, sales_order_line, product, product_revision, product_attribute, production_route, route_operation, work_order.
Üretim: production_plan, plan_operation, production_run, production_event, production_counter, downtime_event, downtime_reason, scrap_event, scrap_reason, operation_assignment.
Kalite: quality_template, quality_template_field, quality_rule, quality_inspection, quality_result, nonconformance, nonconformance_action, approval.
Varlık: machine, machine_capability, machine_state_event, meter_reading, maintenance_plan, maintenance_work_order, breakdown, breakdown_action, spare_part, machine_spare_part, maintenance_part_usage.
Tedarik: warehouse, bin_location, material, inventory_lot, stock_movement, stock_reservation, supplier, purchase_request, purchase_request_line, purchase_order, goods_receipt.
Sevkiyat/maliyet: packing_unit, shipment, shipment_line, shipment_check, estimated_cost, actual_cost, cost_line.
Yönetim: kpi_snapshot, oee_snapshot, command_center_projection, decision_suggestion, report_job.

## 8. Tablo ilişkileri
Business tabloları `organization_id` ile kuruma bağlanır. Sipariş satırı ürün revizyonuna, iş emri sipariş satırına ve üretim rotasına bağlıdır. Her üretim operasyonu iş emri ve rota operasyonuna, çalışma kaydı makine/vardiya/personel atamalarına bağlıdır. Fire, duruş ve kalite kayıtları üretim run/operation ile ilişkilidir. Serbest metinle makine/personel/müşteri adı saklanmaz; FK kullanılır. Ana kayıtlar hard-delete edilmez, pasifleştirilir.

## 9. Komuta Merkezi tasarımı
İlk 5 saniye kuralı için üç seviye kullanılır: üstte Kritik Uyarılar ve gecikme riski; ortada aktif vardiya/üretim/makine durumu; altta hedef-gerçekleşen, fire, kalite, bakım, stok ve sevkiyat. Kart sayısı role göre değişir. Operatör tüm fabrikayı değil kendi makine/işini; amir vardiyayı; müdür fabrikayı görür. Ayrıntı karta dokununca açılır.

## 10. Menü yapısı
Ana: Komuta Merkezi.
İş Akışı: Siparişler, İş Emirleri, Planlama, Üretim.
Operasyon: Kalite, Bakım, Stok & Satın Alma, Sevkiyat.
Kayıtlar: Müşteriler, Ürünler, Personel, Makineler, Malzemeler & Parçalar.
Yönetim: Raporlar & KPI, Görevler/Bildirimler, Sistem Ayarları.
Rolün yetkisi olmayan menü hiç gösterilmez. QR ve global arama her ekrandan erişilir.

## 11. Üretim iş akışı
Planlanan operasyon -> ön koşul kontrolü -> makine/personel/malzeme doğrulama -> hazırlık başlat -> ilk ürün kalite onayı -> üretim başlat -> sayaç/fire/duruş/ara kalite olayları -> üretim bitir -> zorunlu kontrol kapanışı -> operasyon tamamla -> sonraki rota adımı. Durum değişiklikleri state machine dışından değiştirilemez.

## 12. Siparişten sevkiyata uçtan uca süreç
Teklif kabulü -> sipariş -> ürün/revizyon seçimi -> benzersiz iş emri -> rota oluşturma -> malzeme uygunluk ve rezervasyon -> kapasite planı -> üretim operasyonları -> kalite kapıları -> paketleme -> sevk kontrol listesi -> sevkiyat -> maliyet kapanışı -> sipariş tamamlandı. Her adımın sorumlusu, zamanı ve onayı kaydedilir.

## 13. Kritik iş kuralları
Kalite onayı olmadan sevkiyat yok. Bakım/arıza durumundaki makinede üretim yok. Aynı makinede iki aktif üretim yok. Yetkinliği olmayan personele kritik makine başlatma yok veya yetkili override gerekir. Negatif kritik stok politikaya göre engel/uyarıdır. Zorunlu kalite kontrolü eksikken operasyon kapanmaz. Aynı personelde çakışan vardiya engellenir. Onaylanmış kaydın doğrudan silinmesi yasaktır.

## 14. Hata önleme mekanizmaları
Form seviyesinde doğrulama + domain kuralı + DB constraint birlikte kullanılır. Kritik butonlar bağlama göre aktif olur. Ön koşullar ekranda “neden yapılamıyor” mesajıyla gösterilir. QR ile yanlış iş/makine seçimi azaltılır. Tolerans alanları otomatik değerlendirilir. Tekrarlanan arıza/fire için eşik uyarıları üretilir. Kritik override işleminde neden ve yetkili kimliği zorunludur.

## 15. Offline çalışma mimarisi
Mobil uygulama yerel veriyi birincil çalışma kaynağı gibi kullanır; repository yerel ve uzak kaynağı birleştirir. Her offline yazma `clientMutationId`, `deviceId`, `entityId`, `operation`, `baseVersion`, `occurredAt`, `payload` ile sync kuyruğuna alınır. Sunucu idempotent işler. Sayaç/fire/duruş gibi kayıtlar append-only olay olduğu için birleştirilir. Ana kayıt çakışmasında optimistic concurrency kullanılır; aynı alan değişmişse otomatik ezme yerine conflict kuyruğuna alınır. Kullanıcı senkronizasyon durumunu görür.

## 16. Teknoloji yığını
Mobil/tablet: Flutter, Riverpod, go_router; Faz 2’de yerel SQLite/Drift.
API: Node.js 22 LTS çizgisi + NestJS 11 + TypeScript.
Veri: PostgreSQL 18, Prisma 7 migration/client.
Gerçek zamanlı: ilk aşamada SSE/WebSocket yalnızca canlı panellerde; CRUD için REST `/api/v1`.
Dosya: S3 uyumlu nesne depolama.
Queue/cache: başlangıçta zorunlu değil; ölçek gerektirdiğinde Redis/BullMQ.
Observability: yapılandırılmış log, correlation id, health endpoint, hata izleme.

## 17. Android APK stratejisi
Tek Flutter kod tabanı telefon/tablet için responsive tasarlanır. `dev`, `staging`, `prod` flavor kullanılır. APK doğrudan kurum cihazlarına dağıtılabilir; üretim için `flutter build apk --split-per-abi` veya kurum politikasına göre tek fat APK üretilebilir. İmza anahtarı GitHub Secrets/CI ortamında tutulur, repoya konmaz. Sürüm `major.minor.patch+build` şeklindedir.

## 18. Yedekleme stratejisi
PostgreSQL için günlük otomatik logical backup + periyodik fiziksel/snapshot yedek. Yedekler uygulama sunucusundan ayrı depoda, şifreli ve retention politikasıyla tutulur. Yönetim panelindeki “yedek oluştur” yalnızca sunucu tarafında job başlatır. Geri yükleme yüksek riskli yetkidir; önce doğrulama, sonra bakım modu ve audit gerekir. Dosya deposu ayrıca versiyonlama/lifecycle ile korunur. Düzenli restore testi yapılmadan yedek “başarılı” sayılmaz.

## 19. Güvenlik mimarisi
TLS, kısa ömürlü access token + güvenli refresh token, cihaz kaydı, parola hash, brute-force rate limit, merkezi permission guard, input validation, dosya tipi/boyut kontrolü, audit, secret yönetimi, DB en az yetki ilkesi. Organizasyon izolasyonu her sorguda scope ile zorunludur; gerekirse PostgreSQL RLS ikinci savunma katmanı olur. Hassas loglara parola/token yazılmaz. Kritik işlemlerde yeniden doğrulama/ikinci onay politikası eklenebilir.

## 20. Geliştirme fazları
Faz 1 Platform çekirdeği; Faz 2 ana kayıtlar; Faz 3 sipariş/iş emri; Faz 4 üretim; Faz 5 kalite/fire; Faz 6 bakım/arıza; Faz 7 stok/satın alma; Faz 8 maliyet/sevkiyat; Faz 9 KPI/rapor; Faz 10 karar destek. Her faz migration, test, lint/typecheck/build ve geri uyumluluk kontrolüyle kapanır.

# Sadeleştirme değerlendirmesi
- **Duruş + Fire + Canlı Üretim** ayrı ana menüler değil, Üretim altında olay türleri olmalı.
- **Arıza + Bakım + Makine geçmişi + Parça kullanımı** Varlık Yönetimi altında birleşmeli.
- **Stok + Yedek Parça stoğu + Satın Alma** tek Tedarik Zinciri verisi kullanmalı; parça kataloğu Varlık tarafında görünür ama stok hareketi tek stok motorundan gelir.
- **Kalite kontrol + uygunsuzluk + müşteri şikayeti** Kalite alanında tek kalite geçmişi oluşturmalı.
- **KPI + OEE + raporlar** Yönetim altında birleşmeli; OEE ayrı uygulama bölümü olmamalı.
- **Vardiya amiri paneli** yeni veri üretmez; Komuta Merkezi’nin role özel görünümüdür.
- **Görevler ve bildirimler** iki ayrı ana sistem yerine ortak “Aksiyon Merkezi” görünümünde sunulabilir; görev kalıcı sorumluluk, bildirim ise olaydır.
- **Doküman yönetimi** bağımsız dosya dolabı olmaktan çok her kayda bağlanan merkezi dosya servisi olmalıdır.
