"""Support ticket management"""
from typing import Dict, Optional
from src.integrations.github_issues import GitHubIssuesClient
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TicketManager:
    """Manage support ticket creation and tracking"""
    
    def __init__(self, github_token: str, repo_owner: str, repo_name: str):
        """
        Initialize ticket manager
        
        Args:
            github_token: GitHub API token
            repo_owner: GitHub repository owner
            repo_name: GitHub repository name
        """
        self.github_client = GitHubIssuesClient(
            token=github_token,
            repo_owner=repo_owner,
            repo_name=repo_name
        )
    
    def create_ticket(
        self,
        user_name: str,
        user_email: str,
        summary: str,
        description: str
    ) -> Dict[str, any]:
        """
        Create a support ticket
        
        Args:
            user_name: User's name
            user_email: User's email
            summary: Ticket summary/title
            description: Detailed description
            
        Returns:
            Dictionary with ticket creation result
        """
        # Validate inputs
        if not user_name or not user_email:
            return {
                "success": False,
                "error": "User name and email are required"
            }
        
        if not summary:
            return {
                "success": False,
                "error": "Ticket summary is required"
            }
        
        # Create the issue in GitHub
        result = self.github_client.create_issue(
            title=summary,
            description=description or "No additional details provided",
            user_name=user_name,
            user_email=user_email
        )
        
        if result["success"]:
            logger.info(f"Support ticket created: #{result['issue_number']}")
        
        return result
    
    def validate_ticket_data(
        self,
        user_name: Optional[str],
        user_email: Optional[str],
        summary: Optional[str],
        description: Optional[str]
    ) -> Dict[str, any]:
        """
        Validate ticket data
        
        Returns:
            Dictionary with validation result and missing fields
        """
        missing_fields = []
        
        if not user_name:
            missing_fields.append("user_name")
        
        if not user_email:
            missing_fields.append("user_email")
        
        if not summary:
            missing_fields.append("summary")
        
        return {
            "valid": len(missing_fields) == 0,
            "missing_fields": missing_fields
        }
