# Maximo GenAI Script Assistant

## Use Case
User of this AI Assitsant is IBM Maximo System Administrator or Technical Developers.
Users will be provide a requirement for which they want to create Jython Automation Script.
AI Assistant will check script code in existing Maximo Autoation Scripts and search for script which fullfils this requirement. 
a) If script is already available then AI Assistant will show message informing same to the user and show the automation script code.
b) If script is not available then AI Assitant will use LLM to generate Maximo Automation Script code in Jython.

## How it works

Below diagram shows architectural components
```
+-------------------+         +------------------------+
| User Prompt Input | ----->  | Sentence Transformer   |
| (via Streamlit UI)|         | (Prompt Embedding)     |
+-------------------+         +------------------------+
                                       |
                                       v
                        +----------------------------+
                        | FAISS Vector Search         |
                        | (Find similar scripts)      |
                        +----------------------------+
                           | Match Found?   | No Match
                          Yes               v
                            |      +------------------------+
                            |      | Mistal LLM in Ollama   |
                            |      | Generate New Script    |
                            |      +------------------------+
                            v
                +-----------------------------+
                | Show Script + Similarity UI |
                +-----------------------------+
```

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

## Demo

When script match is found then show existing script to user without generating script from LLM-

![image](https://github.com/user-attachments/assets/4fed3474-1ef8-4922-b001-4180355f4f21)

When no script match is found then script is generate from LLM-

![image](https://github.com/user-attachments/assets/756e827a-6305-4218-b213-315c3e989604)

## Execute

```
cd maximo-ai-script-assistant
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python embed_script.py
streamlit run app/ui_app.py
```
