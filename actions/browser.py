import webbrowser

def open_url(url):
    webbrowser.open(url)
    return f"URL opened successfully: {url}"

def open_google():
    webbrowser.open("https://www.google.com")
    return "Google opened successfully"


def google_search(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    return f"Here are your search results"