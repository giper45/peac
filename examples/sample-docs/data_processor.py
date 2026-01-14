"""
Example implementation of a data processor with validation and error handling.

This module demonstrates best practices for:
- Type hints and documentation
- Input validation
- Error handling
- Logging
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class DataRecord:
    """Represents a single data record with validation."""
    id: int
    name: str
    value: float
    
    def __post_init__(self):
        """Validate fields after initialization."""
        if self.id < 0:
            raise ValueError("ID must be non-negative")
        if not self.name:
            raise ValueError("Name cannot be empty")
        if self.value < 0:
            raise ValueError("Value must be non-negative")


class DataProcessor:
    """Process and validate data records with configurable thresholds."""
    
    def __init__(self, threshold: float = 0.0):
        """
        Initialize the data processor.
        
        Args:
            threshold: Minimum value threshold for filtering records
        """
        self.threshold = threshold
        self._processed_count = 0
    
    def process_records(self, records: List[Dict]) -> List[DataRecord]:
        """
        Process raw data records into validated DataRecord objects.
        
        Args:
            records: List of dictionaries containing record data
            
        Returns:
            List of validated DataRecord objects
            
        Raises:
            ValueError: If record data is invalid
        """
        processed = []
        
        for raw_record in records:
            try:
                record = DataRecord(
                    id=raw_record.get('id', 0),
                    name=raw_record.get('name', ''),
                    value=raw_record.get('value', 0.0)
                )
                
                if record.value >= self.threshold:
                    processed.append(record)
                    self._processed_count += 1
                    
            except ValueError as e:
                logger.warning(f"Skipping invalid record: {e}")
                continue
        
        logger.info(f"Processed {len(processed)} records")
        return processed
    
    def get_statistics(self, records: List[DataRecord]) -> Dict[str, float]:
        """
        Calculate statistics for processed records.
        
        Args:
            records: List of DataRecord objects
            
        Returns:
            Dictionary with statistical measures
        """
        if not records:
            return {"count": 0, "sum": 0.0, "average": 0.0}
        
        values = [r.value for r in records]
        return {
            "count": len(values),
            "sum": sum(values),
            "average": sum(values) / len(values),
            "min": min(values),
            "max": max(values)
        }
    
    @property
    def processed_count(self) -> int:
        """Total number of successfully processed records."""
        return self._processed_count
