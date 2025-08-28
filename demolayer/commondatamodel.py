import enum
from dataclasses import dataclass


class InVESTInputType(enum.Enum):
    DEM = 'digital elevation model'
    K_FACTOR = 'soil erodibility'


@dataclass
class RasterLayer():
    source_catalog_dataset_url: str
    source_rest_data: str
    name: str
    invest_type: InVESTInputType
    license: str
    description: str


@dataclass
class VectorLayer():
    source_catalog_dataset_url: str
    source_rest_data: str
    name: str
    license: str
    description: str
