def model(dbt, fal):
    dbt.config(materialized="table")
    dbt.config(fal_environment="sentiment-analysis")
    dbt.config(fal_machine="GPU")
    from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
    import numpy as np
    import pandas as pd
    import torch

    # Check if a GPU is available and set the device index
    device_index = 0 if torch.cuda.is_available() else -1

    # Load the model and tokenizer
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Create the sentiment-analysis pipeline with the specified device
    classifier = pipeline("sentiment-analysis", model=model_name, tokenizer=tokenizer, device=device_index)

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
