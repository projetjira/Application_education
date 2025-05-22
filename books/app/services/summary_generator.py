import logging
from typing import Dict, Any, Optional
import httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Groq API key hardcoded directly in the code
# Note: In a production environment, this would be a security risk
GROQ_API_KEY = "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"

async def generate_book_summary(book_data: Dict[str, Any]) -> Optional[str]:
    """
    Génère un résumé de livre à l'aide de l'API Groq.
    """
    # API key is hardcoded, so no need to check if it exists
    
    try:
        # Construire le prompt pour le LLM
        prompt = f"""
        Génère un résumé détaillé et engageant pour ce livre:
        
        Titre: {book_data['title']}
        Catégorie: {book_data['category']}
        
        Le résumé doit être informatif, captivant et doit donner envie au lecteur de découvrir le livre.
        Il doit faire environ 3-4 paragraphes.
        
        Si le livre fait partie d'une série ou est écrit par un auteur connu, tu peux mentionner ces informations si elles sont pertinentes.
        """
        
        # Appel à l'API Groq avec gestion des erreurs
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                logger.info(f"Sending request to Groq API for book: {book_data['title']}")
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",  # Groq API endpoint
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {GROQ_API_KEY}"
                    },
                    json={
                        "model": "llama3-70b-8192",  # Groq model name
                        "messages": [
                            {"role": "system", "content": "Tu es un assistant littéraire spécialisé dans la rédaction de résumés de livres attractifs et informatifs."},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 500
                    }
                )
                
                if response.status_code != 200:
                    logger.error(f"Error from Groq API: {response.text}")
                    return "Erreur lors de la génération du résumé"
                
                response_data = response.json()
                summary = response_data["choices"][0]["message"]["content"].strip()
                return summary
            except httpx.RequestError as e:
                logger.error(f"Groq API request failed: {e}")
                return "Erreur de connexion lors de la génération du résumé"
            except Exception as e:
                logger.error(f"Unexpected error in Groq API call: {e}")
                return "Erreur lors de la génération du résumé"
            
    except Exception as e:
        logger.error(f"Error generating summary: {e}")
        return "Erreur lors de la génération du résumé"

# Alternative implementation using Hugging Face API as fallback
async def generate_summary_huggingface(book_data: Dict[str, Any]) -> Optional[str]:
    """
    Fallback implementation using Hugging Face API when Grok fails
    """
    # Hardcoded Hugging Face API key
    HF_API_KEY = "hf_1234567890abcdefghijklmnopqrstuvwxyz"
    
    try:
        # Construire le prompt
        prompt = f"""
        Génère un résumé détaillé et engageant pour ce livre:
        
        Titre: {book_data['title']}
        Catégorie: {book_data['category']}
        
        Le résumé doit être informatif, captivant et doit donner envie au lecteur de découvrir le livre.
        Le résumé doit faire environ 3-4 paragraphes.
        """
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                logger.info(f"Sending fallback request to Hugging Face API for book: {book_data['title']}")
                response = await client.post(
                    "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
                    headers={"Authorization": f"Bearer {HF_API_KEY}"},
                    json={"inputs": prompt}
                )
                
                if response.status_code != 200:
                    logger.error(f"Error from Hugging Face API: {response.text}")
                    return "Erreur lors de la génération du résumé"
                
                summary = response.json()[0]["generated_text"]
                # Clean up the summary to remove the prompt from the response
                if summary.startswith(prompt):
                    summary = summary[len(prompt):].strip()
                return summary
            except httpx.RequestError as e:
                logger.error(f"Hugging Face API request failed: {e}")
                return "Erreur de connexion lors de la génération du résumé"
            except Exception as e:
                logger.error(f"Unexpected error in Hugging Face API call: {e}")
                return "Erreur lors de la génération du résumé"
            
    except Exception as e:
        logger.error(f"Error generating summary with Hugging Face: {e}")
        return "Erreur lors de la génération du résumé"
