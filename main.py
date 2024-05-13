import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/index.html"

def main(threshold: int = 5):
    # threshold, c'est le "seuil" définie ici à 5
    with requests.Session() as session:
    
        response = session.get(BASE_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        # soup.find("ul", class_="nav nav-list").find_all("a")
        # Alternative
        categories = soup.select("ul.nav.nav-list a")
        categories_url = [category["href"] for category in categories]
        
        for category_url in categories_url:
            absolute_url = urljoin(BASE_URL, category_url)
            # print(absolute_url)
            response = session.get(absolute_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            books = soup.select("article.product_pod")
            # print(len(books))
            number_of_books = len(books)
            category_title = soup.select_one("h1").text
            if number_of_books <= threshold:
                print(f"La catégorie '{category_title}' ne contient pas assez de livres: ({number_of_books})")
            else:
                print(f"La catégorie '{category_title}' contient assez de livres: ({number_of_books})")
                
        
if __name__ == '__main__':
    main(threshold=5)

# aside = soup.find('div', class_='side_categories')
# categories_div = aside.find('ul').find('li').find('ul')
# categories = [child.text.strip() for child in categories_div.children if child.name]

# images = soup.find('section').find_all('img')