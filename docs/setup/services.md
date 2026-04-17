# Dienste-Konfiguration

> Detaillierte Einrichtungshinweise für die wichtigsten Dienste.  
> Zugangsdaten immer aus **Bitwarden** holen.

## Medien-Stack Einrichtung (Reihenfolge!)

Die *arr-Apps müssen in dieser Reihenfolge konfiguriert werden:

```
1. qBittorrent + VPN  →  Sicherstellen dass VPN funktioniert
2. FlareSolverr       →  Läuft einfach im Hintergrund
3. Prowlarr           →  Indexer einrichten, FlareSolverr verbinden
4. Radarr             →  Mit Prowlarr + qBittorrent verbinden
5. Sonarr             →  Mit Prowlarr + qBittorrent verbinden
6. Bazarr             →  Mit Sonarr + Radarr verbinden
7. Overseerr/Seerr    →  Mit Radarr + Sonarr verbinden
8. Plex               →  Medienbibliothek auf /mnt/user/data zeigen
9. Huntarr            →  Mit Sonarr/Radarr verbinden
10. Cleanuparr        →  Mit Sonarr/Radarr/qBittorrent verbinden
```

### Dateistruktur für Medien

```
/mnt/user/data/
├── downloads/
│   ├── complete/
│   └── incomplete/
├── movies/
├── tv/
└── music/
```

Alle *arr-Apps und qBittorrent müssen auf dieselben Pfade zeigen!

---

## Nextcloud AIO

1. Mastercontainer starten
2. AIO-Interface öffnen: http://192.168.1.160:8080
3. Admin-Passwort aus Bitwarden → "Nextcloud Admin"
4. Domain eintragen (via Nginx Proxy Manager erreichbar)
5. Nextcloud-Daten-Pfad: `/mnt/user/nextcloud`
6. Alle AIO-Sub-Container starten lassen

**Wichtig:** Nextcloud AIO braucht eine echte Domain mit SSL für volle Funktionalität.

---

## Immich

1. PostgreSQL_Immich Container zuerst starten
2. Immich Container starten
3. Ersteinrichtung: http://192.168.1.160:8086
4. Admin-Account erstellen → Login in Bitwarden speichern
5. Bibliothek zeigt auf: `/mnt/user/photos`

---

## n8n

1. Container starten
2. http://192.168.1.160:5679 aufrufen
3. Account einrichten → Login in Bitwarden
4. Workflows werden in appdata gespeichert → automatisch in Backup

---

## Nginx Proxy Manager

Externe Domains (SSL via Let's Encrypt):
- Für jeden Dienst einen Proxy Host anlegen
- Domain → interne IP + Port
- SSL-Zertifikat automatisch von Let's Encrypt

**Wichtig:** Port 80 + 443 müssen im Router auf 192.168.1.160 weitergeleitet sein.

---

## qBittorrent VPN

1. VPN-Konfigurationsdatei aus Bitwarden → in appdata ablegen
2. Container starten
3. Prüfen ob VPN aktiv: http://192.168.1.160:8080 → IP-Check
4. Wenn kein VPN → Downloads werden blockiert (Sicherheitsfeature)

---

## Duplicacy Backup

1. http://192.168.1.160:3875 aufrufen
2. Login aus Bitwarden → "Duplicacy"
3. Backup-Quellen: `/mnt/user/data`, `/mnt/user/photos`, `/mnt/user/nextcloud`
4. Backup-Ziel: Cloud-Credentials aus Bitwarden → "Duplicacy Backup-Ziel"
5. Zeitplan: Täglich 03:00 Uhr
