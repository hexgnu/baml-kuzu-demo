import streamlit as st
from run_graphrag import GraphRAG
from semantic_rag import SemanticRAG

st.set_page_config(page_title="Graph RAG with Kuzu", page_icon="🔍", layout="wide")

st.title("Compare and Contrast each RAG")

question = st.text_input("Enter question:", placeholder="What are the side effects of Morphine?")

@st.cache_resource
def get_graph_rag():
    return GraphRAG()

rag = get_graph_rag()


# @st.cache_resource
def get_semantic_rag():
    return SemanticRAG()

sem_rag = get_semantic_rag()

if question:
    sem_rag_result = sem_rag.run(question)

    st.write(sem_rag_result)

    rag_result = rag.run(question)

    st.write(rag_result)

