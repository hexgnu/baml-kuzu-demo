import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set


def load_json_file(file_path: str) -> List[dict]:
    """Load JSON data from a file."""
    with open(file_path, "r") as f:
        return json.load(f)


def extract_all_strings(data: List[dict]) -> Set[str]:
    """Extract all string values from nested JSON structure."""
    all_strings = set()

    for item in data:
        # Add condition
        all_strings.add(item["condition"])
        
        # Add drug names (generic and brand)
        for drug in item["drug"]:
            all_strings.add(drug["generic_name"])
            all_strings.update(brand for brand in drug["brand_names"] if brand)
        
        # Add side effects
        all_strings.update(effect for effect in item["side_effects"] if effect)

    return all_strings


def evaluate_extraction(human_path: str, extracted_path: str) -> Dict[str, int]:
    """Compare human annotated data with extracted data and return metrics."""
    human_data = load_json_file(human_path)
    extracted_data = load_json_file(extracted_path)

    human_strings = extract_all_strings(human_data)
    extracted_strings = extract_all_strings(extracted_data)

    metrics = {
        "exact_match": len(human_strings.intersection(extracted_strings)),
        "missing": len(human_strings - extracted_strings),
        "potential_hallucination": len(extracted_strings - human_strings),
    }

    return metrics


def run_evaluation(
    human_dir: Path = Path("../../data/human_annotated_data"),
    extracted_dir: Path = Path("../../data/extracted_data"),
) -> Dict[str, Dict[str, int]]:
    """Run evaluation on all matching files in human_annotated_data and extracted_data."""
    results = {}

    # Find all JSON files with the prefix "drugs" in human_annotated_data
    for human_file in human_dir.glob("drugs*.json"):
        filename = human_file.name
        extracted_file = extracted_dir / filename

        # Check if corresponding file exists in extracted_data
        if extracted_file.exists():
            results[filename] = evaluate_extraction(str(human_file), str(extracted_file))

    return results


def main():
    """Main function to run evaluation and print results."""
    results = run_evaluation()

    # Print results
    print("Evaluation Results:")
    print("===================")

    for filename, metrics in results.items():
        total = metrics["exact_match"] + metrics["missing"] + metrics["potential_hallucination"]
        print(f"\nFile: {filename}")
        print(f"  Exact matches: {metrics['exact_match']} ({metrics['exact_match']/total:.1%})")
        print(f"  Missing items: {metrics['missing']} ({metrics['missing']/total:.1%})")
        print(f"  Potential hallucinations: {metrics['potential_hallucination']} ({metrics['potential_hallucination']/total:.1%})")

    # Calculate totals
    totals = defaultdict(int)
    for metrics in results.values():
        for metric, count in metrics.items():
            totals[metric] += count
    
    grand_total = totals["exact_match"] + totals["missing"] + totals["potential_hallucination"]
    
    print("\nTotals across all files:")
    print(f"  Total exact matches: {totals['exact_match']} ({totals['exact_match']/grand_total:.1%})")
    print(f"  Total missing items: {totals['missing']} ({totals['missing']/grand_total:.1%})")
    print(f"  Total potential hallucinations: {totals['potential_hallucination']} ({totals['potential_hallucination']/grand_total:.1%})")


if __name__ == "__main__":
    main()
