"""AI Agent with Google Gemini and function calling"""
import google.generativeai as genai
from typing import List, Dict, Optional
import json
import logging
from src.functions import FUNCTION_DECLARATIONS, FunctionExecutor
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CustomerSupportAgent:
    """AI agent for customer support with function calling capabilities"""
    
    def __init__(self, vector_store, ticket_manager):
        """
        Initialize the customer support agent
        
        Args:
            vector_store: VectorStore instance
            ticket_manager: TicketManager instance
        """
        # Configure Gemini
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        
        # Initialize model with function calling
        self.model = genai.GenerativeModel(
            model_name=Config.GEMINI_MODEL,
            tools=FUNCTION_DECLARATIONS
        )
        
        # Initialize function executor
        company_info = {
            "name": Config.COMPANY_NAME,
            "email": Config.COMPANY_EMAIL,
            "phone": Config.COMPANY_PHONE
        }
        
        self.function_executor = FunctionExecutor(
            vector_store=vector_store,
            ticket_manager=ticket_manager,
            company_info=company_info
        )
        
        # System instruction
        self.system_instruction = Config.SYSTEM_PROMPT
        
        # Conversation history
        self.conversation_history = []
    
    def add_to_history(self, role: str, content: str):
        """Add a message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content
        })
        
        # Keep only recent history
        if len(self.conversation_history) > Config.MAX_CONVERSATION_HISTORY * 2:
            self.conversation_history = self.conversation_history[-Config.MAX_CONVERSATION_HISTORY * 2:]
    
    def get_chat_history_for_gemini(self) -> List[Dict]:
        """Format chat history for Gemini API"""
        formatted_history = []
        
        for msg in self.conversation_history:
            formatted_history.append({
                "role": "user" if msg["role"] == "user" else "model",
                "parts": [msg["content"]]
            })
        
        return formatted_history
    
    def process_message(self, user_message: str, user_name: str = None, user_email: str = None) -> str:
        """
        Process a user message and generate a response
        
        Args:
            user_message: User's message
            user_name: User's name (optional, needed for ticket creation)
            user_email: User's email (optional, needed for ticket creation)
            
        Returns:
            Agent's response
        """
        # Add user message to history
        self.add_to_history("user", user_message)
        
        try:
            # Create chat session with history
            chat = self.model.start_chat(history=self.get_chat_history_for_gemini())
            
            # Send message
            response = chat.send_message(user_message)
            
            # Handle function calls
            max_iterations = 5
            iteration = 0
            
            while iteration < max_iterations:
                # Check if there are function calls
                if response.candidates[0].content.parts:
                    part = response.candidates[0].content.parts[0]
                    
                    # Check if it's a function call
                    if hasattr(part, 'function_call') and part.function_call:
                        function_call = part.function_call
                        function_name = function_call.name
                        function_args = dict(function_call.args)
                        
                        logger.info(f"Function call: {function_name} with args: {function_args}")
                        
                        # Add user info to ticket creation if available
                        if function_name == "create_support_ticket":
                            if user_name:
                                function_args["user_name"] = user_name
                            if user_email:
                                function_args["user_email"] = user_email
                        
                        # Execute function
                        function_result = self.function_executor.execute_function(
                            function_name, function_args
                        )
                        
                        logger.info(f"Function result: {function_result}")
                        
                        # Send function result back to model
                        response = chat.send_message({
                            "function_response": {
                                "name": function_name,
                                "response": function_result
                            }
                        })
                        
                        iteration += 1
                    else:
                        # No function call, we have the final response
                        break
                else:
                    break
            
            # Extract final text response
            final_response = response.text
            
            # Add to history
            self.add_to_history("assistant", final_response)
            
            return final_response
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            error_message = f"I apologize, but I encountered an error: {str(e)}. Please try again or contact support directly."
            self.add_to_history("assistant", error_message)
            return error_message
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")
    
    def get_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history
