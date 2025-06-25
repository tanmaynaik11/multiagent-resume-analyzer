import qdrant_client
from qdrant_client.models import Distance, VectorParams, PointStruct, FieldCondition, MatchAny
from sentence_transformers import SentenceTransformer

# Connect to Qdrant instance (Docker running locally)
client = qdrant_client.QdrantClient(host="localhost", port=6333)

# Define collection name
collection_name = "skills_graph_rag"

# Delete existing collection (clean slate)
if collection_name in client.get_collections().collections:
    client.delete_collection(collection_name)
    print(f"✅ Existing collection '{collection_name}' deleted.")

# Define embedding model
embedder = SentenceTransformer("BAAI/bge-small-en-v1.5")
vector_size = embedder.get_sentence_embedding_dimension()

# Create Qdrant collection
client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
)

print(f"✅ Collection '{collection_name}' created with vector size {vector_size}.")

# Define expanded skill graph
skill_graph = {
    "Machine Learning": [
        "Supervised Learning",
        "Unsupervised Learning",
        "Reinforcement Learning",
        "Feature Engineering",
        "Model Evaluation",
        "Model Interpretability"
    ],
    "Data Science": [
        "Data Cleaning",
        "Exploratory Data Analysis",
        "Statistical Modeling",
        "Hypothesis Testing",
        "Time Series Forecasting",
        "Anomaly Detection"
    ],
    "LLMs / NLP": [
        "LLM Fine-Tuning",
        "RAG Pipelines",
        "Prompt Engineering",
        "NER Skill Extraction",
        "Text Summarization",
        "Semantic Search",
        "Embedding Optimization"
    ],
    "Computer Vision": [
        "Object Detection",
        "Image Segmentation",
        "Pose Estimation",
        "CNN Architectures",
        "Vision Transformers (ViT)",
        "Multi-Modal Models",
        "Real-Time Inference"
    ],
    "MLOps / Deployment": [
        "FastAPI Deployment",
        "Dockerized Microservices",
        "Kubernetes Pipelines",
        "CI/CD Pipelines",
        "Monitoring with MLFlow",
        "Cloud Model Deployment",
        "Serverless Inference"
    ],
    "Cloud Platforms": [
        "AWS S3",
        "AWS Lambda",
        "GCP Vertex AI",
        "Azure ML",
        "Distributed Training on Cloud",
        "GPU Optimization"
    ],
    "Orchestration / Multi-Agent Systems": [
        "CrewAI Orchestration",
        "LangGraph State Machines",
        "Autonomous Agents",
        "LLM-as-a-Judge Evaluation",
        "Skill Gap Analysis Agents"
    ]
}

# Populate Qdrant
points = []

point_id = 0
for parent_skill, subskills in skill_graph.items():
    # Parent skill point
    parent_embedding = embedder.encode(parent_skill)
    points.append(PointStruct(
        id=point_id,
        vector=parent_embedding.tolist(),
        payload={
            "skill_type": "parent",
            "skill": parent_skill,
            "subskills": subskills
        }
    ))
    point_id += 1

    # Subskills
    for subskill in subskills:
        sub_embedding = embedder.encode(subskill)
        points.append(PointStruct(
            id=point_id,
            vector=sub_embedding.tolist(),
            payload={
                "skill_type": "subskill",
                "skill": subskill,
                "parent_skill": parent_skill
            }
        ))
        point_id += 1

# Insert into Qdrant
client.upsert(
    collection_name=collection_name,
    points=points
)

print("✅ Graph-structured skill taxonomy loaded into Qdrant successfully.")
