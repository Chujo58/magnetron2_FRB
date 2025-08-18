#!/bin/bash

# Function to prepare the event with the given event ID:
prepare_event() {
    local event_id=$1
    echo "Preparing event with ID: $event_id"
    python load.py ${event_id}
}

# Function to run the post-processing script:
run_post_processing() {
    local event_id=$1
    echo "Running post-processing for event ID: $event_id"
    python showresults.py

    mkdir -p results_${event_id}

    mv log_prior_weights.txt "results_${event_id}/log_prior_weights_${event_id}.txt"
    mv weights.txt "results_${event_id}/weights_${event_id}.txt"
    mv posterior_sample.txt "results_${event_id}/posterior_sample_${event_id}.txt"

    mv levels.txt "results_${event_id}/levels_${event_id}.txt"
    mv sample_info.txt "results_${event_id}/sample_info_${event_id}.txt"
    mv sample.txt "results_${event_id}/sample_${event_id}.txt"
    
    cp temp.json "results_${event_id}/temp.json"
    cp OPTIONS "results_${event_id}/OPTIONS"
    cp main "results_${event_id}/main"
}

# Main script execution
if [ $# -ne 1 ]; then
    echo "Usage: $0 <event_id>"
    exit 1
fi

# For loop for running multiple events
for event_id in "$@"; do
    prepare_event $event_id
    ./main -t 16 # Assuming 16 threads for processing
    run_post_processing $event_id
done