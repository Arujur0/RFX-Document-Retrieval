from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langsmith import traceable, Client
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate

from dotenv import load_dotenv
import openai
import os

load_dotenv()
## LOADING RFX DOCSs
def load_docs(paths):
    docs = []
    for path in paths:
        loader = PyPDFLoader(path)
        docs.extend(loader.load())
    return docs

## RETRIEVE EMBEDDINGS
def get_embed(docs):
    embeds = OpenAIEmbeddings(model="text-embedding-ada-002")
    vectors = Chroma.from_documents(docs, embeds)
    return vectors


## QUERIES DOCS BASED ON USER INPUT & CHAT HISTORY

def setup_chatgpt(vectors):
    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

    retrieval = vectors.as_retriever()

    prompt = [
        ("system", "Use the following pieces of retrieved context to answer the question: {context}. If you don't know the answer just say that you don't know."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ]

    
    templates = ChatPromptTemplate.from_messages(prompt)
    docs_stuff = create_stuff_documents_chain(llm, templates)
    rag_chain = create_retrieval_chain(retrieval, docs_stuff)
    return rag_chain


def process_response(chain, question, chat_history, retriever):
    response = chatbot.invoke({"context": retriever, "input": question, "chat_history": chat_history})

    return response['answer']


pwd = os.getcwd()
paths = [os.path.join(pwd, "RFX_DOCS\\",i) for i in os.listdir("RFX_DOCS")]

docs = load_docs(paths)

text_splits = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=250)
splits = text_splits.split_documents(docs)
vectors = get_embed(splits)

retriever = vectors.as_retriever()
chatbot = setup_chatgpt(vectors)

history = []

print("Ask questions about the RFX documents. Type 'exit' to quit.")
while True:
    question = input("ASK YOUR QUERY HERE: \n\n ")
    if question.lower() in ['exit']:
        print("THIS IS THE END OF THE CHAT")
        break
    else:
        try:
            response = process_response(chatbot, question, history, retriever)
            print(response)
            history.append(HumanMessage(content=question))
            history.append(AIMessage(content=response))

        except Exception as e:
            print("Something went wrong, Here is the error: \n{e}\n")

vectors.delete_collection()