import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

# ==========================================
# TIER 1: RULE-BASED REGEX ENGINE
# ==========================================
DARK_PATTERN_REGEX = {
    "False Urgency": r"(?i)(only \d+ left|hurry|countdown|offer ends|expires in|limited time|flash sale|deal ends in|almost gone|last chance|selling out fast|act fast|don't miss out)",
    "Social Proof Pressure": r"(?i)(\d+ people are viewing|in high demand|selling fast|others have this in their cart|bought this in the last|trending now|highly rated by|\d+ people recently viewed|everyone is buying)",
    "Forced Continuity": r"(?i)(auto-renew|cancel anytime|subscription will automatically|card will be charged|free trial converts to|billed monthly|by continuing you agree to be charged|recurring billing)",
    "Confirmshaming": r"(?i)(no thanks, I hate saving money|I prefer paying full price|no, I don't want to|I don't like free things|I'd rather lose out|No thanks, I'll pay more|I don't care about my security)",
    "Hidden Costs": r"(?i)(handling fee|service fee|convenience fee|processing fee|taxes and fees apply at checkout|additional charges may apply|shipping calculated at checkout|admin fee)"
}

def regex_detect(snippet):
    """Checks snippet against known dark pattern regex rules."""
    for category, pattern in DARK_PATTERN_REGEX.items():
        if re.search(pattern, snippet):
            return category
    return None

# ==========================================
# TIER 2: MACHINE LEARNING BASELINE
# ==========================================
# Dataset to train the TF-IDF + Logistic Regression model.
TRAIN_DATA = [
    # --- Dark Patterns (1) ---
    ("only 2 tickets left at this price", 1),
    ("15 people are viewing this right now", 1),
    ("no thanks, I prefer to lose money", 1),
    ("your subscription will automatically renew", 1),
    ("claim your prize before time runs out", 1),
    ("hurry, sale ends in 05:00 minutes", 1),
    ("no thanks, I hate discounts", 1),
    ("your card will be charged automatically after trial", 1),
    ("30 people added this to their cart today", 1),
    ("processing fee added to cart", 1),
    ("you will be billed $29.99 monthly", 1),
    ("don't miss out on this one-time offer", 1),
    ("I prefer to pay full price for this", 1),
    ("others are buying this right now, act fast", 1),
    ("limited time offer expires soon", 1),
    ("service fee applied at final checkout", 1),
    ("no, I don't want to protect my purchase", 1),
    ("flash sale almost over", 1),
    
    # --- Standard UI / Safe Text (0) ---
    ("checkout and pay", 0),
    ("home page", 0),
    ("contact us", 0),
    ("log in to your account", 0),
    ("privacy policy", 0),
    ("add to cart", 0),
    ("proceed to checkout", 0),
    ("forgot password?", 0),
    ("create an account", 0),
    ("terms and conditions", 0),
    ("read more about our team", 0),
    ("careers at our company", 0),
    ("search products", 0),
    ("filter by category", 0),
    ("view product details", 0),
    ("shopping bag", 0),
    ("user profile settings", 0),
    ("dashboard home", 0),
    ("frequently asked questions", 0),
    ("subscribe to our newsletter", 0),
    ("submit payment", 0)
]

X_train = [text for text, label in TRAIN_DATA]
y_train = [label for text, label in TRAIN_DATA]

# Build and train the pipeline instantly on boot
ml_pipeline = make_pipeline(TfidfVectorizer(), LogisticRegression())
ml_pipeline.fit(X_train, y_train)

def ml_detect(snippet):
    """Returns the probability (0.0 to 1.0) that a snippet is a dark pattern."""
    prob = ml_pipeline.predict_proba([snippet])[0][1]
    return prob

# ==========================================
# AGGREGATION & SCORING LOGIC
# ==========================================
def analyze_snippets(snippets):
    """
    Runs all snippets through both tiers and calculates a final page manipulation score.
    Returns: (page_score, flagged_results_list)
    """
    results = []
    total_manipulation_weight = 0
    
    for snippet in snippets:
        category = "None"
        confidence = 0.0
        is_flagged = False
        
        # 1. Check Regex First (High Confidence)
        regex_match = regex_detect(snippet)
        
        if regex_match:
            is_flagged = True
            category = regex_match
            confidence = 0.95 # 95% confident if it hits an exact regex rule
            
        else:
            # 2. Fallback to ML Model
            ml_prob = ml_detect(snippet)
            if ml_prob > 0.65: # Threshold for ML flagging
                is_flagged = True
                category = "ML Flagged (Suspicious Language)"
                confidence = ml_prob
                
        if is_flagged:
            total_manipulation_weight += confidence
            results.append({
                "Snippet": snippet,
                "Category": category,
                "Confidence (%)": round(confidence * 100, 1)
            })
            
    # Calculate final 0-100 Manipulation Score
    # Formula: Each flagged item adds ~20 points based on its confidence. Capped at 100.
    page_score = min(100, (total_manipulation_weight * 20))
    
    return round(page_score, 1), results