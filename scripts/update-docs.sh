#!/bin/bash
# Sammelt aktuelle Systeminfos und schreibt sie in temporäre Dateien
# Wird von Claude Code aufgerufen um die Docs zu aktualisieren

DOCS_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DATA_DIR="$DOCS_DIR/scripts/data"
mkdir -p "$DATA_DIR"

echo "[$(date)] Sammle Systemdaten..."

# Unraid Version & System
cat > "$DATA_DIR/system.txt" << EOF
UNRAID_VERSION=$(cat /etc/unraid-version 2>/dev/null | grep version | cut -d'"' -f2)
HOSTNAME=$(hostname)
KERNEL=$(uname -r)
CPU=$(grep "model name" /proc/cpuinfo | head -1 | cut -d: -f2 | xargs)
RAM_TOTAL=$(free -h | grep Mem | awk '{print $2}')
RAM_USED=$(free -h | grep Mem | awk '{print $3}')
UPTIME=$(uptime -p)
LOAD=$(cat /proc/loadavg | cut -d' ' -f1-3)
EOF

# Disk-Nutzung
df -h /mnt/disk1 /mnt/disk2 /mnt/cache 2>/dev/null > "$DATA_DIR/disk_usage.txt"

# Array-Status
mdcmd status 2>/dev/null > "$DATA_DIR/array_status.txt"

# Docker Container
docker ps -a --format "{{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null > "$DATA_DIR/containers.txt"

# Docker Container Anzahl
RUNNING=$(docker ps -q 2>/dev/null | wc -l)
STOPPED=$(docker ps -aq --filter "status=exited" 2>/dev/null | wc -l)
echo "RUNNING=$RUNNING" > "$DATA_DIR/container_stats.txt"
echo "STOPPED=$STOPPED" >> "$DATA_DIR/container_stats.txt"

echo "[$(date)] Systemdaten gesammelt in $DATA_DIR"
echo "Übergebe an Claude Code zur Dokumentations-Aktualisierung..."
