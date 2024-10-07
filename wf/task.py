import subprocess
import sys
import time
from pathlib import Path

from latch.executions import rename_current_execution
from latch.resources.tasks import small_task
from latch.types.directory import LatchOutputDir
from latch.types.file import LatchFile

sys.stdout.reconfigure(line_buffering=True)


@small_task
def task(
    run_name: str, input_file: LatchFile, output_directory: LatchOutputDir
) -> LatchOutputDir:
    rename_current_execution(str(run_name))

    print("-" * 60)
    print("Creating local directories")
    local_output_dir = Path(f"/root/outputs/{run_name}")
    local_output_dir.mkdir(parents=True, exist_ok=True)

    print("Running Aggrescan3D")
    command = f"""
        source /opt/conda/bin/activate aggrescan3d_env && \
        aggrescan -i 2gb1 -w {local_output_dir} -v 4
    """

    try:
        subprocess.run(command, shell=True, executable="/bin/bash")
        print("Done")
    except Exception as e:
        print("FAILED")
        print(e)
        time.sleep(6000)

    print("Returning results")
    return LatchOutputDir(str("/root/outputs"), output_directory.remote_path)
