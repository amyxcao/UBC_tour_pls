from ..interfaces import QueryRewriter, Query


class DefaultQueryRewriter(QueryRewriter):
    def process(self, query: Query) -> list[Query]:
        # Example implementation: simply return the original query
        return [query]
