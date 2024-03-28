from flask import Flask, request
import json
import query
import weaviate

app = Flask(__name__)

@app.route('/')
def index():
    return json.dumps({'you have successfully reached the server'})

@app.route('/search', methods=['GET', 'POST'])
def search():
    print('establishing connection...')
    #connect to the database
    client = weaviate.Client(
        url="http://weaviate:8080",
        additional_headers = {"X-HuggingFace-Api-Key": "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"}
    )
    print('connection made! asking yandex...')
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        interview = request.json.get('search_interview')
        result = query.main(interview, client)
        return json.dumps(result, ensure_ascii=False, indent=2)
    else:
        return "Content type is not supported! i need json."


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
