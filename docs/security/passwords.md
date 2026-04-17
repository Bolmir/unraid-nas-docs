# Passwörter & Zugangsdaten

> Alle Passwörter sind ausschliesslich in **Bitwarden** gespeichert.
> Diese Seite dokumentiert nur *wo* die Einträge zu finden sind – keine Passwörter im Klartext!

## Bitwarden Zugang

| | |
|---|---|
| **URL** | https://vault.bitwarden.com |
| **App** | iOS / Android / Browser-Extension |
| **Master-Passwort** | Auswendig kennen – nirgendwo digital speichern! |
| **2FA** | Aktiviert (Authenticator-App) |

---

## Bitwarden-Einträge nach Kategorie

### Unraid & System

| Bitwarden-Eintrag | Inhalt |
|-------------------|--------|
| `Unraid HOMELAB` | WebUI-Login, Root-Passwort |
| `Unraid Lizenz` | Lizenz-Key (auch als Dateianhang) |
| `LUKS Keyfile` | Verschlüsselungs-Keyfile als Dateianhang |
| `SSH HOMELAB` | SSH-Schlüssel für Remote-Zugriff |

### Docker-Dienste

| Bitwarden-Eintrag | Inhalt |
|-------------------|--------|
| `Nginx Proxy Manager` | Admin-Login, Domain-Konfiguration |
| `Nextcloud Admin` | Admin-Login |
| `Immich` | Admin-Login |
| `Immich PostgreSQL` | DB-Benutzer & Passwort |
| `FileBrowser` | Login |
| `Homarr` | Login |
| `Open-WebUI` | Login |
| `n8n` | Login, API-Keys für Workflows |
| `WAHA` | API-Key |
| `Plex` | Account (plex.tv) |
| `Overseerr / Seerr` | Login |
| `Sonarr` | API-Key |
| `Radarr` | API-Key |
| `Prowlarr` | API-Key |
| `Bazarr` | API-Key |
| `qBittorrent` | Login |
| `qBittorrent VPN` | VPN-Konfigurationsdatei als Anhang |
| `TeamSpeak 6` | Admin-Token, Server-Passwort |
| `Valheim Server` | Server-Passwort |
| `Duplicacy` | Login, Backup-Ziel-Credentials |

### Externe Dienste

| Bitwarden-Eintrag | Inhalt |
|-------------------|--------|
| `GitHub Bolmir` | GitHub-Login, Personal Access Token |
| `Domain / DNS` | Domain-Registrar Login, DNS-Einträge |

---

## Sicherheitshinweise

- ✅ Master-Passwort auswendig kennen
- ✅ 2FA für Bitwarden aktiviert halten
- ✅ Bitwarden Emergency Sheet ausgedruckt und sicher aufbewahrt
- ✅ LUKS Keyfile als Bitwarden-Anhang gespeichert
- ⚠️ Niemals Passwörter in Dokumentationen oder Git-Repos speichern
- ⚠️ Nach einem Sicherheitsvorfall alle Passwörter erneuern

## Passwort-Rotation

Nach folgenden Ereignissen alle betroffenen Passwörter erneuern:
- Kompromittierung des Systems
- Entlassung von Personen mit Zugangsdaten
- Sicherheitslücke in einem Dienst
- Jährliche Rotation empfohlen für Admin-Passwörter
