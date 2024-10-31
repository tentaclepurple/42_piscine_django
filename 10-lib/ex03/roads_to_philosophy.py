import sys
import requests
from bs4 import BeautifulSoup


class PhilosophyFinder:

    def __init__(self):
        self.visited_pages = []

    def search_wikipedia(self, path):
        url = f'https://en.wikipedia.org{path}'

        # Fetch the Wikipedia page
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            print("Error fetching the page:", e)
            return

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get the page title
        title = soup.find(id='firstHeading').text
        
		if title in self.visited_pages:
            print("It leads to an infinite loop!")
            return

        self.visited_pages.append(title)

        print(title)

        # Check if we've reached the Philosophy page
        if title == 'Philosophy':
            print(f"{len(self.visited_pages)} roads "
					f"from {self.visited_pages[0]} to Philosophy")
            return

        # Find the first valid link in the main content
        content = soup.find(id='mw-content-text')
        first_link = self.find_first_link(content)

        if not first_link:
            print("It leads to a dead end!")
            return

        # Continue to the next page by following the link
        self.search_wikipedia(first_link)

    def find_first_link(self, content):
        """Find the first valid link in the main content."""
        for paragraph in content.find_all("p", recursive=False):

            for link in paragraph.find_all("a", recursive=False):
                
				href = link.get("href")
                if href and href.startswith('/wiki/') \
						and not href.startswith(('/wiki/Wikipedia:',
												'/wiki/Help:')):
                    return href

        return None


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 roads_to_philosophy.py <search_term>")
        return

    search_term = sys.argv[1].replace(" ", "_")
    start_path = f"/wiki/{search_term}"

    wiki_search = PhilosophyFinder()
    wiki_search.search_wikipedia(start_path)


if __name__ == '__main__':
    main()
