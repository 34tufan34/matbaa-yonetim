# Kritik iş kuralları — başlangıç kataloğu

| Kod | Kural | Seviye |
|---|---|---|
| PROD-001 | Bakım/arıza durumundaki makinede üretim başlatılamaz | Engelle |
| PROD-002 | Aynı makinede aynı anda iki aktif production_run olamaz | Engelle |
| PROD-003 | Yetkinliği geçersiz personel makineyi başlatamaz; politika izin verirse yetkili override gerekir | Engelle/Onay |
| PROD-004 | Zorunlu kalite kontrolü eksikse operasyon tamamlanamaz | Engelle |
| QUAL-001 | Tolerans dışı kritik sonuç kalite onayı olmadan kapatılamaz | Engelle |
| SHIP-001 | Kalite onayı yoksa sevkiyat tamamlanamaz | Engelle |
| SHIP-002 | Paketleme ve miktar kontrolü tamamlanmadan sevk kapanamaz | Engelle |
| STOCK-001 | Kritik malzeme yetersizse üretim başlatma politikaya göre engellenir veya yetkili override ister | Engelle/Onay |
| HR-001 | Aynı personele çakışan vardiya atanamaz | Engelle |
| MAINT-001 | Sayaç/tarih eşiği aşan kritik bakım için uyarı ve planlama aksiyonu oluşturulur | Kritik uyarı |
| AUD-001 | Onay, silme, düzeltme, override ve yetki değişikliği audit kaydı olmadan tamamlanamaz | Engelle |
| SYNC-001 | Aynı clientMutationId ikinci kez uygulanamaz | Engelle/Idempotent |
