# Matbaa Yönetim Sistemi

Merkezi, modüler ve offline-first matbaa işletim sistemi.

## Sürüm
v0.1.0 — Faz 1 başlangıç iskeleti

## Monorepo
- `apps/api`: NestJS + Prisma + PostgreSQL backend
- `apps/mobile`: Flutter Android/tablet istemcisi
- `docs`: mimari, veri modeli ve geliştirme planı

## Faz 1 kapsamı
- Organizasyon temeli
- Kullanıcı / rol / yetki veri modeli
- Sistem ayarları ve dinamik sözlük yapısı
- Audit log temeli
- Offline senkronizasyon sözleşmesi
- Komuta Merkezi için ilk mobil kabuk

## Hızlı başlangıç
1. PostgreSQL başlat: `docker compose up -d db`
2. `apps/api/.env.example` dosyasını `.env` olarak kopyala.
3. API bağımlılıklarını kur: `cd apps/api && npm install`
4. Prisma client üret: `npm run prisma:generate`
5. Migration uygula: `npm run prisma:migrate`
6. API çalıştır: `npm run start:dev`
7. Flutter SDK ile `cd apps/mobile && flutter pub get && flutter run`

GitHub Actions her geliştirme pushunda API ve Flutter kontrollerini çalıştırır, ayrıca web test paketi üretir. APK ise yalnızca manuel kilometre taşı/final workflow’u ile üretilir. Ayrıntılar için `docs/TESTING.md`.
