from typing import Optional

from latch.resources.launch_plan import LaunchPlan
from latch.resources.workflow import workflow
from latch.types.directory import LatchDir, LatchOutputDir
from latch.types.file import LatchFile
from latch.types.metadata import (Fork, ForkBranch, LatchAuthor, LatchMetadata,
                                  LatchParameter, LatchRule, Params, Section,
                                  Spoiler, Text)

from wf.task import aggrescan3d_task

flow = [
    Section(
        "Input",
        Fork(
            "input_type",
            "Choose input type",
            single_pdb=ForkBranch(
                "Single PDB File",
                Params("input_pdb"),
            ),
            pdb_folder=ForkBranch(
                "Folder of PDB Files",
                Params("input_pdb_folder"),
            ),
        ),
        Spoiler(
            "Analysis Options",
            Params(
                # "dynamic",
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
    repository="https://github.com/latchbio-workflows/wf-latchbio-aggrescan3d",
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
        "input_type": LatchParameter(),
        "input_pdb": LatchParameter(
            display_name="Input PDB",
            description="Input PDB file or PDB code for analysis",
            batch_table_column=True,
        ),
        "input_pdb_folder": LatchParameter(
            display_name="Input PDB Folder",
            description="Folder containing multiple PDB files for analysis",
            batch_table_column=True,
        ),
        "output_directory": LatchParameter(
            display_name="Output Directory",
            description="Directory to store the analysis results",
            batch_table_column=True,
        ),
        # "dynamic": LatchParameter(
        #     display_name="Dynamic Analysis",
        #     description="Use the dynamic module for the simulation",
        # ),
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
    # movie: Optional[str] = None,
) -> LatchOutputDir:
    """
    Aggrescan3D (A3D) 2.0: tructure-based prediction tool for protein aggregation properties

    <p align="center">
        <img src="https://media.springernature.com/lw685/springer-static/image/chp%3A10.1007%2F978-1-4939-7756-7_21/MediaObjects/421474_1_En_21_Fig4_HTML.gif" alt="Aggrescan figure" width="800px"/>
    </p>

    <p align="center">
    <img src="https://user-images.githubusercontent.com/31255434/182289305-4cc620e3-86ae-480f-9b61-6ca83283caa5.jpg" alt="Latch Verified" width="100">
    </p>
    <p align="center">
    <strong>
    Latch Verified
    </strong>
    </p>

    ## Aggrescan3D

    Protein aggregation is a critical issue in various human disorders and poses a significant challenge in the production of therapeutic proteins. Aggrescan3D (A3D) 2.0 addresses this need by providing an in-silico method to predict the aggregation propensities of proteins in their folded states, assisting in the engineering of soluble protein-based drugs and the study of disease-associated protein variants.

    Aggrescan3D uses protein 3D-structures in PDB format as input, derived from X-ray diffraction, solution NMR, or modeling approaches. The structures are energetically minimized before analysis. The method projects an experimentally derived intrinsic aggregation propensity scale for natural amino acids onto the protein 3D structure.

    A3D calculates the aggregation propensity for spherical regions centered on every residue Cα carbon, providing a unique structurally corrected aggregation value (A3D score) for each amino acid in the structure. It focuses on protein surfaces, discarding the negligible contribution of highly hydrophobic residues hidden in the core of folded proteins.

    This approach allows A3D to identify aggregation patches that are typically not contiguous in sequence, outperforming linear sequence or composition-based algorithms.

    ### Key Features

    - Structure-based prediction of protein aggregation properties
    - Extension to larger and multimeric proteins
    - Simultaneous prediction of changes in protein solubility and stability upon mutation
    - Rapid screening for functional protein variants with improved solubility
    - Virtual mutation capabilities for designing variants with increased solubility

    ### Applications

    A3D can be used to predict aggregation propensities in folded proteins, design protein variants with increased solubility, study disease-associated protein variants, and optimize protein-based therapeutics.

    ## Credits

    Aleksander Kuriata, Valentin Iglesias, Jordi Pujols, Mateusz Kurcinski, Sebastian Kmiecik, Salvador Ventura,
    Aggrescan3D (A3D) 2.0: prediction and engineering of protein solubility,
    Nucleic Acids Research, Volume 47, Issue W1, 02 July 2019, Pages W300–W307,
    https://doi.org/10.1093/nar/gkz321

    """
    return aggrescan3d_task(
        run_name=run_name,
        input_type=input_type,
        input_pdb=input_pdb,
        input_pdb_folder=input_pdb_folder,
        output_directory=output_directory,
        # dynamic=dynamic,
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
        "input_type": "single_pdb",
        "input_pdb": LatchFile(
            "s3://latch-public/proteinengineering/aggrescan3d/2gb1.pdb"
        ),
    },
)
