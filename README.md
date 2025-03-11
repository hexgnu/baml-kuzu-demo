# Graph extraction and Graph RAG with BAML and Kuzu

This repository contains a demonstration of transforming unstructured data from clinical notes
and drug side effects into a knowledge graph in Kuzu. The graph is then used to answer questions
about the data using a Graph RAG pipeline.

Tools used
- [BAML](https://github.com/boundaryml/baml): AI and LLM prompting framework
- [Kuzu](https://github.com/kuzudb/kuzu): Embedded, fast, scalable graph database
- [Streamlit](https://github.com/streamlit/streamlit): Visualization framework for building custom web apps

## Overview

The goal is to show how to build modular "agents" (i.e., prompt pipelines that accomplish a
subtask) that can then be strung together to accomplish more complex tasks. BAML allows users
to compose together these kinds of agents with testing and validation capabilities, by offering
a reliable means to generate structured outputs from LLMs.

Kuzu is used as a data store for the graph, and Streamlit is used to build a simple UI for
interacting with the graph.

The general components of the pipeline are shown in the diagram below.

![](./assets/drug-side-effects-graph-rag.png)

## Setup

Ensure you have Python 3.11+ installed.

1. Clone this repository
2. Install the required dependencies:
   ```bash
   # Install the uv package manager
   curl -fsSL https://get.uvm.dev | bash
   # Install the dependencies
   uv sync
   ```

## Extract data from images and text

To extract data from images and text, run the following command:

```bash
cd src
# Extract data from images that represent tables from the PDF of drugs and side effects
uv run image_extractor.py
# Extract data from the text of clinical notes
uv run notes_extractor.py
```

This will output JSON files into the `../data/extracted_data` directory.

## Creating the graph

To create the graph in Kuzu, run the following command:

```bash
cd src
uv run 01_create_drug_graph.py
```

This will persist the Kuzu graph locally in the `ex_kuzu_db` directory.

To add the patient data to the graph, run the following command:

```bash
cd src
uv run 02_create_patient_graph.py
```
This will augment the pre-existing graph (from the prior step) with the data from the
patient notes.

## Running the Graph RAG chatbot

To run the Streamlit application:

```bash
cd src
uv run streamlit run streamlit_app.py
```

The application will be available at http://localhost:8501 by default.

## Sample questions

The application comes with several sample questions you can try:
- "What drug brands are there for lansoprazole?"
- "What are the side effects of morphine?"

## How it works

1. The user enters a question in natural language
2. BAML converts the question to a Cypher query
3. The Cypher query is executed against the Kuzu graph database
4. The results are processed and a natural language answer is generated
5. Both the query and answer are displayed to the user

## Notes

- The application maintains a history of up to 10 recent questions and answers
- You can clear the history using the "Clear History" button
- A debug mode is available in the sidebar that provides:
  - The GraphRAG schema used for generating Cypher queries
  - Detailed information about the latest result
  - A direct Cypher query execution interface for testing


> [!NOTE]
> The Graph RAG application is far from perfect and has room for improvement. For example,
> custom modules can be incorporated downstream of Text2Cypher to check the Cypher queries
> for syntax errors before execution. In addition, corrector agents could be added to the
> pipeline to increase robustness so that fewer questions result in an empty response.

---

## Evaluation

Part of the motivation for this project was to evaluate the performance of BAML and the given
LLM for the task of extracting data from unstructured text. We have two tasks to evaluate:

1. Extracting drugs and side effects from a table in a PDF
2. Extracting medications and side effects from clinical notes

To evaluate the performance of the image extractor, run the following command:

```bash
uv run evals/image_extractor_eval.py
```

To evaluate the performance of the notes extractor, run the following command:

```bash
uv run evals/notes_extractor_eval.py
```

### Image extractor results

The results from multiple models being compared are shown below. Cost numbers (from the OpenRouter API),
where possible, are also noted for each model, alongside the percentage of relevant matches found
between the human annotated data and the extracted data.

| **File: `drugs_1.json`** | **Count** | **Percentage** |
|------------------------|-----------|----------------|
| Exact matches          | 79        | 100.0%         |
| Missing items          | 0         | 0.0%           |
| Potential hallucinations | 0       | 0.0%           |

| **File: `drugs_2.json`** | **Count** | **Percentage** |
|------------------------|-----------|----------------|
| Exact matches          | 97        | 89.8%          |
| Missing items          | 2         | 1.9%           |
| Potential hallucinations | 9       | 8.3%           |

| **Totals across all files** | **Count** | **Percentage** |
|----------------------------|-----------|----------------|
| Total exact matches        | 176       | 94.1%          |
| Total missing items        | 2         | 1.1%           |
| Total potential hallucinations | 9     | 4.8%           |

In the case of `gpt-4o-mini`, the model is really good at memorizing data from its training,
so not all the potential hallucinations are actually hallucinations. See below for the cases
where the evaluation thinks the model may have hallucinated:

```
File: drugs_2.json
  Potentially hallucinated items in extracted data (please verify):
    <Missing> (human annotated) --- 'Accupril' (extracted)
    <Missing> (human annotated) --- 'Altace' (extracted)
    <Missing> (human annotated) --- 'Capoten' (extracted)
    <Missing> (human annotated) --- 'Lotensin' (extracted)
    <Missing> (human annotated) --- 'Prinivil' (extracted)
    <Missing> (human annotated) --- 'Trimethoprim' (extracted)
    <Missing> (human annotated) --- 'Vasotec' (extracted)
    <Missing> (human annotated) --- 'Zestril' (extracted)
```
In `drugs_2.json`, the model produced the brands `Accupril`, `Altace`, `Capoten`, `Lotensin`, and so on.
In ALL cases (100% of the time, over 10 runs), the model identified the **correct** drug
brands even though they were not present in the image file, because the model effectively memorized
the data from its training. From a business perspective, the model is correct, and a human
would mark these as correct extractions, not hallucinations.

However, the model is not perfect, and in the case of `gpt-4o-mini`, it missed the following extractions
with very minor errors:

```
File: drugs_2.json
  Mismatched items (different values for corresponding elements):
    'Cozarr' (human annotated) --- 'Cozar' (extracted)
  Items missing from extracted data:
    'Sulfamethoxazole/Trimethoprim' (human annotated) --- 'Trimethoprim' (extracted)
```

These mismatches, though minor, would need to be fixed by a human in the loop.

### Notes extractor results

The results from the notes extractor are shown below.

| **Totals across all notes files** | **Count** | **Percentage** |
|-----------------------------------|-----------|----------------|
| Total exact matches               | 19        | 100.0%         |
| Total missing items               | 0         | 0.0%           |
| Total potential hallucinations    | 0         | 0.0%           |
| Total mismatches                  | 0         | 0.0%           |

There are no hallucinations or mismatches in the notes extractor!

## Evaluation results for multiple models

Over time, the performance of more models can be easily and efficiently tested with BAML. The total number of
exact matches (for the exact same prompt) are aggregated and shown below.
Cost numbers are as obtained from the OpenRouter API on average across 3 runs.

| **Model** | **Image extractor** | **Notes extractor** | **Total cost**
| --- | --- | --- | --- |
| gpt-4o-mini | 176 | 19 | $0.000075 |
| claude-3-5-sonnet | 164 | 19 | $0.0037 |

To do: Add a better summary table comparing more models (both open source and commercial).

