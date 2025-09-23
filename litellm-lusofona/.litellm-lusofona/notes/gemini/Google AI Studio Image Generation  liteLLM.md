---
title: "Google AI Studio Image Generation | liteLLM"
source: "https://docs.litellm.ai/docs/providers/google_ai_studio/image_gen"
author:
published:
created: 2025-09-23
description: "Google AI Studio provides powerful image generation capabilities using Google's Imagen models to create high-quality images from text descriptions."
tags:
  - "clippings"
---
Google AI Studio provides powerful image generation capabilities using Google's Imagen models to create high-quality images from text descriptions.

## Overview

| Property | Details |
| --- | --- |
| Description | Google AI Studio Image Generation uses Google's Imagen models to generate high-quality images from text descriptions. |
| Provider Route on LiteLLM | `gemini/` |
| Provider Doc | [Google AI Studio Image Generation ↗](https://ai.google.dev/gemini-api/docs/imagen) |
| Supported Operations | [`/images/generations`](https://docs.litellm.ai/docs/providers/google_ai_studio/#image-generation) |

## Setup

### API Key

```python
# Set your Google AI Studio API key
import os
os.environ["GEMINI_API_KEY"] = "your-api-key-here"
```

Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

## Image Generation

### Usage - LiteLLM Python SDK

### Usage - LiteLLM Proxy Server

#### 1\. Configure your config.yaml

```yaml
Google AI Studio Image Generation Configurationmodel_list:
  - model_name: google-imagen
    litellm_params:
      model: gemini/imagen-4.0-generate-001
      api_key: os.environ/GEMINI_API_KEY
  model_info:
    mode: image_generation

general_settings:
  master_key: sk-1234
```

#### 2\. Start LiteLLM Proxy Server

```bash
Start LiteLLM Proxy Serverlitellm --config /path/to/config.yaml

# RUNNING on http://0.0.0.0:4000
```

#### 3\. Make requests with OpenAI Python SDK

## Supported Parameters

Google AI Studio Image Generation supports the following OpenAI-compatible parameters:

| Parameter | Type | Description | Default | Example |
| --- | --- | --- | --- | --- |
| `prompt` | string | Text description of the image to generate | Required | `"A sunset over the ocean"` |
| `model` | string | The model to use for generation | Required | `"gemini/imagen-4.0-generate-001"` |
| `n` | integer | Number of images to generate (1-4) | `1` | `2` |
| `size` | string | Image dimensions | `"1024x1024"` | `"512x512"`, `"1024x1024"` |

1. Create an account at [Google AI Studio](https://aistudio.google.com/)
2. Generate an API key from [API Keys section](https://aistudio.google.com/app/apikey)
3. Set your `GEMINI_API_KEY` environment variable
4. Start generating images using LiteLLM

## Additional Resources

- [Google AI Studio Documentation](https://ai.google.dev/gemini-api/docs)
- [Imagen Model Overview](https://ai.google.dev/gemini-api/docs/imagen)
- [LiteLLM Image Generation Guide](https://docs.litellm.ai/docs/completion/image_generation)