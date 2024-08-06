# All the parameters

# Backend (Langchain/Langgraph)

EMBEDDING_MODEL = "text-embedding-3-large"  # Must be a model from OpenAI

OPENAI_MODEL = "gpt-4o-mini"
ANTHROPIC_MODEL = "claude-3-5-sonnet-20240620"  # "claude-3-opus-20240229"
GOOGLE_MODEL = "gemini-1.5-flash"
VERTEXAI_MODEL = "gemini-1.5-flash"  # "gemini-1.5-pro"
OLLAMA_MODEL = "llama3.1"

OPENAI_MENU = "OpenAI / GPT"
ANTHROPIC_MENU = "Anthropic / Claude"
GOOGLE_MENU = "Google / Gemini"
VERTEXAI_MENU = "Google (VertexAI) / Gemini"
OLLAMA_MENU = "MetaAI (Ollama) / Llama"

DEFAULT_MODEL = ANTHROPIC_MENU  # One of the model menu choices
DEFAULT_MENU_CHOICE = 1  # OpenAI: 0, Anthropic: 1, Google: 2, Google/VertexAI: 3, MetaAI/Ollama: 4
DEFAULT_TEMPERATURE = 0.2  # OpenAI: 0-2, Anthropic: 0-1

VECTORDB_MAX_RESULTS = 5
BM25_MAX_RESULTS = 5

OLLAMA_URL = "http://myvm1.edocloud.be:11434"  # "http://35.209.146.25" / "http://localhost:11434" 

CHROMA_SERVER = True
CHROMA_SERVER_HOST = "myvm2.edocloud.be"
CHROMA_SERVER_PORT = "8000"
CHROMA_COLLECTION_NAME = "bmae"  # Name of the collection in the vector DB

SYSTEM_PROMPT = """
You are a history and art history specialist. You assist the users in finding, describing, and displaying artworks related to history and art history.

Answer in the same language as the question.

If you already have the answer to the question, then no need to call tools.

At the end of the answer:

- Only if requested in the question, display one or more images of the artworks (see the JSON "og:image" fields).
- Give the links to the web pages about the artworks (see the JSON "url" fields).

Examples of markdown code:

- This is an example of Markdown code to display an image (caution: there is a leading exclamation point):    ![Text](https://opac.kbr.be/digitalCollection/images/image.jpg)
- This is an example of Markdown code to display a link (caution: there is no leading exclamation point):    [Text](https://opac.kbr.be/digitalCollection/pages/page.html)
"""

# Frontend (Streamlit)

LOGO_PATH = "./images/logo-image.jpg"
ASSISTANT_ICON = "👑"
ASSISTANT_NAME = "Art History Explorer"

HELLO_MESSAGE = "Hello! Bonjour! Hallo! 👋"
NEW_CHAT_MESSAGE = "New chat / Nouvelle conversation / Nieuw gesprek"
USER_PROMPT = "Enter your question / Entrez votre question / Voer uw vraag in"

ABOUT_TEXT = """
### About this assistant

This artificial intelligence assistant allows you to ask all kinds of questions regarding history and art history. It is especially build to display images. To answer, the assistant \
queries different images databases or the internet.

### Concernant cet assistant

Cet assistant d'intelligence artificielle permet de poser toutes sortes de questions sur l'histoire et l'histoire de l'art. Il est spécialement conçu pour afficher des images. Pour répondre, \
l'assistant interroge différentes bases de données d'images ou internet.

### Over deze assistent

Deze assistent met kunstmatige intelligentie stelt je in staat om allerlei vragen te stellen over geschiedenis en kunstgeschiedenis. Hij is speciaal gebouwd om afbeeldingen weer te geven. \
Om te antwoorden, raadpleegt de assistent verschillende afbeeldingendatabases of het internet.
"""

SIDEBAR_FOOTER = """
_________
Hybrid RAG agent with memory powered by Langchain and Langgraph. Web interface powered by Streamlit. *(c) Eric Dodémont, 2024.* Github: https://github.com/dodeeric/ragai-agent (Ragai Agent)
"""
