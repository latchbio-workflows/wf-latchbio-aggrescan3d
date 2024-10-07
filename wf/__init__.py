from latch.resources.workflow import workflow
from latch.types.directory import LatchOutputDir
from latch.types.file import LatchFile
from latch.types.metadata import LatchAuthor, LatchMetadata, LatchParameter

from wf.task import task

metadata = LatchMetadata(
    display_name="Aggrescan3D",
    author=LatchAuthor(
        name="LatchBio",
    ),
    parameters={
        "input_file": LatchParameter(
            display_name="Input File",
            batch_table_column=True,
        ),
        "output_directory": LatchParameter(
            display_name="Output Directory",
            batch_table_column=True,
        ),
    },
)


@workflow(metadata)
def aggrescan3d_workflow(
    input_file: LatchFile, output_directory: LatchOutputDir
) -> LatchOutputDir:
    return task(input_file=input_file, output_directory=output_directory)
