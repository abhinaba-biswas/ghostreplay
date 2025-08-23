import json
from datetime import datetime
from typing import Dict, Any
from pathlib import Path
from .models import IncidentContext


class LogParser:
    """Parses structured JSON logs into IncidentContext objects."""
    
    @staticmethod
    def parse_log_file(file_path: str) -> IncidentContext:
        """Parse a JSON log file into an IncidentContext."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Log file not found: {file_path}")
        
        with open(path, 'r') as f:
            log_data = json.load(f)
        
        return LogParser.parse_log_dict(log_data)
    
    @staticmethod
    def parse_log_dict(log_data: Dict[str, Any]) -> IncidentContext:
        """Parse a dictionary into an IncidentContext."""
        # Handle timestamp parsing
        timestamp_str = log_data.get('timestamp')
        if isinstance(timestamp_str, str):
            # Try common timestamp formats
            try:
                timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            except ValueError:
                try:
                    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    timestamp = datetime.now()
        else:
            timestamp = datetime.now()
        
        return IncidentContext(
            method=log_data.get('method', 'GET'),
            endpoint=log_data.get('endpoint', '/unknown'),
            body=log_data.get('body'),
            stack=log_data.get('stack', 'No stack trace available'),
            timestamp=timestamp,
            status_code=log_data.get('status_code'),
            error_message=log_data.get('error_message'),
            user_id=log_data.get('user_id')
        )