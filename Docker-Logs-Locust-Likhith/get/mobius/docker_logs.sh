#!/bin/bash

CONTAINER_ID="a0088cc599a5"  # Replace with your container ID
OUTPUT_FILE="/home/vaibhav/Docker-Logs-Locust-Likhith/mobius/Locust4/docker_stats_output.txt"
DURATION=$((30 * 60))  # 30 minutes in seconds

# Clear previous content of the output file
echo "" > "$OUTPUT_FILE"

# Calculate end time
END_TIME=$(( $(date +%s) + DURATION ))

# Loop until end time
while true; do
    # Get current stats and append to the output file
    docker stats --no-stream "$CONTAINER_ID" >> "$OUTPUT_FILE"
    sleep 5  # Capture stats every 5 seconds (adjust as needed)
done

