from dataclasses import dataclass, field

from .visualization_output import VisualizationOutput
from ..output_format import OutputFormat


@dataclass(slots=True)
class VisualizationState:
    outputs: dict[OutputFormat, VisualizationOutput] = field(default_factory=dict)

    def get_output(
            self,
            format_name: OutputFormat,
    ) -> VisualizationOutput | None:
        return self.outputs.get(format_name)

    def get_or_create_output(
            self,
            format_name: OutputFormat,
    ) -> VisualizationOutput:
        output = self.outputs.get(format_name)

        if output is None:
            output = VisualizationOutput()
            self.outputs[format_name] = output

        return output

    def has_full_product(
            self,
            format_name: OutputFormat,
    ) -> bool:
        output = self.outputs.get(format_name)

        return (
                output is not None
                and output.has_full_product()
        )

    def has_wm_tiles(
            self,
            format_name: OutputFormat,
    ) -> bool:
        output = self.outputs.get(format_name)

        return (
                output is not None
                and output.has_wm_tiles()
        )

    def set_full_product(
            self,
            format_name: OutputFormat,
            path,
    ) -> None:
        output = self.get_or_create_output(format_name)
        output.full_product = path

    def set_wm_tiles(
            self,
            format_name: OutputFormat,
            path,
            zoom_levels: list[int] | None = None,
    ) -> None:
        output = self.get_or_create_output(format_name)

        output.wm_tiles = path
        output.wm_tiles_zoom_levels = zoom_levels if zoom_levels is not None else []

    def to_dict(self) -> dict:
        return {
            "outputs": {
                format_name.value: output.to_dict()
                for format_name, output in self.outputs.items()
            },
        }

    @classmethod
    def from_dict(cls, data: dict) -> "VisualizationState":
        return cls(
            outputs={
                OutputFormat(format_name): VisualizationOutput.from_dict(output)
                for format_name, output
                in data.get("outputs", {}).items()
            },
        )
