
import https from 'https';

const keys = [
    { name: 'Current (jaesoo Park)', key: 'BSAplc8XO2RomfcdM-TZF0S4t5nbIoD' },
    { name: 'Candidate 2 (vivace02)', key: 'BSA9-oMJAhDqdSKCkrxGarHZoVqGwO_' },
    { name: 'Candidate 3 (brave01)', key: 'BSAxLWCYwZRlkOaFEoyHos9r_CUdDRp' }
];

async function testKey(keyItem) {
    return new Promise((resolve) => {
        const options = {
            hostname: 'api.search.brave.com',
            path: '/res/v1/web/search?q=openclaw&count=1',
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'X-Subscription-Token': keyItem.key
            }
        };

        const req = https.request(options, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                if (res.statusCode === 200) {
                    console.log(`✅ [SUCCESS] ${keyItem.name}: Working!`);
                    resolve(true);
                } else {
                    console.log(`❌ [FAILED] ${keyItem.name}: Status ${res.statusCode} - ${data.substring(0, 100)}`);
                    resolve(false);
                }
            });
        });

        req.on('error', (e) => {
            console.log(`❌ [ERROR] ${keyItem.name}: ${e.message}`);
            resolve(false);
        });

        req.end();
    });
}

async function run() {
    console.log("Testing Brave API Keys...\n");
    for (const k of keys) {
        await testKey(k);
    }
}

run();
