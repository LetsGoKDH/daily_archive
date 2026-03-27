import os

# arXiv categories to track
ARXIV_CATEGORIES = ["cs.AI", "cs.CL", "cs.SD", "eess.AS", "cs.LG", "cs.CV"]

# Semantic Scholar venues (Phase 2)
S2_VENUES = ["Interspeech", "ICASSP", "ACL", "EMNLP", "IEEE/ACM Transactions"]

# Human-readable category labels
CATEGORY_LABELS = {
    "cs.AI": "AI",
    "cs.CL": "NLP",
    "cs.SD": "Speech/Audio",
    "eess.AS": "Audio Signal",
    "cs.LG": "Machine Learning",
    "cs.CV": "Computer Vision",
}

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
