## Repository Structure
- `code`: Contains the magnetron2_FRB model and C++ code.
- `include`: Contains the extra C++ library headers.
- `postprocess`: Contains the postprocessing code.
- `notebooks`: Contains Jupyter notebooks for postprocessing.

## How to run the model
### Create the input file for the code
The input file format needs to be `json`. Specifically, the `.json` file should contain:
- `profile`: contains the time profile of the FRB
- `times`: contains the times array of the FRB
- `std`: contains the standard deviation/error of the time profile
- `eid` (Optional): contains information on the event ID
- `npz` (Optional): contains the path to the `.npz` file (used for running [fitburst](https://github.com/CHIMEFRB/fitburst) afterwards)

<div style="padding: 2%; width: calc(100%-2*2%); background: #521515ff; border-radius: 10px;">
If you are running the code by hand in the CLI, you can name the file <b>temp.json</b>. Else please name the file <b>eventid.json</b> where eventid is the ID of the event you are loading.
</div>

You can also use the `load.py` script if you have `.npz` files containing your data (used for [fitburst](https://github.com/CHIMEFRB/fitburst)). This will load the data from the `eventid.npz` file. It also uses functions from [CHIMEFRB/baseband-analysis](https://github.com/CHIMEFRB/baseband-analysis) so make sure you have those packages installed. (You may need to also install [danielemichilli/DM_phase](https://github.com/danielemichilli/DM_phase)).
``` bash
python load.py eventid --path path_to_npz_files
```

### Running the model from the CLI by hand
1. Make sure your input file is called `temp.json`
2. Run the model: you can multithread this code by using the `-t` flag followed by a number of CPU cores you want to use.
``` bash
./main -t num_cpu_cores
```
3. Post-process the outputs: this script will create 3 plots
    - `model_with_data.png`: Time profile with highlighted peaks (prominence cutoff of 0.1 - [change here](https://github.com/Chujo58/magnetron2_FRB/blob/4388fe999644ffa70ef3cb9c88b3b88d88520f34/postprocess/postprocess.py#L106)) and final mean model
    - `number_of_bursts_distribution.png`: Distribution of the number of components in the posterior sample
    - `topology_peak_finding.png`: [findpeaks](https://erdogant.github.io/findpeaks/pages/html/index.html)'s topology peak finder results
``` bash
./postprocess.sh eventid
```

### Using the automated script
1. Make sure your input file is called `eventid.json`
2. Run the model using the shell script (uses 16 cores - [change here](https://github.com/Chujo58/magnetron2_FRB/blob/4388fe999644ffa70ef3cb9c88b3b88d88520f34/code/run.sh#L53)). Post-processing is done right after model is finished running.
``` bash
./run.sh eventid
```

For more information on the magnetron model, look into the [README.rst](https://github.com/Chujo58/magnetron2_FRB/blob/main/README.rst) file.