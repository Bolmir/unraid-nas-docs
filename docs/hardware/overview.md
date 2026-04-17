# Hardware Übersicht

> Zuletzt aktualisiert: 2026-04-17

## System

| Komponente | Details |
|-----------|---------|
| **Hostname** | HOMELAB |
| **Betriebssystem** | Unraid 7.2.4 |
| **Kernel** | 6.12.54-Unraid |
| **CPU** | Intel Core i3-12100 (12th Gen, 4 Kerne / 8 Threads) |
| **RAM** | 32 GB |
| **Boot-Medium** | SanDisk USB 3.2 Gen1 (14.3 GB) |

## Festplatten

### Array-Festplatten

| Slot | Modell | Kapazität | Dateisystem | Belegung |
|------|--------|-----------|-------------|---------|
| Parity | Seagate ST12000VN0008 | 12 TB | — | Parität |
| Disk 1 | WD WD40EFZX-68AWUN0 | 4 TB | XFS | 2.1T / 3.7T (58%) |
| Disk 2 | WD WD40EFZX-68AWUN0 | 4 TB | XFS | 1.8T / 3.7T (50%) |

### Cache

| Gerät | Modell | Kapazität | Dateisystem | Belegung |
|-------|--------|-----------|-------------|---------|
| Cache | Samsung 970 EVO Plus 500GB (NVMe) | 500 GB | XFS | 205G / 466G (44%) |

### Array-Status

- **Status:** STARTED
- **Aktive Disks:** 3 (1 Parity + 2 Data)
- **Verschlüsselung:** LUKS aktiv (Keyfile: `/root/keyfile`)

## Netzwerk

| Interface | Typ | IP-Adresse |
|-----------|-----|-----------|
| `br0` (bond0/eth0) | Ethernet (Bonding) | 192.168.1.160/24 |
| Gateway | — | 192.168.1.1 |
| DNS | — | 192.168.1.1 |
