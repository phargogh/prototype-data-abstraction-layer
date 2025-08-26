from dataclasses import dataclass


@dataclass
class RasterLayer():
    source_catalog_dataset_url: str
    source_rest_data: str
    name: str
    invest_type: str  # enum?
    license: str
    description: str
