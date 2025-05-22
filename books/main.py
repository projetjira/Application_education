import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from app.models import create_tables
from app.routers import recommendations, summaries

# Charger les variables d'environnement
load_dotenv()

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Créer l'application FastAPI
app = FastAPI(
    title="Book Recommendations API",
    description="API pour les recommandations de livres et la génération de résumés",
    version="1.0.0"
)

# Configuration CORS pour permettre les requêtes depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, limitez aux domaines spécifiques
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routeurs pour les différentes fonctionnalités
app.include_router(recommendations.router, prefix="/api")
app.include_router(summaries.router, prefix="/api")

# Route racine
@app.get("/")
async def root():
    return {
        "message": "Bienvenue sur l'API de recommandation de livres",
        "docs": "/docs",
        "endpoints": {
            "recommendations": "/api/recommendations",
            "book_summary": "/api/books/summary",
            "refresh_books": "/api/refresh-recommendations"
        }
    }

# Événement de démarrage de l'application
@app.on_event("startup")
async def startup_event():
    try:
        # Vérifier les variables d'environnement requises
        required_env_vars = ["POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_DB", "POSTGRES_HOST"]
        missing_vars = [var for var in required_env_vars if not os.getenv(var)]
        
        if missing_vars:
            logger.warning(f"Variables d'environnement manquantes: {', '.join(missing_vars)}")
            logger.warning("Certaines fonctionnalités pourraient ne pas fonctionner correctement")
        
        # Vérifier la clé API OpenAI
        if not os.getenv("OPENAI_API_KEY"):
            logger.warning("OPENAI_API_KEY manquante. La génération de résumés ne fonctionnera pas.")
        
        # Créer les tables dans la base de données
        try:
            create_tables()
            logger.info("Tables de base de données créées avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de la création des tables: {e}")
            
        logger.info("Application démarrée avec succès")
    except Exception as e:
        logger.error(f"Erreur lors du démarrage de l'application: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
