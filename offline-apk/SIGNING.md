# UPM Production Android Signing

Production package ID: `com.tufanprintops.uretimperformans.production`

Starting with v1.3.0, production APKs must be signed with the same private signing key.

Expected signing certificate SHA-256:

`E9:B8:12:EC:D6:FE:0F:D2:D6:D4:C5:5E:E1:A3:F4:5A:76:15:74:38:82:FA:86:EE:0E:87:AD:F9:E8:FF:C1:D6`

The private keystore and credentials are intentionally **not stored in this public repository**. The build workflow produces an unsigned release APK. The final production APK is signed outside GitHub with the protected production keystore, then verified with Android `apksigner` before distribution.

Release rules:

1. Keep the package ID unchanged.
2. Increase `versionCode` for every release.
3. Sign every production APK with the exact same keystore/alias.
4. Verify APK Signature Scheme v2/v3 and the expected certificate fingerprint before distribution.
5. Never replace the production signing key unless a deliberate migration is planned.
