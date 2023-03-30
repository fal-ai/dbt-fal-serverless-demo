def model(dbt, fal):
    dbt.config(materialized="table")
    dbt.config(fal_environment="sentiment-analysis")
    dbt.config(fal_machine="GPU-T4")
    from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
    import numpy as np
    import pandas as pd
    import torch

    # Check if a GPU is available and set the device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    print(f"Running sentiment analysis on: {device}")

    # Load the model and tokenizer
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    model = AutoModelForSequenceClassification.from_pretrained(model_name).to(device)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Create the sentiment-analysis pipeline
    classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

    ticket_data = dbt.ref("zendesk_ticket_data")
    ticket_descriptions = ticket_data["DESCRIPTION"].tolist()

    # Run the sentiment analysis on the ticket descriptions
    description_sentiment_analysis = classifier(ticket_descriptions)
    rows = []

    for id, sentiment in zip(ticket_data.ID, description_sentiment_analysis):
        rows.append((int(id), sentiment["label"], sentiment["score"]))

    records = np.array(rows, dtype=[("id", int), ("label", "U8"), ("score", float)])

    sentiment_df = pd.DataFrame.from_records(records)

    return sentiment_df
