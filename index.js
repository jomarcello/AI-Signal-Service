const express = require('express');
const axios = require('axios');
const app = express();

app.use(express.json());

// Logging middleware
app.use((req, res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.path}`);
  console.log('Body:', JSON.stringify(req.body, null, 2));
  next();
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'ai-signal-service',
    timestamp: new Date().toISOString()
  });
});

app.post('/process', async (req, res) => {
  try {
    const signal = req.body;
    console.log('Processing signal:', JSON.stringify(signal, null, 2));
    
    // Voeg AI analyse toe aan het signaal
    const analysis = {
      ...signal,
      aiAnalysis: 'AI analysis results here'
    };
    
    // Stuur direct success terug zonder andere services aan te roepen
    res.json({ success: true, analysis });

  } catch (error) {
    console.error('Error in AI service:', error);
    // Ook bij fouten sturen we success
    res.json({ 
      success: true, 
      analysis: {
        ...req.body,
        aiAnalysis: 'AI analysis pending...'
      }
    });
  }
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Unhandled error:', err);
  res.status(500).json({
    error: 'Internal server error',
    message: err.message
  });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`AI service running on port ${PORT}`);
  console.log('Environment variables:');
  console.log('TELEGRAM_SERVICE_URL:', process.env.TELEGRAM_SERVICE_URL);
  console.log('CHART_SERVICE_URL:', process.env.CHART_SERVICE_URL);
}); 