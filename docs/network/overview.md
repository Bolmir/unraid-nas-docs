# Netzwerk

> Zuletzt aktualisiert: 2026-04-17

## Grundkonfiguration

| Einstellung | Wert |
|-------------|------|
| **IP-Adresse** | 192.168.1.160/24 |
| **Gateway** | 192.168.1.1 |
| **DNS** | 192.168.1.1 |
| **Interface** | br0 (Bond: eth0) |
| **Netzwerk** | 192.168.1.0/24 |

## Docker-Netzwerke

| Netzwerk | Subnetz |
|----------|---------|
| docker0 (default bridge) | 172.17.0.0/16 |
| br-5434ff7cab7b | 172.18.0.0/16 |
| br-cadab7b6248f | 172.19.0.0/16 |
| br-86f00758d771 | 172.20.0.0/16 |

## Reverse Proxy

**Nginx Proxy Manager** läuft auf Port 80/443 und verwaltet den externen Zugriff auf die Dienste.

## Wichtige interne Ports

| Dienst | Port |
|--------|------|
| Unraid WebUI | 80 / 443 |
| Plex | direkt (host network) |
| Nextcloud | 11000 |
| Immich | 8086 |
| Open-WebUI (Ollama) | 8082 |
| Ollama API | 11434 |
| Sonarr | 8989 |
| Radarr | 7878 |
| Prowlarr | 9696 |
| qBittorrent | 8080 |
| n8n | 5679 |
| Homarr Dashboard | 10004 |
| FileBrowser | 8081 |
| Nginx Proxy Manager | 81 (Admin) |
| TeamSpeak 6 | 9987/UDP |
