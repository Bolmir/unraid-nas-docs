# Disaster Recovery Plan

> ⚠️ Dieses Dokument ist das wichtigste im gesamten Wiki. Im Notfall hier starten.
> Alle Passwörter sind in **Bitwarden** gespeichert.

---

## Notfall-Szenarien

### Szenario 1: Einzelne Datenfestplatte ausgefallen

**Symptom:** Unraid meldet eine Disk als "disabled" oder fehlt  
**Datenverlust:** Keiner (Parity vorhanden)  
**Dringlichkeit:** Mittel – System läuft weiter, aber ohne Redundanz

**Vorgehen:**
1. Unraid WebUI öffnen → **Main**
2. Ausgefallene Disk identifizieren (rot markiert)
3. Neue Ersatz-Festplatte besorgen (mind. gleiche Kapazität)
4. System herunterfahren
5. Alte Disk ausbauen, neue einbauen
6. Unraid starten → **Main** → neue Disk dem freien Slot zuweisen
7. **New Config** → Disk dem richtigen Slot zuweisen
8. Array starten → **Parity ist jetzt ungültig** → Parity neu schreiben lassen
9. Warten bis Parity-Sync abgeschlossen (~12h für 12TB)

---

### Szenario 2: Cache-NVMe ausgefallen

**Symptom:** Cache-Disk fehlt, `/mnt/cache` nicht erreichbar  
**Datenverlust:** Möglich! Daten auf Cache aber noch nicht auf Array = verloren  
**Dringlichkeit:** Hoch

**Vorgehen:**
1. Prüfen was noch auf Cache ist: `ls /mnt/cache/` (wenn noch erreichbar)
2. Neue NVMe einbauen (Samsung 970 EVO Plus 500GB oder ähnlich)
3. Unraid starten → neue Disk als Cache zuweisen
4. **Format** ausführen
5. **appdata** aus Appdata-Backup-Plugin wiederherstellen
6. Container-Konfigurationen werden automatisch wiederhergestellt
7. Docker-Container neu starten

---

### Szenario 3: Parity-Disk ausgefallen

**Symptom:** Parity-Disk (Seagate 12TB) fehlt oder ist defekt  
**Datenverlust:** Keiner – Array läuft ohne Redundanz weiter  
**Dringlichkeit:** Mittel – aber neue Parity-Disk so schnell wie möglich!

**Vorgehen:**
1. System läuft normal weiter (ohne Schutz)
2. Neue 12TB+ Disk besorgen
3. Alte Parity ausbauen, neue einbauen
4. **Main** → neue Disk als Parity zuweisen
5. Array starten → **Parity-Sync** startet automatisch
6. Warten (~12-24h)

---

### Szenario 4: USB-Boot-Stick ausgefallen

**Symptom:** Server bootet nicht mehr, Unraid nicht erreichbar  
**Datenverlust:** Keiner (Daten auf Array-Disks, nicht auf USB)  
**Dringlichkeit:** Hoch – Server nicht verfügbar

