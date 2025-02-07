from flask import Flask, request, jsonify
import openai
import os
import json
import requests
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Required environment variables
required_env_vars = [
    "OPENAI_API_KEY",
    "TELEGRAM_SERVICE_URL",
    "CHART_SERVICE_URL"
]

# Validate environment variables
for var in required_env_vars:
    if not os.getenv(var):
        raise RuntimeError(f"Missing required environment variable: {var}")

# OpenAI configuration
openai.api_key = os.getenv("OPENAI_API_KEY")

# Rest of your existing code...

@app.route('/process', methods=['POST'])
def process_signal():
    try:
        signal = request.json
        
        # Add AI analysis
        analysis = analyze_signal(signal)
        signal['aiAnalysis'] = analysis
        
        # Forward to Telegram Service
        telegram_url = os.getenv('TELEGRAM_SERVICE_URL')
        requests.post(f"{telegram_url}/send", json=signal)
        
        # Forward to Chart Service
        chart_url = os.getenv('CHART_SERVICE_URL')
        requests.post(f"{chart_url}/generate", json=signal)
        
        return jsonify({
            'success': True,
            'analysis': signal
        })
    except Exception as e:
        logger.error(f'Error in AI service: {str(e)}')
        return jsonify({
            'error': 'Failed to process signal',
            'details': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'ai-signal-service',
        'dependencies': {
            'openai': bool(os.getenv('OPENAI_API_KEY')),
            'telegram': bool(os.getenv('TELEGRAM_SERVICE_URL')),
            'chart': bool(os.getenv('CHART_SERVICE_URL'))
        }
    })
