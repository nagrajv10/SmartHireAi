import re
import fitz  # PyMuPDF
from typing import Dict, Any, Optional

def extract_text_from_pdf(pdf_path_or_bytes: str | bytes) -> str:
    """Extracts raw text from a PDF file path or bytes."""
    text = ""
    if isinstance(pdf_path_or_bytes, str):
        doc = fitz.open(pdf_path_or_bytes)
    else:
        doc = fitz.open(stream=pdf_path_or_bytes, filetype="pdf")
    
    for page in doc:
        text += page.get_text("text") + "\n"
    
    doc.close()
    return text

def clean_text(text: str) -> str:
    """Cleans extracted text by removing extra whitespaces and special characters."""
    # Remove special characters but keep punctuation needed for structure (and + for phones, @ for emails)
    text = re.sub(r'[^\w\s\.,;:()/\-@\+]', ' ', text)
    # Remove multiple spaces/newlines
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_email(text: str) -> Optional[str]:
    """Extracts the first valid email address found in the text."""
    # Common email regex pattern
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(pattern, text)
    return match.group(0) if match else None

def extract_phone(text: str) -> Optional[str]:
    """Extracts a phone number. Supports US/International formats loosely."""
    # Patterns for basic phone number matching, e.g. +1-234-567-8900, (123) 456-7890, 1234567890
    pattern = r'''(?x)
        (?:(?:\+?\d{1,3}[\s-]?)?      # optional country code
        (?:\(?\d{3}\)?[\s-]?)?        # area code
        \d{3}[\s-]?\d{4})             # main number
    '''
    # Use re.findall to get all possible numbers, filter by minimum length to avoid fake matches
    matches = [m for m in re.findall(pattern, text) if len(re.sub(r'\D', '', m)) >= 10]
    return matches[0].strip() if matches else None

def extract_total_experience(text: str, sections: Dict[str, str]) -> float:
    """Estimates total years of experience from the resume text or experience section."""
    combined_text = sections.get("summary", "") + " " + sections.get("experience", "") + " " + text
    
    # Simple regex for experience extraction (e.g. '3+ years', '3 to 5 years', '5 years of experience')
    exp_match = re.search(r'(\d+(?:\.\d+)?)(?:\s*(?:\+|-|to)\s*\d+)?\s*(?:\+)?\s*(?:years?|yrs?)(?:\s*of\s*experience)?', combined_text, re.IGNORECASE)
    if exp_match:
        try:
            return float(exp_match.group(1))
        except ValueError:
            pass
            
    # As a fallback, try to calculate from date ranges in the experience section (Very naive implementation)
    exp_text = sections.get("experience", "")
    years = re.findall(r'\b(19\d{2}|20\d{2})\b', exp_text)
    if years:
        years = sorted([int(y) for y in years])
        if len(years) >= 2:
            return float(max(years) - min(years))
            
    return 0.0

def extract_sections(text: str) -> Dict[str, str]:
    """Basic rule-based section identification using regex."""
    sections: Dict[str, str] = {
        "experience": "",
        "education": "",
        "skills": "",
        "projects": "",
        "summary": ""
    }
    
    # Common headers
    headers = {
        "experience": r"(?i)\b(?:experience|work history|employment history)\b",
        "education": r"(?i)\b(?:education|academic background)\b",
        "skills": r"(?i)\b(?:skills|technical skills|technologies)\b",
        "projects": r"(?i)\b(?:projects|personal projects)\b",
        "summary": r"(?i)\b(?:summary|objective|profile)\b"
    }
    
    lines = text.split('.') # Basic split for processing
    current_section: Optional[str] = None
    
    for line in lines:
        line_clean = line.strip().lower()
        matched_section = None
        for sec, pattern in headers.items():
            if re.match(pattern, line_clean) and len(line_clean.split()) < 5:
                matched_section = sec
                break
        
        if matched_section:
            current_section = matched_section
        elif current_section is not None:
            sections[str(current_section)] += line + ".\n"
            
    # Fallback if no sections identified
    if not any(sections.values()):
        sections["summary"] = text
        
    return sections

def extract_jd_features(text: str) -> Dict[str, Any]:
    """Extracts features from Job Descriptions."""
    cleaned = clean_text(text)
    
    # Simple regex for experience extraction (e.g. '3+ years', '3 to 5 years', '5 years')
    experience = 0.0
    exp_match = re.search(r'(\d+)(?:\s*(?:\+|-|to)\s*\d+)?\s*(?:years?|yrs?)', cleaned, re.IGNORECASE)
    if exp_match:
        experience = float(exp_match.group(1))
        
    from .skill_extractor import extract_skills_from_text
    skills = extract_skills_from_text(cleaned)
    
    return {
        "required_skills": skills,
        "experience_years": experience,
        "clean_text": cleaned
    }
