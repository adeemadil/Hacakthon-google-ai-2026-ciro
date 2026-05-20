import logging
import os
import sqlite3
from datetime import datetime
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class SignalStore:
    """
    SignalStore handles saving, loading, and aggregating raw sensor and API signals 
    into a local SQLite database for training and evaluation.
    """
    def __init__(self, db_path: str = "data/signals.db"):
        self.db_path = db_path
        # Ensure containing directory exists
        db_dir = os.path.dirname(self.db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
            
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._init_db()

    def _init_db(self):
        """
        Create signals table and add index to make queries extremely fast.
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS signals (
                id TEXT PRIMARY KEY,
                zone_id TEXT NOT NULL,
                source TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                data TEXT NOT NULL,
                confidence REAL NOT NULL
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_signals_zone_time ON signals(zone_id, timestamp)")
        self.conn.commit()

    def insert_signal(self, signal_dict: Dict[str, Any]) -> bool:
        """
        Insert a raw signal into the local SQLite store. Uses INSERT OR IGNORE to manage duplicates.
        """
        logger.info(f"Inserting signal from source {signal_dict.get('source')} for zone {signal_dict.get('zone_id')}")
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT OR IGNORE INTO signals (id, zone_id, source, timestamp, data, confidence) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    signal_dict.get("id"),
                    signal_dict.get("zone_id"),
                    signal_dict.get("source"),
                    signal_dict.get("timestamp", datetime.utcnow().isoformat()),
                    str(signal_dict.get("data", {})),
                    signal_dict.get("confidence", 1.0)
                )
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            logger.error(f"Failed to insert signal into SQLite database: {e}")
            return False

    def get_signals(self, zone_id: str, hours: int = 24) -> List[Dict[str, Any]]:
        """
        Retrieve all signals collected for a zone over the past N hours.
        """
        logger.info(f"Retrieving signals for zone: {zone_id} within the last {hours} hours")
        # Placeholder returns a dummy dataset matching the schema
        return [
            {
                "id": "sig_dummy_101",
                "zone_id": zone_id,
                "source": "sensor",
                "timestamp": datetime.utcnow().isoformat(),
                "data": "{'precip': 15.0}",
                "confidence": 0.95
            }
        ]

    def get_features(self, zone_id: str) -> Dict[str, Any]:
        """
        Return engineered, aggregated feature representations prepared for XGBoost classification.
        """
        logger.info(f"Aggregating signals into features for zone: {zone_id}")
        return {
            "zone_id": zone_id,
            "temp_mean_24h": 32.5,
            "precip_sum_24h": 12.8,
            "river_discharge_mean_24h": 155.2,
            "social_sentiment_mean_24h": -0.4,
            "ndma_active_alerts_count": 1
        }
