// Learn more about clients at https://docs.boundaryml.com/docs/snippets/clients/overview

client<llm> GPT4o {
  provider openai
  options {
    model "gpt-4o"
    api_key env.OPENAI_API_KEY
  }
}

client<llm> GTP4oMiniExtract {
  provider openai
  options {
    model "gpt-4o-mini"
    api_key env.OPENAI_API_KEY
    temperature 0.0
  }
}

client<llm> GTP4oMiniGenerate {
  provider openai
  options {
    model "gpt-4o-mini"
    api_key env.OPENAI_API_KEY
    temperature 0.3
  }
}
  
client<llm> Gemini2Flash {
  provider google-ai
  options {
    model "gemini-2.0-flash"
    api_key env.GOOGLE_API_KEY
  }
}

client<llm> OpenRouterClaude35Sonnet {
  provider "openai-generic"
  options {
    base_url "https://openrouter.ai/api/v1"
    api_key env.OPENROUTER_API_KEY
    model "anthropic/claude-3.5-sonnet"
    headers {
      "HTTP-Referer" "https://kuzudb.com" // Optional
      "X-Title" "Kuzu" // Optional
    }
  }
}

client<llm> OpenRouterGPT4oMini {
  provider "openai-generic"
  options {
    base_url "https://openrouter.ai/api/v1"
    api_key env.OPENROUTER_API_KEY
    model "openai/gpt-4o-mini"
    temperature 0.1
    seed 42
    headers {
      "HTTP-Referer" "https://kuzudb.com" // Optional
      "X-Title" "Kuzu" // Optional
    }
  }
}

client<llm> Claude {
  provider anthropic
  options {
    model "claude-3-5-sonnet-20240620"
    api_key env.ANTHROPIC_API_KEY
  }
}

client<llm> FastAnthropic {
  provider anthropic
  options {
    model "claude-3-haiku-20240307"
    api_key env.ANTHROPIC_API_KEY
  }
}

client<llm> FastOpenAI {
  provider openai
  options {
    model "gpt-4o-mini"
    api_key env.OPENAI_API_KEY
  }
}

client<llm> Fast {
  provider round-robin
  options {
    // This will alternate between the two clients
    // Learn more at https://docs.boundaryml.com/docs/snippets/clients/round-robin
    strategy [FastAnthropic, FastOpenAI]
  }
}

client<llm> Openai {
  provider fallback
  options {
    // This will try the clients in order until one succeeds
    // Learn more at https://docs.boundaryml.com/docs/snippets/clients/fallback
    strategy [GPT4o, FastOpenAI]
  }
}