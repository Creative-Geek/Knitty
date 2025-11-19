"""Job posting processing, web scraping, and RAG extraction."""

import json
import logging
import sys
import asyncio
from typing import Optional, Dict, Any
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_core.prompts import ChatPromptTemplate
from ..config.settings import Settings
from .llm_clients import LLMClients
from ..config.prompts import PromptManager

logger = logging.getLogger(__name__)


class JobProcessor:
    """Processes job postings from URLs or text."""
    
    def __init__(self, llm_clients: LLMClients, prompt_manager: PromptManager, settings: Settings):
        """Initialize job processor."""
        self.llm_clients = llm_clients
        self.prompt_manager = prompt_manager
        self.settings = settings
    
    async def fetch_url(self, job_posting_url: str) -> str:
        """Fetch HTML content from URL using Playwright."""
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        
        def run_sync_playwright():
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()
                page.goto(job_posting_url, wait_until="networkidle")
                
                content = page.content()
                browser.close()
                return content
        
        try:
            content = await asyncio.to_thread(run_sync_playwright)
            logger.info(f"Fetched HTML from URL: {job_posting_url}")
            return content
        except Exception as e:
            logger.error(f"Error fetching URL: {e}")
            raise ValueError(f"Failed to fetch URL: {e}")
    
    def clean_html(self, html_content: str) -> str:
        """Clean HTML and extract text content."""
        try:
            soup = BeautifulSoup(html_content, "html.parser")
            
            # Remove script and style tags
            for tag in soup(["script", "style"]):
                tag.decompose()
            
            text = soup.get_text(separator="\n", strip=True)
            logger.info(f"Cleaned HTML, extracted {len(text)} characters")
            return text
        except Exception as e:
            logger.error(f"Error cleaning HTML: {e}")
            raise ValueError(f"Failed to clean HTML: {e}")
    
    def _embed_text(self, text: str) -> InMemoryVectorStore:
        """Create vector store from text."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.settings.chunk_size,
            chunk_overlap=self.settings.chunk_overlap
        )
        
        documents = [Document(page_content=text)]
        chunks = text_splitter.split_documents(documents)
        logger.info(f"Created {len(chunks)} chunks for RAG")
        
        vector_store = InMemoryVectorStore.from_documents(
            chunks,
            self.llm_clients.embed_llm
        )
        
        return vector_store
    
    def extract_job_with_rag(self, job_extracted_text: str) -> Dict[str, Any]:
        """Extract structured job information using RAG."""
        try:
            # Create vector store
            vector_store = self._embed_text(job_extracted_text)
            
            # Retrieve relevant chunks
            retriever = vector_store.as_retriever(search_kwargs={"k": 3})
            query = "job title responsibilities qualifications requirements description"
            relevant_pieces = retriever.invoke(query)
            
            if not relevant_pieces:
                logger.warning("No relevant chunks found in RAG")
                return {"error": "No relevant job information found"}
            
            combined_context = "\n\n".join([doc.page_content for doc in relevant_pieces[:3]])
            
            # Extract structured information
            complete_job_rag_prompt = ChatPromptTemplate.from_messages([
                ("system", self.prompt_manager.job_rag_prompt),
                ("human", "Extract the job details from this text:\n\n{text}")
            ])
            
            chain = complete_job_rag_prompt | self.llm_clients.fast_llm
            response = chain.invoke({"text": combined_context})
            
            # Parse JSON response
            json_text = response.content.strip()
            
            # Remove code blocks if present
            if json_text.startswith('```json'):
                json_text = json_text[7:]
            if json_text.startswith('```'):
                json_text = json_text[3:]
            if json_text.endswith('```'):
                json_text = json_text[:-3]
            json_text = json_text.strip()
            
            job_posting_data = json.loads(json_text)
            logger.info("Successfully extracted job information via RAG")
            return job_posting_data
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {e}")
            raise ValueError(f"Failed to parse job information: {e}")
        except Exception as e:
            logger.error(f"Error in RAG extraction: {e}")
            raise ValueError(f"Failed to extract job information: {e}")
    
    async def extract_job_posting_from_url(self, job_posting_url: str) -> Dict[str, Any]:
        """Complete pipeline for extracting job posting from URL."""
        html_content = await self.fetch_url(job_posting_url)
        job_extracted_text = self.clean_html(html_content)
        job_posting_data = self.extract_job_with_rag(job_extracted_text)
        return job_posting_data
    
    def extract_keywords(self, job_posting_text: str) -> str:
        """Extract keywords from job posting using Fast LLM."""
        try:
            prompt = self.prompt_manager.format_job_keywords_prompt(job_posting_text)
            response = self.llm_clients.fast_llm.invoke([("human", prompt)])
            
            # Clean JSON response
            content = response.content.strip()
            if content.startswith('```json'):
                content = content[7:]
            if content.startswith('```'):
                content = content[3:]
            if content.endswith('```'):
                content = content[:-3]
            content = content.strip()
            
            logger.info("Extracted keywords from job posting")
            return content
        except Exception as e:
            logger.error(f"Error extracting job keywords: {e}")
            raise ValueError(f"Failed to extract job keywords: {e}")

