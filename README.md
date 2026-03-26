# 🤖 ChatBotDSinHVAC: Domain-Specific Knowledge Base QA Bot for HVAC

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.7+-blue.svg" />
  <img alt="LangChain" src="https://img.shields.io/badge/LangChain-Integration-blue" />
  <img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white" />
  <img alt="OpenAI API" src="https://img.shields.io/badge/OpenAI_API-Integration-412991?logo=openai&logoColor=white" />
  <img alt="Pinecone" src="https://img.shields.io/badge/Pinecone-Vector_DB-black" />
  <img alt="License" src="https://img.shields.io/badge/license-MIT-green" />
</p>

<p align="center">
  <strong>English</strong> | <a href="README_zh.md">中文</a>
</p>

---

> **Note:** This is a personal project developed in 2023 for exploring the application of Large Language Models (LLMs) in the domain of Heating, Ventilation, and Air Conditioning (HVAC).

## 📑 Table of Contents
- [Introduction](#-introduction)
- [Background & Motivation](#-background--motivation)
- [Project Goals](#-project-goals)
- [Tech Stack](#-tech-stack)
- [Architecture & Features](#-architecture--features)
- [Project Structure](#-project-structure)
- [Installation & Quick Start](#-installation--quick-start)
- [Usage & Demo](#-usage--demo)
- [Future Work](#-future-work)
- [Acknowledgements](#-acknowledgements)

### 🌟 Introduction
**ChatBotDSinHVAC** is a specialized Question-Answering (QA) chatbot tailored for the HVAC domain. Built with Python and powered by a custom domain-specific vector knowledge base, this project was developed to bridge the gap between Large Language Models (LLMs) and specialized engineering disciplines.

### ❓ Background & Motivation
This project was initiated shortly after the release of ChatGPT in December 2022. Early [domain-specific tests](https://mp.weixin.qq.com/s/YxXkTFGD5j37AglY6_GaSQ) revealed that while ChatGPT showed promise in HVAC topics, it frequently suffered from factual inaccuracies and "AI hallucinations." This highlighted a clear issue: LLMs lacked sufficient training on specialized, publicly unavailable HVAC data.

The HVAC domain presents unique data challenges:
- **Data Privacy:** As an intersection of real estate and energy sectors, much of the data is highly sensitive, requires anonymization, and is rarely open-source.
- **Fragmented Knowledge:** The professional community is relatively niche, and high-quality, reliable domain knowledge is scattered and difficult to obtain online.

To address this, this project explores a Research & Development (R&D) approach: utilizing a Vector Database (Pinecone) via LangChain to continuously update and expand the LLM’s foundational HVAC knowledge.

### 🎯 Project Goals
The main objective is to provide a reliable, multi-turn conversational model for HVAC students, researchers, and entry-level professionals.

Compared to raw foundational models, **ChatBotDSinHVAC** aims to:
- **Reduce AI hallucinations** when answering HVAC-specific questions.
- **Enhance the accuracy and depth** of domain-specific knowledge retrieval.
- **Lower the barrier of entry** for HVAC practitioners looking to leverage AI in their workflows.

### 💻 Tech Stack
- **Language:** Python 3.7+
- **LLM Framework:** [LangChain](https://github.com/hwchase17/langchain)
- **Vector Database:** [Pinecone](https://www.pinecone.io/)
- **Core Model:** OpenAI API
- **Frontend UI:** [Streamlit](https://streamlit.io/)
- **Backend Server:** [Flask](https://flask.palletsprojects.com/)

### 🛠️ Architecture & Features
The system leverages the tech stack mentioned above.

It consists of two primary modules:
1. **Vector Knowledge Base Construction:** 
   - Reads domain-specific documents across various topics.
   - Performs text splitting, chunking, embedding, and storage into the vector database.
   - Easily updatable by processing new documents.
2. **Retrieval-Augmented Generation (RAG) QA:**
   - Takes user queries and performs similarity matching within the vector database.
   - Returns the most relevant results and combines them with the chat history to construct a comprehensive prompt.
   - Calls the LLM to generate an accurate, context-aware answer.

**Data Flow Architecture:**

![Data Flow](pic/dataflow.png)

### 📁 Project Structure
```text
ChatBotDSinHVAC/
├── pic/                        # Images used in README and frontend
├── scripts/                    # Utility scripts
├── utils/                      # Helper modules
├── frontend.py                 # Streamlit web frontend script (Legacy)
├── backend.py                  # Core backend logic (RAG query, LLM calling) (Legacy)
├── baseclass.py                # Base definitions and data structures
├── createDB.py                 # Core script to create/update vector database
├── logWriter.py                # Logging utility
├── requirements.txt            # Minimal dependencies list
└── README.md                   # Project documentation
```

### 💻 Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SheltonXiao/ChatBotDSinHVAC.git
   cd ChatBotDSinHVAC
   ```

2. **Configure Environment:**
   Make sure you have **Python 3.7+** installed. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize Personal Vector Database:**
   If you wish to build your own customized knowledge base:
   - Configure your API keys for **OpenAI** and **Pinecone**.
   - Manually create a `data/` directory in the project root.
   - Place your anonymized, domain-specific documents inside the `data/` folder.
   - Run the construction script:
   ```bash
   python createDB.py
   ```

4. **Run the QA Application (Legacy Frontend/Backend):**
   > *Note: The frontend and backend scripts (`frontend.py`, `backend.py`) were part of the original repository but are no longer actively synced or updated. They remain for reference and local testing.*
   
   First, start the Flask backend server:
   ```bash
   python backend.py
   ```
   
   Then, in a new terminal, start the Streamlit frontend:
   ```bash
   streamlit run frontend.py
   ```

### 🚀 Usage & Demo
Access the live demonstration running on a local server *(Note: The demo may not be online 24/7. Feel free to contact the author for access)*: [Live Demo](http://chatbotdshvac.natapp1.cc)

**Performance Comparison:**
The system successfully mitigates hallucination issues seen in standard LLMs:
- **ChatBotDSinHVAC Answer (Accurate & Contextual):**
  ![Example](pic/example.png)
- **Standard ChatGPT Answer (Inaccurate summary missing domain context):**
  ![GPT Example](pic/gptexample.png)

### 🔮 Future Work
- Enhance multi-turn conversation memory and contextual understanding.
- Continuously expand the domain-specific knowledge base.
- Integrate open-source LLMs (e.g., Llama, ChatGLM) for localized, privacy-first deployment.
- Optimize the Streamlit frontend UI/UX.

*(Note: This 2023 project is a proof-of-concept RAG implementation. Further accuracy improvements could be achieved through model fine-tuning.)*

### 🙏 Acknowledgements
The development of this project was inspired by and references the following excellent open-source works:
- [LangChain-ChatGLM-Webui](https://github.com/thomas-yanxin/LangChain-ChatGLM-Webui)
- [langchain-ChatGLM](https://github.com/imClumsyPanda/langchain-ChatGLM)
- [hugging-llm](https://github.com/datawhalechina/hugging-llm)
- [OpenChatPaper](https://github.com/liuyixin-louis/OpenChatPaper)
