def model(dbt, fal):
    dbt.config(materialized="table")
    dbt.config(fal_environment="funny", fal_machine="GPU-T4")
    from transformers import pipeline
    import numpy as np
    import pandas as pd

    ticket_data = dbt.ref("zendesk_ticket_data")
    ticket_descriptions = list(ticket_data.description)
    classifier = pipeline("sentiment-analysis", accelerator="cuda")
    description_sentimet_analysis = classifier(ticket_descriptions)
    rows = []

    for id, sentiment in zip(ticket_data.id, description_sentimet_analysis):
        rows.append((int(id), sentiment["label"], sentiment["score"]))

    records = np.array(rows, dtype=[("id", int), ("label", "U8"), ("score", float)])

    sentiment_df = pd.DataFrame.from_records(records)

    return sentiment_df
