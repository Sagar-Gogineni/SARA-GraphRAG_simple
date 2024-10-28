import os
from llama_index.core import  SimpleDirectoryReader
from llama_index.core import SimpleDirectoryReader
from llama_index.core import PropertyGraphIndex
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core.indices.property_graph import SchemaLLMPathExtractor
from llama_index.core import StorageContext
from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore
from graph_rag.kg_schema import entities,relations,schema
from llama_index.core import StorageContext
import nest_asyncio 
nest_asyncio.apply()
from llama_index.core import SimpleDirectoryReader
from dotenv import load_dotenv
load_dotenv()

username = os.getenv('NEO4J_USERNAME')
password = os.getenv('NEO4J_PASSWORD')
url = os.getenv("NEO4J_URI")
# print(url)


def construct_kg():
    graph_store = Neo4jPropertyGraphStore(username, password, url)
    # load documents
    documents = SimpleDirectoryReader(input_dir='graph_rag/data_store').load_data()
    # print(documents)
    # Define graph extractor based on schema 
    schema_kg_extractor = SchemaLLMPathExtractor(
        llm=OpenAI(model="gpt-4o-mini"),
        possible_entities=entities,
        possible_relations=relations,
        kg_validation_schema=schema,
        strict=True,  # if false, will allow triplets outside of the schema
        num_workers=4,
        max_triplets_per_chunk=10,
        )
    storage_context = StorageContext.from_defaults(graph_store=graph_store)
    # Extract graph from documents
    index = PropertyGraphIndex.from_documents(
        documents,
        embed_model=OpenAIEmbedding(model_name="text-embedding-3-small"),
        kg_extractors=[
        schema_kg_extractor
        ],
        property_graph_store=graph_store,
        storage_context=storage_context,
        show_progress=True,
    )
    # index.storage_context.persist(persist_dir="graph_rag/index_storage")
    
    # query_engine = index.as_query_engine(include_text=True)
    # response = query_engine.query("who is olaf")
    # print(response)
    graph_store.close()


