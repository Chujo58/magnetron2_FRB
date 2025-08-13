import sys, json

sys.path.insert(0, "/arc/home/clegue/DM_phase")
sys.path.append("/arc/home/clegue/baseband-analysis")

from baseband_analysis.dev import Morphology_utils as mu

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

reader = ocf.npz_reader(f"{path}/{eid}.npz")
writer = ocf.npz_writer(reader)
writer.save("temp.npz")

profile = mu.get_profile(reader.data_full)
times = reader.times
std = np.std(reader.data_full, 0)

with open("temp.json", "w") as f:
    json.dump(
        {"profile": list(profile), "times": list(times), "std": list(std), "eid": eid}, f, indent=4
    )
