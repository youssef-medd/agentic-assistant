from duckduckgo_search import DDGS
def web_search(query, max_results=3):
    results = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append(f"Title: {r['title']}\nSnippet: {r['body']}\nSource: {r['href']}\n")
        return "\n".join(results) if results else "No results found."
    except Exception as e:
        return f"Search failed: {e}"