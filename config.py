import os

# All available arXiv categories and their labels
ALL_CATEGORIES = {
    "cs.AI": "AI",
    "cs.CL": "NLP",
    "cs.SD": "Speech/Audio",
    "eess.AS": "Audio Signal",
    "cs.LG": "Machine Learning",
    "cs.CV": "Computer Vision",
    "cs.CR": "Cryptography",
    "cs.DB": "Databases",
    "cs.DC": "Distributed Computing",
    "cs.DS": "Data Structures",
    "cs.GT": "Game Theory",
    "cs.HC": "HCI",
    "cs.IR": "Information Retrieval",
    "cs.IT": "Information Theory",
    "cs.LO": "Logic",
    "cs.MA": "Multiagent Systems",
    "cs.NE": "Neural/Evolutionary",
    "cs.NI": "Networking",
    "cs.PL": "Programming Languages",
    "cs.RO": "Robotics",
    "cs.SE": "Software Engineering",
    "cs.SI": "Social Networks",
    "cs.SY": "Systems & Control",
    "eess.SP": "Signal Processing",
    "stat.ML": "Statistics/ML",
    "math.OC": "Optimization",
    "q-bio.QM": "Quantitative Biology",
    "physics.comp-ph": "Computational Physics",
}

# arXiv categories: override via env var ARXIV_CATEGORIES (comma-separated)
# e.g. ARXIV_CATEGORIES="cs.CL,cs.SD,eess.AS"
_default_categories = ["cs.AI", "cs.CL", "cs.SD", "eess.AS", "cs.LG", "cs.CV"]
_env_categories = os.environ.get("ARXIV_CATEGORIES", "")
ARXIV_CATEGORIES = [c.strip() for c in _env_categories.split(",") if c.strip()] if _env_categories else _default_categories

# Build labels for active categories
CATEGORY_LABELS = {cat: ALL_CATEGORIES.get(cat, cat) for cat in ARXIV_CATEGORIES}

# Semantic Scholar venues (Phase 2)
S2_VENUES = ["Interspeech", "ICASSP", "ACL", "EMNLP", "IEEE/ACM Transactions"]

# Limits
MAX_PAPERS_PER_DAY = 50
ARXIV_MAX_RESULTS = 200

# OpenAI API
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
SUMMARY_MODEL = "gpt-4.1-nano"
SUMMARY_BATCH_SIZE = 5

# Semantic Scholar API (Phase 2)
S2_API_KEY = os.environ.get("S2_API_KEY", "")

# Paths
SITE_DIR = os.path.join(os.path.dirname(__file__), "site")
DATA_DIR = os.path.join(SITE_DIR, "data")
ARCHIVE_DIR = os.path.join(SITE_DIR, "archive")
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "builder", "templates")
