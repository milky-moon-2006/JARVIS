import urllib.parse, webbrowser
SITES={"google":"https://www.google.com","youtube":"https://www.youtube.com","chatgpt":"https://chatgpt.com","openai":"https://openai.com","gemini":"https://gemini.google.com","whatsapp":"https://web.whatsapp.com"}
def open_site(name):
    url=SITES.get(name.lower())
    if not url: return False
    webbrowser.open(url); return True
def google_search(q): webbrowser.open("https://www.google.com/search?q="+urllib.parse.quote(q))
def youtube_search(q): webbrowser.open("https://www.youtube.com/results?search_query="+urllib.parse.quote(q))
