# Matbaa Yönetim Sistemi — Hedef Mimari

## Mimari stil
Modüler monolit ile başlanır. Her iş alanı kendi domain sınırına, servislerine ve tablolarına sahiptir; tek PostgreSQL kümesi ve tek API deploy edilir. Erken mikroservis kullanılmaz. Bunun nedeni üretim tesislerinde ağ, operasyon ve bakım maliyetini düşük tutarken domain ayrımını korumaktır. Gerektiğinde bildirim, dosya, raporlama veya makine telemetrisi bağımsız servise ayrılabilir.

## 9 iş alanı
1. Platform: kimlik, RBAC, ayarlar, audit, dosya, bildirim, sync.
2. Ticari: müşteri, teklif, sipariş.
3. Ürün Mühendisliği: ürün/iş kartı, rota/reçete, teknik dosya.
4. Üretim: planlama, iş emri, operasyon, vardiya, duruş, fire.
5. Kalite: kontrol planı/formu, kontrol sonucu, uygunsuzluk, şikayet.
6. Varlık Yönetimi: makine, arıza, bakım, yedek parça.
7. Tedarik Zinciri: stok, depo, satın alma, tedarikçi, sevkiyat.
8. Maliyet: tahmini/gerçek maliyet, maliyet kalemleri.
9. Yönetim: Komuta Merkezi, KPI, OEE, rapor, karar destek.

## Temel kararlar
- Ana kayıt tekliği: müşteri, personel, makine, parça ve malzeme tek ana kaynaktan tanımlanır.
- İşlem kayıtları append-only tercih eder; düzeltme yeni kayıt/ters kayıtla yapılır.
- Düzenlenebilir ana kayıtlarda `version` alanı ile optimistic concurrency uygulanır.
- Tüm offline yazmalar `clientMutationId` ile idempotent olmalıdır.
- Kritik durum değişimleri state machine üzerinden yapılır; ekrandan doğrudan status yazılmaz.
- Tahmin/AI çıktıları `decision_suggestion` olarak saklanır; gerçek üretim kaydıyla aynı tabloda tutulmaz.

## Veri akışı
Müşteri -> Sipariş -> İş Emri -> Ürün Sürümü -> Üretim Rotası -> Planlama -> Operasyon Emri -> Makine/Personel -> Üretim Olayları -> Kalite/Fire/Duruş -> Paketleme -> Sevkiyat -> Maliyet Kapanışı.

Stok, bakım, kalite ve audit bu zincire çapraz bağlanır.

## Offline yaklaşımı
Mobil cihaz yerel veriyi önce yazar. Her mutasyon şu zarfla kuyruğa girer:
- clientMutationId
- deviceId
- entityType/entityId
- operation
- baseVersion
- occurredAt
- payload

Sunucu aynı clientMutationId ikinci kez gelirse yeniden işlem yapmaz. Ana veri çakışmasında baseVersion kontrol edilir. Operasyon sayacı, fire, duruş gibi olay kayıtları mümkün olduğunca append-only olduğu için otomatik birleştirilir. Aynı alanın eşzamanlı düzenlenmesi gibi gerçek çatışmalar `conflict` durumuna alınır ve yetkili kullanıcıya gösterilir.

## Komuta Merkezi read model
Komuta Merkezi doğrudan onlarca tabloyu her yenilemede join etmez. Üretim, kalite, bakım ve stok olaylarından beslenen özet read-model/projection üretir. Bu hem 5 saniyelik anlaşılırlık hedefini hem de tablet performansını destekler.
