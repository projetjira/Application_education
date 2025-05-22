from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from ..models import get_db, RecommendedBook
from ..services.scraper import get_books_with_filters, get_all_books

router = APIRouter(tags=["book-recommendations"])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.get("/recommendations", response_model=List[dict])
async def get_book_recommendations(
    category: Optional[str] = Query(None, description="Filter books by category"),
    price_min: Optional[float] = Query(None, description="Minimum price for filtering"),
    price_max: Optional[float] = Query(None, description="Maximum price for filtering"),
    db: Session = Depends(get_db)
):
    """
    Get book recommendations with optional filtering.
    
    - Filter by category
    - Filter by price range (min and max)
    """
    try:
        # Check if we already have books in the database
        db_books = db.query(RecommendedBook).all()
        
        # If the DB is empty, fetch books from the scraper and save them
        if not db_books:
            logger.info("No books found in database, fetching from source...")
            # This might take some time for the initial fetch
            scraped_books = get_all_books()
            
            # Save books to the database
            for book in scraped_books:
                db_book = RecommendedBook(
                    title=book["title"],
                    price=book["price"],
                    category=book["category"],
                    availability=book["availability"],
                    image_url=book.get("image_url")
                )
                db.add(db_book)
            
            db.commit()
            logger.info(f"Saved {len(scraped_books)} books to database")
            
            # Query again to get the books with IDs
            db_books = db.query(RecommendedBook).all()
        
        # Apply filters to database query
        query = db.query(RecommendedBook)
        
        if category:
            query = query.filter(RecommendedBook.category.ilike(f"%{category}%"))
        
        if price_min is not None:
            query = query.filter(RecommendedBook.price >= price_min)
            
        if price_max is not None:
            query = query.filter(RecommendedBook.price <= price_max)
            
        # Execute the query
        filtered_books = query.all()
        
        # Convert SQLAlchemy models to dictionaries
        return [book.to_dict() for book in filtered_books]
    
    except Exception as e:
        logger.error(f"Error in get_book_recommendations: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/refresh-recommendations")
async def refresh_book_recommendations(db: Session = Depends(get_db)):
    """
    Admin endpoint to refresh the book recommendations from the source website.
    This will rescrape the website and update the database.
    """
    try:
        # Clear existing books
        db.query(RecommendedBook).delete()
        db.commit()
        
        # Fetch new books
        scraped_books = get_all_books()
        
        # Save books to the database
        for book in scraped_books:
            db_book = RecommendedBook(
                title=book["title"],
                price=book["price"],
                category=book["category"],
                availability=book["availability"],
                image_url=book.get("image_url")
            )
            db.add(db_book)
        
        db.commit()
        
        return {"status": "success", "message": f"Successfully refreshed {len(scraped_books)} books"}
    except Exception as e:
        logger.error(f"Error refreshing book recommendations: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to refresh books: {str(e)}")
