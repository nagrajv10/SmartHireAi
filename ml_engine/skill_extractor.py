import spacy
from spacy.matcher import PhraseMatcher

# Default taxonomy
DEFAULT_TAXONOMY = [
    "python", "java", "c++", "javascript", "react", "node.js", "aws", "docker",
    "kubernetes", "machine learning", "deep learning", "nlp", "computer vision",
    "pytorch", "tensorflow", "scikit-learn", "sql", "postgresql", "mongodb",
    "fastapi", "django", "flask", "mlops", "data science", "data engineering",
    "gcp", "azure", "html", "css", "typescript", "git", "linux", "elasticsearch"
]

class SkillExtractor:
    def __init__(self, taxonomy=None):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Model not installed, using blank as fallback (e.g. before downloading in user environment)
            self.nlp = spacy.blank("en")
        
        self.matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        self.taxonomy = taxonomy or DEFAULT_TAXONOMY
        self._build_matcher()
        
    def _build_matcher(self):
        patterns = [self.nlp.make_doc(text) for text in self.taxonomy]
        self.matcher.add("SKILLS", patterns)
        
    def extract_skills(self, text: str) -> list[str]:
        """Extracts skills from text using phrase matching and NLP."""
        doc = self.nlp(text)
        matches = self.matcher(doc)
        
        skills_found = set()
        for match_id, start, end in matches:
            span = doc[start:end]
            skills_found.add(span.text.lower())
            
        return list(skills_found)

# Dependency injection / Singleton pattern for easy import
skill_extractor = SkillExtractor()

def extract_skills_from_text(text: str) -> list[str]:
    return skill_extractor.extract_skills(text)
