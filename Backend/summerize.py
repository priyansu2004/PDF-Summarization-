from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

# Initialize models and embeddings (only once)
llm = HuggingFaceEndpoint(
    repo_id="openai/gpt-oss-20b",
    task="text-generation",
)

model = ChatHuggingFace(llm=llm)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def process_pdf_and_query(pdf_path: str, query: str) -> str:
    """
    DYNAMIC: Process ANY PDF uploaded by user with LangChain
    
    Args:
        pdf_path: Path to the uploaded PDF file
        query: User's question
        
    Returns:
        Answer based on the uploaded PDF content
    """
    # Load the user's uploaded PDF with LangChain PyPDFLoader
    pdf_loader = PyPDFLoader(pdf_path)
    pdf_documents = pdf_loader.load()  # Load the actual PDF
    
    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    docs = text_splitter.split_documents(pdf_documents)
    
    # Create vector store from THIS specific PDF
    vector_store = Chroma.from_documents(
        documents=docs, 
        embedding=embeddings, 
        collection_name="pdf_vectors"
    )
    
    # Create retriever
    retriever = vector_store.as_retriever(
        search_type="mmr", 
        search_kwargs={"k": 3, "lambda_cut": 0.5}
    )
    
    # Retrieve relevant documents from THIS PDF
    retrieved_docs = retriever.invoke(query)
    
    # Extract context
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    
    # Create prompt template
    template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant for providing answers based on context and query."),
        ("human", "Answer the question based on the context below.\n\n{context}\n\nQuestion: {question}")
    ])
    
    messages = template.format_messages(context=context, question=query)
    result = model.invoke(messages)
    
    return result.content.strip()