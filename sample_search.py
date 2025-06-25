from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

# Connect to your running Qdrant instance
client = QdrantClient(host="localhost", port=6333)

embedder = SentenceTransformer("BAAI/bge-small-en-v1.5")

query = "Multi-agent orchestration"
query_vector = embedder.encode(query)

results = client.search(
    collection_name="skills_graph_rag",
    query_vector=query_vector.tolist(),
    limit=5
)

for hit in results:
    print(f"Skill: {hit.payload['skill']}, Score: {hit.score:.3f}")
