"""Config and key storage for GrokBot Free."""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONFIG_FILE = HERE / "user_config.json"

PROVIDERS: dict[str, dict[str, str]] = {
    "OpenRouter (Free & Multi)": {
        "base_url": "https://openrouter.ai/api/v1",
        "default_model": "nvidia/nemotron-3.5-lightning:free",
        "desc": "Aggregator with 15+ 100% free models & paid models",
    },
    "xAI (Grok Official)": {
        "base_url": "https://api.x.ai/v1",
        "default_model": "grok-2-latest",
        "desc": "Official Grok model family by xAI",
    },
    "OpenAI": {
        "base_url": "https://api.openai.com/v1",
        "default_model": "gpt-4o",
        "desc": "GPT-4o, o1, o3-mini models",
    },
    "Anthropic": {
        "base_url": "https://api.anthropic.com/v1",
        "default_model": "claude-3-7-sonnet-20250219",
        "desc": "Claude 3.7 Sonnet & Opus models",
    },
    "Google DeepMind (Gemini)": {
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
        "default_model": "gemini-2.0-flash",
        "desc": "Gemini 2.0 Flash & Gemini 1.5 Pro",
    },
    "DeepSeek": {
        "base_url": "https://api.deepseek.com/v1",
        "default_model": "deepseek-chat",
        "desc": "DeepSeek V3 & DeepSeek R1 reasoning models",
    },
    "Groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "default_model": "llama-3.3-70b-versatile",
        "desc": "Ultra-fast LPU inference (Llama, Gemma, DeepSeek)",
    },
    "Cerebras Systems": {
        "base_url": "https://api.cerebras.ai/v1",
        "default_model": "llama3.3-70b",
        "desc": "Wafer-scale engine instant token inference",
    },
    "Mistral AI": {
        "base_url": "https://api.mistral.ai/v1",
        "default_model": "mistral-large-latest",
        "desc": "Mistral Large, Codestral, Pixtral",
    },
    "Meta AI (via Llama API)": {
        "base_url": "https://api.llama-api.com",
        "default_model": "llama3.3-70b",
        "desc": "Meta Llama open weights ecosystem",
    },
    "Together AI": {
        "base_url": "https://api.together.xyz/v1",
        "default_model": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "desc": "Fast cloud inference across open models",
    },
    "Fireworks AI": {
        "base_url": "https://api.fireworks.ai/inference/v1",
        "default_model": "accounts/fireworks/models/llama-v3p3-70b-instruct",
        "desc": "High-throughput serverless compound AI models",
    },
    "Cohere": {
        "base_url": "https://api.cohere.com/v2",
        "default_model": "command-r-plus",
        "desc": "Command R+ and enterprise language models",
    },
    "MiniMax": {
        "base_url": "https://api.minimaxi.chat/v1",
        "default_model": "abab6.5s-chat",
        "desc": "High-intelligence bilingual and multimodal models",
    },
    "Zhipu AI (GLM)": {
        "base_url": "https://open.bigmodel.cn/api/paas/v4",
        "default_model": "glm-4-plus",
        "desc": "GLM-4 & CogView foundation models",
    },
    "Moonshot AI (Kimi)": {
        "base_url": "https://api.moonshot.cn/v1",
        "default_model": "moonshot-v1-8k",
        "desc": "Kimi long-context conversation models",
    },
    "Alibaba Cloud (Qwen)": {
        "base_url": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
        "default_model": "qwen-max",
        "desc": "Tongyi Qianwen Qwen 2.5 series",
    },
    "Baidu (Ernie Bot)": {
        "base_url": "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat",
        "default_model": "ernie-4.0",
        "desc": "Baidu Ernie Bot foundation model",
    },
    "Tencent AI (Hunyuan)": {
        "base_url": "https://api.hunyuan.cloud.tencent.com/v1",
        "default_model": "hunyuan-pro",
        "desc": "Tencent Hunyuan large language model",
    },
    "Hugging Face": {
        "base_url": "https://api-inference.huggingface.co/v1",
        "default_model": "Qwen/Qwen2.5-72B-Instruct",
        "desc": "Open source hub serverless endpoints",
    },
    "Perplexity": {
        "base_url": "https://api.perplexity.ai",
        "default_model": "sonar-pro",
        "desc": "Online search-grounded citation models",
    },
    "NVIDIA NIM": {
        "base_url": "https://integrate.api.nvidia.com/v1",
        "default_model": "meta/llama-3.3-70b-instruct",
        "desc": "NVIDIA optimized NIM microservices",
    },
    "SambaNova Systems": {
        "base_url": "https://api.sambanova.ai/v1",
        "default_model": "Meta-Llama-3.3-70B-Instruct",
        "desc": "DataScale high speed chip inference",
    },
    "Nebius AI": {
        "base_url": "https://api.studio.nebius.ai/v1",
        "default_model": "meta-llama/Meta-Llama-3.1-70B-Instruct",
        "desc": "Cloud GPU infrastructure and token studio",
    },
    "Novita AI": {
        "base_url": "https://api.novita.ai/v3/openai",
        "default_model": "meta-llama/llama-3.3-70b-instruct",
        "desc": "Cost-effective open model API services",
    },
    "Lepton AI": {
        "base_url": "https://api.lepton.ai/v1",
        "default_model": "llama3-3-70b",
        "desc": "Cloud deployment platform for foundation models",
    },
    "OctoAI": {
        "base_url": "https://text.octoai.run/v1",
        "default_model": "meta-llama-3.1-70b-instruct",
        "desc": "OctoAI compute serverless inference",
    },
    "Anyscale": {
        "base_url": "https://api.endpoints.anyscale.com/v1",
        "default_model": "meta-llama/Meta-Llama-3-70B-Instruct",
        "desc": "Ray-powered fast production endpoints",
    },
    "AI21 Labs": {
        "base_url": "https://api.ai21.com/studio/v1",
        "default_model": "jamba-1.5-large",
        "desc": "Jamba SSM-Transformer hybrid models",
    },
    "Replicate": {
        "base_url": "https://api.replicate.com/v1",
        "default_model": "meta/meta-llama-3-70b-instruct",
        "desc": "Open-source models running in cloud containers",
    },
    "RunPod": {
        "base_url": "https://api.runpod.ai/v2",
        "default_model": "serverless-llama-3",
        "desc": "Serverless GPUs and custom endpoint APIs",
    },
    "Lambda Labs": {
        "base_url": "https://api.lambdalabs.com/v1",
        "default_model": "hermes-3-llama-3.1-405b",
        "desc": "High-performance GPU cloud model hosting",
    },
    "Vultr": {
        "base_url": "https://api.vultrinference.com/v1",
        "default_model": "llama2-13b-chat",
        "desc": "Global cloud serverless server API",
    },
    "CoreWeave": {
        "base_url": "https://api.coreweave.com/v1",
        "default_model": "llama-3-70b",
        "desc": "Specialized cloud GPU infrastructure",
    },
    "IBM (Watsonx)": {
        "base_url": "https://us-south.ml.cloud.ibm.com/ml/v1",
        "default_model": "ibm/granite-3-8b-instruct",
        "desc": "Enterprise IBM Granite and open models",
    },
    "Microsoft Azure AI": {
        "base_url": "https://your-resource.openai.azure.com/openai/deployments/your-deployment",
        "default_model": "gpt-4o",
        "desc": "Azure Foundry & OpenAI enterprise deployments",
    },
    "Amazon Bedrock": {
        "base_url": "https://bedrock-runtime.us-east-1.amazonaws.com",
        "default_model": "anthropic.claude-3-5-sonnet",
        "desc": "AWS managed foundation model service",
    },
    "ElevenLabs": {
        "base_url": "https://api.elevenlabs.io/v1",
        "default_model": "eleven_monolingual_v1",
        "desc": "Voice AI and audio synthesis API",
    },
    "Stability AI": {
        "base_url": "https://api.stability.ai/v1",
        "default_model": "stable-diffusion-v3",
        "desc": "Stable Diffusion text-to-image API",
    },
    "Runway": {
        "base_url": "https://api.runwayml.com/v1",
        "default_model": "gen-3-alpha",
        "desc": "AI video and motion generation API",
    },
    "Pika Labs": {
        "base_url": "https://api.pika.art/v1",
        "default_model": "pika-2.0",
        "desc": "Generative video effects and animation API",
    },
    "Midjourney (Proxy)": {
        "base_url": "https://api.midjourneyapi.xyz/mj/v2",
        "default_model": "midjourney-v6",
        "desc": "Midjourney generative imagery API gateway",
    },
    "Custom / Local (Ollama / vLLM)": {
        "base_url": "http://127.0.0.1:11434/v1",
        "default_model": "qwen2.5:latest",
        "desc": "Any custom OpenAI-compatible local server",
    },
}

DEFAULT_CONFIG = {
    "provider_name": "OpenRouter (Free & Multi)",
    "api_key": "",
    "model": "nvidia/nemotron-3.5-lightning:free",
    "base_url": "https://openrouter.ai/api/v1",
}


def load_config() -> dict:
    if CONFIG_FILE.is_file():
        try:
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            merged = dict(DEFAULT_CONFIG)
            merged.update(data)
            return merged
        except Exception:
            pass
    return dict(DEFAULT_CONFIG)


def save_config(data: dict):
    try:
        CONFIG_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
    except Exception:
        pass
