# Shares (Freigaben)

> Zuletzt aktualisiert: 2026-04-17

Alle Shares sind unter `/mnt/user/` erreichbar.

| Share | Zweck |
|-------|-------|
| **appdata** | Konfigurationsdaten der Docker-Container |
| **data** | Hauptdatenablage (Medien, Downloads, etc.) |
| **domains** | VM-Disk-Images |
| **fileshare** | Allgemeine Dateifreigabe |
| **isos** | ISO-Images für VMs |
| **nextcloud** | Nextcloud-Datenspeicher |
| **photos** | Fotobibliothek (Immich) |
| **system** | Systemdaten |

## Hinweise

- Array-Disks nutzen **XFS** als Dateisystem
- **LUKS-Verschlüsselung** aktiv – Keyfile: `/root/keyfile`
- Spindown-Delay: 0 (deaktiviert)
