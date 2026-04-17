# Unraid Neuinstallation

> Passwörter: alle in **Bitwarden** gespeichert

## Voraussetzungen

- USB-Stick (mind. 2 GB) – aktuell: SanDisk 3.2 Gen1
- Lizenz-Key (in Bitwarden gespeichert)
- Internetzugang für Download

## Schritt 1 – USB-Stick vorbereiten

1. [Unraid USB Flash Creator](https://unraid.net/de/download) herunterladen
2. USB-Stick anschliessen, Tool starten
3. Version wählen: **7.2.4** (aktuell)
4. Auf USB-Stick schreiben
5. Nach dem Schreiben: Datei `config/go` auf dem USB-Stick öffnen und prüfen

## Schritt 2 – Erststart

1. USB-Stick in den Server stecken (eigener USB-Port, nicht über Hub)
2. Im BIOS: Boot von USB aktivieren, UEFI-Boot
3. Server starten → Unraid bootet
4. Unter http://tower (oder IP per DHCP) erreichbar
5. Lizenz aktivieren: **Main → Registration** → Key aus Bitwarden eintragen

## Schritt 3 – Netzwerk konfigurieren

| Einstellung | Wert |
|-------------|------|
| IP-Adresse | 192.168.1.160 (statisch) |
| Subnet | 255.255.255.0 |
| Gateway | 192.168.1.1 |
| DNS | 192.168.1.1 |
| Hostname | HOMELAB |

**Settings → Network** → statische IP setzen → Apply

## Schritt 4 – Array konfigurieren

| Slot | Disk | Seriennummer |
|------|------|-------------|
| Parity | Seagate ST12000VN0008 | WRS1JZF0 |
| Disk 1 | WD WD40EFZX-68AWUN0 | (Bitwarden) |
| Disk 2 | WD WD40EFZX-68AWUN0 | (Bitwarden) |
| Cache | Samsung 970 EVO Plus NVMe | (Bitwarden) |

1. **Main** → Disks zuweisen
2. Array starten → **Format** bei neuen Disks bestätigen
3. Dateisystem: **XFS**

## Schritt 5 – LUKS-Verschlüsselung

> ⚠️ Keyfile unbedingt vorher auf externen Datenträger sichern!

1. **Settings → Disk Settings** → Encryption aktivieren
2. Keyfile liegt unter `/root/keyfile` (Backup in Bitwarden als Dateianhang)
3. Array stoppen → verschlüsselt neu starten

## Schritt 6 – Shares erstellen

| Share | Cache-Einstellung | Verwendung |
|-------|------------------|-----------|
| appdata | Only | Docker-Configs |
| data | Yes | Medien/Downloads |
| domains | Only | VM-Images |
| fileshare | Yes | Dateifreigabe |
| isos | Only | ISO-Images |
| nextcloud | Yes | Nextcloud-Daten |
| photos | Yes | Fotos (Immich) |
| system | Only | Systemdaten |

## Schritt 7 – Plugins installieren

Reihenfolge einhalten:

1. **Community Applications** (zuerst!)
2. NerdTools
3. User Scripts
4. Appdata Backup
5. rclone
6. Folder View 2
7. GPU Stat / Intel GPU Top
8. Claude Code

## Schritt 8 – Docker aktivieren

**Settings → Docker** → Enable → Storage: `/mnt/user/appdata` → Apply

→ Danach Container einzeln wiederherstellen (siehe [Docker Setup](docker.md))
