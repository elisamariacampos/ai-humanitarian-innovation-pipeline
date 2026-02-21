
"""
AI Content Publisher Pipeline (Open Template)
============================================

This is a generic publishing pipeline template that:

1. Receives approved content (e.g., from a spreadsheet or JSON)
2. Sends text to an AI API for rewriting
3. Fetches a contextual image from a stock image API
4. Publishes the result as a draft to WordPress via REST API

⚠️ This template does NOT include:
- Real API keys
- Real WordPress credentials
- Personal site URLs
- Private endpoints

Users must configure their own credentials and endpoints.

Required packages:
    pip install requests openai

"""

import requests
import base64

# ─────────────────────────────────────────────
# CONFIGURATION (USER MUST EDIT)
# ─────────────────────────────────────────────

OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
IMAGE_API_KEY = "YOUR_IMAGE_API_KEY"

WORDPRESS_URL = "https://yourwordpresssite.com"
WORDPRESS_USERNAME = "your_username"
WORDPRESS_APP_PASSWORD = "your_application_password"

AI_MODEL = "gpt-4o-mini"


# ─────────────────────────────────────────────
# AI REWRITE FUNCTION
# ─────────────────────────────────────────────

def rewrite_with_ai(title, content):

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": AI_MODEL,
        "messages": [
            {"role": "system", "content": "You are an editorial assistant focused on social impact journalism."},
            {"role": "user", "content": f"Rewrite the following article professionally:\n\nTitle: {title}\n\n{content}"}
        ]
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        print("AI rewrite failed:", response.text)
        return content


# ─────────────────────────────────────────────
# IMAGE FETCH FUNCTION (Generic Example)
# ─────────────────────────────────────────────

def fetch_image(query):

    headers = {
        "Authorization": IMAGE_API_KEY
    }

    response = requests.get(
        f"https://api.exampleimage.com/search?query={query}&per_page=1",
        headers=headers
    )

    if response.status_code == 200:
        data = response.json()
        return data["results"][0]["image_url"]
    else:
        print("Image fetch failed:", response.text)
        return None


# ─────────────────────────────────────────────
# WORDPRESS DRAFT PUBLISHER
# ─────────────────────────────────────────────

def publish_to_wordpress(title, content, image_url=None):

    credentials = f"{WORDPRESS_USERNAME}:{WORDPRESS_APP_PASSWORD}"
    token = base64.b64encode(credentials.encode())

    headers = {
        "Authorization": f"Basic {token.decode()}",
        "Content-Type": "application/json"
    }

    post_data = {
        "title": title,
        "content": content,
        "status": "draft"
    }

    response = requests.post(
        f"{WORDPRESS_URL}/wp-json/wp/v2/posts",
        headers=headers,
        json=post_data
    )

    if response.status_code == 201:
        print("Draft created successfully.")
    else:
        print("WordPress publishing failed:", response.text)


# ─────────────────────────────────────────────
# MAIN EXECUTION EXAMPLE
# ─────────────────────────────────────────────

def run_publisher_pipeline():

    example_title = "Sample Social Innovation Article"
    example_content = "This is a placeholder article content for demonstration purposes."

    rewritten = rewrite_with_ai(example_title, example_content)
    image_url = fetch_image("social innovation")

    publish_to_wordpress(example_title, rewritten, image_url)


if __name__ == "__main__":
    run_publisher_pipeline()
