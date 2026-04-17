# HOMELAB – Unraid NAS Dokumentation

> Automatisch gepflegt von Claude AI | Letzte Aktualisierung: 2026-04-17

!!! warning "Im Notfall"
    Direktlink zum Notfallplan: [Disaster Recovery](disaster-recovery/plan.md)  
    Passwörter: [Bitwarden](https://vault.bitwarden.com) → vault.bitwarden.com

## Schnellübersicht

| | |
|---|---|
| **Hostname** | HOMELAB |
| **IP** | 192.168.1.160 |
| **Unraid** | 7.2.4 |
| **CPU** | Intel i3-12100 (12th Gen) |
| **RAM** | 32 GB |
| **Array** | 2× WD 4TB + Seagate 12TB Parity |
| **Cache** | Samsung 970 EVO Plus 500GB NVMe |
| **Container** | 33 (29 aktiv) |

## Navigation

| Bereich | Beschreibung |
|---------|-------------|
| [Hardware](hardware/overview.md) | CPU, RAM, Festplatten, Netzwerk |
| [Plugins](software/plugins.md) | Installierte Unraid-Plugins |
| [Shares](software/shares.md) | Freigaben und Dateisysteme |
| [Docker Container](services/docker-containers.md) | Alle laufenden Dienste |
| [Netzwerk](network/overview.md) | IPs, Ports, Reverse Proxy |
| [Unraid Einrichtung](setup/unraid.md) | Schritt-für-Schritt Neuinstallation |
| [Docker Setup](setup/docker.md) | Alle Container einrichten |
| [Dienste-Konfiguration](setup/services.md) | Medienstack, Nextcloud, etc. |
| [Passwörter](security/passwords.md) | Bitwarden-Einträge Übersicht |
| [Disaster Recovery](disaster-recovery/plan.md) | **Notfallplan – hier starten!** |
| [Backup & Wartung](maintenance/backup.md) | Backup-Strategie |

## Dienste (Schnellzugriff)

| Dienst | URL | Port |
|--------|-----|------|
| Unraid WebUI | http://192.168.1.160 | 80 |
| Homarr Dashboard | http://192.168.1.160:10004 | 10004 |
| Plex | http://192.168.1.160:32400 | 32400 |
| Nextcloud | http://192.168.1.160:11000 | 11000 |
| Immich | http://192.168.1.160:8086 | 8086 |
| Open-WebUI (KI) | http://192.168.1.160:8082 | 8082 |
| n8n | http://192.168.1.160:5679 | 5679 |
| Sonarr | http://192.168.1.160:8989 | 8989 |
| Radarr | http://192.168.1.160:7878 | 7878 |
| Prowlarr | http://192.168.1.160:9696 | 9696 |
| qBittorrent | http://192.168.1.160:8080 | 8080 |
| Overseerr | http://192.168.1.160:5055 | 5055 |
| Nginx Proxy Manager | http://192.168.1.160:81 | 81 |
| FileBrowser | http://192.168.1.160:8081 | 8081 |
| Duplicacy | http://192.168.1.160:3875 | 3875 |
| TeamSpeak 6 | 192.168.1.160 | 9987/UDP |
