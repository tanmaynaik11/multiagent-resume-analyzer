import streamlit as st
import redis
import pickle
import chromadb

st.title("Multi-Agent System Admin Dashboard")

# Redis Connection
st.header("🔑 Redis Shared Memory")
redis_client = redis.Redis(host='localhost', port=6379, db=0)

redis_keys = redis_client.keys('*')
if redis_keys:
    selected_key = st.selectbox("Select Redis Key:", [key.decode() for key in redis_keys])
    if selected_key:
        raw_data = redis_client.get(selected_key)
        try:
            parsed_data = pickle.loads(raw_data)
            st.json(parsed_data)
        except:
            st.write(raw_data.decode())
else:
    st.write("No keys found in Redis.")

# ChromaDB Connection
st.header("📦 ChromaDB Vector Store")
client = chromadb.HttpClient(host="localhost", port=8000)
collection = client.get_or_create_collection("skills")

st.write(f"Total documents in 'skills' collection: {collection.count()}")

if collection.count() > 0:
    results = collection.get()
    for idx, doc_id in enumerate(results["ids"]):
        st.write(f"Document {idx+1}:")
        st.write(f"ID: {doc_id}")
        st.write(f"Document: {results['documents'][idx]}")
        st.write(f"Metadata: {results['metadatas'][idx]}")
        st.write("---")
