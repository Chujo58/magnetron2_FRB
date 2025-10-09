#!/bin/bash

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
if [ $# -lt 1 ]; then
    echo "Usage: $0 <event_id>"
    exit 1
fi

# For loop for running multiple events
for event_id in "$@"; do
    run_post_processing $event_id
done
