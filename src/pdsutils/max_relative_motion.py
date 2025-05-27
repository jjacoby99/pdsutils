import warnings
# ignore only the "delim_whitespace" FutureWarning from pandas parsers
warnings.filterwarnings(
    "ignore",
    category=FutureWarning,
    message="The 'delim_whitespace' keyword in pd.read_csv is deprecated.*"
)

import numpy as np
import pandas as pd
import os
import re
from typing import List, Optional, Sequence, Dict 

def maximum_relative_motion(base_folder: str,
                            cases: List[int],
                            reals: List[int],
                            rb_names: List[str],
                            ts: float,
                            axes: Optional[Sequence[str]] = None) -> Dict:
    """
    Analyses a set of result folders (Case0x/Realization00y/Results)
    and finds the maximum relative motion (x/y/z/roll/pitch/yaw between adjacent
    rigid bodies in the chain. The chain order is defined by the order of 
    names provided in rb_names

    @Params:
      base_folder: root folder containing Case0?/Realization00?/Results
      cases:       list of case numbers (1–9) (eg [1, 3, 4, 5, 8])
      reals:       list of realization numbers (1–9) (eg [2,3,5])
      rb_names:    list of rigid-body names, e.g. ["Walkway1",...,"Walkway50"]
      ts:          start time (seconds) to skip initial transients
      axes:        which relative motions to check (any subset of ["x", "y", "z", "roll", "pitch" "yaw"])

    @Returns:
      A dict containing a map of each axis of interest to the relevant statistics from the analysis
      For example, when calculating maximum relative yaw, the result would be
      {"yaw":{"max": maximum_relative_yaw,
              "time": time_of_max_relative_yaw,
              "idx": index of max_relative_yaw in chain (if max relative yaw occurs between bodies 5 and 6, idx = 5),
              "which": realization string indicating realization of max occurrence (eg "Case05, Realization003")
             }}
    """
    if axes is None:
        axes = ["x", "y", "z", "roll", "pitch", "yaw"]

    valid = {"x", "y", "z", "roll", "pitch", "yaw"}
    if not set(axes) <= valid:
        bad = set(axes) - valid
        raise ValueError(f"Unknown axis(es): {bad}; choose from {valid}")

    # constants for column prefixes
    T_NAME   = "t(sec)"
    X_PFX    = "x(m)"
    Y_PFX    = "y(m)"
    Z_PFX    = "z(m)"
    ROLL_PFX = "roll(deg)"
    PITCH_PFX= "pitch(deg)"
    YAW_PFX  = "yaw(deg)"

    prefix_map = {"x"     : X_PFX,
                  "y"     : Y_PFX,
                  "z"     : Z_PFX,
                  "roll"  : ROLL_PFX,
                  "pitch" : PITCH_PFX,
                  "yaw"   : YAW_PFX}
    col_index =  {"x"     : 1,
                  "y"     : 2,       
                  "z"     : 3,
                  "roll"  : 4,
                  "pitch" : 5,
                  "yaw"   : 6}
    
    
    # helper to pull the integer suffix off an rb_name
    def extract_index(name: str) -> int:
        m = re.search(r"(\d+)$", name)
        if not m:
            raise ValueError(f"Couldn’t parse numeric suffix from '{name}'")
        return int(m.group(1))

    # initialize trackers
    stats = {
        ax: {"max": 0.0, "time": 0.0, "idx": None, "which": ""}
        for ax in axes
        }

    # sanity-check cases and reals
    for c in cases:
        if not  (1 <= c <= 9):
            raise RuntimeError(f"Provided case list contained a case not in [1, 9]: {c}")
    for r in reals:
        if not  (1 <= c <= 9):
            raise RuntimeError(f"Provided case list contained a realization not in [1, 9]: {r}")

    for case in cases:
        for real in reals:
            tag = f"Case0{case}, Realization00{real}"

            # build the DataFrame for this realization
            dfs = []
            for i, rb in enumerate(rb_names):
                rb_idx = extract_index(rb)
                fn = os.path.join(base_folder,
                                  f"Case0{case}",
                                  f"Realization00{real}",
                                  "Results",
                                  rb,
                                  "position.dat")

                # first body: read time + [motions]
                if i == 0:
                    usecols = [0] + [col_index[ax] for ax in axes]
                    names = [T_NAME] + [f"{prefix_map[ax]}{rb_idx}" for ax in axes]
                    dfs.append(
                        pd.read_csv(fn,
                                    delim_whitespace=True,
                                    engine="c",
                                    skiprows=2 + int(ts / 0.1),
                                    usecols=usecols,
                                    names=names)
                    )
                else:
                    usecols = [col_index[ax] for ax in axes]
                    names = [f"{prefix_map[ax]}{rb_idx}" for ax in axes]
                    dfs.append(
                        pd.read_csv(fn,
                                    delim_whitespace=True,
                                    engine="c",
                                    skiprows=2 + int(ts / 0.1),
                                    usecols=usecols,
                                    names=names)
                    )

            df = pd.concat(dfs, axis=1)

            # inner helper to find max adjacent diff for a given prefix
            def check_axis(prefix: str, key: str):
                # filter & numeric‐sort columns
                cols = df.filter(regex=rf"^{re.escape(prefix)}\d+$").columns
                
                sub = df[cols]

                # adjacent absolute differences
                diffs = sub.diff(axis=1).iloc[:, 1:].abs().values
                flat = diffs.argmax()
                t_idx, pair_idx = divmod(flat, diffs.shape[1])
                max_val = diffs[t_idx, pair_idx]
                time_val = df[T_NAME].iat[t_idx]
                first_col = cols[pair_idx]
                idx_val   = extract_index(first_col)

                # update global if bigger
                if max_val > stats[key]["max"]:
                    stats[key].update({
                        "max":   max_val,
                        "time":  time_val,
                        "idx":   idx_val,
                        "which": tag
                    })

            # check yaw, pitch, roll
            for ax in axes:
                check_axis(prefix_map[ax], ax)
    return stats
