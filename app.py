from flask import Flask, request, jsonify
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)

# Load spaCy model for NER
nlp = spacy.load("en_core_web_sm")

# Initialize Sentiment Analyzer
sentiment_analyzer = SentimentIntensityAnalyzer()

API_KEY = "vamshi"
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the NLP API! Use /analyze endpoint."})

@app.route('/analyze', methods=['POST'])
def analyze():
    key = request.headers.get('x-api-key')
    if key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    sentence = data.get("sentence", "")

    if not sentence:
        return jsonify({"error": "No sentence provided"}), 400

    # Sentiment Analysis
    sentiment_scores = sentiment_analyzer.polarity_scores(sentence)
    sentiment = "positive" if sentiment_scores["compound"] > 0 else "negative" if sentiment_scores["compound"] < 0 else "neutral"

    # Named Entity Recognition (NER)
    doc = nlp(sentence)
    entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]

    return jsonify({
        "sentence": sentence,
        "sentiment": sentiment,
        "entities": entities
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
