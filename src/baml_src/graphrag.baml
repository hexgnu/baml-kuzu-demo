// --- Data models ---
class Query {
  query string
}

class Answer {
  question string
  answer string
}

// --- Functions ---

function RAGText2Cypher(schema: string, question: string) -> Query | null {
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

function RAGAnswerQuestion(context: Answer) -> Answer {
  client Gemini2Flash
  prompt #"
    Answer the question in full sentences using the provided context.
    Do not make up an answer. If the information is not provided in the context, say so clearly.

    {{ _.role("user") }}
    QUESTION: {{ context.question }}
    RELEVANT CONTEXT: {{ context.answer }}

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
    context {
      question "What are the side effects of Morphine? Answer in a numbered list.",
      answer "{s.name: 'Morphine', side_effects: ['rash', 'queasiness', 'dry mouth', 'drowsiness', 'throwing up', 'constipation', 'dizziness', 'confusion']}"
    }
  }
}

test GenerationDrugGenericHasBrand {
  functions [RAGAnswerQuestion]
  args {
    context {
      question "What drug brands are there for Lansoprazole?",
      answer "{s.name: 'Lansoprazole', brand_names: ['Prevacid']}"
    }
  }
}

test GenerationMissingContext {
  functions [RAGAnswerQuestion]
  args {
    context {
      question "Can you tell me the side effects of Metformin?",
      answer ""
    }
  }
}
