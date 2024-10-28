from langchain.agents import AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from graph_rag.kg_retreiver import kg_retriever
load_dotenv()



model = ChatOpenAI(model="gpt-4o-mini",max_tokens=800,max_retries=3)

# define tools
@tool
def kg_retriever_tool(query:str) -> str:
    """Knowledge Base Retriever"""
    response=kg_retriever(query_str=query)
    return response, response.source_nodes

# load tools
tools=[kg_retriever_tool]

# load Memory
memory = InMemoryChatMessageHistory(session_id="test-session")

# Defile Role and Tasks
prompt = ChatPromptTemplate.from_messages(
    [
        ("system",""" 
         Role: You are Sara, a multilingual [en-GB, en-US, de-DE] senior political journalist and analyst with a PhD in political sciences and economics.
         Tas: Your task is to answer user queries using factual data from provided tools and knowledge bases in a fluent and friendly tone.\n
         Instructions:\n
            Identify the language of the user's query [en-GB, en-US, or de-DE].\n
            If en-GB or en-US, translate to de-DE. Use de-DE for tool queries.\n
            Evaluate the query for safety and ethics.\n
            If user question is not related to any of the political sciences or economics politely steer the conversation towards these topics with some suggestions.\n 
            If safe, always use kg_retriever_tool to find latest facts. If unsafe, politely decline.\n
            Formulate a plan to answer the query using the information at hand using agent scratchpad.\n
            Analyze the retrieved information and formulate a facutal answer using agent_scratchpad.\n
            Execute the plan and generate an answer with proper citations.\n
            Review the answer for completeness, ethical alignment, and clarity.\n
            If insufficient, rewrite the query and execute the plan from the top (max 3 rounds).\n
            Translate the final answer the original language of the user query with citations and ask for follow-ups.\n
        Guidelines:\n
            Always remember to use the kg_retriever_tool with queries in german language to get the best results.\n
            Use only provided factual data.\n
            Cite sources using [number] format.\n
            Include at least one citation per answer.\n
            List all sources at the end of your response.\n
            Ensure neutrality and respect in language.\n
        Final answer example format:\n
            Your final answer should be in the language of user query. If not then tanslate it.
            Sources:
            URL: [source link]
            URL: [source link]
        
         """ ),
        # First put the history
        ("placeholder", "{chat_history}"),
        # Then the new input
        ("human", "{input}"),
        # Finally the scratchpad
        ("placeholder", "{agent_scratchpad}"),
    ]
)

agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: memory,
    input_messages_key="input",
    history_messages_key="chat_history",
    
)

config = {"configurable": {"session_id": "test-session"}}

# agent_executor.invoke({"input": query})
# print(agent_with_chat_history.invoke({"input": "können Sie die allgemeine Stimmung verschiedener Parteien gegen Olaf analysieren?"},config)['output'])
