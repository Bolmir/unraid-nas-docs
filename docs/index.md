# HOMELAB – Unraid NAS Dokumentation

> Automatisch gepflegt von Claude AI | Letzte Aktualisierung: 2026-04-17

## Schnellübersicht

| | |
|---|---|
| **Hostname** | HOMELAB |
| **IP** | 192.168.1.160 |
| **Unraid** | 7.2.4 |
| **CPU** | Intel i3-12100 |
| **RAM** | 32 GB |
| **Array** | 2× 4TB + 12TB Parity |
| **Cache** | 500GB NVMe |
| **Container** | 33 (29 aktiv) |

## Navigation

- [Hardware](hardware/overview.md) – CPU, RAM, Festplatten, Netzwerk
- [Plugins](software/plugins.md) – Installierte Unraid-Plugins
- [Shares](software/shares.md) – Freigaben und Dateisysteme
- [Docker Container](services/docker-containers.md) – Alle laufenden Dienste
- [Netzwerk](network/overview.md) – IPs, Ports, Reverse Proxy
- [Backup & Wartung](maintenance/backup.md) – Backup-Strategie, Disk-Status

## Dienste (Schnellzugriff)

| Dienst | URL |
|--------|-----|
| Unraid WebUI | http://192.168.1.160 |
| Homarr Dashboard | http://192.168.1.160:10004 |
| Plex | http://192.168.1.160:32400 |
| Nextcloud | http://192.168.1.160:11000 |
| Immich | http://192.168.1.160:8086 |
| Open-WebUI (KI) | http://192.168.1.160:8082 |
| n8n | http://192.168.1.160:5679 |
| Sonarr | http://192.168.1.160:8989 |
| Radarr | http://192.168.1.160:7878 |
| Nginx Proxy Manager | http://192.168.1.160:81 |
| FileBrowser | http://192.168.1.160:8081 |
| Duplicacy | http://192.168.1.160:3875 |
