from fastapi import APIRouter
import logging
import os
from .models import create_tables
from .routers import recommendations, summaries

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Création d'un routeur principal pour le module books
books_router = APIRouter(prefix="/books-api", tags=["books"])

# Inclure les sous-routeurs
books_router.include_router(recommendations.router)
books_router.include_router(summaries.router)

# Fonction pour initialiser le module books
def init_books_module():
    try:
        # Vérifier si les variables d'environnement nécessaires sont définies
        if not os.getenv("OPENAI_API_KEY"):
            logger.warning("OPENAI_API_KEY not found in environment variables. Summary generation will be limited.")
        
        # Créer les tables dans la base de données si elles n'existent pas
        create_tables()
        logger.info("Books module initialized successfully")
        
    except Exception as e:
        logger.error(f"Error initializing books module: {e}")
        raise
