# Docker Container

> Zuletzt aktualisiert: 2026-04-17

## Medien & Entertainment

| Container | Image | Port | Status | Beschreibung |
|-----------|-------|------|--------|-------------|
| **binhex-plex** | binhex/arch-plex | — | ✅ Läuft | Plex Media Server |
| **binhex-sonarr** | binhex/arch-sonarr | 8989 | ✅ Läuft | TV-Serien Verwaltung |
| **binhex-radarr** | binhex/arch-radarr | 7878 | ✅ Läuft | Film-Verwaltung |
| **bazarr** | linuxserver/bazarr | 6767 | ✅ Läuft | Untertitel-Verwaltung |
| **binhex-seerr** | binhex/arch-seerr | 5055 | ✅ Läuft | Medien-Anfragen (Overseerr) |
| **binhex-prowlarr** | binhex/arch-prowlarr | 9696 | ✅ Läuft | Indexer-Verwaltung |
| **binhex-flaresolverr** | binhex/arch-flaresolverr | 8191 | ✅ Läuft | Cloudflare-Bypass für Prowlarr |
| **binhex-qbittorrentvpn** | binhex/arch-qbittorrentvpn | 8080 | ✅ Läuft | qBittorrent mit VPN |
| **Huntarr** | huntarr/huntarr | 9705 | ✅ Läuft | Automatischer Medien-Hunter |
| **Cleanuparr** | ghcr.io/cleanuparr/cleanuparr | 11011 | ✅ Läuft | Aufräum-Automatisierung |

## Fotos & Dateien

| Container | Image | Port | Status | Beschreibung |
|-----------|-------|------|--------|-------------|
| **immich** | imagegenius/immich | 8086 | ✅ Läuft | Foto-Bibliothek & KI-Analyse |
| **PostgreSQL_Immich** | tensorchord/pgvecto-rs:pg16 | 5433 | ✅ Läuft | Datenbank für Immich |
| **FileBrowser-PNP** | filebrowser/filebrowser | 8081 | ✅ Läuft | Web-Dateimanager |

## Cloud & Produktivität

| Container | Image | Port | Status | Beschreibung |
|-----------|-------|------|--------|-------------|
| **nextcloud-aio-nextcloud** | nextcloud/aio-nextcloud | 9000 | ✅ Läuft | Nextcloud (AIO) |
| **nextcloud-aio-apache** | nextcloud/aio-apache | 11000 | ✅ Läuft | Nextcloud Web-Server |
| **nextcloud-aio-database** | nextcloud/aio-postgresql | 5432 | ✅ Läuft | Nextcloud Datenbank |
| **nextcloud-aio-redis** | nextcloud/aio-redis | 6379 | ✅ Läuft | Nextcloud Cache |
| **nextcloud-aio-collabora** | nextcloud/aio-collabora | 9980 | ✅ Läuft | Office Online (Collabora) |
| **nextcloud-aio-imaginary** | nextcloud/aio-imaginary | — | ✅ Läuft | Bildverarbeitung |
| **nextcloud-aio-whiteboard** | nextcloud/aio-whiteboard | 3002 | ✅ Läuft | Whiteboard |
| **nextcloud-aio-notify-push** | nextcloud/aio-notify-push | — | ✅ Läuft | Push-Benachrichtigungen |
| **nextcloud-aio-mastercontainer** | nextcloud/all-in-one | — | ❌ Gestoppt | AIO Management |

## KI & Automatisierung

| Container | Image | Port | Status | Beschreibung |
|-----------|-------|------|--------|-------------|
| **ollama** | ollama/ollama | 11434 | ✅ Läuft | Lokale KI-Modelle |
| **open-webui** | open-webui/open-webui | 8082 | ✅ Läuft | Web-UI für Ollama |
| **n8n-birreweich** | n8nio/n8n | 5679 | ✅ Läuft | Automatisierungs-Workflows (n8n) |
| **waha** | devlikeapro/waha | 3001 | ✅ Läuft | WhatsApp HTTP API |

## Netzwerk & Infrastruktur

| Container | Image | Port | Status | Beschreibung |
|-----------|-------|------|--------|-------------|
| **Nginx-Proxy-Manager-Official** | jc21/nginx-proxy-manager | 80, 443, 81 | ✅ Läuft | Reverse Proxy |
| **Duplicacy** | saspus/duplicacy-web | 3875 | ✅ Läuft | Backup-Lösung |

## Gaming & Kommunikation

| Container | Image | Port | Status | Beschreibung |
|-----------|-------|------|--------|-------------|
| **binhex-official-teamspeak6-server** | teamspeaksystems/teamspeak6-server | 9987/UDP | ✅ Läuft | TeamSpeak 6 Server |
| **Valheim** | ich777/steamcmd:valheim | — | ❌ Gestoppt | Valheim Game Server |

## Sonstiges

| Container | Image | Port | Status | Beschreibung |
|-----------|-------|------|--------|-------------|
| **Tor-Browser** | ich777/torbrowser | 5800 | ✅ Läuft | Tor Browser (Web-UI) |
| **OpenClaw** | openclaw/openclaw | — | ❌ Gestoppt | OpenClaw |

---

**Gesamt:** 33 Container (29 laufend, 4 gestoppt)
