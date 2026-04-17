#!/bin/bash
# Wöchentliches Dokumentations-Update
# Wird durch Unraid User Scripts jeden Montag um 03:00 UTC ausgeführt

set -e
DOCS_DIR="/root/unraid-nas-docs"
LOG="$DOCS_DIR/scripts/update.log"

log() { echo "[$(date '+%Y-%m-%d %H:%M')] $1" >> "$LOG"; }

log "=== Update gestartet ==="

source "$DOCS_DIR/.env"
cd "$DOCS_DIR"
git pull origin main >> "$LOG" 2>&1

# Wiki-Repo aktualisieren
WIKI_DIR="/tmp/wiki-update-auto"
rm -rf "$WIKI_DIR"
git clone https://${GITHUB_TOKEN}@github.com/Bolmir/unraid-nas-docs.wiki.git "$WIKI_DIR" >> "$LOG" 2>&1
cd "$WIKI_DIR"
git config user.email "patrick@gschwend.one"
git config user.name "Claude AI (Auto-Update)"

# ── Systemdaten sammeln ──────────────────────────────────────────
DATE=$(date '+%Y-%m-%d')
UNRAID_VERSION=$(cat /etc/unraid-version | grep version | cut -d'"' -f2)
KERNEL=$(uname -r)
CPU=$(grep "model name" /proc/cpuinfo | head -1 | cut -d: -f2 | xargs)
RAM_TOTAL=$(free -h | grep Mem | awk '{print $2}')
RAM_USED=$(free -h | grep Mem | awk '{print $3}')
UPTIME=$(uptime -p)
LOAD=$(cat /proc/loadavg | cut -d' ' -f1-3)
ARRAY_STATE=$(mdcmd status 2>/dev/null | grep "^mdState=" | cut -d= -f2)

RUNNING=$(docker ps -q 2>/dev/null | wc -l | tr -d ' ')
STOPPED=$(docker ps -aq --filter "status=exited" 2>/dev/null | wc -l | tr -d ' ')
TOTAL=$(docker ps -aq 2>/dev/null | wc -l | tr -d ' ')

# Disk-Belegung
DISK1_USE=$(df -h /mnt/disk1 2>/dev/null | awk 'NR==2{print $3}')
DISK1_SIZE=$(df -h /mnt/disk1 2>/dev/null | awk 'NR==2{print $2}')
DISK1_PCT=$(df /mnt/disk1 2>/dev/null | awk 'NR==2{print $5}' | tr -d '%')
DISK2_USE=$(df -h /mnt/disk2 2>/dev/null | awk 'NR==2{print $3}')
DISK2_SIZE=$(df -h /mnt/disk2 2>/dev/null | awk 'NR==2{print $2}')
DISK2_PCT=$(df /mnt/disk2 2>/dev/null | awk 'NR==2{print $5}' | tr -d '%')
CACHE_USE=$(df -h /mnt/cache 2>/dev/null | awk 'NR==2{print $3}')
CACHE_SIZE=$(df -h /mnt/cache 2>/dev/null | awk 'NR==2{print $2}')
CACHE_PCT=$(df /mnt/cache 2>/dev/null | awk 'NR==2{print $5}' | tr -d '%')

log "Systemdaten: Unraid $UNRAID_VERSION | Array: $ARRAY_STATE | Container: $RUNNING laufend, $STOPPED gestoppt"
log "Disks: Disk1 $DISK1_USE/$DISK1_SIZE ($DISK1_PCT%) | Disk2 $DISK2_USE/$DISK2_SIZE ($DISK2_PCT%) | Cache $CACHE_USE/$CACHE_SIZE ($CACHE_PCT%)"

# Snapshot speichern
mkdir -p "$DOCS_DIR/scripts/data"
cat > "$DOCS_DIR/scripts/data/snapshot.txt" << SNAP
DATE=$DATE
UNRAID_VERSION=$UNRAID_VERSION
KERNEL=$KERNEL
ARRAY_STATE=$ARRAY_STATE
RUNNING=$RUNNING
STOPPED=$STOPPED
TOTAL=$TOTAL
DISK1=$DISK1_USE/$DISK1_SIZE (${DISK1_PCT}%)
DISK2=$DISK2_USE/$DISK2_SIZE (${DISK2_PCT}%)
CACHE=$CACHE_USE/$CACHE_SIZE (${CACHE_PCT}%)
LOAD=$LOAD
UPTIME=$UPTIME
SNAP

# ── Docs aktualisieren ───────────────────────────────────────────

# 1. Datum "Zuletzt aktualisiert" in allen Docs
find "$WIKI_DIR" -name "*.md" -exec \
    sed -i "s/Zuletzt aktualisiert: [0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}/Zuletzt aktualisiert: $DATE/g" {} \;

