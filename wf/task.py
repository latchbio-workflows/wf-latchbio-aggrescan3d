import subprocess
import sys
import time
from pathlib import Path
from typing import List, Optional

from latch.executions import rename_current_execution
from latch.functions.messages import message
from latch.resources.tasks import large_task, medium_task
from latch.types.directory import LatchDir, LatchOutputDir
from latch.types.file import LatchFile

sys.stdout.reconfigure(line_buffering=True)


@medium_task
def aggrescan3d_task(
    run_name: str,
    input_type: str,
    input_pdb: Optional[LatchFile] = None,
    input_pdb_folder: Optional[LatchDir] = None,
    output_directory: LatchOutputDir = LatchOutputDir("latch:///Aggrescan3D"),
    # dynamic: bool = False,
    distance: Optional[float] = None,
    cabs_config: Optional[str] = None,
    n_models: Optional[int] = None,
    verbose: int = 2,
    chain: Optional[str] = None,
) -> LatchOutputDir:
    rename_current_execution(str(run_name))

    print("-" * 60)
    print("Creating local directories")
    local_output_dir = Path(f"/root/outputs/{run_name}")
    local_output_dir.mkdir(parents=True, exist_ok=True)

    print("-" * 60)
    print("Preparing input files")
    input_files: List[Path] = []
    if input_type == "single_pdb" and input_pdb:
        input_files = [Path(input_pdb.local_path)]
    elif input_type == "pdb_folder" and input_pdb_folder:
        input_files = list(Path(input_pdb_folder.local_path).glob("*.pdb"))

    if not input_files:
        error_message = "No input PDB files found"
        print(error_message)
        message("error", {"title": "Aggrescan3D failed", "body": error_message})
        sys.exit(1)

    print(f"Found {len(input_files)} PDB file(s) to process")

    for input_file in input_files:
        print(f"Processing {input_file.name}")
        file_output_dir = local_output_dir / input_file.stem
        file_output_dir.mkdir(parents=True, exist_ok=True)

        command = [
            "aggrescan",
            "-i",
            str(input_file),
            "-w",
            str(file_output_dir),
            "-v",
            str(verbose),
        ]

        if distance:
            command.extend(["-D", str(distance)])
        # if dynamic:
        #     command.append("-d")
        if cabs_config:
            command.extend(["--cabs_config", cabs_config])
        if n_models:
            command.extend(["--n_models", str(n_models)])
        if chain:
            command.extend(["-C", chain])

        print(f"Running command: {' '.join(command)}")

        try:
            subprocess.run(command, check=True)
            print(f"Completed processing {input_file.name}")
        except Exception as e:
            error_message = f"Aggrescan3D failed for {input_file.name}: {e}"
            print(error_message)
            message("error", {"title": "Aggrescan3D failed", "body": error_message})
            continue

    print("-" * 60)
    print("Returning results")
    time.sleep(1000)
    return LatchOutputDir(str("/root/outputs"), output_directory.remote_path)
