# Geliştirme fazları ve kabul kriterleri

## Faz 1 — Platform çekirdeği
Kullanıcı, rol/yetki, organizasyon, ayarlar, sözlükler, audit, cihaz/sync sözleşmesi. Kabul: yetkisiz işlem engellenir, ayar listeleri kod değişmeden genişletilir, kritik değişiklik auditlenir.

## Faz 2 — Ana kayıtlar
Personel, makine, müşteri, ürün, malzeme, parça. Kabul: tek kaynak ilkesi ve pasifleştirme uygulanır.

## Faz 3 — Sipariş ve iş emirleri
Sipariş -> iş emri -> rota. Kabul: benzersiz iş numarası, revizyonlu ürün kartı, durum makinesi.

## Faz 4 — Üretim
Planlama, vardiya, canlı üretim, duruş. Kabul: aynı makinede iki aktif iş engellenir; offline başlangıç/bitiş senkronize olur.

## Faz 5 — Kalite ve fire
Dinamik form oluşturucu, zorunlu kontroller, uygunsuzluk, fire nedenleri.

## Faz 6 — Bakım ve arıza
Sayaç/tarih bazlı bakım, arıza, parça kullanımı, tekrar analizi.

## Faz 7 — Stok ve satın alma
Lot/raf, rezervasyon, hareket defteri, minimum stok, satın alma akışı.

## Faz 8 — Maliyet ve sevkiyat
Tahmini/gerçek maliyet; kalite ve paketleme kapısı olan sevkiyat.

## Faz 9 — KPI / rapor
OEE, termin, fire, duruş, bakım uyumu, maliyet, PDF/Excel export.

## Faz 10 — Karar destek
Açıklanabilir öneriler, kaynak veri bağlantısı, güven skoru ve kullanıcı onayı.
