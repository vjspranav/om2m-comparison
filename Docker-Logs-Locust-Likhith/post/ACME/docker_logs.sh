#!/bin/bash

CONTAINER_ID="279b3cf3c92b"  # Replace with your container ID
OUTPUT_FILE="/home/vaibhav/Docker-Logs-Locust-Likhith/post/ACME/Locust4/docker_stats_output.txt"

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
