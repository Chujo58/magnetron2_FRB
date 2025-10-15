#!/bin/bash

# Function to prepare the event with the given event ID:
prepare_event() {
    local event_id=$1
    echo "Preparing event with ID: $event_id"
    python load.py ${event_id}
}

load_temp(){
    local event_id=$1
    cp "${event_id}.json" "temp.json"
}

# Function to run the post-processing script:
run_post_processing() {
    local event_id=$1
    echo "Running post-processing for event ID: $event_id"
    python showresults.py

    path="../output/results_${event_id}"
    if [ ! -d "$path" ]; then
        mkdir -p "$path"
    fi

    mv log_prior_weights.txt "$path/log_prior_weights.txt"
    mv weights.txt "$path/weights.txt"
    mv posterior_sample.txt "$path/posterior_sample.txt"

    mv levels.txt "$path/levels.txt"
    mv sample_info.txt "$path/sample_info.txt"
    mv sample.txt "$path/sample.txt"

    cp temp.json "${path}/temp.json"
    cp OPTIONS "${path}/OPTIONS"
    cp main "${path}/main"

    cd ../postprocess
    python postprocess.py --event_id "${event_id}"
    cd ../code
}

# Main script execution
if [ $# -lt 2 ]; then
    echo "Usage: $0 <event_id> <num_cores>"
    exit 1
fi

load_temp $1
./main -t $2
run_post_processing $1

# For loop for running multiple events
#for event_id in "$@"; do
    #prepare_event $event_id
 #   load_temp $event_id
 #   ./main -t 16 # Assuming 16 threads for processing
 #   run_post_processing $event_id
#done
