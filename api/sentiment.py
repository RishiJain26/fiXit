from flask import Flask, jsonify,request
from transformers import pipeline
import re
import os
import requests
API_URL = "https://api-inference.huggingface.co/models/lxyuan/distilbert-base-multilingual-cased-sentiments-student"
headers = {"Authorization": "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"} 

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response

# pipe = pipeline("text-classification", model="lxyuan/distilbert-base-multilingual-cased-sentiments-student")
app = Flask(__name__)

def parse_transcript(text):
    dialogues = re.findall(r"\[(.*?)\]([^\[]*)", text)
    parsed_dialogues = [{"speaker": speaker, "text": dialogue.strip()} for speaker, dialogue in dialogues]
    return parsed_dialogues

def analyze_sentiment(parsed_dialogue):
    result = []
    for dialogue in parsed_dialogue:
        result_dialogue = query(dialogue['text'])
        result.append({"speaker": dialogue['speaker'], "text": dialogue['text'], "score": result_dialogue[0]})
    return result 


@app.route('/',methods = ['POST'])
def get_data():
    data = request.get_json()
    print(data)
    if 'transcript' in data:
        transcript_content = data['transcript']
        parsed_dialogue = parse_transcript(transcript_content)
        sentiment_result = analyze_sentiment(parsed_dialogue)
        return jsonify(sentiment_result)
    
    return jsonify({'Status':'Error in File'}),400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port,debug=True)