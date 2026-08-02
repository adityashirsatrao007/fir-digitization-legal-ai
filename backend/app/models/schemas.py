"""
Pydantic models for API request/response schemas
"""
from datetime import datetime

from pydantic import BaseModel, Field


class IPCSection(BaseModel):
    """Represents an IPC section found in the FIR"""
    section: str = Field(..., description="IPC section number (e.g., '302', '376')")
    title: str = Field(..., description="Title of the section")
    description: str = Field(..., description="Brief description of the offense")
    punishment: str = Field(..., description="Punishment as per IPC")
    category: str = Field(..., description="Category of offense (e.g., 'Against Person', 'Against Property')")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score of extraction")


class FIRExtraction(BaseModel):
    """Result of FIR text extraction"""
    raw_text: str = Field(..., description="Raw extracted text from FIR image")
    cleaned_text: str = Field(..., description="Cleaned and processed text")
    translated_text: str | None = Field(None, description="Translated text into English if original was in a regional language")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Overall OCR confidence")
    language_detected: str = Field(default="en", description="Detected language")
    extraction_method: str = Field(..., description="OCR method used (easyocr/trocr)")


class FIRAnalysis(BaseModel):
    """Complete FIR analysis result"""
    extraction: FIRExtraction
    ipc_sections: list[IPCSection] = Field(default_factory=list, description="List of IPC sections found")
    complainant_name: str | None = Field(None, description="Name of complainant if found")
    accused_name: str | None = Field(None, description="Name of accused if found")
    incident_date: str | None = Field(None, description="Date of incident if found")
    incident_location: str | None = Field(None, description="Location of incident if found")
    police_station: str | None = Field(None, description="Police station name if found")
    fir_number: str | None = Field(None, description="FIR number if found")
    summary: str = Field(..., description="AI-generated summary of the FIR")
    timestamp: datetime = Field(default_factory=datetime.now)


class ExtractIPCRequest(BaseModel):
    """Request for IPC extraction from text"""
    text: str = Field(..., min_length=10, description="Text to extract IPC sections from")


class ExtractIPCResponse(BaseModel):
    """Response for IPC extraction"""
    ipc_sections: list[IPCSection]
    raw_matches: list[str] = Field(default_factory=list, description="Raw regex matches found")
    total_found: int


class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    detail: str | None = None
