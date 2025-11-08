#!/usr/bin/env python3
# Copyright 2025 LibreLane Contributors
#
# Adapted from OpenLane
#
# Copyright 2023 Efabless Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import yaml
import click
import shutil
from librelane.common.misc import mkdirp

from librelane.flows import Flow
from librelane.config import Macro

__dir__ = os.path.dirname(os.path.realpath(__file__))


@click.command(context_settings={"ignore_unknown_options": True})
@click.option("--pdk-root", type=click.Path(dir_okay=True, file_okay=False))
@click.option("--pdk", type=str)
@click.option("--run-tag", type=click.Path(dir_okay=True, file_okay=False))
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def main(
    pdk_root,
    pdk,
    run_tag,
    args,
):

    TargetFlow = Flow.factory.get("Classic")

    if 1:
        TargetFlow = Flow.factory.get("OpenInOpenROAD")

    ff_dir = os.path.join(__dir__, "src", "flipflop")
    ff_config_path = os.path.join(ff_dir, "config.yaml")
    ff_config = yaml.safe_load(open(ff_config_path))
    
    design_dir = os.path.join(__dir__, "src", "flipflop")
    mkdirp(design_dir)

    flow = TargetFlow(
        ff_config,
        design_dir = design_dir,
        pdk_root   = pdk_root,
        pdk        = pdk,
    )

    ff_state_out = flow.start(tag=run_tag)
    
    ff_macro = Macro.from_state(ff_state_out)
    ff_macro.instantiate("my_ff_1", (15, 15))
    ff_macro.instantiate("my_ff_2", (15, 45))
    ff_macro.instantiate("my_ff_3", (50, 15))
    ff_macro.instantiate("my_ff_4", (50, 45))

    print(ff_macro)
    
    aaa

    ####
    
    verilog_files = [
        os.path.join(__dir__, "src", "hold_violations_3.sv")
    ]
    
    # Flow configuration
    flow_cfg = {
        # Design
        "DESIGN_NAME"           : "hold_violations_3",

        # Sources
        "VERILOG_FILES"         : verilog_files,

        # Clock
        "CLOCK_PORT"            : "clk_i",
        "CLOCK_PERIOD"          : 10, # 10ns = 100MHz

        # Die area
        "FP_SIZING"             : "absolute",
        "DIE_AREA"              : [0, 0, 100, 100],
        "PL_TARGET_DENSITY_PCT" : 60,
        
        "MACROS": {"flipflop": ff_macro},
        
        "PDN_HOFFSET": 5,
        "PDN_HPITCH" : 12.4,
    }
    
    flow = TargetFlow(
        flow_cfg,
        design_dir = ".",
        pdk_root   = pdk_root,
        pdk        = pdk,
    )

    flow.start(tag=run_tag)

if __name__ == "__main__":
    main()
