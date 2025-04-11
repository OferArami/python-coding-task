from typing import Dict, Any, List
from dummyjson_client import DummyJsonClient
from exceptions import APIError

class Plugin:
    def __init__(self, username: str, password: str):
        self.client = DummyJsonClient(username, password)
    
    def test_connectivity(self) -> bool:
        """Test connectivity to the API."""
        return self.client.test_connectivity()
    
    def collect_evidence(self) -> Dict[str, Any]:
        """Collect all required evidence."""
        if not self.test_connectivity():
            raise APIError("Failed to establish connection with the API")
        
        evidence = {
            "E1": self._collect_user_details(),
            "E2": self._collect_posts(),
            "E3": self._collect_posts_with_comments()
        }
        
        return evidence
    
    def _collect_user_details(self) -> Dict[str, Any]:
        """Collect evidence E1: User details."""
        return self.client.get_user_details()
    
    def _collect_posts(self) -> Dict[str, Any]:
        """Collect evidence E2: List of posts."""
        return self.client.get_posts()
    
    def _collect_posts_with_comments(self) -> Dict[str, Any]:
        """Collect evidence E3: List of posts with comments."""
        return self.client.get_posts_with_comments() 