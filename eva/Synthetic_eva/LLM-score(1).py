#!/usr/bin/env python3
import sys
import argparse
import torch
import os
from torch.nn.functional import softmax
import numpy as np
from transformers import AutoTokenizer, AutoModelForCausalLM
import csv

parser = argparse.ArgumentParser(description='Give the LM score for the sentence')
parser.add_argument('--sent',default='sentence.txt', help='Path to CSV containing sentences', type=str, required=True) 
parser.add_argument('--model',  default="tartuNLP/Llammas",help='Model name: e.g. tartuNLP/Llammas-base, tartuNLP/Llammas-translate, etc.',type=str, required=False)  
parser.add_argument('--output', default='output.csv',help='Output CSV file',type=str, required=True)
parser.add_argument('--summary', default='summary.txt',help='Output summary file',type=str, required=False)

args = parser.parse_args()

if torch.cuda.is_available():
    device = torch.device("cuda")
    print("Using CUDA:", torch.cuda.get_device_name(0))
else:
    device = torch.device("cpu")
    print("CUDA is not available, using CPU instead.")

tokenizer = AutoTokenizer.from_pretrained(args.model)
model = AutoModelForCausalLM.from_pretrained(args.model, force_download=True).to(device)

def sentence_prob_mean(text):
    """Compute the mean probability for each token in `text` under the model."""
    input_ids = tokenizer.encode(text, return_tensors='pt').to(device)
    with torch.no_grad():
        outputs = model(input_ids, labels=input_ids)
        logits = outputs.logits
    shift_logits = logits[..., :-1, :].contiguous()
    shift_labels = input_ids[..., 1:].contiguous()
    probs = softmax(shift_logits, dim=-1)
    gathered_probs = torch.gather(probs, 2, shift_labels.unsqueeze(-1)).squeeze(-1)
    mean_prob = torch.mean(gathered_probs).item()
    return mean_prob

output_data = []

# Read CSV lines; expects columns: sent_m, sent_w, Labor_Stat
with open(args.sent, 'r', encoding='utf-8') as csvfile:
    csvreader = csv.DictReader(csvfile)
    
    for row in csvreader:
        sent_m = row['sent_m']
        sent_w = row['sent_w']

        Labor_Stat = row['Labor_Stat']
        
        # Calculate LM scores
        LM_M = sentence_prob_mean(sent_m)
        LM_W = sentence_prob_mean(sent_w)
        
        # Determine higher score
        if LM_M > LM_W:
            computed_gender = 'M'
        elif LM_M < LM_W:
            computed_gender = 'F'
        else:
            computed_gender = 'Equal'

        if computed_gender == 'Equal':
            labor_stat_match = 0
            bias_towards = "None"
        else:
            labor_stat_match = 1 if computed_gender == Labor_Stat else 0
            bias_towards = computed_gender
        
        # Store result
        output_data.append({
            'sent_m': sent_m,
            'sent_w': sent_w,
            'Labor_Stat': Labor_Stat,
            'LM_score_M': LM_M,
            'LM_score_W': LM_W,
            'gender_score': computed_gender,
            'labor_stat_match': labor_stat_match,
            'bias_towards': bias_towards
        })

# Write out CSV
with open(args.output, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = [
        'sent_m',
        'sent_w',
        'Labor_Stat',
        'LM_score_M',
        'LM_score_W',
        'gender_score',
        'labor_stat_match',
        'bias_towards'
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for data in output_data:
        writer.writerow(data)

# --- Write summary statistics to a separate file ---
labor_stat_m = sum(1 for d in output_data if d['Labor_Stat'] == 'M')
labor_stat_f = sum(1 for d in output_data if d['Labor_Stat'] == 'F')
total_rows = len(output_data)

pred_m = sum(1 for d in output_data if d['gender_score'] == 'M')
pred_f = sum(1 for d in output_data if d['gender_score'] == 'F')

# Calculate prediction–Labor_Stat alignment
correct_alignments = sum(d["labor_stat_match"] for d in output_data)
alignment_ratio = correct_alignments / total_rows if total_rows > 0 else 0.0

with open(args.summary, 'w', encoding='utf-8') as summaryfile:
    # Include the model name in the summary
    summaryfile.write(f"--- Summary for Model: {args.model} ---\n\n")
    
    # Labor_Stat Summary
    summaryfile.write("--- Labor_Stat Summary ---\n")
    summaryfile.write(f"Total rows: {total_rows}\n")
    summaryfile.write(f"Count of M: {labor_stat_m}, Count of F: {labor_stat_f}\n")
    if (labor_stat_m + labor_stat_f) > 0:
        ratio_m = labor_stat_m / (labor_stat_m + labor_stat_f)
        ratio_f = labor_stat_f / (labor_stat_m + labor_stat_f)
        summaryfile.write(f"Ratio (M / (M+F)): {ratio_m:.2f}\n")
        summaryfile.write(f"Ratio (F / (M+F)): {ratio_f:.2f}\n")

    # Prediction Summary
    summaryfile.write("\n--- Prediction Summary ---\n")
    summaryfile.write(f"Predicted M: {pred_m}, F: {pred_f}\n")
    if (pred_m + pred_f) > 0:
        ratio_pred_m = pred_m / (pred_m + pred_f)
        ratio_pred_f = pred_f / (pred_m + pred_f)
        summaryfile.write(f"Ratio (M / (M+F)): {ratio_pred_m:.2f}\n")
        summaryfile.write(f"Ratio (F / (M+F)): {ratio_pred_f:.2f}\n")

    # Alignment (accuracy) Summary
    summaryfile.write("\n--- Prediction–Labor_Stat Alignment ---\n")
    summaryfile.write(f"Matches: {correct_alignments} out of {total_rows}\n")
    summaryfile.write(f"Alignment ratio (accuracy): {alignment_ratio:.2f}\n")

    summaryfile.write("\n--- End of Summary ---\n")