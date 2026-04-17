#!/bin/bash
# Wöchentliches Dokumentations-Update via Claude Code
# Wird durch Unraid User Scripts ausgeführt

set -e
DOCS_DIR="/root/unraid-nas-docs"
LOG="$DOCS_DIR/scripts/update.log"

echo "[$(date '+%Y-%m-%d %H:%M')] === Update gestartet ===" >> "$LOG"

# GitHub-Token laden
source "$DOCS_DIR/.env"
cd "$DOCS_DIR"

# Remote auf aktuellen Stand bringen
git pull origin main >> "$LOG" 2>&1

# ── Systemdaten sammeln ──────────────────────────────────────────
UNRAID_VERSION=$(cat /etc/unraid-version | grep version | cut -d'"' -f2)
HOSTNAME=$(hostname)
KERNEL=$(uname -r)
CPU=$(grep "model name" /proc/cpuinfo | head -1 | cut -d: -f2 | xargs)
RAM_TOTAL=$(free -h | grep Mem | awk '{print $2}')
RAM_USED=$(free -h | grep Mem | awk '{print $3}')
UPTIME=$(uptime -p)
LOAD=$(cat /proc/loadavg | cut -d' ' -f1-3)
DATE=$(date '+%Y-%m-%d')

DISK_USAGE=$(df -h /mnt/disk1 /mnt/disk2 /mnt/cache 2>/dev/null)
ARRAY_STATE=$(mdcmd status 2>/dev/null | grep "^mdState=" | cut -d= -f2)
CONTAINERS=$(docker ps -a --format "{{.Names}}\t{{.Status}}" 2>/dev/null)
RUNNING=$(docker ps -q 2>/dev/null | wc -l)
STOPPED=$(docker ps -aq --filter "status=exited" 2>/dev/null | wc -l)

# Snapshot-Datei für Nachvollziehbarkeit speichern
mkdir -p "$DOCS_DIR/scripts/data"
cat > "$DOCS_DIR/scripts/data/snapshot.txt" << SNAPSHOT
DATE=$DATE
UNRAID_VERSION=$UNRAID_VERSION
HOSTNAME=$HOSTNAME
KERNEL=$KERNEL
CPU=$CPU
RAM_TOTAL=$RAM_TOTAL
RAM_USED=$RAM_USED
UPTIME=$UPTIME
LOAD=$LOAD
ARRAY_STATE=$ARRAY_STATE
CONTAINERS_RUNNING=$RUNNING
CONTAINERS_STOPPED=$STOPPED

DISK_USAGE:
$DISK_USAGE

CONTAINERS:
$CONTAINERS
SNAPSHOT

echo "[$(date '+%Y-%m-%d %H:%M')] Systemdaten gesammelt" >> "$LOG"

# ── Claude aktualisiert die Dokumentation ────────────────────────
PROMPT="Du bist ein Dokumentations-Assistent für ein Unraid NAS namens HOMELAB.

Heute ist: $DATE
Die Dokumentation liegt in: /root/unraid-nas-docs/docs/

Aktuelle Systemdaten:
- Unraid Version: $UNRAID_VERSION
- Kernel: $KERNEL
- Uptime: $UPTIME
- Load: $LOAD
- RAM: $RAM_USED von $RAM_TOTAL verwendet
- Array-Status: $ARRAY_STATE
- Docker-Container: $RUNNING laufend, $STOPPED gestoppt

Festplatten-Belegung:
$DISK_USAGE

Docker-Container-Status:
$CONTAINERS

Aufgaben:
1. Aktualisiere das Datum 'Zuletzt aktualisiert' auf $DATE in allen docs/-Dateien
2. Aktualisiere die Disk-Belegungszahlen in docs/hardware/overview.md und docs/maintenance/backup.md
3. Aktualisiere die Container-Anzahl (laufend/gestoppt) in docs/services/docker-containers.md und docs/index.md
4. Falls sich Container-Status geändert hat (✅/❌), aktualisiere docs/services/docker-containers.md
5. Prüfe ob Unraid-Version in docs/hardware/overview.md korrekt ist ($UNRAID_VERSION)
6. Mache NUR Änderungen die durch die obigen Daten begründet sind. Keine inhaltlichen Umstrukturierungen.

Führe alle notwendigen Datei-Änderungen durch und antworte am Ende mit einer kurzen Zusammenfassung was du geändert hast."

echo "[$(date '+%Y-%m-%d %H:%M')] Claude wird aufgerufen..." >> "$LOG"
CHANGES=$(echo "$PROMPT" | claude --print 2>> "$LOG")
echo "[$(date '+%Y-%m-%d %H:%M')] Claude fertig: $CHANGES" >> "$LOG"

# ── Git commit & push ─────────────────────────────────────────────
git config user.email "patrick@gschwend.one"
git config user.name "Claude AI (Auto-Update)"

if git diff --quiet && git diff --cached --quiet; then
    echo "[$(date '+%Y-%m-%d %H:%M')] Keine Änderungen – kein Commit nötig" >> "$LOG"
else
    git add -A
    git commit -m "Auto-Update $DATE: Systemdaten aktualisiert"
    git push origin main >> "$LOG" 2>&1
    echo "[$(date '+%Y-%m-%d %H:%M')] Gepusht zu GitHub" >> "$LOG"
fi

echo "[$(date '+%Y-%m-%d %H:%M')] === Update abgeschlossen ===" >> "$LOG"
