import re
import unicodedata
from difflib import SequenceMatcher


# ==========================================
# 1. NAME NORMALIZATION
# ==========================================

LOOKALIKE_MAP = str.maketrans({
    "0": "o",
    "1": "i",
    "3": "e",
    "4": "a",
    "5": "s",
    "7": "t",
    "@": "a",
    "$": "s",
})

SUSPICIOUS_WORDS = {
    "login", "signin", "verify", "secure",
    "account", "support", "offers", "discount",
    "payment", "wallet", "claim", "reward"
}

BENIGN_WORDS = {
    "careers", "jobs", "press", "news",
    "community", "history"
}


def normalize_name(name):
    """Remove spaces and special characters."""
    name = unicodedata.normalize("NFKC", name or "")
    name = name.casefold()
    name = "".join(
        ch for ch in name
        if not unicodedata.combining(ch)
    )
    return re.sub(r"[^a-z0-9]", "", name)


def skeleton_name(name):
    """Convert common look-alike characters."""
    return normalize_name(name).translate(LOOKALIKE_MAP)


# ==========================================
# 2. SIMILARITY DETECTION
# ==========================================

def calculate_similarity(brand, candidate):
    """Return similarity as a percentage."""
    brand = normalize_name(brand)
    candidate = normalize_name(candidate)

    if not brand or not candidate:
        return 0

    similarity = SequenceMatcher(
        None, brand, candidate
    ).ratio()

    return round(similarity * 100, 2)


def levenshtein_distance(first, second):
    """Count insertions, deletions and substitutions."""
    if len(first) < len(second):
        first, second = second, first

    previous = list(range(len(second) + 1))

    for i, char1 in enumerate(first, start=1):
        current = [i]

        for j, char2 in enumerate(second, start=1):
            insert_cost = current[j - 1] + 1
            delete_cost = previous[j] + 1
            replace_cost = previous[j - 1] + (
                char1 != char2
            )

            current.append(
                min(insert_cost, delete_cost, replace_cost)
            )

        previous = current

    return previous[-1]


def is_character_swap(brand, candidate):
    """Detect one adjacent character transposition."""
    if len(brand) != len(candidate):
        return False

    differences = [
        i for i, (a, b) in enumerate(zip(brand, candidate))
        if a != b
    ]

    if len(differences) != 2:
        return False

    i, j = differences

    return (
        j == i + 1
        and brand[i] == candidate[j]
        and brand[j] == candidate[i]
    )


def get_detection_reasons(brand_name, candidate_name):
    """Identify possible look-alike patterns."""
    brand = normalize_name(brand_name)
    candidate = normalize_name(candidate_name)
    reasons = []

    if not brand or not candidate:
        return ["Brand or candidate name is empty"]

    if brand == candidate:
        return ["Exact normalized name match"]

    if skeleton_name(brand_name) == skeleton_name(candidate_name):
        reasons.append("Possible look-alike character substitution")

    if is_character_swap(brand, candidate):
        reasons.append("Adjacent character swap detected")

    distance = levenshtein_distance(brand, candidate)

    if distance == 1 and len(brand) > 1:
        reasons.append("One character insertion, deletion or substitution")

    if brand in candidate and brand != candidate:
        reasons.append("Brand name combined with extra characters")

    if candidate in brand and brand != candidate:
        reasons.append("Candidate is a shortened brand-like name")

    # Detect extra words such as nike-offers or nike-login.
    words = re.findall(
        r"[a-z0-9]+",
        unicodedata.normalize(
            "NFKC", candidate_name
        ).casefold()
    )

    suspicious = set(words) & SUSPICIOUS_WORDS

    if suspicious and any(
        normalize_name(word) == brand for word in words
    ):
        reasons.append(
            "Brand name with suspicious terms: "
            + ", ".join(sorted(suspicious))
        )

    return reasons or ["No strong look-alike pattern detected"]


# ==========================================
# 3. SEVERITY CLASSIFICATION
# ==========================================

def classify_severity(score):
    """Convert risk score to severity level."""
    if score >= 80:
        return "CRITICAL"
    elif score >= 60:
        return "HIGH"
    elif score >= 35:
        return "MEDIUM"
    else:
        return "LOW"


# ==========================================
# 4. RISK SCORING
# ==========================================

