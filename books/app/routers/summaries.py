from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import logging
from typing import Optional, Dict, Any

from ..models import get_db, RecommendedBook
from ..services.summary_generator import generate_book_summary, generate_summary_huggingface

router = APIRouter(tags=["book-summaries"])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.get("/books/summary")
async def get_book_summary(
    book_id: Optional[int] = Query(None, description="ID of the book to summarize"),
    title: Optional[str] = Query(None, description="Title of the book to summarize"),
    db: Session = Depends(get_db)
):
    """
    Generate a summary for a book using a language model.
    
    You can identify the book either by ID or by title.
    """
    if not book_id and not title:
        raise HTTPException(
            status_code=400, 
            detail="You must provide either a book_id or a title"
        )
    
    try:
        # Find the book in the database
        book = None
        
        if book_id:
            book = db.query(RecommendedBook).filter(RecommendedBook.id == book_id).first()
        elif title:
            book = db.query(RecommendedBook).filter(RecommendedBook.title.ilike(f"%{title}%")).first()
        
        if not book:
            raise HTTPException(
                status_code=404,
                detail=f"Book not found with the provided {'ID' if book_id else 'title'}"
            )
        
        # Convert book to dictionary for the summary generator
        book_data = book.to_dict()
        
        # Try to generate summary using OpenAI first
        logger.info(f"Generating summary for book: {book_data['title']}")
        summary = await generate_book_summary(book_data)
        
        # Check if Groq summary generation failed and try Hugging Face as fallback
        if summary and summary.startswith("Erreur"):
            logger.warning("Groq summary generation failed, trying Hugging Face fallback")
            huggingface_summary = await generate_summary_huggingface(book_data)
            if huggingface_summary and not huggingface_summary.startswith("Erreur"):
                summary = huggingface_summary
        
        # Return the book details and the generated summary
        return {
            "book": book_data,
            "summary": summary
        }
    
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error generating book summary: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate summary: {str(e)}"
        )
