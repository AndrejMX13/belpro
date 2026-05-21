#!/bin/bash
# Start crond in the background (daemonises itself).
crond -l 2
# Start the ops notification server in the foreground (becomes the main process).
exec python3 /app/scripts/ops_server.py
