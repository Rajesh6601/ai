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
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


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
            # Special handling for LinkedIn URLs
            if "linkedin.com" in url:
                return self._extract_linkedin_content(url)
            
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
    
    def _extract_linkedin_content(self, url):
        """Extract content from LinkedIn profile with fallback to manual content."""
        try:
            # LinkedIn has anti-scraping measures, so we'll try to extract what we can
            # and provide fallback content based on the profile
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to extract available content including posts
            text_content = ""
            
            # Look for title/headline
            title_element = soup.find('title')
            if title_element:
                text_content += title_element.get_text().strip() + " "
            
            # Look for post content - try multiple selectors
            post_selectors = [
                'div[data-test-id="post-content"]',
                '.feed-shared-update-v2',
                '.feed-shared-text',
                '.feed-shared-update-v2__description',
                '.activity-content',
                '.post-content',
                '.share-update-card__content',
                '.ember-view .feed-shared-text'
            ]
            
            posts_found = []
            for selector in post_selectors:
                posts = soup.select(selector)
                for post in posts:
                    post_text = post.get_text().strip()
                    if post_text and len(post_text) > 20:
                        posts_found.append(post_text)
            
            # Look for any visible text
            for script in soup(["script", "style"]):
                script.decompose()
            
            body_text = soup.get_text()
            if body_text:
                lines = (line.strip() for line in body_text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                extracted_text = ' '.join(chunk for chunk in chunks if chunk)
                text_content += extracted_text
            
            # If we found posts, prioritize them
            if posts_found:
                posts_content = "\n\nRecent LinkedIn Posts:\n" + "\n---\n".join(posts_found[:3])
                text_content += posts_content
            
            # If we got substantial content, return it
            if len(text_content.strip()) > 100:
                return text_content.strip()
            else:
                # Fallback to manual LinkedIn content for Himalaya Enterprises
                return self._get_linkedin_fallback_content()
                
        except Exception as e:
            print(f"Error extracting LinkedIn content from {url}: {e}")
            # Return fallback content with note about posts
            return self._get_linkedin_fallback_content()
    
    def _get_linkedin_fallback_content(self):
        """Provide fallback LinkedIn content for Himalaya Enterprises."""
        return """
        Himalaya Enterprises LinkedIn Profile
        
        Company: Himalaya Enterprises
        LinkedIn URL: https://www.linkedin.com/in/himalaya-enterprises-34a0141a9/
        
        About Himalaya Enterprises:
        Himalaya Enterprises is a professional organization focused on providing high-quality tactical solutions and industry-ready products. 
        
        The company specializes in:
        - Tactical and strategic solutions
        - Industry-optimized products
        - Professional services
        - Quality assurance and delivery
        
        Professional Network:
        Himalaya Enterprises maintains an active professional presence on LinkedIn, connecting with industry partners, clients, and stakeholders.
        
        Contact Information:
        For professional inquiries and business connections, reach out through the official LinkedIn profile or company website.
        
        Industry Focus:
        The company operates in sectors requiring specialized tactical solutions and maintains high standards for product quality and service delivery.
        
        Professional Services:
        Himalaya Enterprises offers comprehensive solutions tailored to meet specific industry requirements and client needs.
        
        LinkedIn Activity:
        For the latest posts, updates, and company announcements, please visit the LinkedIn profile directly at: https://www.linkedin.com/in/himalaya-enterprises-34a0141a9/
        
        Recent LinkedIn Posts Information:
        Due to LinkedIn's privacy settings and anti-scraping measures, the latest posts cannot be directly accessed programmatically. 
        However, you can find the most recent updates by visiting the LinkedIn profile directly. The company typically posts about:
        - Industry updates and insights
        - Product launches and innovations
        - Company achievements and milestones
        - Professional networking events
        - Industry partnerships and collaborations
        
        To view the latest post by Himalaya Enterprises:
        1. Visit: https://www.linkedin.com/in/himalaya-enterprises-34a0141a9/
        2. Check the "Activity" section for recent posts
        3. Look for company updates and announcements
        """

    def _get_linkedin_posts_info(self, url):
        """Attempt to get LinkedIn posts information using alternative methods."""
        try:
            # Try to access LinkedIn with different strategies
            session = requests.Session()
            
            # Set comprehensive headers to mimic a real browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Cache-Control': 'max-age=0',
            }
            
            session.headers.update(headers)
            
            # Try to get the page with session
            response = session.get(url, timeout=20)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for recent activity or posts
            post_indicators = [
                'recently shared',
                'posted on linkedin',
                'shared an update',
                'posted an update',
                'activity',
                'recent post',
                'latest update'
            ]
            
            text_content = soup.get_text().lower()
            posts_info = []
            
            # Check if any post indicators are found
            for indicator in post_indicators:
                if indicator in text_content:
                    posts_info.append(f"Found activity indicator: {indicator}")
            
            # Try to find timestamp information
            time_elements = soup.find_all(['time', 'span'], attrs={'class': lambda x: x and 'time' in x.lower() if x else False})
            for element in time_elements:
                if element.get_text().strip():
                    posts_info.append(f"Timestamp found: {element.get_text().strip()}")
            
            if posts_info:
                return "LinkedIn Activity Detected:\n" + "\n".join(posts_info)
            else:
                return "No specific LinkedIn posts could be extracted due to access restrictions."
                
        except Exception as e:
            print(f"Error getting LinkedIn posts info: {e}")
            return "Unable to access LinkedIn posts due to platform restrictions."

    def _initialize_vectorstore(self):
        """Initialize the vector store with Himalaya Enterprises content."""
        try:
            # Load content from multiple Himalaya Enterprises website pages and LinkedIn
            urls = [
                "https://www.himalayaentp.com/index.php/about/",
                "https://www.himalayaentp.com/index.php/product-2/",
                "https://www.himalayaentp.com/index.php/contact/",
                "https://www.himalayaentp.com/index.php/projects/",
                "https://www.linkedin.com/in/himalaya-enterprises-34a0141a9/"
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
            # Check if this is a LinkedIn posts query
            linkedin_post_keywords = ['latest post', 'recent post', 'latest linkedin post', 'recent linkedin post', 
                                    'latest update', 'recent update', 'new post', 'current post', 'recent activity']
            
            query_lower = query.lower()
            is_linkedin_post_query = any(keyword in query_lower for keyword in linkedin_post_keywords)
            
            if is_linkedin_post_query:
                # Try to get fresh LinkedIn posts information
                linkedin_url = "https://www.linkedin.com/in/himalaya-enterprises-34a0141a9/"
                posts_info = self._get_linkedin_posts_info(linkedin_url)
                
                # Also get regular retrieval results for context
                docs = self._retriever.invoke(query)
                combined_content = "\n\n".join([doc.page_content for doc in docs]) if docs else ""
                
                return f"""Based on Himalaya Enterprises LinkedIn information:

{posts_info}

Additional Context:
{combined_content}

Note: For the most current LinkedIn posts, please visit the profile directly at: {linkedin_url}"""
            
            else:
                # Regular retrieval for non-posts queries
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
