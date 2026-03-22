import random
import string
import re
from locust import HttpUser, task, between

class PhotoAlbumUser(HttpUser):
    wait_time = between(2, 5) # Slightly longer wait for realism
    host = "https://gallery-488215.ey.r.appspot.com"

    def extract_csrf(self, response):
        """Extracts CSRF token from HTML or Cookies."""
        # Try to find it in the HTML source first
        match = re.search(r'name="csrfmiddlewaretoken"\s+value="([^"]+)"', response.text)
        if match:
            return match.group(1)
        # Fallback to cookies
        return response.cookies.get("csrftoken", "")

    def on_start(self):
        """User Setup: Register and Login."""
        suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        self.username = f"tester_{suffix}"
        self.password = "Pass12345!"

        # --- 1. GET SIGNUP PAGE ---
        res = self.client.get("/signup/")
        token = self.extract_csrf(res)

        # --- 2. POST SIGNUP ---
        # We add the Referer header to satisfy Django's security checks
        headers = {"X-CSRFToken": token, "Referer": f"{self.host}/signup/"}
        self.client.post("/signup/", data={
            "username": self.username,
            "password1": self.password,
            "password2": self.password,
            "csrfmiddlewaretoken": token
        }, headers=headers)

        # --- 3. GET LOGIN PAGE ---
        res = self.client.get("/login/")
        token = self.extract_csrf(res)

        # --- 4. POST LOGIN ---
        headers = {"X-CSRFToken": token, "Referer": f"{self.host}/login/"}
        self.client.post("/login/", data={
            "username": self.username,
            "password": self.password,
            "csrfmiddlewaretoken": token
        }, headers=headers)

    @task(2)
    def view_gallery(self):
        self.client.get("/")

    @task(1)
    def upload_and_delete(self):
        """Full lifecycle: Upload then Delete."""
        # --- A. UPLOAD ---
        res = self.client.get("/upload/")
        token = self.extract_csrf(res)
        
        dummy_file = ("test.jpg", b"fake-image-content", "image/jpeg")
        headers = {"X-CSRFToken": token, "Referer": f"{self.host}/upload/"}
        
        up_res = self.client.post("/upload/", 
            data={"title": "Locust Photo", "csrfmiddlewaretoken": token},
            files={"image": dummy_file},
            headers=headers
        )

        # --- B. DELETE (only if upload was successful) ---
        if up_res.status_code == 200 or up_res.status_code == 302:
            # Re-fetch home to get the delete URL of the new photo
            home_res = self.client.get("/")
            token = self.extract_csrf(home_res)
            
            # Find the first delete link available to this user
            match = re.search(r'/delete/(\d+)/', home_res.text)
            if match:
                pk = match.group(1)
                del_headers = {"X-CSRFToken": token, "Referer": f"{self.host}/"}
                self.client.post(f"/delete/{pk}/", 
                    data={"csrfmiddlewaretoken": token}, 
                    headers=del_headers
                )