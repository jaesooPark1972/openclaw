"""
AirLLM Inference wrapper for OpenClaw.
Based on "99% don't know this low-VRAM method" (AirLLM).
Runs locally.

Requirements: pip install airllm
"""

import sys
import os
import time
from pathlib import Path

# Verify installation
try:
    from airllm import AutoModel
except ImportError:
    print("❌ AirLLM not installed. Run: pip install airllm")
    sys.exit(1)

model_id = "Qwen/Qwen3-Next-80B-A3B-Thinking"  # SOTA Qwen3 Series 80B (Thinking Mode)
# model_id = "Qwen/Qwen2.5-72B-Instruct" 

def run_inference(prompt: str):
    print(f"🚀 Initializing AirLLM with model: {model_id}")
    print("⚠️  First run will download the model (huge). Ensure disk space!")
    
    start_time = time.time()
    
    try:
        # AirLLM automatically handles layer-wise inference
        model = AutoModel.from_pretrained(
            model_id,
            device_map="auto",
            compression="4bit" # Use 4bit to save even more memory
        )
        
        input_text = [
            f"User: {prompt}",
            "Assistant: "
        ]

        print("generating...")
        input_tokens = model.tokenizer(input_text,
            return_tensors="pt", 
            return_attention_mask=False, 
            truncation=True, 
            max_length=128, 
            padding=False)
            
        generation_output = model.generate(
            input_tokens['input_ids'].cuda(), 
            max_new_tokens=50,
            use_cache=True,
            return_dict_in_generate=True)

        output = model.tokenizer.decode(generation_output.sequences[0])
        
        end_time = time.time()
        print(f"\n✅ Output:\n{output}")
        print(f"⏱️ Time taken: {end_time - start_time:.2f}s")
        
    except Exception as e:
        print(f"❌ Inference Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_prompt = " ".join(sys.argv[1:])
    else:
        user_prompt = "Explain quantum physics in one sentence."
    
    run_inference(user_prompt)
