
// import fetch from 'node-fetch'; // Native fetch

async function testGroq() {
    console.log("Testing Groq API...");
    const apiKey = "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";

    try {
        const res = await fetch("https://api.groq.com/openai/v1/chat/completions", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${apiKey}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                model: "llama-3.3-70b-versatile",
                messages: [{ role: "user", content: "Hello" }]
            })
        });

        if (!res.ok) {
            console.log(`❌ Groq Error: ${res.status}`);
            console.log(await res.text());
            return;
        }

        const data = await res.json();
        console.log("✅ Groq Response:", data.choices[0].message.content);
    } catch (e) {
        console.log("❌ Connection Failed:", e);
    }
}

testGroq();
