---
title: "Gemini - Google AI Studio | liteLLM"
source: "https://docs.litellm.ai/docs/providers/gemini"
author:
published:
created: 2025-09-23
description: "| Property | Details |"
tags:
  - "clippings"
---
| Property | Details |
| --- | --- |
| Description | Google AI Studio is a fully-managed AI development platform for building and using generative AI. |
| Provider Route on LiteLLM | `gemini/` |
| Provider Doc | [Google AI Studio ↗](https://aistudio.google.com/) |
| API Endpoint for Provider | [https://generativelanguage.googleapis.com](https://generativelanguage.googleapis.com/) |
| Supported OpenAI Endpoints | `/chat/completions`, [`/embeddings`](https://docs.litellm.ai/docs/embedding/supported_embedding#gemini-ai-embedding-models), `/completions` |
| Pass-through Endpoint | [Supported](https://docs.litellm.ai/docs/pass_through/google_ai_studio) |

  

## API Keys

```python
import os
os.environ["GEMINI_API_KEY"] = "your-api-key"
```

## Sample Usage

```python
from litellm import completion
import os

os.environ['GEMINI_API_KEY'] = ""
response = completion(
    model="gemini/gemini-pro", 
    messages=[{"role": "user", "content": "write code for saying hi from LiteLLM"}]
)
```

## Supported OpenAI Params

- temperature
- top\_p
- max\_tokens
- max\_completion\_tokens
- stream
- tools
- tool\_choice
- functions
- response\_format
- n
- stop
- logprobs
- frequency\_penalty
- modalities
- reasoning\_content
- audio (for TTS models only)

**Anthropic Params**

- thinking (used to set max budget tokens across anthropic/gemini models)

[**See Updated List**](https://github.com/BerriAI/litellm/blob/main/litellm/llms/gemini/chat/transformation.py#L70)

## Usage - Thinking / reasoning\_content

LiteLLM translates OpenAI's `reasoning_effort` to Gemini's `thinking` parameter. [Code](https://github.com/BerriAI/litellm/blob/620664921902d7a9bfb29897a7b27c1a7ef4ddfb/litellm/llms/vertex_ai/gemini/vertex_and_google_ai_studio_gemini.py#L362)

Added an additional non-OpenAI standard "disable" value for non-reasoning Gemini requests.

**Mapping**

| reasoning\_effort | thinking |
| --- | --- |
| "disable" | "budget\_tokens": 0 |
| "low" | "budget\_tokens": 1024 |
| "medium" | "budget\_tokens": 2048 |
| "high" | "budget\_tokens": 4096 |

**Expected Response**

```python
ModelResponse(
    id='chatcmpl-c542d76d-f675-4e87-8e5f-05855f5d0f5e',
    created=1740470510,
    model='claude-3-7-sonnet-20250219',
    object='chat.completion',
    system_fingerprint=None,
    choices=[
        Choices(
            finish_reason='stop',
            index=0,
            message=Message(
                content="The capital of France is Paris.",
                role='assistant',
                tool_calls=None,
                function_call=None,
                reasoning_content='The capital of France is Paris. This is a very straightforward factual question.'
            ),
        )
    ],
    usage=Usage(
        completion_tokens=68,
        prompt_tokens=42,
        total_tokens=110,
        completion_tokens_details=None,
        prompt_tokens_details=PromptTokensDetailsWrapper(
            audio_tokens=None,
            cached_tokens=0,
            text_tokens=None,
            image_tokens=None
        ),
        cache_creation_input_tokens=0,
        cache_read_input_tokens=0
    )
)
```

### Pass thinking to Gemini models

You can also pass the `thinking` parameter to Gemini models.

This is translated to Gemini's [`thinkingConfig` parameter](https://ai.google.dev/gemini-api/docs/thinking#set-budget).

## Text-to-Speech (TTS) Audio Output

### Supported Models

LiteLLM supports Gemini TTS models with audio capabilities (e.g. `gemini-2.5-flash-preview-tts` and `gemini-2.5-pro-preview-tts`). For the complete list of available TTS models and voices, see the [official Gemini TTS documentation](https://ai.google.dev/gemini-api/docs/speech-generation).

### Limitations

### Quick Start

### Advanced Usage

You can combine TTS with other Gemini features:

For more information about Gemini's TTS capabilities and available voices, see the [official Gemini TTS documentation](https://ai.google.dev/gemini-api/docs/speech-generation).

## Passing Gemini Specific Params

### Response schema

LiteLLM supports sending `response_schema` as a param for Gemini-1.5-Pro on Google AI Studio.

**Response Schema**

**Validate Schema**

To validate the response\_schema, set `enforce_validation: true`.

LiteLLM will validate the response against the schema, and raise a `JSONSchemaValidationError` if the response does not match the schema.

JSONSchemaValidationError inherits from `openai.APIError`

Access the raw response with `e.raw_response`

### GenerationConfig Params

To pass additional GenerationConfig params - e.g. `topK`, just pass it in the request body of the call, and LiteLLM will pass it straight through as a key-value pair in the request body.

[**See Gemini GenerationConfigParams**](https://ai.google.dev/api/generate-content#v1beta.GenerationConfig)

**Validate Schema**

To validate the response\_schema, set `enforce_validation: true`.

## Specifying Safety Settings

In certain use-cases you may need to make calls to the models and pass [safety settings](https://ai.google.dev/docs/safety_setting_gemini) different from the defaults. To do so, simple pass the `safety_settings` argument to `completion` or `acompletion`. For example:

```python
response = completion(
    model="gemini/gemini-pro", 
    messages=[{"role": "user", "content": "write code for saying hi from LiteLLM"}],
    safety_settings=[
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE",
        },
    ]
)
```

## Tool Calling

```python
from litellm import completion
import os
# set env
os.environ["GEMINI_API_KEY"] = ".."

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        },
    }
]
messages = [{"role": "user", "content": "What's the weather like in Boston today?"}]

response = completion(
    model="gemini/gemini-1.5-flash",
    messages=messages,
    tools=tools,
)
# Add any assertions, here to check response args
print(response)
assert isinstance(response.choices[0].message.tool_calls[0].function.name, str)
assert isinstance(
    response.choices[0].message.tool_calls[0].function.arguments, str
)
```

### URL Context

### Code Execution Tool

## JSON Mode

## Gemini-Pro-Vision

LiteLLM Supports the following image types passed in `url`

- Images with direct links - [https://storage.googleapis.com/github-repo/img/gemini/intro/landmark3.jpg](https://storage.googleapis.com/github-repo/img/gemini/intro/landmark3.jpg)
- Image in local storage -./localimage.jpeg

## Sample Usage

```python
import os
import litellm
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()
os.environ["GEMINI_API_KEY"] = os.getenv('GEMINI_API_KEY')

prompt = 'Describe the image in a few sentences.'
# Note: You can pass here the URL or Path of image directly.
image_url = 'https://storage.googleapis.com/github-repo/img/gemini/intro/landmark3.jpg'

# Create the messages payload according to the documentation
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": prompt
            },
            {
                "type": "image_url",
                "image_url": {"url": image_url}
            }
        ]
    }
]

# Make the API call to Gemini model
response = litellm.completion(
    model="gemini/gemini-pro-vision",
    messages=messages,
)

# Extract the response content
content = response.get('choices', [{}])[0].get('message', {}).get('content')

# Print the result
print(content)
```

## Usage - PDF / Videos / etc. Files

### Inline Data (e.g. audio stream)

LiteLLM follows the OpenAI format and accepts sending inline data as an encoded base64 string.

The format to follow is

```python
data:<mime_type>;base64,<encoded_data>
```

\*\* LITELLM CALL \*\*

```python
import litellm
from pathlib import Path
import base64
import os

os.environ["GEMINI_API_KEY"] = "" 

litellm.set_verbose = True # 👈 See Raw call 

audio_bytes = Path("speech_vertex.mp3").read_bytes()
encoded_data = base64.b64encode(audio_bytes).decode("utf-8")
print("Audio Bytes = {}".format(audio_bytes))
model = "gemini/gemini-1.5-flash"
response = litellm.completion(
    model=model,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Please summarize the audio."},
                {
                    "type": "file",
                    "file": {
                        "file_data": "data:audio/mp3;base64,{}".format(encoded_data), # 👈 SET MIME_TYPE + DATA
                    }
                },
            ],
        }
    ],
)
```

\*\* Equivalent GOOGLE API CALL \*\*

```python
# Initialize a Gemini model appropriate for your use case.
model = genai.GenerativeModel('models/gemini-1.5-flash')

# Create the prompt.
prompt = "Please summarize the audio."

# Load the samplesmall.mp3 file into a Python Blob object containing the audio
# file's bytes and then pass the prompt and the audio to Gemini.
response = model.generate_content([
    prompt,
    {
        "mime_type": "audio/mp3",
        "data": pathlib.Path('samplesmall.mp3').read_bytes()
    }
])

# Output Gemini's response to the prompt and the inline audio.
print(response.text)
```

### https:// file

```python
import litellm
import os

os.environ["GEMINI_API_KEY"] = "" 

litellm.set_verbose = True # 👈 See Raw call 

model = "gemini/gemini-1.5-flash"
response = litellm.completion(
    model=model,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Please summarize the file."},
                {
                    "type": "file",
                    "file": {
                        "file_id": "https://storage...", # 👈 SET THE IMG URL
                        "format": "application/pdf" # OPTIONAL
                    }
                },
            ],
        }
    ],
)
```

### gs:// file

```python
import litellm
import os

os.environ["GEMINI_API_KEY"] = "" 

litellm.set_verbose = True # 👈 See Raw call 

model = "gemini/gemini-1.5-flash"
response = litellm.completion(
    model=model,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Please summarize the file."},
                {
                    "type": "file",
                    "file": {
                        "file_id": "gs://storage...", # 👈 SET THE IMG URL
                        "format": "application/pdf" # OPTIONAL
                    }
                },
            ],
        }
    ],
)
```

## Chat Models

| Model Name | Function Call | Required OS Variables |
| --- | --- | --- |
| gemini-pro | `completion(model='gemini/gemini-pro', messages)` | `os.environ['GEMINI_API_KEY']` |
| gemini-1.5-pro-latest | `completion(model='gemini/gemini-1.5-pro-latest', messages)` | `os.environ['GEMINI_API_KEY']` |
| gemini-2.0-flash | `completion(model='gemini/gemini-2.0-flash', messages)` | `os.environ['GEMINI_API_KEY']` |
| gemini-2.0-flash-exp | `completion(model='gemini/gemini-2.0-flash-exp', messages)` | `os.environ['GEMINI_API_KEY']` |
| gemini-2.0-flash-lite-preview-02-05 | `completion(model='gemini/gemini-2.0-flash-lite-preview-02-05', messages)` | `os.environ['GEMINI_API_KEY']` |

## Context Caching

Use Google AI Studio context caching is supported by

```bash
{
    {
        "role": "system",
        "content": ...,
        "cache_control": {"type": "ephemeral"} # 👈 KEY CHANGE
    },
    ...
}
```

in your message content block.

### Custom TTL Support

You can now specify a custom Time-To-Live (TTL) for your cached content using the `ttl` parameter:

```bash
{
    {
        "role": "system",
        "content": ...,
        "cache_control": {
            "type": "ephemeral",
            "ttl": "3600s"  # 👈 Cache for 1 hour
        }
    },
    ...
}
```

**TTL Format Requirements:**

- Must be a string ending with 's' for seconds
- Must contain a positive number (can be decimal)
- Examples: `"3600s"` (1 hour), `"7200s"` (2 hours), `"1800s"` (30 minutes), `"1.5s"` (1.5 seconds)

**TTL Behavior:**

- If multiple cached messages have different TTLs, the first valid TTL encountered will be used
- Invalid TTL formats are ignored and the cache will use Google's default expiration time
- If no TTL is specified, Google's default cache expiration (approximately 1 hour) applies

### Architecture Diagram

![](https://docs.litellm.ai/assets/ideal-img/gemini_context_caching.1d6e4bf.1884.png)

**Notes:**

- [Relevant code](https://github.com/BerriAI/litellm/blob/main/litellm/llms/vertex_ai/context_caching/vertex_ai_context_caching.py#L255)
- Gemini Context Caching only allows 1 block of continuous messages to be cached.
- If multiple non-continuous blocks contain `cache_control` - the first continuous block will be used. (sent to `/cachedContent` in the [Gemini format](https://ai.google.dev/api/caching#cache_create-SHELL))
- The raw request to Gemini's `/generateContent` endpoint looks like this:
```bash
curl -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-001:generateContent?key=$GOOGLE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
      "contents": [
        {
          "parts":[{
            "text": "Please summarize this transcript"
          }],
          "role": "user"
        },
      ],
      "cachedContent": "'$CACHE_NAME'"
    }'
```