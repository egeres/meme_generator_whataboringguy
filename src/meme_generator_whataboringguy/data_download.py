from pathlib import Path
import requests
import wikipedia
import wikipediaapi
from bs4 import BeautifulSoup
from urllib.parse import unquote


def fuzzy_search_wikipedia(query):
    # Perform a search for titles using the `wikipedia` library
    search_results = wikipedia.search(query)

    if not search_results:
        return "No results found."

    # Take the first result and use `wikipediaapi` to get the full URL
    first_result = search_results[0]
    wiki_wiki = wikipediaapi.Wikipedia("MyProjectName (merlin@example.com)", "en")
    page = wiki_wiki.page(first_result)

    if page.exists():
        return page.fullurl
    else:
        return "Page does not exist, even though it was found in search."


def get_infobox_image_url_new(page_title):
    if page_title.startswith("http://") or page_title.startswith("https://"):
        # Extract the title and decode URL encoding
        page_title = unquote(page_title.split("/")[-1])
        # For C++, we need to use the actual title
        # if page_title == "C++":
        #     page_title = "C++"

    api_url = "https://en.wikipedia.org/w/api.php"

    # Get the page content parsed as HTML
    params = {
        "action": "parse",
        "page": page_title,
        "prop": "text",
        "format": "json",
    }

    response = requests.get(api_url, params=params)
    data = response.json()

    if "error" in data:
        print(f"Error fetching page: {data['error'].get('info', 'Unknown error')}")
        return

    html_content = data["parse"]["text"]["*"]

    # Use BeautifulSoup to parse the HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # Find the infobox
    infobox = soup.find("table", {"class": "infobox"})
    if not infobox:
        print("No infobox found on this page.")
        return

    # Find the image in the infobox
    image = infobox.find("img")
    if not image:
        print("No image found in the infobox.")
        return

    # The image URL might be relative, so we need to make it absolute
    image_url = "https:" + image["src"]
    # print(image_url)

    return image_url


if __name__ == "__main__":
    dir_target = Path(__file__).parent.parent.parent / "images_download_aa"
    dir_target.mkdir(exist_ok=True)

    for i in [
        "C plus plus programming language",
        "numpy Python library",
    ]:
        url_article = fuzzy_search_wikipedia(i)
        url_img = get_infobox_image_url_new(url_article)
        print(url_img)

        # Add user-agent header to mimic a browser request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 "
            "Safari/537.36"
        }
        response = requests.get(url_img, headers=headers)
        if response.status_code == 200:
            with open(dir_target / f"{i}.png", "wb") as f:
                f.write(response.content)
        else:
            print(f"Error downloading image: Status code {response.status_code}")
