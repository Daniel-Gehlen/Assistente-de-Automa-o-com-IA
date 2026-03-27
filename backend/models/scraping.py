from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class ScrapingRequest(BaseModel):
    url: str = Field(..., description="URL para scraping")
    data: Dict[str, Any] = Field(..., description="Dados coletados")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Metadados adicionais")

class ScrapingResponse(BaseModel):
    doc_id: Optional[str] = None
    status: str
    error: Optional[str] = None

class ScrapedData(BaseModel):
    url: str
    data: Dict[str, Any]
    metadata: Optional[Dict[str, Any]]
    created_at: datetime
