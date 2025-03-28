class Chunk { 
    document string @description(#"the document that was uncovered in a RAG query"#)
    distance float @description(#"the cosine distance from query to this chunk"#)
}

// class Answer {
//   question string
//   answer string
// }
function QuestionAnswer(question: string, chunks: Chunk[]) -> Answer {
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
    RELEVANT CONTEXT: {{ chunks }}

    {{ ctx.output_format }}

    RESPONSE:
  "#
}