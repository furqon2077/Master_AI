"""Function calling definitions for the AI agent"""
import json
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Function schemas for Google Gemini function calling
FUNCTION_DECLARATIONS = [
    {
        "name": "search_documents",
        "description": "Search the knowledge base for information to answer user questions. Use this when the user asks a question that might be answered in the documentation.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to find relevant information in the knowledge base"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "create_support_ticket",
        "description": "Create a support ticket when the user requests it or when you cannot find an answer in the knowledge base. The ticket will be created in the issue tracking system.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_name": {
                    "type": "string",
                    "description": "The user's full name"
                },
                "user_email": {
                    "type": "string",
                    "description": "The user's email address"
                },
                "summary": {
                    "type": "string",
                    "description": "Brief summary/title of the issue (one sentence)"
                },
                "description": {
                    "type": "string",
                    "description": "Detailed description of the issue or question"
                }
            },
            "required": ["user_name", "user_email", "summary", "description"]
        }
    },
    {
        "name": "get_company_info",
        "description": "Get company contact information when the user asks about how to contact support, company details, or wants to speak with someone.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]


class FunctionExecutor:
    """Execute functions called by the AI agent"""
    
    def __init__(self, vector_store, ticket_manager, company_info):
        """
        Initialize function executor
        
        Args:
            vector_store: VectorStore instance for document search
            ticket_manager: TicketManager instance for ticket creation
            company_info: Dictionary with company information
        """
        self.vector_store = vector_store
        self.ticket_manager = ticket_manager
        self.company_info = company_info
    
    def search_documents(self, query: str) -> Dict:
        """
        Search documents in the knowledge base
        
        Args:
            query: Search query
            
        Returns:
            Dictionary with search results
        """
        logger.info(f"Searching documents for: {query}")
        
        try:
            results = self.vector_store.search(query, top_k=3)
            
            if not results:
                return {
                    "success": False,
                    "message": "No relevant information found in the knowledge base.",
                    "results": []
                }
            
            # Format results with citations
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "content": result["content"],
                    "source": result["metadata"]["source"],
                    "page": result["metadata"]["page"]
                })
            
            return {
                "success": True,
                "message": "Found relevant information",
                "results": formatted_results
            }
            
        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}")
            return {
                "success": False,
                "message": f"Error searching knowledge base: {str(e)}",
                "results": []
            }
    
    def create_support_ticket(
        self,
        user_name: str,
        user_email: str,
        summary: str,
        description: str
    ) -> Dict:
        """
        Create a support ticket
        
        Args:
            user_name: User's name
            user_email: User's email
            summary: Ticket summary
            description: Ticket description
            
        Returns:
            Dictionary with ticket creation result
        """
        logger.info(f"Creating support ticket for {user_name}")
        
        try:
            result = self.ticket_manager.create_ticket(
                user_name=user_name,
                user_email=user_email,
                summary=summary,
                description=description
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error creating ticket: {str(e)}")
            return {
                "success": False,
                "error": f"Failed to create ticket: {str(e)}"
            }
    
    def get_company_info(self) -> Dict:
        """
        Get company contact information
        
        Returns:
            Dictionary with company information
        """
        return {
            "success": True,
            "company_name": self.company_info["name"],
            "email": self.company_info["email"],
            "phone": self.company_info["phone"]
        }
    
    def execute_function(self, function_name: str, function_args: Dict) -> Dict:
        """
        Execute a function by name
        
        Args:
            function_name: Name of the function to execute
            function_args: Arguments for the function
            
        Returns:
            Function execution result
        """
        if function_name == "search_documents":
            return self.search_documents(**function_args)
        
        elif function_name == "create_support_ticket":
            return self.create_support_ticket(**function_args)
        
        elif function_name == "get_company_info":
            return self.get_company_info()
        
        else:
            return {
                "success": False,
                "error": f"Unknown function: {function_name}"
            }
