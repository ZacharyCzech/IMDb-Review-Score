import torch
from transformers import pipeline


def analyze_reviews(reviews):
    device_id = 0 if torch.cuda.is_available() else -1
    classifier = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        device=device_id
    )

    positive_count = 0
    negative_count = 0
    results = []

    for text in reviews:
        truncated_text = text[:512]
        out = classifier(truncated_text)[0]
        label = out["label"]
        score = out["score"]
        results.append((text, label, score))
        if label == "POSITIVE":
            positive_count += 1
        else:
            negative_count += 1

    total = len(reviews)
    if total > 0:
        pos_pct = (positive_count / total) * 100
        neg_pct = (negative_count / total) * 100
    else:
        pos_pct = 0
        neg_pct = 0

    return results, pos_pct, neg_pct
