import streamlit as st

from run_graphrag import GraphRAG

# Set page configuration
st.set_page_config(page_title="Graph RAG with Kuzu", page_icon="🔍", layout="wide")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# Function to process a question
def process_question(question):
    with st.spinner("Generating answer..."):
        try:
            # Call the Graph RAG run method with a single question
            rag_result = rag.run(question)

            if rag_result and len(rag_result) > 0:
                result = rag_result  # Get the first result

                # Add to chat history (most recent first)
                st.session_state.chat_history.insert(0, result)
                # Keep only the last 10 entries
                if len(st.session_state.chat_history) > 10:
                    st.session_state.chat_history = st.session_state.chat_history[:10]
            else:
                st.error("No result was returned. Please try a different question.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.exception(e)


# Function to clear chat history
def clear_history():
    st.session_state.chat_history = []


# Initialize Graph RAG
@st.cache_resource
def get_graph_rag():
    return GraphRAG()


rag = get_graph_rag()

# App title
st.title("Graph RAG with Kuzu")

st.markdown("Ask questions about the data in your Kuzu database and get answers powered by RAG.")

# Create two columns for the main interface
col1, col2 = st.columns([2, 1])

with col1:
    # User input
    with st.form(key="question_form"):
        question = st.text_input(
            "Enter your question:", placeholder="What are the side effects of Morphine?"
        )
        submit_button = st.form_submit_button("Ask")

    # Process the question when submitted
    if submit_button and question:
        process_question(question)

    # Clear history button
    if st.session_state.chat_history:
        if st.button("Clear History"):
            clear_history()

with col2:
    # Sidebar with sample questions
    st.subheader("Sample Questions")
    sample_questions = [
        "What drug brands are there for lansoprazole?",
        "What are the side effects of morphine?",
        "what drug brands treats heartburn?",
    ]

    for sample in sample_questions:
        if st.button(sample, key=f"sample_{sample}"):
            process_question(sample)

# Display the most recent result
if st.session_state.chat_history:
    st.subheader("Latest Response")
    latest = st.session_state.chat_history[0]

    # Display the question
    st.markdown(f"**Question:** {latest['question']}")

    # Display the Cypher query in a code block (full width)
    st.subheader("Generated Cypher Query")
    if latest["cypher"] != "N/A":
        st.code(latest["cypher"], language="cypher")
    else:
        st.error("No Cypher query was generated for this question. Try rephrasing your question.")

    # Display the answer (full width)
    st.subheader("Answer")
    if isinstance(latest, dict) and "response" in latest:
        if latest["response"] != "N/A":
            st.markdown(latest["response"])
        else:
            st.warning(
                "No answer was generated. This could be due to no results from the query or an error in processing."
            )
    else:
        st.error("Unexpected result format. Please check the structure of the response.")

    # Divider
    st.divider()

# Display chat history
if len(st.session_state.chat_history) > 1:
    st.subheader("Chat History")

    for i, item in enumerate(st.session_state.chat_history[1:], 1):
        with st.expander(f"Question {i}: {item['question']}"):
            st.markdown(f"**Question:** {item['question']}")

            st.markdown("**Cypher Query:**")
            if item["cypher"] != "N/A":
                st.code(item["cypher"], language="cypher")
            else:
                st.error("No Cypher query was generated.")

            st.markdown("**Answer:**")
            if item["response"] != "N/A":
                st.markdown(item["response"])
            else:
                st.warning("No answer was generated.")

# About section in the sidebar
with st.sidebar:
    st.header("About")
    st.markdown("""
    This application uses Graph RAG to:
    1. Convert natural language questions to Cypher queries
    2. Execute the queries against a Kuzu graph database
    3. Generate natural language answers
    """)

    st.markdown("---")
    st.markdown(
        "**Graph RAG** combines the power of graph databases with Retrieval Augmented Generation to provide answers based on the underlying data structure."
    )

    # Debug mode toggle
    st.markdown("---")
    debug_mode = st.checkbox("Debug Mode", value=False)

    if debug_mode:
        st.subheader("Debug Information")
        st.write("Graph RAG Schema:")
        st.code(rag.baml_schema)

        if st.session_state.chat_history:
            st.write("Latest Result Object:")
            st.json(st.session_state.chat_history[0])

        # Direct Cypher query execution
        st.subheader("Execute Cypher Query Directly")
        with st.form("cypher_form"):
            cypher_query = st.text_area("Enter Cypher Query:", height=100)
            execute_button = st.form_submit_button("Execute")

        if execute_button and cypher_query:
            try:
                # Execute the query directly
                response = rag.conn.execute(cypher_query)

                # Process the results
                results = []
                try:
                    while response.has_next():
                        item = response.get_next()
                        results.append(item)
                except AttributeError:
                    # Handle the case where response doesn't have has_next/get_next
                    results = response

                st.success("Query executed successfully")
                st.write("Results:")
                st.json(results)
            except Exception as e:
                st.error(f"Error executing query: {str(e)}")
                st.exception(e)
