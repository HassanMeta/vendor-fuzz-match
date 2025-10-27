"""Vendor matching service using fuzzy string matching"""

from rapidfuzz import fuzz
import re


def normalize_vendor_name(name):
    """Normalize vendor name for better matching

    Args:
        name: Vendor name string

    Returns:
        str: Normalized vendor name
    """
    if not isinstance(name, str):
        return ""

    # Convert to lowercase
    normalized = name.lower().strip()

    # Remove extra spaces
    normalized = re.sub(r"\s+", " ", normalized)

    # Remove common suffixes
    suffixes = ["inc", "llc", "ltd", "corp", "corporation", "co", "company"]
    for suffix in suffixes:
        normalized = re.sub(rf"\b{suffix}\.?\b", "", normalized)

    # Remove punctuation
    normalized = re.sub(r"[^\w\s]", "", normalized)

    # Remove middle initials (e.g., "John M Doe" -> "john doe")
    normalized = re.sub(r"\b\w\b", "", normalized)
    normalized = re.sub(r"\s+", " ", normalized)

    return normalized.strip()


def calculate_similarity(str1, str2):
    """Calculate similarity score between two strings

    Args:
        str1: First string
        str2: Second string

    Returns:
        float: Similarity score (0-100)
    """
    if not str1 or not str2:
        return 0.0

    # Use multiple matching strategies
    ratio_score = fuzz.ratio(str1.lower(), str2.lower())
    partial_score = fuzz.partial_ratio(str1.lower(), str2.lower())
    token_sort_score = fuzz.token_sort_ratio(str1.lower(), str2.lower())

    # Weighted average
    combined_score = ratio_score * 0.4 + partial_score * 0.3 + token_sort_score * 0.3

    return combined_score


def find_matching_vendors(vendor_list, threshold=85):
    """Find and group matching vendors

    Args:
        vendor_list: List of vendor names
        threshold: Similarity threshold (0-100)

    Returns:
        dict: Groups of matching vendors
    """
    unique_vendors = list(set([str(v).strip() for v in vendor_list if str(v).strip()]))

    matches = {}
    processed = set()

    for vendor in unique_vendors:
        if vendor in processed:
            continue

        # Find similar vendors
        group = [vendor]
        processed.add(vendor)

        for other_vendor in unique_vendors:
            if other_vendor in processed:
                continue

            similarity = calculate_similarity(vendor, other_vendor)

            if similarity >= threshold:
                group.append(other_vendor)
                processed.add(other_vendor)

        if len(group) > 1:
            matches[vendor] = group

    return matches


def process_vendor_dataframe(df, vendor_column="Vendor", amount_column="Amount"):
    """Process CSV and identify matching vendors

    Args:
        df: DataFrame with vendor transaction data
        vendor_column: Name of vendor column
        amount_column: Name of amount column

    Returns:
        dict: Processing results with matched groups and statistics
    """
    if df.empty:
        return {"error": "DataFrame is empty"}

    vendor_df = df[[vendor_column]].copy()
    vendor_df = vendor_df.dropna()

    # Find matching vendors
    matches = find_matching_vendors(vendor_df[vendor_column].tolist())

    # Calculate statistics
    total_vendors = len(vendor_df[vendor_column].unique())
    matched_groups = len(matches)
    total_matched_vendors = sum(len(group) for group in matches.values())

    # Create summary
    summary = []
    for canonical_name, group in matches.items():
        group_amount = (
            df[df[vendor_column].isin(group)][amount_column].sum()
            if amount_column in df.columns
            else 0
        )

        summary.append(
            {
                "Primary Name": canonical_name,
                "Matched Names": ", ".join(group),
                "Variations": len(group),
                "Total Amount": round(group_amount, 2)
                if amount_column in df.columns
                else "N/A",
            }
        )

    return {
        "matches": matches,
        "summary": summary,
        "stats": {
            "total_unique_vendors": total_vendors,
            "matched_groups": matched_groups,
            "total_matched_vendors": total_matched_vendors,
            "unmatched_vendors": total_vendors - total_matched_vendors,
        },
    }
