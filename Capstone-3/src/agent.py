"""AI Agent with OpenAI GPT and function calling"""
from openai import OpenAI
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
        # Initialize OpenAI client
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.OPENAI_MODEL
        
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
    
    def get_messages_for_openai(self, user_message: str) -> List[Dict]:
        """Format messages for OpenAI API"""
        messages = [
            {"role": "system", "content": self.system_instruction}
        ]
        
        # Add conversation history
        for msg in self.conversation_history:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Add current message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        return messages
    
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
            # Prepare messages
            messages = self.get_messages_for_openai(user_message)
            
            # Call OpenAI with function calling
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=FUNCTION_DECLARATIONS,
                tool_choice="auto",
                temperature=Config.OPENAI_TEMPERATURE,
                max_tokens=Config.OPENAI_MAX_TOKENS
            )
            
            # Handle function calls
            max_iterations = 5
            iteration = 0
            
            while iteration < max_iterations:
                message = response.choices[0].message
                
                # Check if there are tool calls
                if message.tool_calls:
                    # Add assistant message to messages
                    messages.append(message)
                    
                    # Process each tool call
                    for tool_call in message.tool_calls:
                        function_name = tool_call.function.name
                        function_args = json.loads(tool_call.function.arguments)
                        
                        logger.info(f"Function call: {function_name} with args: {function_args}")
                        
                        # Add user info to ticket creation if available
                        if function_name == "create_support_ticket":
                            # Only use default/session values if LLM didn't extract them
                            if user_name and "user_name" not in function_args:
                                function_args["user_name"] = user_name
                            elif user_name and function_args.get("user_name") in ["Guest", "Unknown", None, ""]:
                                # If LLM put a placeholder, try to use session value (though session might also be Guest)
                                # But if session is Guest, it's fine. If session was real name, we want it.
                                # Actually, primarily we want to NOT overwrite if LLM found a real name.
                                pass 
                            
                            # Simple logic: If LLM provided a value, trust it. If not, use passed value.
                            # But wait, previous logic was ALWAYS overwrite. 
                            # New logic: valid if key missing or empty.
                            if not function_args.get("user_name") and user_name:
                                function_args["user_name"] = user_name
                                
                            if not function_args.get("user_email") and user_email:
                                function_args["user_email"] = user_email
                        
                        # Execute function
                        function_result = self.function_executor.execute_function(
                            function_name, function_args
                        )
                        
                        logger.info(f"Function result: {function_result}")
                        
                        # Add function result to messages
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": function_name,
                            "content": json.dumps(function_result)
                        })
                    
                    # Call OpenAI again with function results
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=messages,
                        tools=FUNCTION_DECLARATIONS,
                        tool_choice="auto",
                        temperature=Config.OPENAI_TEMPERATURE,
                        max_tokens=Config.OPENAI_MAX_TOKENS
                    )
                    
                    iteration += 1
                else:
                    # No more function calls, we have the final response
                    break
            
            # Extract final text response
            final_response = response.choices[0].message.content
            
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
