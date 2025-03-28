###############################################################################
#
#  Welcome to Baml! To use this generated code, please run the following:
#
#  $ pip install baml-py
#
###############################################################################

# This file was generated by BAML: please do not edit it. Instead, edit the
# BAML files and re-generate this code.
#
# ruff: noqa: E501,F401
# flake8: noqa: E501,F401
# pylint: disable=unused-import,line-too-long
# fmt: off

file_map = {
    
    "clients.baml": "// Learn more about clients at https://docs.boundaryml.com/docs/snippets/clients/overview\n \nclient<llm> OpenRouterGPT4oMini {\n  provider \"openai-generic\"\n  options {\n    base_url \"https://openrouter.ai/api/v1\"\n    api_key env.OPENROUTER_API_KEY\n    model \"openai/gpt-4o-mini\"\n    temperature 0.0\n    headers {\n      \"HTTP-Referer\" \"https://kuzudb.com\" // Optional\n      \"X-Title\" \"Kuzu\" // Optional\n    }\n  }\n}\n\nclient<llm> OpenRouterGPT4o {\n  provider \"openai-generic\"\n  options {\n    base_url \"https://openrouter.ai/api/v1\"\n    api_key env.OPENROUTER_API_KEY\n    model \"openai/gpt-4o\"\n    temperature 0.0\n    headers {\n      \"HTTP-Referer\" \"https://kuzudb.com\" // Optional\n      \"X-Title\" \"Kuzu\" // Optional\n    }\n  }\n}\n\nclient<llm> OpenRouterClaude35Sonnet {\n  provider \"openai-generic\"\n  options {\n    base_url \"https://openrouter.ai/api/v1\"\n    api_key env.OPENROUTER_API_KEY\n    model \"anthropic/claude-3.5-sonnet\"\n    temperature 0.0\n    headers {\n      \"HTTP-Referer\" \"https://kuzudb.com\" // Optional\n      \"X-Title\" \"Kuzu\" // Optional\n    }\n  }\n}\n\nclient<llm> OpenRouterGPT4oMiniGenerate {\n  provider \"openai-generic\"\n  options {\n    base_url \"https://openrouter.ai/api/v1\"\n    api_key env.OPENROUTER_API_KEY\n    model \"openai/gpt-4o-mini\"\n    temperature 0.3\n    headers {\n      \"HTTP-Referer\" \"https://kuzudb.com\" // Optional\n      \"X-Title\" \"Kuzu\" // Optional\n    }\n  }\n}\n\nclient<llm> Gemini2Flash {\n  provider google-ai\n  options {\n    model \"gemini-2.0-flash\"\n    api_key env.GOOGLE_API_KEY\n    generationConfig {\n      temperature 0.0\n    }\n  }\n}\n\nclient<llm> GTP4oMiniExtract {\n  provider openai\n  options {\n    model \"gpt-4o-mini\"\n    api_key env.OPENAI_API_KEY\n    temperature 0.0\n  }\n}\n\nclient<llm> GTP4oMiniGenerate {\n  provider openai\n  options {\n    model \"gpt-4o-mini\"\n    api_key env.OPENAI_API_KEY\n    temperature 0.3\n  }\n}\n\nclient<llm> GPT4o {\n  provider openai\n  options {\n    model \"gpt-4o\"\n    api_key env.OPENAI_API_KEY\n    temperature 0.0\n  }\n}\n\nclient<llm> FastOpenAI {\n  provider openai\n  options {\n    model \"gpt-4o-mini\"\n    api_key env.OPENAI_API_KEY\n  }\n}\n\nclient<llm> Fast {\n  provider round-robin\n  options {\n    // This will alternate between the two clients\n    // Learn more at https://docs.boundaryml.com/docs/snippets/clients/round-robin\n    strategy [OpenRouterGPT4oMini, FastOpenAI]\n  }\n}\n\nclient<llm> OpenaiFallback {\n  provider fallback\n  options {\n    // This will try the clients in order until one succeeds\n    // Learn more at https://docs.boundaryml.com/docs/snippets/clients/fallback\n    strategy [GTP4oMiniGenerate, GPT4o]\n  }\n}\n\n// Custom LLM inference server by YourTechBud\nclient<llm> Inferix_Gemma3_27b {\n  provider openai-generic\n  options {\n    base_url \"https://inferix.yourtechbud.studio/inferix/v1/llm\"\n    api_key env.INFERIX_API_KEY\n    model \"gemma3:27b\"\n    temperature 0.2\n  }\n}\n",
    "generators.baml": "\n// This helps use auto generate libraries you can use in the language of\n// your choice. You can have multiple generators if you use multiple languages.\n// Just ensure that the output_dir is different for each generator.\ngenerator target {\n    // Valid values: \"python/pydantic\", \"typescript\", \"ruby/sorbet\"\n    output_type \"python/pydantic\"\n    // Where the generated code will be saved (relative to baml_src/)\n    output_dir \"../\"\n    // The version of the BAML package you have installed (e.g. same version as your baml-py or @boundaryml/baml).\n    // The BAML VSCode extension version should also match this version.\n    version \"0.78.0\"\n    // Valid values: \"sync\", \"async\"\n    // This controls what `b.FunctionName()` will be (sync or async).\n    // Regardless of this setting, you can always explicitly call either of the following:\n    // - b.sync.FunctionName()\n    // - b.async_.FunctionName() (note the underscore to avoid a keyword conflict)\n    default_client_mode sync\n}   ",
    "graphrag.baml": "// --- Data models ---\nclass Cypher {\n  query string\n}\n\nclass Answer {\n  question string\n  answer string\n}\n\n// --- Functions ---\n\nfunction RAGText2Cypher(schema: string, question: string) -> Cypher {\n  client Gemini2Flash\n  prompt #\"\n    You are an expert in translating natural language questions into Cypher statements.\n    You will be provided with a question and a graph schema.\n    Use only the provided relationship types and properties in the schema to generate a Cypher\n    statement.\n    The Cypher statement could retrieve nodes, relationships, or both.\n    Do not include any explanations or apologies in your responses.\n    Do not respond to any questions that might ask anything else than for you to construct a\n    Cypher statement.\n    Answer in no more than 5 sentences\n\n    {{ _.role(\"user\") }}\n    Task: Generate a Cypher statement to query a graph database.\n\n    {{ schema}}\n\n    The question is:\n    {{ question }}\n\n    Instructions:\n    1. Use only the provided node and relationship types and properties in the schema.\n    2. When returning results, return property values rather than the entire node or relationship.\n    3. ALWAYS use the WHERE clause to compare string properties, and compare them using the\n       LOWER() function.\n\n    {{ ctx.output_format }}\n  \"#\n}\n\nfunction RAGAnswerQuestion(question: string, context: string) -> Answer {\n  client OpenRouterGPT4oMiniGenerate\n  prompt #\"\n    You are an AI assistant using Retrieval-Augmented Generation (RAG).\n    RAG enhances your responses by retrieving relevant information from a knowledge base.\n    You will be provided with a question and relevant context. Use only this context to answer\n    the question IN FULL SENTENCES.\n    Do not make up an answer. If you don't know the answer, say so clearly.\n    Always strive to provide concise, helpful, and context-aware answers.\n\n    {{ _.role(\"user\") }}\n    QUESTION: {{ question }}\n    RELEVANT CONTEXT: {{ context }}\n\n    {{ ctx.output_format }}\n\n    RESPONSE:\n  \"#\n}\n\n// --- Test cases ---\n\ntest CypherDrugCausesSymptom {\n  functions [RAGText2Cypher]\n  args {\n    schema #\"\n    ALWAYS RESPECT THE EDGE DIRECTIONS:\n    ---\n    (:DrugGeneric) -[:CAN_CAUSE]-> (:Symptom)\n    (:DrugGeneric) -[:HAS_BRAND]-> (:DrugBrand)\n    (:Condition) -[:IS_TREATED_BY]-> (:DrugGeneric)\n    ---\n\n    Node properties:\n    - DrugGeneric\n        - name: string\n    - DrugBrand\n        - name: string\n    - Condition\n        - name: string\n    - Symptom\n        - name: string\n\n    Edge properties:\n    \"#\n    question \"What are the side effects of Morphine?\"\n  }\n}\n\ntest CypherDrugCausesSymptomLowercase {\n  functions [RAGText2Cypher]\n  args {\n    schema #\"\n    ALWAYS RESPECT THE EDGE DIRECTIONS:\n    ---\n    (:DrugGeneric) -[:CAN_CAUSE]-> (:Symptom)\n    (:DrugGeneric) -[:HAS_BRAND]-> (:DrugBrand)\n    (:Condition) -[:IS_TREATED_BY]-> (:DrugGeneric)\n    ---\n\n    Node properties:\n    - DrugGeneric\n        - name: string\n    - DrugBrand\n        - name: string\n    - Condition\n        - name: string\n    - Symptom\n        - name: string\n\n    Edge properties:\n    \"#\n    question \"What are the side effects of lansoprazole?\"\n  }\n}\n\ntest CypherDrugGenericHasBrand {\n  functions [RAGText2Cypher]\n  args {\n    schema #\"\n    ALWAYS RESPECT THE EDGE DIRECTIONS:\n    ---\n    (:DrugGeneric) -[:CAN_CAUSE]-> (:Symptom)\n    (:DrugGeneric) -[:HAS_BRAND]-> (:DrugBrand)\n    (:Condition) -[:IS_TREATED_BY]-> (:DrugGeneric)\n    ---\n\n    Node properties:\n    - DrugGeneric\n        - name: string\n    - DrugBrand\n        - name: string\n    - Condition\n        - name: string\n    - Symptom\n        - name: string\n\n    Edge properties:\n    \"#\n    question \"What drug brands are there for Lansoprazole?\"\n  }\n}\n\ntest GenerationDrugCausesSymptom {\n  functions [RAGAnswerQuestion]\n  args {\n    question \"What are the side effects of Morphine? Answer in a numbered list.\",\n    context \"{'s.name': 'Morphine', 's.side_effects': ['rash', 'queasiness', 'dry mouth', 'drowsiness', 'throwing up', 'constipation', 'dizziness', 'confusion']}\"\n  }\n}\n\ntest GenerationDrugGenericHasBrand {\n  functions [RAGAnswerQuestion]\n  args {\n    question \"What drug brands are there for Lansoprazole?\",\n    context \"{'s.name': 'Lansoprazole', 's.brand_names': ['Prevacid']}\"\n  }\n}\n\ntest GenerationMissingContext {\n  functions [RAGAnswerQuestion]\n  args {\n    question \"Can you tell me the side effects of Metformin?\",\n    context \"\"\n  }\n}\n",
    "image_extractor.baml": "// Extract drug information and its known side effects from a table in an image\nclass Drug {\n    generic_name string\n    brand_names string[] @description(\"Strip the ® character at the end of the brand names\")\n}\n\nclass ConditionAndDrug {\n    condition string\n    drug Drug[]\n    side_effects string[]\n}\n\nfunction ExtractFromImage(img: image) -> ConditionAndDrug[] {\n  client OpenRouterGPT4oMini\n  prompt #\"\n    You are an expert at extracting healthcare and pharmaceutical information.\n\n    Extract the condition, drug names and side effects from these columns:\n    - Reason for drug\n    - Drug names: Generic name & (Brand name)\n    - Side effects\n\n    {{ ctx.output_format }}\n\n    {{ _.role(\"user\") }}\n    {{ img }}\n  \"#\n}\n\ntest TestOne {\n  functions [ExtractFromImage]\n  args {\n    img {\n      file \"../../data/img/drugs_1.png\"\n    }\n  }\n}\n\ntest TestTwo {\n  functions [ExtractFromImage]\n  args {\n    img {\n      file \"../../data/img/drugs_2.png\"\n    }\n  }\n}\n",
    "notes_extractor.baml": "// Extract medication information and side effects experienced by the patient from nurse's notes\nclass Medication {\n  name string\n  date string @description(\"Date format is YYYY-MM-DD\")\n  dosage string @description(\"Dosage of the medication\")\n  frequency string @description(\"Frequency of the medication\")\n}\n\nclass PatientInfo {\n  patient_id string\n  medication Medication\n  side_effects string[] @description(\"Do not list intensity or frequency of the side effect\")\n}\n\nfunction ExtractMedicationInfo(notes: string) -> PatientInfo[] {\n  client OpenRouterGPT4oMini\n  prompt #\"\n    Extract the medication information from the following nurse's notes.\n    Include only documented side effects, not vital signs or observations.\n    When listing side effects, do not describe its intensity or frequency.\n    ONLY list the name of the side effect.\n\n    {{ ctx.output_format }}\n\n    {{ _.role(\"user\") }} {{ notes }}\n  \"#\n}\n\ntest TestWithVitalSigns {\n  functions [ExtractMedicationInfo]\n  args {\n    notes #\"\n      Patient ID: X7F3Q\n      Date: October 12 2024\n      Medication: Ramipril 5mg PO daily\n      Side Effects: Patient reports persistent dry cough and occasional dizziness when standing.\n      BP reduced from 156/92 to 132/78. No angioedema observed. Will continue to monitor for hypotension.\n    \"#\n  }\n}\n\ntest TestNegation {\n  functions [ExtractMedicationInfo]\n  args {\n    notes #\"\n      Patient ID: L9M2W\n      Date: November 3 2024\n      Medication: Metformin 1000mg BID\n      Side Effects: Reports mild nausea after morning dose. Denies diarrhea. Blood sugar levels stable.\n    \"#\n  }\n}",
    "simplerag.baml": "class Chunk { \n    document string @description(#\"the document that was uncovered in a RAG query\"#)\n    distance float @description(#\"the cosine distance from query to this chunk\"#)\n}\n\n// class Answer {\n//   question string\n//   answer string\n// }\nfunction QuestionAnswer(question: string, chunks: Chunk[]) -> Answer {\n  client OpenRouterGPT4oMiniGenerate\n  prompt #\"\n    You are an AI assistant using Retrieval-Augmented Generation (RAG).\n    RAG enhances your responses by retrieving relevant information from a knowledge base.\n    You will be provided with a question and relevant context. Use only this context to answer\n    the question IN FULL SENTENCES.\n    Do not make up an answer. If you don't know the answer, say so clearly.\n    Always strive to provide concise, helpful, and context-aware answers.\n\n    {{ _.role(\"user\") }}\n    QUESTION: {{ question }}\n    RELEVANT CONTEXT: {{ chunks }}\n\n    {{ ctx.output_format }}\n\n    RESPONSE:\n  \"#\n}",
}

def get_baml_files():
    return file_map