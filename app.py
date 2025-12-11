from flask import Flask, render_template, request, jsonify
from ab_testing_coach import run_ab_test
from prediction_coach import run_prediction_coach
import json

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>AI Marketing Optimizer</h1>
    <h2>A/B Testing</h2>
    <form action="/ab_test" method="post">
        <input type="text" name="topic" placeholder="Campaign topic" required>
        <input type="number" name="variants" value="3" min="2" max="5">
        <button type="submit">Run A/B Test</button>
    </form>
    
    <h2>Prediction Coach</h2>
    <form action="/predict" method="post">
        <input type="text" name="topic" placeholder="Content topic" required>
        <button type="submit">Get Predictions</button>
    </form>
    '''

@app.route('/ab_test', methods=['POST'])
def ab_test():
    topic = request.form['topic']
    variants = int(request.form.get('variants', 3))
    
    try:
        result = run_ab_test(topic, num_variants=variants)
        return f"<h2>A/B Test Results</h2><pre>{json.dumps(result, indent=2)}</pre>"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/predict', methods=['POST'])
def predict():
    topic = request.form['topic']
    
    try:
        result = run_prediction_coach(topic)
        return f"<h2>Prediction Results</h2><pre>{json.dumps(result, indent=2)}</pre>"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)