import os
from typing import Optional, Type, Any
from langchain.tools import BaseTool
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from pydantic import BaseModel, Field, PrivateAttr
from bs4 import BeautifulSoup
import requests


class HimalayaSearchInput(BaseModel):
    """Input for Himalaya Enterprises search tool."""
    query: str = Field(description="Search query for Himalaya Enterprises information")


class HimalayaWebLoaderTool(BaseTool):
    """Tool for searching Himalaya Enterprises information from their website."""
    
    name: str = "himalaya_enterprises_search"
    description: str = (
        "Search for information about Himalaya Enterprises from their official website. "
        "Use this tool when users ask about Himalaya Enterprises, their services, products, "
        "projects, location, contact information, or any company-specific details."
    )
    args_schema: Type[BaseModel] = HimalayaSearchInput
    
    # Use private attributes for internal state
    _vectorstore: Any = PrivateAttr(default=None)
    _retriever: Any = PrivateAttr(default=None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._initialize_vectorstore()
    
    def _extract_text_content(self, url):
        """Extract clean text content from a URL using BeautifulSoup."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up the text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text
        except Exception as e:
            print(f"Error extracting text from {url}: {e}")
            return None
    
    def _initialize_vectorstore(self):
        """Initialize the vector store with Himalaya Enterprises content."""
        try:
            # Load content from multiple Himalaya Enterprises website pages
            urls = [
                "https://www.himalayaentp.com/index.php/about/",
                "https://www.himalayaentp.com/index.php/product-2/",
                "https://www.himalayaentp.com/index.php/contact/",
                "https://www.himalayaentp.com/index.php/projects/"
            ]
            
            all_texts = []
            for url in urls:
                print(f"Loading content from: {url}")
                
                # Try custom text extraction first
                text_content = self._extract_text_content(url)
                if text_content and len(text_content.strip()) > 100:
                    print(f"Successfully extracted text content from {url}")
                    print(f"Sample content: {text_content[:200]}...")
                    all_texts.append({"page_content": text_content, "metadata": {"source": url}})
                else:
                    # Fallback to WebBaseLoader
                    print(f"Falling back to WebBaseLoader for {url}")
                    web_loader = WebBaseLoader(url)
                    data = web_loader.load()
                    if data:
                        print(f"Loaded {len(data)} documents from {url}")
                        print(f"Sample content: {data[0].page_content[:200]}...")
                        all_texts.extend([{"page_content": doc.page_content, "metadata": doc.metadata} for doc in data])
            
            print(f"Total documents loaded: {len(all_texts)}")
            
            if not all_texts:
                raise Exception("No content could be loaded from any URL")
            
            # Create Document objects for text splitting
            from langchain.schema import Document
            documents = [Document(page_content=item["page_content"], metadata=item["metadata"]) for item in all_texts]
            
            # Split the documents
            text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                chunk_size=500, 
                chunk_overlap=50
            )
            doc_splits = text_splitter.split_documents(documents)
            print(f"Total document chunks after splitting: {len(doc_splits)}")
            
            # Create embeddings
            embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
            
            # Create vector store
            self._vectorstore = Chroma.from_documents(
                documents=doc_splits,
                collection_name="himalaya-enterprises",
                embedding=embeddings
            )
            
            # Create retriever
            self._retriever = self._vectorstore.as_retriever(search_kwargs={"k": 3})
            print("Vector store initialized successfully!")
            
        except Exception as e:
            print(f"Error initializing Himalaya Enterprises vectorstore: {e}")
            import traceback
            traceback.print_exc()
            self._vectorstore = None
            self._retriever = None
    
    def _run(self, query: str) -> str:
        """Execute the search for Himalaya Enterprises information."""
        if not self._retriever:
            return "Sorry, I couldn't load information about Himalaya Enterprises at the moment."
        
        try:
            # Retrieve relevant documents
            docs = self._retriever.invoke(query)
            
            if not docs:
                return "No relevant information found about Himalaya Enterprises for your query."
            
            # Combine the retrieved content
            combined_content = "\n\n".join([doc.page_content for doc in docs])
            
            return f"Based on Himalaya Enterprises official information:\n\n{combined_content}"
            
        except Exception as e:
            return f"Error searching Himalaya Enterprises information: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async version of the search."""
        return self._run(query)


def get_himalaya_tool():
    """Return the Himalaya Enterprises search tool."""
    return HimalayaWebLoaderTool()