**Vorgehen:**
1. Neuen USB-Stick (mind. 2GB) besorgen
2. [Unraid USB Flash Creator](https://unraid.net/de/download) herunterladen
3. Version 7.2.4 auf neuen Stick schreiben
4. Lizenz-Key aus Bitwarden → auf neuem Stick aktivieren
5. Netzwerk-Konfiguration wiederherstellen:
   - IP: 192.168.1.160 (statisch)
   - Hostname: HOMELAB
6. Array-Disks werden automatisch erkannt
7. LUKS-Keyfile: aus Bitwarden (Dateianhang) nach `/root/keyfile` kopieren
8. Plugins neu installieren (Reihenfolge beachten → [Unraid Setup](../setup/unraid.md))
9. Docker-Container aus appdata neu starten

---

### Szenario 5: Komplettausfall (Mainboard/CPU/RAM)

**Symptom:** Hardware irreparabel defekt, Neubeschaffung nötig  
**Datenverlust:** Keiner (Daten auf Disks)  
**Dringlichkeit:** Hoch – alles neu aufbauen

**Neue Hardware (Empfehlung gleiche oder besser):**
- CPU: Intel i3-12100 oder neuer (LGA1700)
- RAM: 2× 16GB DDR4
- Mainboard: mit mind. 4 SATA-Ports + 1 M.2

**Vorgehen:**
1. Neue Hardware beschaffen und zusammenbauen
2. Neuen USB-Boot-Stick erstellen (→ Szenario 4)
3. Alle Festplatten anschliessen:
   - Seagate 12TB → Parity
   - 2× WD 4TB → Disk 1 & 2
   - Samsung NVMe → Cache
4. Array-Erkennung: Unraid erkennt vorhandene Disks automatisch
5. LUKS-Keyfile aus Bitwarden wiederherstellen
6. **Kein Format!** – bestehende Daten bleiben erhalten
7. Plugins + Docker wie oben

---

### Szenario 6: Ransomware / Datenverschlüsselung

**Symptom:** Dateien verschlüsselt, nicht mehr lesbar  
**Datenverlust:** Abhängig vom letzten Backup  
**Dringlichkeit:** Kritisch

**Vorgehen:**
1. Sofort Netzwerk trennen (LAN-Kabel ziehen!)
2. Server herunterfahren
3. Duplicacy-Backup prüfen (von externem Gerät aus!)
4. Befallene Disks identifizieren
5. System komplett neu aufsetzen (→ Szenario 5)
6. Nur Backup einspielen, keine alten Dateien übernehmen
7. Alle Passwörter in Bitwarden nach Wiederherstellung ändern
8. Einfallstor identifizieren und schliessen

---

## Backup-Strategie (3-2-1 Regel)

| # | Kopie | Ort | Lösung |
|---|-------|-----|--------|
| 1 | Original | NAS Array | Unraid Array |
| 2 | Lokale Kopie | Appdata-Backup | Appdata Backup Plugin |
| 3 | Offsite | Cloud | Duplicacy → Cloud |

### Was wird gesichert?

| Daten | Lösung | Frequenz |
|-------|--------|----------|
| appdata (Docker-Configs) | Appdata Backup Plugin | Täglich |
| Wichtige Daten | Duplicacy | Täglich |
| Fotos | Immich + Duplicacy | Kontinuierlich |
| Nextcloud-Daten | Nextcloud + Duplicacy | Täglich |

---

## Wichtige Dateien & Pfade

| Datei | Pfad | Backup-Ort |
|-------|------|-----------|
| LUKS Keyfile | `/root/keyfile` | Bitwarden (Dateianhang) |
| Unraid Lizenz | `/boot/config/registration.dat` | Bitwarden |
| Docker-Configs | `/mnt/user/appdata/` | Appdata Backup |
| USB-Boot-Config | `/boot/config/` | Auf USB-Stick |

---

## Notfall-Kontakte & Ressourcen

| Ressource | URL |
|-----------|-----|
| Unraid Forum | https://forums.unraid.net |
| Unraid Docs | https://docs.unraid.net |
| Diese Dokumentation | https://bolmir.github.io/unraid-nas-docs |
| Bitwarden | https://vault.bitwarden.com |

---

## Checkliste nach Wiederherstellung

- [ ] Alle Docker-Container laufen
- [ ] Nextcloud erreichbar und Daten vollständig
- [ ] Immich Fotos vorhanden
- [ ] Plex-Bibliothek vollständig
- [ ] n8n Workflows aktiv
- [ ] Nginx Proxy Manager – alle Proxy-Hosts aktiv
- [ ] Duplicacy – Backup-Jobs aktiv
- [ ] Appdata Backup – Zeitplan aktiv
- [ ] Parity-Check durchführen
- [ ] Diese Dokumentation aktuell?
