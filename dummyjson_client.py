import requests
from typing import Dict, Any
from exceptions import APIError

class DummyJsonClient:
    BASE_URL = "https://dummyjson.com"
    TIMEOUT = 10  # Default timeout in seconds
    
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.token = None
        self.session = requests.Session()
        self.user_id = None
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        try:
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                raise APIError("Authentication failed")
            elif response.status_code == 404:
                raise APIError(f"Resource not found: {response.url}")
            elif response.status_code == 500:
                raise APIError("Internal server error")
            else:
                raise APIError(f"API request failed with status code {response.status_code}")
        except requests.exceptions.JSONDecodeError:
            raise APIError(f"Invalid JSON response from API: {response.text[:100]}...")
        
    def test_connectivity(self) -> bool:
        try:
            print(f"Testing connectivity to {self.BASE_URL}")
            response = self.session.post(f"{self.BASE_URL}/auth/login", json={"username": self.username, "password": self.password}, timeout=self.TIMEOUT)
            data = self._handle_response(response)
            
            self.token = data.get("accessToken")
            
            # Set the authorization header
            if self.token:
                self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                self.user_id = data.get("id")
                return True
            else:
                print("No accessToken found in authentication response")
                return False
        except Exception as e:
            print(f"Connectivity test failed: {str(e)}")
            return False
    
    def get_user_details(self) -> Dict[str, Any]:
        if not self.token:
            raise APIError("Not authenticated")
        
        try:
            if self.user_id:
                url = f"{self.BASE_URL}/users/{self.user_id}"
            else:
                url = f"{self.BASE_URL}/auth/me"
                
            print(f"Fetching user details from {url}")
            response = self.session.get(url, timeout=self.TIMEOUT)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching user details: {str(e)}")
            raise APIError(f"Failed to get user details: {str(e)}")
    
    def get_posts(self, limit: int = 60) -> Dict[str, Any]:
        try:
            print(f"Fetching posts with limit={limit}")
            response = self.session.get(f"{self.BASE_URL}/posts", params={"limit": limit}, timeout=self.TIMEOUT)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching posts: {str(e)}")
            raise APIError(f"Failed to get posts: {str(e)}")
    
    def get_posts_with_comments(self, limit: int = 60) -> Dict[str, Any]:
        try:
            posts = self.get_posts(limit)
            
            # Get comments for each post
            for post in posts.get("posts", []):
                post_id = post.get("id")
                print(f"Fetching comments for post ID {post_id}")
                try:
                    response = self.session.get(f"{self.BASE_URL}/posts/{post_id}/comments", timeout=self.TIMEOUT)
                    comments = self._handle_response(response)
                    post["comments"] = comments.get("comments", [])
                except Exception as e:
                    print(f"Failed to get comments for post {post_id}: {str(e)}")
                    post["comments"] = []
            
            return posts
        except requests.exceptions.RequestException as e:
            print(f"Error fetching posts with comments: {str(e)}")
            raise APIError(f"Failed to get posts with comments: {str(e)}")
