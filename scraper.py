import requests
from bs4 import BeautifulSoup

def fetch_html(url):
    """
    Attempts to fetch the HTML content of a URL.
    Returns a tuple: (html_content, error_message)
    """
    # Use a standard User-Agent so websites don't immediately block us as a bot
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Triggers an error for 404, 500, etc.
        return response.text, None
    except requests.exceptions.RequestException as e:
        return None, f"Could not fetch URL. The site might block bots or require JavaScript. Error: {e}"

def extract_ui_snippets(html_content):
    """
    Parses HTML and extracts short text snippets from likely UI elements.
    """
    soup = BeautifulSoup(html_content, 'lxml')
    snippets = set() # Use a set to automatically remove duplicate text
    
    # 1. Target standard interactive UI tags
    ui_tags = ['button', 'a', 'span', 'label', 'strong', 'em', 'h3', 'h4']
    for tag in soup.find_all(ui_tags):
        text = tag.get_text(separator=' ', strip=True)
        # Keep only short phrases (e.g., 2 to 20 words). Dark patterns are punchy.
        if text and 1 < len(text.split()) <= 20:
            snippets.add(text)
            
    # 2. Target divs, but safely. Divs often hold entire articles.
    # We only want direct text inside a div, not all its nested children.
    for div in soup.find_all('div'):
        text = "".join(div.find_all(string=True, recursive=False)).strip()
        if text and 1 < len(text.split()) <= 15:
            snippets.add(text)
            
    return list(snippets)

def process_input(user_input, is_url=True):
    """
    Master function to handle either a URL or raw HTML/Text.
    """
    if is_url:
        html, error = fetch_html(user_input)
        if error:
            return [], error
        return extract_ui_snippets(html), None
    else:
        # If the user pasted raw HTML or text, skip the requests module
        return extract_ui_snippets(user_input), None