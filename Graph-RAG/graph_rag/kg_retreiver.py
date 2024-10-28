
import os
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import PropertyGraphIndex
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore
from llama_index.core.prompts import PromptTemplate
from llama_index.core.query_engine import CitationQueryEngine
from llama_index.core.indices.property_graph import VectorContextRetriever
from llama_index.core.indices.property_graph import TextToCypherRetriever

import nest_asyncio 
nest_asyncio.apply()
from dotenv import load_dotenv
load_dotenv()

username = os.getenv('NEO4J_USERNAME')
password = os.getenv('NEO4J_PASSWORD')
url = os.getenv("NEO4J_URI")

def kg_retriever(query_str):
    # load existing index
    graph_store = Neo4jPropertyGraphStore(username, password, url,database="neo4j")
    
    index = PropertyGraphIndex.from_existing(
    property_graph_store=graph_store,
    llm=OpenAI(model="gpt-4o-mini"),
    embed_model=OpenAIEmbedding(model_name="text-embedding-3-small")
    )

    # configure prompts for citations
    CITATION_QA_TEMPLATE = PromptTemplate(
    "System: You are a senior political jounalist and analyst. You have PHD in political sciences and economics.\n"
    "Task: Answer the user question soely based on the retrieved context_str.\n"
    "Instructions: All your output(s) must contain factual citations and sources that is present in the context_str.\n "
    "Guidelines:\n"
    "When referencing information from a source, "
    "cite the appropriate source(s) using their corresponding numbers. "
    "Every answer should include at least one source citation. "
    "Only cite a source when you are explicitly referencing it. "
    "If none of the sources are helpful, you should indicate that. "
    "For example:\n"
    "Source 1:\n"
    "The sky is red in the evening and blue in the morning.\n"
    "Source 2:\n"
    "Water is wet when the sky is red.\n"
    "Query: When is water wet?\n"
    "Answer: Water will be wet when the sky is red [2], "
    "which occurs in the evening [1].\n"
    "List of sources: "
    "Now it's your turn. Below are several numbered sources of information:"
    "\n------\n"
    "{context_str}"
    "\n------\n"
    "Query: {query_str}\n"
    "Answer: "
    )

    DEFAULT_RESPONSE_TEMPLATE = (
    "Generated Cypher query:\n{query}\n\n" "Cypher Response:\n{response}"
    )
    DEFAULT_ALLOWED_FIELDS = index.property_graph_store.get_schema_str()

    DEFAULT_TEXT_TO_CYPHER_TEMPLATE = (
        index.property_graph_store.text_to_cypher_template,
    )

    # configure Cypher retreiver
    cypher_retriever = TextToCypherRetriever(
    index.property_graph_store,
    # customize the LLM, defaults to Settings.llm
    llm=OpenAI(model="gpt-4o-mini"),
    # customize the text-to-cypher template.
    # Requires `schema` and `question` template args
    text_to_cypher_template=DEFAULT_TEXT_TO_CYPHER_TEMPLATE,
    # customize how the cypher result is inserted into
    # a text node. Requires `query` and `response` template args
    response_template=DEFAULT_RESPONSE_TEMPLATE,
    # an optional callable that can clean/verify generated cypher
    cypher_validator=index.property_graph_store.get_schema_str(),
    # allowed fields in the resulting
    allowed_output_field=DEFAULT_ALLOWED_FIELDS,
    )

    # configure vector retriever
    vector_retriever = VectorContextRetriever(
    index.property_graph_store,
    # only needed when the graph store doesn't support vector queries
    # vector_store=index.vector_store,
    embed_model=OpenAIEmbedding(model_name="text-embedding-3-small"),
    # include source chunk text with retrieved paths
    include_text=True,
    # the number of nodes to fetch
    similarity_top_k=100,
    # the depth of relations to follow after node retrieval
    path_depth=5,
    )

    # query_engine = index.as_query_engine(include_text=True,similarity_top_k=50)
    query_engine = CitationQueryEngine.from_args(
    index,
    # increase the citation chunk size!
    citation_chunk_size=1024,
    similarity_top_k=100,
    citation_qa_template=CITATION_QA_TEMPLATE,
    retrievers=[cypher_retriever,vector_retriever],
    # response_mode="tree_summarize",
    )
    response = query_engine.query(query_str)
    graph_store.close()
    return response


# construct_kg()
response=kg_retriever("who is green party")
# ("was hat Olaf zu der Veranstaltung gesagt")
print(response)
    #   ("können Sie die allgemeine Stimmung verschiedener Parteien gegen Olaf analysieren?"))
for i in range(len(response.source_nodes)):
    print(response.source_nodes[i].node.get_text())
