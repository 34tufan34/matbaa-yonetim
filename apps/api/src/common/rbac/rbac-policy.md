# RBAC politikası

Yetki kodu biçimi: `<modül>.<eylem>`.

Örnekler:
- `machines.read`
- `machines.write`
- `production.start`
- `quality.approve`
- `shipment.approve`
- `audit.read`

Rol yalnızca yetki paketidir. İş kuralı kontrolü rol adına göre değil izin koduna göre yapılır.
Kritik eylemler için ayrıca bağlamsal kural uygulanır; örn. `shipment.approve` izni olsa bile kalite onayı yoksa sevkiyat tamamlanamaz.
