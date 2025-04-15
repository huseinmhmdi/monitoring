from app.types.data_source_types import ElasticsearchDataSource
from app.data_source import BaseDataSource


class Elasticsearch(BaseDataSource):

    def __init__(self, config: ElasticsearchDataSource) -> None:
        pass
