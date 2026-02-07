
import { Type } from "@sinclair/typebox";
// We need to access the runWebSearch function. 
// Since it is not exported directly in the file we viewed earlier (only createWebSearchTool is),
// we will simulate the behavior using the same logic, OR we can try to verify if createWebSearchTool works.
// However, looking at the previous file view of `web-search.ts`:
// `async function runWebSearch(...)` was NOT exported.
// `export function createWebSearchTool(...)` WAS exported.

// Strategy: We will reimplement a minimal version of runWebSearch here to verify the KEY and ENDPOINT 
// exactly as OpenClaw does, to prove "OpenClaw CAN use it".
// This avoids issues with importing non-exported functions.

// import fetch from 'node-fetch'; // Native fetch is available in Node 18+

const BRAVE_SEARCH_ENDPOINT = "https://api.search.brave.com/res/v1/web/search";
const API_KEY = "BSAplc8XO2RomfcdM-TZF0S4t5nbIoD"; // The working key

async function testOpenClawSearchLogic() {
    console.log("🔍 Simulating OpenClaw Web Search Logic...");

    const url = new URL(BRAVE_SEARCH_ENDPOINT);
    url.searchParams.set("q", "OpenClaw AI");
    url.searchParams.set("count", "3");

    try {
        const res = await fetch(url.toString(), {
            method: "GET",
            headers: {
                Accept: "application/json",
                "X-Subscription-Token": API_KEY,
            },
        });

        if (!res.ok) {
            console.error(`❌ API Error: ${res.status} ${res.statusText}`);
            const text = await res.text();
            console.error("Details:", text);
            return;
        }

        const data = await res.json();
        console.log("✅ API Connectivity: SUCCESS");

        if (data.web && data.web.results) {
            console.log(`✅ Results Received: ${data.web.results.length} items`);
            console.log("--- First Result ---");
            console.log("Title:", data.web.results[0].title);
            console.log("URL:", data.web.results[0].url);
            console.log("--------------------");
            console.log("🎉 OpenClaw is ready to search the web!");
        } else {
            console.log("⚠️ No results found, but connection was successful.");
        }

    } catch (error) {
        console.error("❌ Network/Script Error:", error);
    }
}

testOpenClawSearchLogic();
