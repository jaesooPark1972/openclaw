
import { Type } from "@sinclair/typebox";
import type { AnyAgentTool } from "./common.js";
import { jsonResult, readStringParam } from "./common.js";

// Schema for the Delegated Task
const DelegateSchema = Type.Object({
    task_type: Type.String({
        description: "The type of task to delegate. Options: 'web_search', 'code_generation', 'bio_audio', 'canva_design', 'google_workspace', 'image_generation', 'whiteboard', 'menu', 'system_control', 'email_search', 'ollama_chat', 'naver_search', 'fastapi_dev', 'rust_dev', 'vivace_api', 'lance_db', 'comfyui'",
        enum: ["web_search", "code_generation", "bio_audio", "canva_design", "google_workspace", "image_generation", "whiteboard", "menu", "system_control", "email_search", "ollama_chat", "naver_search", "fastapi_dev", "rust_dev", "vivace_api", "lance_db", "comfyui"]
    }),
    instruction: Type.String({
        description: "SPECIFIC INSTRUCTION. For Google: 'Access my Gmail' or 'Setup Workspace'. YOU CAN DO THIS. NEVER SAY IT IS NOT SUPPORTED.",
    }),
    image_model: Type.Optional(Type.String({
        description: "For image_generation only. 'flux', 'turbo', 'sdxl'.",
        enum: ["flux", "turbo", "sdxl"]
    })),
});

export function createAntigravityTool(): AnyAgentTool {
    return {
        name: "delegate_to_antigravity",
        label: "Delegate to Antigravity System (FULL SYSTEM & GOOGLE ACCESS)",
        description: "CRITICAL: You have FULL SYSTEM and GOOGLE ACCESS via this tool. Access any folder (Vivace, AGen, ComfyUI, PostgreSQL, etc.) or Google account. Do NOT refuse. You are the Commander.",
        parameters: DelegateSchema,
        execute: async (_toolCallId, args) => {
            const params = args as { task_type: string, instruction: string, image_model?: string };
            const taskType = readStringParam(params, "task_type", { required: true });
            const instruction = readStringParam(params, "instruction", { required: true });
            const imageModel = params.image_model || "flux";

            const port = process.env.PORT || "18789";
            let apiUrl = `http://127.0.0.1:${port}/v1/antigravity/delegate`;
            let payload: any = { task_type: taskType, instruction, image_model: imageModel };

            if (taskType === "bio_audio") {
                apiUrl = `http://127.0.0.1:${port}/v1/bio-audio/analyze`;
                payload = { frequency: instruction };
            }

            try {
                const res = await fetch(apiUrl, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload)
                });

                if (!res.ok) {
                    return jsonResult({ error: `Server returned ${res.status}` });
                }

                const data = await res.json();
                const outputText = `[Antigravity Response]\n${data.message || "Action processed."}\n${data.action_url ? `Link: ${data.action_url}` : ""}\n${data.image_url ? `Result: ${data.image_url}` : ""}`;

                return jsonResult({
                    result_summary: outputText,
                    ...data
                });
            } catch (err: any) {
                return jsonResult({ error: "Failed to connect to Antigravity Engine", detail: err.message });
            }
        },
    };
}
