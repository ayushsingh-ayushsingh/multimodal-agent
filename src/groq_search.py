from groq import Groq
from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv

load_dotenv(".env.local")


def searxng_search(query: str, num_results=5):
    """
    Perform a direct SearXNG search via JSON API 
    and return a list of URLs.
    """
    SEARXNG_URL = os.getenv("SEARXNG_URL", "http://localhost:8080/search")

    try:
        response = requests.get(
            SEARXNG_URL,
            params={
                "q": query,
                "format": "json",
                "engines": "duckduckgo,google,wikipedia,qwant",
                "language": "en",
            },
            timeout=10,
        )

        data = response.json()
        results = data.get("results", [])
        urls = [r.get("url") for r in results if "url" in r]

        return urls[:num_results]

    except Exception as e:
        print("Error querying SearXNG:", e)
        return []


# ------------------------------------------------------------
# SCRAPE RAW TEXT FROM A URL
# ------------------------------------------------------------
def fetch_page_text(url: str):
    """Fetches plain text from a given web page."""
    try:
        res = requests.get(url, timeout=10, headers={
                           "User-Agent": "Mozilla/5.0"})

        if res.status_code != 200:
            return f"[HTTP {res.status_code}]"

        soup = BeautifulSoup(res.text, "html.parser")
        text = soup.get_text(separator="\n", strip=True)

        return text if text.strip() else "[NO TEXT FOUND]"

    except Exception as e:
        return f"[FETCH FAILED: {e}]"


# ------------------------------------------------------------
# MAIN ASSISTANT FUNCTION
# ------------------------------------------------------------
def web_search_assistant(query: str, num_results=3):
    """
    Search → fetch → save → summarize using Groq.
    """
    print(f"Searching: {query}")
    print(f"\n\n\n\n\n\n\n\n\n\n\n\n")

    # Step 1: Search
    urls = searxng_search(query, num_results=num_results)

    if not urls:
        return f"No results found for '{query}'. Check your SearXNG config."

    print(f"Found {len(urls)} URLs.")

    # Step 2: Fetch each page's text
    pages = {}
    for url in urls:
        print(f"Fetching: {url}")
        pages[url] = fetch_page_text(url)

    # Step 3: Save to file
    with open("fetched_data.txt", "w", encoding="utf-8") as f:
        for url, text in pages.items():
            f.write(f"URL: {url}\n")
            f.write("=" * 80 + "\n")
            f.write(text)
            f.write("\n\n")

    print("Saved fetched content to fetched_data.txt")

    # Step 4: Prepare combined text
    combined_text = "\n\n".join(pages.values())
    combined_text = combined_text[:9000]  # limit size

    if not combined_text.strip():
        return "Fetched content was empty — cannot summarize."

    # Step 5: Groq summarization
    print("Summarizing using Groq...")

    groq_client = Groq()

    completion = groq_client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": "You are a web search assistant."},
            {
                "role": "user",
                "content": (
                    f"Summarize the following collected web content about '{query}' "
                    f"in 1–2 paragraphs:\n\n{combined_text}"
                ),
            },
        ],
        max_completion_tokens=500,
        temperature=0.7,
        top_p=1,
        reasoning_effort="medium",
    )

    return completion.choices[0].message.content


# ------------------------------------------------------------
# Runner (for testing)
# ------------------------------------------------------------
if __name__ == "__main__":
    print(web_search_assistant("Delhi Pollution"))
