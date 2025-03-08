import os
import fnmatch
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

load_dotenv()  

def load_markdown_files(directory_path):
    """
    Recursively load all Markdown files from the specified directory and its subdirectories.

    Args:
        directory_path (str): The path to the root directory.

    Returns:
        list: A list of loaded documents.
    """
    markdown_files = []
    for root, _, filenames in os.walk(directory_path):
        for filename in fnmatch.filter(filenames, '*.md'):
            file_path = os.path.join(root, filename)
            loader = TextLoader(file_path, encoding='utf-8')
            markdown_files.extend(loader.load())
    return markdown_files

def process_documents(documents):
    """
    Split documents into manageable chunks using a text splitter.

    Args:
        documents (list): A list of documents to split.

    Returns:
        list: A list of split documents.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""]
    )
    return text_splitter.split_documents(documents)

def create_vector_store(documents):
    """
    Create a vector store from the processed documents.

    Args:
        documents (list): A list of processed documents.

    Returns:
        FAISS: A FAISS vector store.
    """
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(documents, embeddings)
    return vector_store


def initialize_qa_system(vector_store):
    """
    Initialize the RetrievalQA system using the vector store.

    Args:
        vector_store (FAISS): The vector store containing document embeddings.

    Returns:
        RetrievalQA: The initialized RetrievalQA system.
    """
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    llm = ChatOpenAI(model_name='gpt-4o', temperature=0)
    qa_system = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    return qa_system


def main():
    """
    Main function to run the RAG system.
    """
    os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

    # Define the directory containing Markdown files
    directory_path = 'ubuntu-docs'

    # Load and process documents
    documents = load_markdown_files(directory_path)
    processed_docs = process_documents(documents)

    # Create vector store and initialize QA system
    vector_store = create_vector_store(processed_docs)
    qa_system = initialize_qa_system(vector_store)

    # Interactive query loop
    while True:
        query = input("Enter your query (or 'exit' to quit): ").strip()
        if query.lower() in ['exit', 'quit']:
            break
        result = qa_system.invoke({"query": query})
        answer = result['result']
        source_docs = result['source_documents']

        print(f"\nAnswer: {answer}\n")
        print("Source Documents:")
        for doc in source_docs:
            print(f"- {doc.metadata['source']}")

if __name__ == "__main__":
    main()
