# Maximo AI Script Assitant

## Use Case
User of this AI Assitsant is IBM Maximo System Administrator or Technical Developers.
Users will be provide a requirement for which they want to create Jython Automation Script.
AI Assistant will check script code in existing Maximo Autoation Scripts and search for script which fullfils this requirement. 
a) If script is already available then AI Assistant will show message informing same to the user and show the automation script code.
b) If script is not available then AI Assitant will use LLM to generate Maximo Automation Script code in Jython.

## How it works

Below diagram shows architectural components

<img width="822" alt="Architecture" src="https://github.com/user-attachments/assets/a2358e84-bbab-498c-9c56-4c944c42c517" />

## Tech Stack & Dependencies

- **Streamlit**: Provides the web-based UI for user interaction with the Maximo AI Script Assistant.
- **FAISS (faiss-cpu)**: Enables fast vector similarity search to find the most relevant existing automation scripts.
- **Sentence-Transformers**: all-MiniLM-L6-v2 model used for embedding generation of user prompts and automation scripts for semantic matching.
- **Mistral:Latest LLM**: Running locally in Ollama and LLM-based generation of new scripts when no suitable match is found.

## Folder Structure
```
maximo-ai-script-assistant/
│
├── app/
│   ├── ui_app.py               # Streamlit frontend
│   ├── embed_scripts.py        # Embedding generator for scripts
│   ├── search_scripts.py       # FAISS-based semantic search
│   └── llm_generate.py         # Script generation via LLM
│
├── data/
│   └── automation_scripts.json # Script dataset with metadata + code
│
├── requirements.txt
└── README.md
```
