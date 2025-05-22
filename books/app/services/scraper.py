import requests
from bs4 import BeautifulSoup
import logging
from typing import List, Dict, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://books.toscrape.com"

def extract_book_data(book_element) -> Dict[str, Any]:
    """Extract book data from a single book element"""
    try:
        # Title
        title = book_element.h3.a["title"]
        
        # Price - extract and convert to float
        price_text = book_element.select_one(".price_color").text
        # Clean the price text of any non-numeric characters except decimal point
        # This will handle encoding issues like the 'Â' character
        import re
        cleaned_price = re.sub(r'[^0-9.]', '', price_text)
        price = float(cleaned_price) if cleaned_price else 0.0
        
        # Category - we might need to get this from the page breadcrumbs or parent page
        # For now, we'll set a placeholder and improve later
        category = "Unknown"
        
        # Availability
        availability_text = book_element.select_one(".availability").text.strip()
        availability = "In stock" in availability_text
        
        # Image URL
        image_relative_url = book_element.select_one("img")["src"]
        image_url = BASE_URL + "/" + image_relative_url.replace("../", "")
        
        # Link to detail page to get more info
        detail_relative_url = book_element.h3.a["href"]
        detail_url = BASE_URL + "/" + detail_relative_url.replace("../", "")
        
        return {
            "title": title,
            "price": price,
            "category": category,
            "availability": availability,
            "image_url": image_url,
            "detail_url": detail_url
        }
    except Exception as e:
        logger.error(f"Error extracting book data: {e}")
        return None

def extract_category_from_page(soup) -> str:
    """Extract category from the page breadcrumbs"""
    try:
        breadcrumb = soup.select(".breadcrumb li")
        if len(breadcrumb) >= 3:  # Home > Category > (possibly subcategory)
            return breadcrumb[2].text.strip()
        return "Unknown"
    except Exception:
        return "Unknown"

def get_books_from_category_page(url: str) -> List[Dict[str, Any]]:
    """Get books from a specific category page"""
    books = []
    try:
        response = requests.get(url)
        if response.status_code != 200:
            logger.error(f"Failed to fetch URL: {url}, status code: {response.status_code}")
            return books
        
        soup = BeautifulSoup(response.text, "html.parser")
        category = extract_category_from_page(soup)
        
        book_elements = soup.select("article.product_pod")
        for book_element in book_elements:
            book_data = extract_book_data(book_element)
            if book_data:
                book_data["category"] = category
                books.append(book_data)
        
        # Check if there's a next page
        next_button = soup.select_one(".next a")
        if next_button:
            next_page_url = url.rsplit('/', 1)[0] + '/' + next_button["href"]
            books.extend(get_books_from_category_page(next_page_url))
        
        return books
    except Exception as e:
        logger.error(f"Error in get_books_from_category_page: {e}")
        return books

def get_all_books() -> List[Dict[str, Any]]:
    """Get all books from the website"""
    all_books = []
    try:
        # Start with the main page to get links to all categories
        response = requests.get(f"{BASE_URL}/index.html")
        if response.status_code != 200:
            logger.error(f"Failed to fetch main page, status code: {response.status_code}")
            return all_books
        
        soup = BeautifulSoup(response.text, "html.parser")
        category_elements = soup.select(".side_categories ul.nav-list li ul li a")
        
        for category_element in category_elements:
            category_url = BASE_URL + "/" + category_element["href"]
            category_books = get_books_from_category_page(category_url)
            all_books.extend(category_books)
            
            # Optional: log progress
            logger.info(f"Scraped {len(category_books)} books from category {category_element.text.strip()}")
            
            # Optional: limit number of categories for testing
            # if len(all_books) > 50:
            #     break
        
        return all_books
    except Exception as e:
        logger.error(f"Error in get_all_books: {e}")
        return all_books

def get_books_with_filters(category: Optional[str] = None, 
                          price_min: Optional[float] = None, 
                          price_max: Optional[float] = None) -> List[Dict[str, Any]]:
    """Get books with optional filters"""
    try:
        # Start with all books
        books = get_all_books()
        
        # Apply filters
        if category:
            books = [book for book in books if book["category"].lower() == category.lower()]
        
        if price_min is not None:
            books = [book for book in books if book["price"] >= price_min]
            
        if price_max is not None:
            books = [book for book in books if book["price"] <= price_max]
            
        return books
    except Exception as e:
        logger.error(f"Error in get_books_with_filters: {e}")
        return []
