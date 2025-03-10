// --- Data models ---
class Cypher {
  query string
}

class Answer {
  question string
  answer string
}

// --- Functions ---

function RAGText2Cypher(schema: string, question: string) -> Cypher {
  client Gemini2Flash
  prompt #"
    You are an expert in translating natural language questions into Cypher statements.
    You will be provided with a question and a graph schema.
    Use only the provided relationship types and properties in the schema to generate a Cypher
    statement.
    The Cypher statement could retrieve nodes, relationships, or both.
    Do not include any explanations or apologies in your responses.
    Do not respond to any questions that might ask anything else than for you to construct a
    Cypher statement.
    Answer in no more than 5 sentences

    {{ _.role("user") }}
    Task: Generate a Cypher statement to query a graph database.

    {{ schema}}

    The question is:
    {{ question }}

    Instructions:
    1. Use only the provided node and relationship types and properties in the schema.
    2. When returning results, return property values rather than the entire node or relationship.
    3. ALWAYS use the WHERE clause to compare string properties, and compare them using the
       LOWER() function.

    {{ ctx.output_format }}
  "#
}

function RAGAnswerQuestion(question: string, context: string) -> Answer {
  client OpenRouterGPT4oMiniGenerate
  prompt #"
    You are an AI assistant using Retrieval-Augmented Generation (RAG).
    RAG enhances your responses by retrieving relevant information from a knowledge base.
    You will be provided with a question and relevant context. Use only this context to answer
    the question IN FULL SENTENCES.
    Do not make up an answer. If you don't know the answer, say so clearly.
    Always strive to provide concise, helpful, and context-aware answers.

    {{ _.role("user") }}
    QUESTION: {{ question }}
    RELEVANT CONTEXT: {{ context }}

    {{ ctx.output_format }}

    RESPONSE:
  "#
}

// --- Test cases ---

test CypherDrugCausesSymptom {
  functions [RAGText2Cypher]
  args {
    schema #"
    ALWAYS RESPECT THE EDGE DIRECTIONS:
    ---
    (:DrugGeneric) -[:CAN_CAUSE]-> (:Symptom)
    (:DrugGeneric) -[:HAS_BRAND]-> (:DrugBrand)
    (:Condition) -[:IS_TREATED_BY]-> (:DrugGeneric)
    ---

    Node properties:
    - DrugGeneric
        - name: string
    - DrugBrand
        - name: string
    - Condition
        - name: string
    - Symptom
        - name: string

    Edge properties:
    "#
    question "What are the side effects of Morphine?"
  }
}

test CypherDrugCausesSymptomLowercase {
  functions [RAGText2Cypher]
  args {
    schema #"
    ALWAYS RESPECT THE EDGE DIRECTIONS:
    ---
    (:DrugGeneric) -[:CAN_CAUSE]-> (:Symptom)
    (:DrugGeneric) -[:HAS_BRAND]-> (:DrugBrand)
    (:Condition) -[:IS_TREATED_BY]-> (:DrugGeneric)
    ---

    Node properties:
    - DrugGeneric
        - name: string
    - DrugBrand
        - name: string
    - Condition
        - name: string
    - Symptom
        - name: string

    Edge properties:
    "#
    question "What are the side effects of lansoprazole?"
  }
}

test CypherDrugGenericHasBrand {
  functions [RAGText2Cypher]
  args {
    schema #"
    ALWAYS RESPECT THE EDGE DIRECTIONS:
    ---
    (:DrugGeneric) -[:CAN_CAUSE]-> (:Symptom)
    (:DrugGeneric) -[:HAS_BRAND]-> (:DrugBrand)
    (:Condition) -[:IS_TREATED_BY]-> (:DrugGeneric)
    ---

    Node properties:
    - DrugGeneric
        - name: string
    - DrugBrand
        - name: string
    - Condition
        - name: string
    - Symptom
        - name: string

    Edge properties:
    "#
    question "What drug brands are there for Lansoprazole?"
  }
}

test GenerationDrugCausesSymptom {
  functions [RAGAnswerQuestion]
  args {
    question "What are the side effects of Morphine? Answer in a numbered list.",
    context "{'s.name': 'Morphine', 's.side_effects': ['rash', 'queasiness', 'dry mouth', 'drowsiness', 'throwing up', 'constipation', 'dizziness', 'confusion']}"
  }
}

test GenerationDrugGenericHasBrand {
  functions [RAGAnswerQuestion]
  args {
    question "What drug brands are there for Lansoprazole?",
    context "{'s.name': 'Lansoprazole', 's.brand_names': ['Prevacid']}"
  }
}

test GenerationMissingContext {
  functions [RAGAnswerQuestion]
  args {
    question "Can you tell me the side effects of Metformin?",
    context ""
  }
}
