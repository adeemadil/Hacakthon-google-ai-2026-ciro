import logging
import random
from typing import Dict, Any, List

logger = logging.getLogger("CIRO.SocialService")

class SocialService:
    """
    SocialService ingests and parses crowdsourced signal feeds (e.g. local X/Twitter
    and WhatsApp groups) to extract raw text-based crisis indicators.
    """
    def __init__(self):
        logger.info("SocialSignal stream parser initialized.")

    async def get_crisis_signals(self, zone_id: str) -> List[Dict[str, Any]]:
        """
        Scan recent crowdsourced feeds for keywords regarding localized floods or heatwaves.
        """
        logger.info(f"Scanning social keyword indicators for zone: {zone_id}")
        
        # Simulating parsed WhatsApp/X reports with the default 0.50 baseline confidence
        mock_posts = [
            {
                "signal_id": f"soc_sig_{random.randint(1000, 9999)}",
                "source": "WhatsApp_Tip",
                "text": f"Severe urban flooding reported near local bazaar in {zone_id}. Streets submerged under 2 feet of water.",
                "sentiment_score": -0.85,
                "confidence": 0.50,
                "impact_level": "High"
            },
            {
                "signal_id": f"soc_sig_{random.randint(1000, 9999)}",
                "source": "X_Post",
                "text": f"Extreme humidity in {zone_id} today. Temperatures touching 43C, public shelters filling rapidly.",
                "sentiment_score": -0.62,
                "confidence": 0.50,
                "impact_level": "Moderate"
            }
        ]
        
        # Return matched feeds under high humidity/precip triggers
        return mock_posts
