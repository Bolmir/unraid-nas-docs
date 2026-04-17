# Backup & Wartung

> Zuletzt aktualisiert: 2026-04-17

## Backup-Lösungen

### Duplicacy
- **Container:** Duplicacy (Port 3875)
- **WebUI:** http://192.168.1.160:3875
- Cloud-fähiges Backup mit Deduplizierung

### Appdata Backup Plugin
- Sichert den `appdata`-Share (Docker-Konfigurationen)
- Konfigurierbar über Unraid-UI unter Plugins

## Array-Wartung

### Parity Check
- Unraid führt automatisch monatliche Parity-Checks durch
- Letzter Check: siehe Unraid-Dashboard
- Letzte bekannte Sync-Fehler: 1 (korrigiert)

### Disk-Status
| Disk | Modell | Kapazität | Belegung |
|------|--------|-----------|---------|
| Parity | Seagate ST12000VN0008 | 12 TB | Parität |
| Disk 1 | WD WD40EFZX-68AWUN0 | 4 TB | 58% belegt |
| Disk 2 | WD WD40EFZX-68AWUN0 | 4 TB | 50% belegt |
| Cache | Samsung 970 EVO Plus | 500 GB | 44% belegt |

## Verschlüsselung

- **LUKS** ist für das Array aktiviert
- Keyfile-Pfad: `/root/keyfile`
- ⚠️ Keyfile-Backup an sicherem Ort aufbewahren!

## Empfehlungen

- [ ] Regelmässige Temperaturüberwachung der Festplatten
- [ ] SMART-Tests monatlich durchführen
- [ ] Duplicacy-Backups auf externen Speicher/Cloud prüfen
- [ ] Keyfile an sicherem externen Ort sichern
