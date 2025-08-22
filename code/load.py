import sys, json

sys.path.insert(0, "/arc/home/clegue/DM_phase")
sys.path.append("/arc/home/clegue/baseband-analysis")

from baseband_analysis.dev import Morphology_utils as mu

# from reload_npz_data import reload

import oscfar as ocf
import argparse

np = ocf.np

parser = argparse.ArgumentParser(description="Argument parser")
parser.add_argument("event", type=int, help="EventID")
parser.add_argument(
    "--path",
    type=str,
    default="/arc/home/clegue/auto-bb-fitburst/npz",
    help="Path where npz files are stored with format event_id.npz.",
)

args = parser.parse_args()
eid = args.event
path = args.path

try:
    npz_path = f"{path}/{eid}.npz"
    reader = ocf.npz_reader(npz_path)
except FileNotFoundError:
    print(f"File {npz_path} not found. Please check the path and event ID.")
    sys.exit(1)

profile = mu.get_profile(reader.data_full)
times = reader.times
std = np.std(reader.data_full, 0)

with open(f"{eid}.json", "w") as f:
    json.dump(
        {
            "profile": list(profile),
            "times": list(times),
            "std": list(std),
            "eid": eid,
            "npz": npz_path,
        },
        f,
        indent=4,
    )
