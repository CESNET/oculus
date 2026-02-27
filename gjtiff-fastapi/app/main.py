import logging
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel

from .gjtiff_wrapper import execute_gjtiff

logger = logging.getLogger(__name__)

app = FastAPI(title="Oculus - GJTIFF FastAPI wrapper service")

class ProcessRequest(BaseModel):
    input_files: list[str]
    output_directory: str
    zoom_levels: list[int]


@app.post("/run-gjtiff")
def run_process(gjtiff_input: ProcessRequest):
    logger.info(f"Got request: {gjtiff_input}")

    result = execute_gjtiff(
        input_files=gjtiff_input.input_files,
        output_directory=Path(gjtiff_input.output_directory),
        zoom_levels=gjtiff_input.zoom_levels
    )

    return {"output": result}