def calculate_risk_score(
    brand_name,
    candidate_name,
    asset_type="unknown"
):
    """Calculate a heuristic risk score from 0 to 100."""

    brand = normalize_name(brand_name)
    candidate = normalize_name(candidate_name)

    if not brand:
        raise ValueError("Brand name cannot be empty")

    if not candidate:
        return 0

    # Exact normalized matches are not flagged by default.
    if brand == candidate:
        return 0

    score = 0
    similarity = calculate_similarity(
        brand_name, candidate_name
    )
    distance = levenshtein_distance(brand, candidate)
    reasons = get_detection_reasons(
        brand_name, candidate_name
    )

    # Look-alike character substitutions.
    if skeleton_name(brand_name) == skeleton_name(candidate_name):
        score += 55

    # Adjacent character transposition.
    elif is_character_swap(brand, candidate):
        score += 45

    # Similar spelling or edit distance.
    elif similarity >= 85 and distance <= 2:
        score += 40

    elif similarity >= 70 and distance <= max(
        2, len(brand) // 3
    ):
        score += 25

    # Extra words or characters.
    if brand in candidate and brand != candidate:
        score += 15

    # Risky words in the candidate name.
    words = set(re.findall(
        r"[a-z0-9]+",
        unicodedata.normalize(
            "NFKC", candidate_name
        ).casefold()
    ))

    if words & SUSPICIOUS_WORDS:
        score += 15

    # Potentially benign context reduces score slightly.
    if words & BENIGN_WORDS:
        score -= 10

    # Domain-like assets deserve a small additional check.
    if (
        asset_type.casefold() in {"domain", "url", "website"}
        and similarity >= 70
    ):
        score += 5

    return max(0, min(100, score))


# ==========================================
# 5. MAIN DETECTION FUNCTION
# ==========================================

def detect_lookalike(
    brand_name,
    candidate_name,
    asset_type="unknown",
    official_assets=None
):
    """
    Detect a possible brand look-alike.

    official_assets: optional list of verified official names.
    This list must come from a trusted source.
    """

    if not normalize_name(brand_name):
        raise ValueError("Brand name cannot be empty")

    official_assets = official_assets or []

    candidate_normalized = normalize_name(candidate_name)

    verified_assets = {
        normalize_name(asset)
        for asset in official_assets
    }

    # Exact verified asset: suppress the alert.
    if candidate_normalized in verified_assets:
        return {
            "brand": brand_name,
            "candidate": candidate_name,
            "similarity": calculate_similarity(
                brand_name, candidate_name
            ),
            "risk_score": 0,
            "severity": "LOW",
            "reasons": ["Matches a verified official asset"],
            "needs_review": False,
            "asset_type": asset_type
        }

    reasons = get_detection_reasons(
        brand_name, candidate_name
    )

    score = calculate_risk_score(
        brand_name,
        candidate_name,
        asset_type
    )

    return {
        "brand": brand_name,
        "candidate": candidate_name,
        "similarity": calculate_similarity(
            brand_name, candidate_name
        ),
        "risk_score": score,
        "severity": classify_severity(score),
        "reasons": reasons,
        "needs_review": score >= 35,
        "asset_type": asset_type
    }


# ==========================================
# 6. TEST MULTIPLE CANDIDATES
# ==========================================

def scan_candidates(
    brand_name,
    candidates,
    asset_type="domain",
    official_assets=None
):
    """Scan a list and return highest-risk results first."""

    results = []

    for candidate in candidates:
        result = detect_lookalike(
            brand_name=brand_name,
            candidate_name=candidate,
            asset_type=asset_type,
            official_assets=official_assets
        )
        results.append(result)

    return sorted(
        results,
        key=lambda item: item["risk_score"],
        reverse=True
    )


# ==========================================
# 7. RUN TESTS
# ==========================================

if __name__ == "__main__":

    brand = "nike"

    test_candidates = [
        "nike",
        "nkie",
        "n1ke",
        "ni ke",
        "nike-offers",
        "nike-login",
        "nikecareers",
        "adidas",
        "nikke"
    ]

    results = scan_candidates(
        brand_name=brand,
        candidates=test_candidates,
        asset_type="domain",
        official_assets=["nike"]
    )

    print("\nDIGITAL RISK PROTECTION PLATFORM")
    print("AI/ML DETECTION ENGINE")
    print("=" * 60)

    for result in results:
        print("\nBrand:", result["brand"])
        print("Candidate:", result["candidate"])
        print("Similarity:", result["similarity"], "%")
        print("Risk Score:", result["risk_score"])
        print("Severity:", result["severity"])
        print("Reasons:", ", ".join(result["reasons"]))
        print("Needs Review:", result["needs_review"])
        print("-" * 60)