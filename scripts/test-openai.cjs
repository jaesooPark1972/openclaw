
const https = require('https');

const apiKey = "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";

const data = JSON.stringify({
    model: "gpt-4o-mini",
    messages: [{ role: "user", content: "Say 'OpenAI OK'" }]
});

const options = {
    hostname: 'api.openai.com',
    path: '/v1/chat/completions',
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
    }
};

const req = https.request(options, (res) => {
    let body = '';
    res.on('data', (chunk) => body += chunk);
    res.on('end', () => {
        if (res.statusCode === 200) {
            console.log("✅ OpenAI Alive:", JSON.parse(body).choices[0].message.content);
        } else {
            console.log(`❌ OpenAI Error ${res.statusCode}:`, body);
        }
    });
});

req.on('error', (e) => {
    console.error(`❌ Request Error: ${e.message}`);
});

req.write(data);
req.end();
