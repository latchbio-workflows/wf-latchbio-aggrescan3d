from typing import Optional

from latch.resources.launch_plan import LaunchPlan
from latch.resources.workflow import workflow
from latch.types.directory import LatchOutputDir
from latch.types.file import LatchFile
from latch.types.metadata import (
    LatchAuthor,
    LatchMetadata,
    LatchParameter,
    LatchRule,
    Params,
    Section,
    Spoiler,
    Text,
)

from wf.task import aggrescan3d_task

flow = [
    Section(
        "Input",
        Params(
            "input_pdb",
        ),
        Spoiler(
            "Analysis Options",
            Params(
                "dynamic",
                "distance",
                "cabs_config",
                "n_models",
                "verbose",
                "chain",
                # "movie",
            ),
        ),
    ),
    Section(
        "Output",
        Params("run_name"),
        Text("Directory for outputs"),
        Params("output_directory"),
    ),
]

metadata = LatchMetadata(
    display_name="Aggrescan3D",
    author=LatchAuthor(
        name="Aleksander Kuriata et al.",
    ),
    license="MIT",
    tags=["Protein Engineering"],
    parameters={
        "run_name": LatchParameter(
            display_name="Run Name",
            description="Name of run",
            batch_table_column=True,
            rules=[
                LatchRule(
                    regex=r"^[a-zA-Z0-9_-]+$",
                    message="Run name must contain only letters, digits, underscores, and dashes. No spaces are allowed.",
                )
            ],
        ),
        "input_pdb": LatchParameter(
            display_name="Input PDB",
            description="Input PDB file or PDB code for analysis",
            batch_table_column=True,
        ),
        "output_directory": LatchParameter(
            display_name="Output Directory",
            description="Directory to store the analysis results",
            batch_table_column=True,
        ),
        "dynamic": LatchParameter(
            display_name="Dynamic Analysis",
            description="Use the dynamic module for the simulation",
        ),
        "distance": LatchParameter(
            display_name="Distance Cutoff",
            description="Distance cutoff for naccess calculations",
        ),
        "cabs_config": LatchParameter(
            display_name="CABS Config",
            description="Configuration file for CABS-flex",
        ),
        "n_models": LatchParameter(
            display_name="Number of Models",
            description="Number of models to generate in dynamic analysis",
        ),
        "verbose": LatchParameter(
            display_name="Verbosity",
            description="Verbosity level (0-4)",
        ),
        "chain": LatchParameter(
            display_name="Chain",
            description="Specific chain to analyze",
        ),
        # "movie": LatchParameter(
        #     display_name="Generate Movie",
        #     description="Generate a movie of the result (mp4 or webm)",
        # ),
    },
    flow=flow,
)


@workflow(metadata)
def aggrescan3d_workflow(
    run_name: str,
    input_pdb: LatchFile,
    output_directory: LatchOutputDir = LatchOutputDir("latch:///Aggrescan3D"),
    dynamic: bool = False,
    distance: Optional[float] = None,
    cabs_config: Optional[str] = None,
    n_models: Optional[int] = None,
    verbose: int = 2,
    chain: Optional[str] = None,
    # movie: Optional[str] = None,
) -> LatchOutputDir:
    """
    Aggrescan3D (A3D) 2.0 is a structure-based prediction tool for protein aggregation properties, taking into account the dynamic fluctuations of proteins.

    <p align="center">
    <img src="https://user-images.githubusercontent.com/31255434/182289305-4cc620e3-86ae-480f-9b61-6ca83283caa5.jpg" alt="Latch Verified" width="100">
    </p>
    <p align="center">
    <strong>
    Latch Verified
    </strong>
    </p>

    ## Overview

    Protein aggregation is a critical issue in various human disorders and poses a significant challenge in the production of therapeutic proteins. Aggrescan3D 2.0 addresses this need by providing an in-silico method to predict the aggregative properties of protein variants associated with diseases and assist in the engineering of soluble protein-based drugs.

    ## Key Features

    - Structure-based prediction of protein aggregation properties
    - Consideration of dynamic protein fluctuations
    - Extension to larger and multimeric proteins
    - Simultaneous prediction of changes in protein solubility and stability upon mutation
    - Rapid screening for functional protein variants with improved solubility
    - REST-ful service for integration into automatic pipelines
    - Enhanced web server interface

    ## Performance
    Aggrescan3D 2.0 has been successfully applied in numerous studies of protein structure-aggregation relationships. The extended capabilities for larger and multimeric proteins, along with the simultaneous prediction of solubility and stability changes, make it a powerful tool for both basic research and biotechnological applications.

    ## Credits
    Aleksander Kuriata, Valentin Iglesias, Jordi Pujols, Mateusz Kurcinski, Sebastian Kmiecik, Salvador Ventura,
    Aggrescan3D (A3D) 2.0: prediction and engineering of protein solubility,
    Nucleic Acids Research, Volume 47, Issue W1, 02 July 2019, Pages W300–W307,
    https://doi.org/10.1093/nar/gkz321

    """
    return aggrescan3d_task(
        run_name=run_name,
        input_pdb=input_pdb,
        output_directory=output_directory,
        dynamic=dynamic,
        distance=distance,
        cabs_config=cabs_config,
        n_models=n_models,
        verbose=verbose,
        chain=chain,
        # movie=movie,
    )


LaunchPlan(
    aggrescan3d_workflow,
    "2gb1 Protein Example",
    {
        "run_name": "2gb1_protein",
        "input_pdb": LatchFile(
            "s3://latch-public/proteinengineering/aggrescan3d/2gb1.pdb"
        ),
    },
)