# 2. Unraid-Version
sed -i "s/Unraid [0-9]\+\.[0-9]\+\.[0-9]\+/Unraid $UNRAID_VERSION/g" \
    "$WIKI_DIR/Hardware.md" \
    "$WIKI_DIR/Home.md" 2>/dev/null || true

# 3. Kernel
sed -i "s|[0-9]\+\.[0-9]\+\.[0-9]\+-Unraid|$KERNEL|g" \
    "$WIKI_DIR/Hardware.md" 2>/dev/null || true

# 4. Disk-Belegung in Hardware.md
sed -i "s/| Disk 1 | WD WD40EFZX-68AWUN0 | 4 TB | XFS | .* |/| Disk 1 | WD WD40EFZX-68AWUN0 | 4 TB | XFS | $DISK1_USE \/ $DISK1_SIZE (${DISK1_PCT}%) |/" \
    "$WIKI_DIR/Hardware.md" 2>/dev/null || true
sed -i "s/| Disk 2 | WD WD40EFZX-68AWUN0 | 4 TB | XFS | .* |/| Disk 2 | WD WD40EFZX-68AWUN0 | 4 TB | XFS | $DISK2_USE \/ $DISK2_SIZE (${DISK2_PCT}%) |/" \
    "$WIKI_DIR/Hardware.md" 2>/dev/null || true
sed -i "s/| Cache | Samsung 970 EVO Plus 500GB (NVMe) | 500 GB | XFS | .* |/| Cache | Samsung 970 EVO Plus 500GB (NVMe) | 500 GB | XFS | $CACHE_USE \/ $CACHE_SIZE (${CACHE_PCT}%) |/" \
    "$WIKI_DIR/Hardware.md" 2>/dev/null || true

# 5. Container-Anzahl in Home.md
sed -i "s/| \*\*Container\*\* | [0-9]* ([0-9]* aktiv) |/| **Container** | $TOTAL ($RUNNING aktiv) |/" \
    "$WIKI_DIR/Home.md" 2>/dev/null || true

# 6. Container-Zusammenfassung in Docker-Container.md
sed -i "s/\*\*Gesamt:\*\* [0-9]* Container ([0-9]* laufend, [0-9]* gestoppt)/**Gesamt:** $TOTAL Container ($RUNNING laufend, $STOPPED gestoppt)/" \
    "$WIKI_DIR/Docker-Container.md" 2>/dev/null || true

# 7. Disk-Belegung in Backup-und-Wartung.md
sed -i "s/| Disk 1 | WD WD40EFZX-68AWUN0 | 4 TB | [0-9]*% belegt |/| Disk 1 | WD WD40EFZX-68AWUN0 | 4 TB | ${DISK1_PCT}% belegt |/" \
    "$WIKI_DIR/Backup-und-Wartung.md" 2>/dev/null || true
sed -i "s/| Disk 2 | WD WD40EFZX-68AWUN0 | 4 TB | [0-9]*% belegt |/| Disk 2 | WD WD40EFZX-68AWUN0 | 4 TB | ${DISK2_PCT}% belegt |/" \
    "$WIKI_DIR/Backup-und-Wartung.md" 2>/dev/null || true
sed -i "s/| Cache | Samsung 970 EVO Plus | 500 GB | [0-9]*% belegt |/| Cache | Samsung 970 EVO Plus | 500 GB | ${CACHE_PCT}% belegt |/" \
    "$WIKI_DIR/Backup-und-Wartung.md" 2>/dev/null || true

log "Wiki-Dateien aktualisiert"

# ── Wiki-Repo pushen ─────────────────────────────────────────────
cd "$WIKI_DIR"
if git diff --quiet; then
    log "Wiki: Keine Änderungen"
else
    git add -A
    git commit -m "Auto-Update $DATE: Disk ${DISK1_PCT}%/${DISK2_PCT}%/${CACHE_PCT}% | Container $RUNNING/$TOTAL | Unraid $UNRAID_VERSION"
    git push origin master >> "$LOG" 2>&1
    log "Wiki gepusht zu GitHub ✓"
fi

# ── Haupt-Repo pushen (Snapshot) ─────────────────────────────────
cd "$DOCS_DIR"
if git diff --quiet && git diff --cached --quiet; then
    log "Repo: Keine Änderungen"
else
    git add -A
    git commit -m "Auto-Update $DATE: Snapshot aktualisiert"
    git push origin main >> "$LOG" 2>&1
    log "Repo gepusht zu GitHub ✓"
fi

log "=== Update abgeschlossen ==="
