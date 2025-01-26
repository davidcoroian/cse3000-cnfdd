"""
Wrapper script for running cnfdd.

Authors:     David Coroian
Contact:     https://github.com/davidcoroian
Date:        2025-01-26
Maintainers: David Coroian
Version:     1.0
Copyright:   (C) 2025, David Coroian
License:     GPLv3
    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; version 3
    of the License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
    02110-1301, USA.

"""

# Expects 1 argument from cnfdd - the delta debugging test CNF instance

import sys
import pandas as pd
import subprocess as subp

# === Paths to I/O files and deps

# example paths
delta_debugger_project_path = "path/to/project_folder"
sharpvelvet_path = "path/to/SharpVelvet"

# path to sharpvelvet
velvet_path = sharpvelvet_path + "src/run_fuzzer.py"
# path to counter config (one tested, the rest for verifying result)
verif_counters_json_path = delta_debugger_project_path + "dd-configs/d4.json"
# path to instances.txt - the script prints the path to intermediate CNF instances 
# used by SharpVelvet
dd_output_instances_path = delta_debugger_project_path + "dd-instances/cnfdd_instances.txt"
# delta debugged counter name from .json file
debugged_counter = "d4"
# delta debugger timelimit per test
dd_test_timeout = "10"
# ====

def velvet_test_cnf():
  # run velvet
  subp.run(["python",
            velvet_path,
            "-c", 
            verif_counters_json_path,
            "-i", 
            dd_output_instances_path,
            "--timeout",
            dd_test_timeout
            ])

  # read velvet report
  dd_temp_velvet_report_path = sharpvelvet_path + "out/dd-temp_fuzz-results.csv"
  dd_test_report = pd.read_csv(dd_temp_velvet_report_path)

  # check if it triggered a bug in tested solver
  dd_test_result = False
  for report_instance in dd_test_report.itertuples(index=False):
    counter_name = report_instance.counter
    if counter_name == debugged_counter:
      if report_instance.timed_out == True:
        dd_test_result = True

  # CNFDD SPECIFIC
  if dd_test_result == True:
    sys.exit(0)
  else:
    sys.exit(1)

  # ---- end CNFDD SPECIFIC

  return dd_test_result


# PYTHON MAIN

dd_cnf_instance = sys.argv[1]

with open(dd_output_instances_path, "w") as cnfdd_file:
  print(dd_cnf_instance, file=cnfdd_file)

velvet_test_cnf()
