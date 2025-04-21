import os
import requests
from typing import Optional

class TranslationApiClient:
    def __init__(self):
        # Default to local development unless explicitly set to production
        is_production = os.getenv('ENV') == 'production'
        self.base_url = os.getenv(
            'TRANSLATION_API_URL',
            'https://ai-translation-api-1f53c7c0c947.herokuapp.com' if is_production else 'http://localhost:8085'
        )

    def translate(
        self,
        source_text: str,
        source_language: str,
        target_language: str,
        source_context: Optional[str] = None
    ) -> dict:
        """
        Get translation from the API's cache or request a new translation
        
        Args:
            source_text: Text to translate
            source_language: Source language code (e.g., 'en')
            target_language: Target language code (e.g., 'nl')
            source_context: Optional context for the translation
        Returns:
            dict: {"result": "translated text"}
        """
        url = f"{self.base_url}/api/translations/translate"
        
        payload = {
            "sourceText": source_text,
            "sourceLanguage": source_language,
            "targetLanguage": target_language,
            "sourceContext": source_context or "",
            "targetPromptText": f"Translate this UI text to {target_language}"
        }
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json() 