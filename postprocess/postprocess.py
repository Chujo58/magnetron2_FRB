import matplotlib.pyplot as plt
import seaborn as sns
import json, os
import oscfar as ocf
import pandas as pd
from scipy.signal import peak_prominences
from findpeaks import findpeaks

np = ocf.np
sns.set_style("whitegrid")

# Argparse command line arguments
import argparse

parser = argparse.ArgumentParser(
    description="Post-process the results of the magnetron2_FRB model."
)

parser.add_argument(
    "--path", type=str, default="../output", help="Path to the results directory."
)
parser.add_argument("--event_id", type=str, help="Event ID for the results.")

args = parser.parse_args()
path = args.path
event_id = args.event_id

path_to_results = f"{path}/results_{event_id}"
os.chdir(path_to_results)
print(f"Changed directory to {path_to_results}\n{os.getcwd()}")


json_file = "temp.json"
# Load the json file:
with open(json_file, "r") as f:
    json_data = json.load(f)

time = json_data["times"]  # time array
profile = json_data["profile"]  # profile array

# Load the sample.txt
sample = np.loadtxt(f"posterior_sample.txt")

background = sample[:, 0]

# Number of dimensions for a single component
burst_dims = list(set(sample[:, 1]))[0]

# Maximum number of components allowed for the model
max_components = int(list(set(sample[:, 2]))[0])

# Now loading back the hyper parameters:
# hyper-parameter (mean) of the exponential distribution used
# as prior for the spike amplitudes
# NOTE: IN LINEAR SPACE, NOT LOG
hyper_mean_amplitude = sample[:, 3]

# hyper-parameter (mean) for the exponential distribution used
# as prior for the spike rise time
# NOTE: IN LINEAR SPACE, NOT LOG
hyper_mean_risetime = sample[:, 4]

# hyper-parameters for the lower and upper limits of the uniform
# distribution osed as a prior for the skew
hyper_lowerlimit_skew = sample[:, 7]
hyper_upperlimit_skew = sample[:, 8]

nbursts = sample[:, 9]

# individual burst parameters for all 100 components
npos = sample[:, 10 : 10 + max_components]  # peak position for all burst components
amp = sample[
    :, 10 + max_components : 10 + max_components * 2
]  # amplitude for all burst components
scale = sample[
    :, 10 + max_components * 2 : 10 + max_components * 3
]  # rise time for all burst components
skew = sample[
    :, 10 + max_components * 3 : 10 + max_components * 4
]  # skewness parameter for all burst

# put all of the parameters together
pars_all = np.array([npos, amp, scale, skew]).T

# # all of the mean models
ymodel_all = sample[:, -len(time) :]  # model flux
ymodel_mean = ymodel_all.mean(axis=0)  # mean model flux


# Do topology peak finding:
fp = findpeaks(method="topology", lookahead=1)
results = fp.fit(ymodel_mean)

fp.plot1d()
plt.savefig(f"topology_peak_finding.png")

df = results["df"]
peaks = df[df["peak"]][~df["valley"]]
temp = np.zeros(len(df))
prominences = peak_prominences(ymodel_mean, peaks["x"].tolist())[0]

for i, x in enumerate(peaks["x"].tolist()):
    temp[int(x)] = prominences[i]

df.insert(2, "prominence", temp)

filtered = df[df["peak"]][~df["valley"]][df["prominence"] > 0.1]
print(filtered)

df.insert(3, "keep", df["prominence"] > 0.1)

filtered.to_csv("filtered_peaks.csv", index=False)

df[df['peak'].astype(bool) & (~df['valley'].astype(bool))].to_csv("identified_peaks.csv", index=False)
df.to_csv("findpeaks_results.csv", index=False)

# Plot the model with the data:
plt.figure(figsize=(10, 6))
plt.plot(time, profile, label="Profile", color="black")
plt.plot(time, ymodel_mean, label="Mean Model", color="blue")
for p in filtered["x"].tolist():
    plt.axvline(
        x=time[p],
        color="red",
        linestyle="--",
        label="Peak" if p == filtered["x"].tolist()[0] else "",
    )
plt.legend()
plt.xlabel("Time (s)")
plt.ylabel("SNR")
plt.title(f"magnetron2_FRB output for Event ID {event_id}")
plt.savefig(f"model_with_data.png")

plt.figure(figsize=(10, 6))
u, c = np.unique(nbursts, return_counts=True)
plt.bar(u, c)
plt.xlabel("Number of components")
plt.ylabel("Count")
plt.title("Distribution of Number of components")
plt.savefig(f"number_of_bursts_distribution.png")
