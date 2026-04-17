# Docker Container Setup

> Alle Passwörter und API-Keys sind in **Bitwarden** unter dem Eintrag des jeweiligen Dienstes gespeichert.

## Grundprinzip

Alle Container-Konfigurationen liegen im Share `appdata` → `/mnt/user/appdata/<container-name>/`

Bei einer Neuinstallation:
1. Appdata-Backup wiederherstellen (siehe [Disaster Recovery](../disaster-recovery/plan.md))
2. Container in Unraid neu anlegen mit denselben Pfaden
3. Alternativ: Unraid Community Apps → Container neu installieren → auf `appdata` zeigen

---

## Netzwerk & Infrastruktur

### Nginx Proxy Manager
- **Image:** jc21/nginx-proxy-manager
- **Port:** 80, 443, 81 (Admin)
- **Appdata:** `/mnt/user/appdata/nginx-proxy-manager`
- **Admin-Login:** Bitwarden → "Nginx Proxy Manager"
- **Hinweis:** Zuerst einrichten! Andere Dienste brauchen den Proxy.

### Konfigurierte Proxy-Hosts
> Eigene Domain und SSL-Zertifikate → Details in Bitwarden

---

## Cloud & Produktivität

### Nextcloud (All-in-One)
- **Image:** nextcloud/all-in-one
- **Port:** 11000 (Web), AIO-Interface auf Port 8080
- **Daten:** `/mnt/user/nextcloud`
- **Appdata:** `/mnt/user/appdata/nextcloud-aio`
- **Login:** Bitwarden → "Nextcloud Admin"
- **Hinweis:** AIO-Mastercontainer zuerst starten, dann die restlichen AIO-Container werden automatisch erstellt

### n8n (Automatisierung)
- **Image:** n8nio/n8n
- **Port:** 5679
- **Appdata:** `/mnt/user/appdata/n8n-birreweich`
- **Login:** Bitwarden → "n8n"
- **Workflows:** Werden im appdata-Verzeichnis gespeichert → im Backup enthalten

### WAHA (WhatsApp API)
- **Image:** devlikeapro/waha
- **Port:** 3001
- **Appdata:** `/mnt/user/appdata/waha`
- **API-Key:** Bitwarden → "WAHA"

---

## KI & Machine Learning

### Ollama
- **Image:** ollama/ollama
- **Port:** 11434
- **Appdata:** `/mnt/user/appdata/ollama`
- **Modelle:** Werden lokal im appdata gespeichert (können gross sein!)
- **Hinweis:** Geladene Modelle nach Neuinstallation erneut pullen: `ollama pull <modell>`

### Open-WebUI
- **Image:** ghcr.io/open-webui/open-webui
- **Port:** 8082
- **Appdata:** `/mnt/user/appdata/open-webui`
- **Login:** Bitwarden → "Open-WebUI"
- **Verbindung:** Ollama API auf `http://192.168.1.160:11434`

---

## Medien-Stack (*arr)

### Plex Media Server
- **Image:** binhex/arch-plex
- **Netzwerk:** host (direkt, kein Port-Mapping nötig)
- **Appdata:** `/mnt/user/appdata/binhex-plex`
- **Medien:** `/mnt/user/data`
- **Login:** Bitwarden → "Plex"

### Sonarr (TV-Serien)
- **Image:** binhex/arch-sonarr
- **Port:** 8989
- **Appdata:** `/mnt/user/appdata/binhex-sonarr`
- **Medien:** `/mnt/user/data`
- **API-Key:** Bitwarden → "Sonarr"

### Radarr (Filme)
- **Image:** binhex/arch-radarr
- **Port:** 7878
- **Appdata:** `/mnt/user/appdata/binhex-radarr`
- **Medien:** `/mnt/user/data`
- **API-Key:** Bitwarden → "Radarr"

### Prowlarr (Indexer)
- **Image:** binhex/arch-prowlarr
- **Port:** 9696
- **Appdata:** `/mnt/user/appdata/binhex-prowlarr`
- **API-Key:** Bitwarden → "Prowlarr"

### Bazarr (Untertitel)
- **Image:** lscr.io/linuxserver/bazarr
- **Port:** 6767
- **Appdata:** `/mnt/user/appdata/bazarr`
- **API-Keys:** Bitwarden → "Bazarr"

### Seerr / Overseerr (Anfragen)
- **Image:** binhex/arch-seerr
- **Port:** 5055
- **Appdata:** `/mnt/user/appdata/binhex-seerr`
- **Login:** Bitwarden → "Overseerr"

### FlareSolverr
- **Image:** binhex/arch-flaresolverr
- **Port:** 8191
- **Keine Konfiguration nötig** – wird von Prowlarr genutzt

### qBittorrent + VPN
- **Image:** binhex/arch-qbittorrentvpn
- **Port:** 8080
- **Appdata:** `/mnt/user/appdata/binhex-qbittorrentvpn`
- **VPN-Config:** Bitwarden → "qBittorrent VPN" (OpenVPN/WireGuard-Config als Anhang)
- **Login:** Bitwarden → "qBittorrent"

### Huntarr
- **Image:** huntarr/huntarr
- **Port:** 9705
- **Appdata:** `/mnt/user/appdata/huntarr`

### Cleanuparr
- **Image:** ghcr.io/cleanuparr/cleanuparr
- **Port:** 11011
- **Appdata:** `/mnt/user/appdata/cleanuparr`

---

## Fotos & Dateien

### Immich
- **Image:** ghcr.io/imagegenius/immich
- **Port:** 8086
- **Fotos:** `/mnt/user/photos`
- **Appdata:** `/mnt/user/appdata/immich`
- **Datenbank:** PostgreSQL_Immich (separater Container, Port 5433)
- **Login:** Bitwarden → "Immich"

### PostgreSQL für Immich
- **Image:** tensorchord/pgvecto-rs:pg16-v0.3.0
- **Port:** 5433
- **Appdata:** `/mnt/user/appdata/postgresql-immich`
- **DB-Passwort:** Bitwarden → "Immich PostgreSQL"

### FileBrowser
- **Image:** filebrowser/filebrowser
- **Port:** 8081
- **Root:** `/mnt/user`
- **Appdata:** `/mnt/user/appdata/filebrowser`
- **Login:** Bitwarden → "FileBrowser"

---

## Gaming & Kommunikation

### TeamSpeak 6
- **Image:** teamspeaksystems/teamspeak6-server
- **Ports:** 9987/UDP, 10022, 10080, 30033
- **Appdata:** `/mnt/user/appdata/teamspeak6`
- **Admin-Token:** Bitwarden → "TeamSpeak 6"

### Valheim
- **Image:** ich777/steamcmd:valheim
- **Appdata:** `/mnt/user/appdata/valheim`
- **Server-Passwort:** Bitwarden → "Valheim Server"
- **Status:** Manuell starten wenn benötigt

---

## Backup

### Duplicacy
- **Image:** saspus/duplicacy-web
- **Port:** 3875
- **Appdata:** `/mnt/user/appdata/duplicacy`
- **Login:** Bitwarden → "Duplicacy"
- **Backup-Ziel:** Bitwarden → "Duplicacy Backup-Ziel"

---

## Dashboard

### Homarr
- **Image:** ghcr.io/homarr-labs/homarr
- **Port:** 10004
- **Appdata:** `/mnt/user/appdata/homarr`
- **Login:** Bitwarden → "Homarr"
