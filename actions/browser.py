import webbrowser

def open_url(url):
    webbrowser.open(url)
    return f"Opening {url}"

def open_google():
    webbrowser.open("https://www.google.com")
    return "Opening Google"


def google_search(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    return f"Searching Google for {query}"