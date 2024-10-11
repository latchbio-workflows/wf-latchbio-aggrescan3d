import subprocess
import sys
from pathlib import Path
from typing import Optional

from latch.executions import rename_current_execution
from latch.functions.messages import message
from latch.resources.tasks import small_task
from latch.types.directory import LatchOutputDir
from latch.types.file import LatchFile

sys.stdout.reconfigure(line_buffering=True)


@small_task
def aggrescan3d_task(
    run_name: str,
    input_pdb: LatchFile,
    output_directory: LatchOutputDir,
    dynamic: bool = False,
    distance: Optional[float] = None,
    cabs_config: Optional[str] = None,
    n_models: Optional[int] = None,
    verbose: int = 2,
    chain: Optional[str] = None,
    # movie: Optional[str] = None,
    # auto_mutation: Optional[str] = None,
) -> LatchOutputDir:
    rename_current_execution(str(run_name))

    print("-" * 60)
    print("Creating local directories")
    local_output_dir = Path(f"/root/outputs/{run_name}")
    local_output_dir.mkdir(parents=True, exist_ok=True)

    print("-" * 60)
    print("Running Aggrescan3D")
    # command = f"""
    #     source /opt/conda/bin/activate aggrescan3d_env && \
    #     aggrescan -i 2gb1 -w {local_output_dir} -v 4
    # """
    command = [
        "aggrescan",
        "-i",
        str(input_pdb.local_path),
        "-w",
        str(local_output_dir),
        "-v",
        str(verbose),
    ]

    if distance:
        command.extend(["-D", str(distance)])
    if dynamic:
        command.append("-d")
    if cabs_config:
        command.extend(["--cabs_config", cabs_config])
    if n_models:
        command.extend(["--n_models", str(n_models)])
    if chain:
        command.extend(["-C", chain])
    # if movie:
    #     command.extend(["-M", movie])
    # if auto_mutation:
    #     command.extend(["-am", auto_mutation])

    print(f"Running command: {' '.join(command)}")

    try:
        subprocess.run(command, check=True)
        print("Done")
    except Exception as e:
        print("FAILED")
        message("error", {"title": "Aggrescan3D failed", "body": f"{e}"})
        sys.exit(1)

    print("-" * 60)
    print("Returning results")
    return LatchOutputDir(str("/root/outputs"), output_directory.remote_path)
