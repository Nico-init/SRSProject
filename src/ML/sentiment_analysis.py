
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import statistics

key = "2503206dd363461ca35e17f4572a8905"
endpoint = "https://scalrelsys.cognitiveservices.azure.com/"


# Authenticate the client using your key and endpoint
def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=ta_credential)
    return text_analytics_client


client = authenticate_client()


# Example method for detecting opinions in text
def sentiment_analysis(documents, target=None):
    documents = [documents]     # if you want to take as input a list of docs remove this line

    result = client.analyze_sentiment(documents, show_opinion_mining=True)
    doc_result = [doc for doc in result if not doc.is_error]

    result_pos = []
    result_neu = []
    result_neg = []
    for document in doc_result:
        positive = document.confidence_scores.positive
        neutral = document.confidence_scores.neutral
        negative = document.confidence_scores.negative
        target_positive = []
        target_neutral = []
        target_negative = []
        if target is not None:
            for sentence in document.sentences:
                for mined_opinion in sentence.mined_opinions:
                    opinion_target = mined_opinion.target
                    if opinion_target.text.upper() == target.upper():
                        target_positive.append(opinion_target.confidence_scores.positive)
                        target_neutral.append(opinion_target.confidence_scores.neutral)
                        target_negative.append(opinion_target.confidence_scores.negative)
            if target_positive:
                positive = statistics.mean(target_positive)
                neutral = statistics.mean(target_neutral)
                negative = statistics.mean(target_negative)
        result_pos.append(positive)
        result_neu.append(neutral)
        result_neg.append(negative)
    if result_pos and result_neu and result_neg:
        return result_pos[0], result_neu[0], result_neg[0]     # if you want to take as input a list of docs, remove [0]
    else:
        raise Exception(f"it was not possible to process the documents {documents}")


if __name__ == "__main__":
    doc = "The food and service were unacceptable, but the concierge were nice. " \
          "Also, it was difficult to talk as it was too much noise."
    pos, neu, neg = sentiment_analysis(doc, "food")
    print(pos)
    print(neu)
    print(neg)

