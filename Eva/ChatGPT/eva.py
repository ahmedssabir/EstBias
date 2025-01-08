import argparse
from pathlib import Path

def read_labels(file_path):
    """Read labels from a file and return them as a list."""
    with open(file_path, 'r') as file:
        labels = file.read().split()
    return labels

def calculate_ratios(labels):
    """Calculate the ratio of male and female labels."""
    f_count = labels.count('F')
    m_count = labels.count('M')
    total = f_count + m_count
    m_ratio = m_count / total if total > 0 else 0
    f_ratio = f_count / total if total > 0 else 0
    return m_ratio, f_ratio

def compare_labels(ground_truth_labels, results_labels):
    """Compare two lists of labels and calculate the percentage of matches."""
    if len(ground_truth_labels) != len(results_labels):
        print("The files do not have the same number of labels.")
        return

    # Count matches
    matches = sum(1 for gt_label, res_label in zip(ground_truth_labels, results_labels) if gt_label == res_label)
    total = len(ground_truth_labels)
    match_percentage = (matches / total) * 100 if total > 0 else 0
    print(f"Match Percentage: {match_percentage:.2f}%")

    # Calculate ratios for ground truth and results
    gt_m_ratio, gt_f_ratio = calculate_ratios(ground_truth_labels)
    res_m_ratio, res_f_ratio = calculate_ratios(results_labels)

    print(f"Ground Truth - Male Ratio: {gt_m_ratio:.2f}, Female Ratio: {gt_f_ratio:.2f}")
    print(f"Results - Male Ratio: {res_m_ratio:.2f}, Female Ratio: {res_f_ratio:.2f}")

def main():
    parser = argparse.ArgumentParser(description="Calculate the percentage of label matches and gender ratios between ground truth and results files.")
    parser.add_argument('ground_truth_file', type=str, help='Path to the ground truth file')
    parser.add_argument('results_file', type=str, help='Path to the results file')
    args = parser.parse_args()
    
    # how-to-run
    # python eva.py labor_stat.txt o1_result.txt

    # Validate that files exist before proceeding
    if not Path(args.ground_truth_file).exists() or not Path(args.results_file).exists():
        print("One or both of the files do not exist. Please check the file paths.")
        return

    ground_truth_labels = read_labels(args.ground_truth_file)
    results_labels = read_labels(args.results_file)
    compare_labels(ground_truth_labels, results_labels)

if __name__ == '__main__':
    main()

