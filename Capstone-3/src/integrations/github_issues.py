"""GitHub Issues integration for support ticket management"""
from github import Github, GithubException
from typing import Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GitHubIssuesClient:
    """Manage support tickets using GitHub Issues"""
    
    def __init__(self, token: str, repo_owner: str, repo_name: str):
        """
        Initialize GitHub client
        
        Args:
            token: GitHub personal access token
            repo_owner: Repository owner username
            repo_name: Repository name
        """
        self.token = token
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        
        try:
            self.client = Github(token)
            self.repo = self.client.get_repo(f"{repo_owner}/{repo_name}")
            logger.info(f"Connected to GitHub repository: {repo_owner}/{repo_name}")
        except GithubException as e:
            logger.error(f"Failed to connect to GitHub: {str(e)}")
            raise
    
    def create_issue(
        self,
        title: str,
        description: str,
        user_name: str,
        user_email: str,
        labels: Optional[list] = None
    ) -> Dict[str, any]:
        """
        Create a GitHub issue for a support ticket
        
        Args:
            title: Issue title (ticket summary)
            description: Issue description (ticket details)
            user_name: User's name
            user_email: User's email
            labels: List of labels to add to the issue
            
        Returns:
            Dictionary with issue details
        """
        try:
            # Format the issue body
            body = f"""**Support Ticket**

**User Information:**
- Name: {user_name}
- Email: {user_email}

**Description:**
{description}
"""
            
            # Default labels
            if labels is None:
                labels = ["support-ticket"]
            
            # Create the issue
            issue = self.repo.create_issue(
                title=title,
                body=body,
                labels=labels
            )
            
            logger.info(f"Created GitHub issue #{issue.number}: {title}")
            
            return {
                "success": True,
                "issue_number": issue.number,
                "issue_url": issue.html_url,
                "title": title
            }
            
        except GithubException as e:
            logger.error(f"Failed to create GitHub issue: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_issue(self, issue_number: int):
        """Get a specific issue by number"""
        try:
            return self.repo.get_issue(issue_number)
        except GithubException as e:
            logger.error(f"Failed to get issue #{issue_number}: {str(e)}")
            return None
    
    def list_open_issues(self, limit: int = 10):
        """List open issues"""
        try:
            issues = self.repo.get_issues(state='open', labels=["support-ticket"])
            return list(issues[:limit])
        except GithubException as e:
            logger.error(f"Failed to list issues: {str(e)}")
            return []
