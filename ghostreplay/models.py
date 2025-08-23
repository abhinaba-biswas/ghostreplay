from datetime import datetime
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


class IncidentContext(BaseModel):
    """Represents a parsed production error incident."""
    method: str = Field(..., description="HTTP method (GET, POST, etc.)")
    endpoint: str = Field(..., description="API endpoint that failed")
    body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")
    stack: str = Field(..., description="Stack trace of the error")
    timestamp: datetime = Field(..., description="When the error occurred")
    status_code: Optional[int] = Field(default=None, description="HTTP status code")
    error_message: Optional[str] = Field(default=None, description="Error message")
    user_id: Optional[str] = Field(default=None, description="User who triggered the error")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class TestGenerationConfig(BaseModel):
    """Configuration for test generation."""
    framework: str = Field(default="pytest", description="Testing framework")
    output_path: str = Field(..., description="Output path for generated test")
    include_mocks: bool = Field(default=True, description="Include mock setup")
    include_fixtures: bool = Field(default=True, description="Include test fixtures")