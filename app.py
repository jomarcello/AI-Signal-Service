from flask import Flask, request, jsonify
import openai
import os
import json

app = Flask(__name__)

# OpenAI configuratie
openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_signal(signal):
    prompt = f"""You are SigmaPips AI, a professional trading analyst. Analyze this trading signal and provide a concise verdict:

Signal Details:
- Symbol: {signal['symbol']}
- Action: {signal['action']}
- Entry Price: {signal['price']}
- Stop Loss: {signal['stopLoss']}
- Take Profit: {signal['takeProfit']}
- Timeframe: {signal['interval']}
- Strategy: {signal['strategy']}

Provide a concise analysis in exactly this format:
"The {signal['symbol']} {signal['action'].lower()} signal [describe momentum and indicators], suggesting [expected movement]. With [describe stop loss characteristics] and [describe risk/reward], this setup [describe opportunity] for disciplined traders."

Keep the analysis to 2-3 lines maximum. Focus on momentum, key levels, and the opportunity. Use professional but clear language.
"""
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are SigmaPips AI, a professional trading analyst. Provide concise, actionable analysis focusing on momentum, key levels, and clear opportunities."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API error: {str(e)}")
        return "AI analysis temporarily unavailable"

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'ai-signal-service'
    })

@app.route('/process', methods=['POST'])
def process_signal():
    try:
        signal = request.json
        
        # Voeg AI analyse toe
        analysis = analyze_signal(signal)
        signal['aiAnalysis'] = analysis
        
        return jsonify({
            'success': True,
            'analysis': signal
        })
    except Exception as e:
        print(f'Error in AI service: {str(e)}')
        return jsonify({
            'error': 'Failed to process signal',
            'details': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 