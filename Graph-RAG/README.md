# Introduction 
- SARA - Political Analyst and Assistant
SARA built on a robust foundation combining Neo4j,LlamaIndex and LangChain, powerful frameworks in the AI space. 
Core Components
    - LlamaIndex: We chose LlamaIndex as the backbone for our data ingestion and Retrieval-Augmented Generation (RAG) pipeline. Its efficiency in handling and indexing large datasets made it an ideal choice for our analytical needs.
    - LangChain: This framework powers our agent interaction design. We implemented temporary chat memory and tool access, enabling the agent to maintain context and perform complex operations.
    - Neo4j Aura: Knowledge graph cloud service for building knowledge graphs.

# Architecture 
    Coming soon!

# Getting Started
Setting up the Agent
1.	Download the zip file or clone from git repo
2.	Create a virtual env using conda or any python virtual env managers
3.	Rename the evn_exmaple file to .env and add your OpenAI api key and Qdrant url and api key
4.	You can get your API Keys here
    - OpenAI API: https://platform.openai.com/docs/overview
    - Qdrant API: https://cloud.qdrant.io/login
    - Neo4j API: https://neo4j.com/product/auradb/?utm_source=GSearch&utm_medium=PaidSearch&utm_campaign=Evergreen&utm_content=EMEA-Search-SEMCE-DSA-None-SEM-SEM-NonABM&utm_term=&utm_adgroup=DSA&gad_source=1&gclid=Cj0KCQjw7Py4BhCbARIsAMMx-_IxaAQUNqw3ngLoyqNt3sglDd0BY-mBwRbuxvcJ_lBIuWtXKbChEJIaAoZ2EALw_wcB

# Build and Test
- To run the Agent locally:
    - Open the teminal and navigate to the downloaded code repo
    - Activate the virtual env 
    - Navigate to dataAalyst-agent using 
        - cd Graph-RAG
        - run *poetry install*
        - run *poetry run streamlit run graph_rag/main.py*
- Docker 
    - Coming soon!
# Contribute

If you want to know more about creating similar agent feel free to contact me @ contact.sagargr@gmail.com 
This repo is only for Educational purpose and stricly not for production use.
