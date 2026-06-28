import pytest
from ml_engine.preprocessing import extract_email, extract_phone, extract_total_experience

def test_extract_email():
    assert extract_email("Contact me at test.user123@example.com for more info.") == "test.user123@example.com"
    assert extract_email("No email here, just some text.") is None
    assert extract_email("Name: John Doe\nEmail: john_doe@domain.co.uk\nPhone: 1234567890") == "john_doe@domain.co.uk"

def test_extract_phone():
    assert extract_phone("My phone is +1-800-555-0199.") == "+1-800-555-0199"
    assert extract_phone("Call me: (555) 123-4567") == "(555) 123-4567"
    assert extract_phone("Mobile: 9876543210") == "9876543210"
    assert extract_phone("A short number 123 is not a phone.") is None
    
def test_extract_total_experience():
    # Direct match in text
    assert extract_total_experience("I have 5.5 years of experience in Python.", {}) == 5.5
    assert extract_total_experience("Over 10+ years working in tech.", {}) == 10.0
    
    # Fallback checking from dates in "experience" section
    sections = {
        "experience": "Worked at Google from 2015 to 2020. Then joined Meta in 2021 until 2025."
    }
    assert extract_total_experience("Some unrelated summary.", sections) == 10.0  # 2025 - 2015
    
    # Defaults to 0 if nothing found
    assert extract_total_experience("Just graduated.", {}) == 0.0
