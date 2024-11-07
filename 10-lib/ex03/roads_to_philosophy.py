import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, unquote


class PhilosophyFinder:

    def __init__(self):
        self.visited_pages = []
        self.session = requests.Session()

    def search_wikipedia(self, path):
        url = f'https://en.wikipedia.org{path}'

        # Fetch the Wikipedia page
        try:
            response = self.session.get(url, allow_redirects=True)
            response.raise_for_status()
        except requests.RequestException as e:
            print("Error fetching the page:", e)
            return

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get the page title
        title = soup.find(id='firstHeading').text
        
        # Handle redirects
        if response.history:
            print(f"Redirected from {unquote(path[6:])} to {title}")
        
        if title in self.visited_pages:
            print("It leads to an infinite loop !")
            return

        self.visited_pages.append(title)
        print(title)

        # Check if we've reached the Philosophy page
        if title == 'Philosophy':
            print(f"{len(self.visited_pages)} roads "
                    f"from {self.visited_pages[0]} to Philosophy !")
            return

        # Find the first valid link in the main content
        content = soup.find(id='mw-content-text')
        first_link = self.find_first_link(content)

        if not first_link:
            print("It's a dead end !")
            return

        # Continue to the next page
        self.search_wikipedia(first_link)

    def find_first_link(self, content):
        """Find the first valid link in the main content."""
        # Find all paragraphs in the main content
        for paragraph in content.find_all("p", recursive=True):
            # Skip paragraphs that are inside parentheses or brackets
            if self.is_inside_parentheses(paragraph):
                continue

            link = self.get_first_valid_link(paragraph)
            if link:
                return link

        return None

    def get_first_valid_link(self, paragraph):
        """Get the first valid link from a paragraph."""
        for link in paragraph.find_all("a"):
            # Skip links in parentheses
            if self.is_inside_parentheses(link):
                continue

            href = link.get("href")
            if self.is_valid_link(href):
                return href
        return None

    def is_valid_link(self, href):
        """Check if a link is valid according to Wikipedia rules."""
        if not href:
            return False
        
        invalid_prefixes = (
            '/wiki/Wikipedia:',
            '/wiki/Help:',
            '/wiki/File:',
            '/wiki/Category:',
            '/wiki/Portal:',
            '/wiki/Template:',
            '/wiki/Template_talk:',
            '/wiki/Talk:'
        )
        
        return (href.startswith('/wiki/') and 
                not href.startswith(invalid_prefixes) and
                ':' not in href[6:])  # Skip namespace links

    def is_inside_parentheses(self, element):
        """Check if an element is inside parentheses or brackets."""
        text = ''.join(str(x) for x in element.previous_siblings)
        return text.count('(') > text.count(')') or text.count('[') > text.count(']')


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 roads_to_philosophy.py <search_term>")
        return

    # Handle special characters in the search term
    search_term = quote(sys.argv[1].replace(" ", "_"))
    start_path = f"/wiki/{search_term}"

    wiki_search = PhilosophyFinder()
    wiki_search.search_wikipedia(start_path)


if __name__ == '__main__':
    main()
