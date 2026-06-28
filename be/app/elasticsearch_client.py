from elasticsearch import AsyncElasticsearch
import os

ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")

es_client = AsyncElasticsearch(ELASTICSEARCH_URL)

async def init_es_indices():
    """Initializes Elasticsearch indices if they do not exist."""
    candidates_index = "candidates"
    if not await es_client.indices.exists(index=candidates_index):
        await es_client.indices.create(
            index=candidates_index,
            body={
                "mappings": {
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "text"},
                        "email": {"type": "keyword"},
                        "phone": {"type": "keyword"},
                        "skills": {"type": "keyword"},
                        "experience_years": {"type": "float"},
                        "education": {"type": "text"},
                        "clean_text": {"type": "text"}
                    }
                }
            }
        )
    
async def index_candidate(candidate_id: int, data: dict):
    """Indexes a candidate document in ElasticSearch."""
    await es_client.index(index="candidates", id=str(candidate_id), document=data)

async def search_candidates(query: str, filters: dict = None):
    """Searches for candidates using full-text search and optional filters."""
    body = {
        "query": {
            "bool": {
                "must": [
                    {"multi_match": {"query": query, "fields": ["skills", "clean_text", "education"]}}
                ]
            }
        }
    }
    
    if filters and "min_experience" in filters:
        body["query"]["bool"].setdefault("filter", []).append({
            "range": {"experience_years": {"gte": filters["min_experience"]}}
        })
        
    response = await es_client.search(index="candidates", body=body, size=10)
    return [hit["_source"] for hit in response["hits"]["hits"]]
