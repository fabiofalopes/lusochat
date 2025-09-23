---
title: "Gemini models  |  Gemini API  |  Google AI for Developers"
source: "https://ai.google.dev/gemini-api/docs/models#gemini-2.5-pro"
author:
published:
created: 2025-09-23
description: "Learn about Google's most advanced AI models including Gemini 2.5 Pro"
tags:
  - "clippings"
---
## Model variants

The Gemini API offers different models that are optimized for specific use cases. Here's a brief overview of Gemini variants that are available:

| Model variant | Input(s) | Output | Optimized for |
| --- | --- | --- | --- |
| [Gemini 2.5 Pro](https://ai.google.dev/gemini-api/docs/#gemini-2.5-pro)   `gemini-2.5-pro` | Audio, images, videos, text, and PDF | Text | Enhanced thinking and reasoning, multimodal understanding, advanced coding, and more |
| [Gemini 2.5 Flash](https://ai.google.dev/gemini-api/docs/#gemini-2.5-flash)   `gemini-2.5-flash` | Audio, images, videos, and text | Text | Adaptive thinking, cost efficiency |
| [Gemini 2.5 Flash-Lite](https://ai.google.dev/gemini-api/docs/#gemini-2.5-flash-lite)   `gemini-2.5-flash-lite` | Text, image, video, audio | Text | Most cost-efficient model supporting high throughput |
| [Gemini 2.5 Flash Live](https://ai.google.dev/gemini-api/docs/#live-api)   `gemini-live-2.5-flash-preview` | Audio, video, and text | Text, audio | Low-latency bidirectional voice and video interactions |
| [Gemini 2.5 Flash Native Audio](https://ai.google.dev/gemini-api/docs/#gemini-2.5-flash-native-audio)   `gemini-2.5-flash-native-audio-preview-09-2025` &   `gemini-2.5-flash-exp-native-audio-thinking-dialog` | Audio, videos, and text | Text and audio, interleaved | High quality, natural conversational audio outputs, with or without thinking |
| [Gemini 2.5 Flash Image Preview](https://ai.google.dev/gemini-api/docs/#gemini-2.5-flash-image-preview)   `gemini-2.5-flash-image-preview` | Images and text | Images and text | Precise, conversational image generation and editing |
| [Gemini 2.5 Flash Preview TTS](https://ai.google.dev/gemini-api/docs/#gemini-2.5-flash-preview-tts)   `gemini-2.5-flash-preview-tts` | Text | Audio | Low latency, controllable, single- and multi-speaker text-to-speech audio generation |
| [Gemini 2.5 Pro Preview TTS](https://ai.google.dev/gemini-api/docs/#gemini-2.5-pro-preview-tts)   `gemini-2.5-pro-preview-tts` | Text | Audio | Low latency, controllable, single- and multi-speaker text-to-speech audio generation |
| [Gemini 2.0 Flash](https://ai.google.dev/gemini-api/docs/#gemini-2.0-flash)   `gemini-2.0-flash` | Audio, images, videos, and text | Text | Next generation features, speed, and realtime streaming. |
| [Gemini 2.0 Flash Preview Image Generation](https://ai.google.dev/gemini-api/docs/#gemini-2.0-flash-preview-image-generation)   `gemini-2.0-flash-preview-image-generation` | Audio, images, videos, and text | Text, images | Conversational image generation and editing |
| [Gemini 2.0 Flash-Lite](https://ai.google.dev/gemini-api/docs/#gemini-2.0-flash-lite)   `gemini-2.0-flash-lite` | Audio, images, videos, and text | Text | Cost efficiency and low latency |
| [Gemini 2.0 Flash Live](https://ai.google.dev/gemini-api/docs/#live-api-2.0)   `gemini-2.0-flash-live-001` | Audio, video, and text | Text, audio | Low-latency bidirectional voice and video interactions |
| [Gemini 1.5 Flash](https://ai.google.dev/gemini-api/docs/#gemini-1.5-flash)   `gemini-1.5-flash` | Audio, images, videos, and text | Text | Fast and versatile performance across a diverse variety of tasks   Deprecated |
| [Gemini 1.5 Flash-8B](https://ai.google.dev/gemini-api/docs/#gemini-1.5-flash-8b)   `gemini-1.5-flash-8b` | Audio, images, videos, and text | Text | High volume and lower intelligence tasks   Deprecated |
| [Gemini 1.5 Pro](https://ai.google.dev/gemini-api/docs/#gemini-1.5-pro)   `gemini-1.5-pro` | Audio, images, videos, and text | Text | Complex reasoning tasks requiring more intelligence   Deprecated |

You can view the rate limits for each model on the [rate limits page](https://ai.google.dev/gemini-api/docs/rate-limits).

### Gemini 2.5 Pro

Gemini 2.5 Pro is our state-of-the-art thinking model, capable of reasoning over complex problems in code, math, and STEM, as well as analyzing large datasets, codebases, and documents using long context.

[Try in Google AI Studio](https://aistudio.google.com/?model=gemini-2.5-pro)

#### Model details

| Property | Description |
| --- | --- |
| Model code | `gemini-2.5-pro` |
| Supported data types | **Inputs**  Audio, images, video, text, and PDF  **Output**  Text |
| Token limits <sup><a href="https://ai.google.dev/gemini-api/docs/#token-size">[*]</a></sup> | **Input token limit**  1,048,576  **Output token limit**  65,536 |
| Capabilities | **Audio generation**  Not supported  **Batch API**  Supported  **Caching**  Supported  **Code execution**  Supported  **Function calling**  Supported  **Image generation**  Not supported  **Live API**  Not supported  **Search grounding**  Supported  **Structured outputs**  Supported  **Thinking**  Supported  **URL context**  Supported |
| Versions | Read the [model version patterns](https://ai.google.dev/gemini-api/docs/models/gemini#model-versions) for more details. - `Stable: gemini-2.5-pro` |
| Latest update | June 2025 |
| Knowledge cutoff | January 2025 |

### Gemini 2.5 Flash

Our best model in terms of price-performance, offering well-rounded capabilities. 2.5 Flash is best for large scale processing, low-latency, high volume tasks that require thinking, and agentic use cases.

[Try in Google AI Studio](https://aistudio.google.com/?model=gemini-2.5-flash)

#### Model details

| Property | Description |
| --- | --- |
| Model code | `gemini-2.5-flash` |
| Supported data types | **Inputs**  Text, images, video, audio  **Output**  Text |
| Token limits <sup><a href="https://ai.google.dev/gemini-api/docs/#token-size">[*]</a></sup> | **Input token limit**  1,048,576  **Output token limit**  65,536 |
| Capabilities | **Audio generation**  Not supported  **Batch API**  Supported  **Caching**  Supported  **Code execution**  Supported  **Function calling**  Supported  **Image generation**  Not supported  **Live API**  Not supported  **Search grounding**  Supported  **Structured outputs**  Supported  **Thinking**  Supported  **URL context**  Supported |
| Versions | Read the [model version patterns](https://ai.google.dev/gemini-api/docs/models/gemini#model-versions) for more details. - Stable: `gemini-2.5-flash` - Preview: `gemini-2.5-flash-preview-05-20` |
| Latest update | June 2025 |
| Knowledge cutoff | January 2025 |

### Gemini 2.5 Flash-Lite

A Gemini 2.5 Flash model optimized for cost-efficiency and high throughput.

[Try in Google AI Studio](https://aistudio.google.com/?model=gemini-2.5-flash-lite)

#### Model details

| Property | Description |
| --- | --- |
| Model code | `gemini-2.5-flash-lite` |
| Supported data types | **Inputs**  Text, image, video, audio, PDF  **Output**  Text |
| Token limits <sup><a href="https://ai.google.dev/gemini-api/docs/#token-size">[*]</a></sup> | **Input token limit**  1,048,576  **Output token limit**  65,536 |
| Capabilities | **Audio generation**  Not supported  **Batch API**  Supported  **Caching**  Supported  **Code execution**  Supported  **Function calling**  Supported  **Image generation**  Not supported  **Live API**  Not supported  **Search grounding**  Supported  **Structured outputs**  Supported  **Thinking**  Supported  **URL context**  Supported |
| Versions | Read the [model version patterns](https://ai.google.dev/gemini-api/docs/models/gemini#model-versions) for more details. - Stable: `gemini-2.5-flash-lite` - Preview: `gemini-2.5-flash-lite-06-17` |
| Latest update | July 2025 |
| Knowledge cutoff | January 2025 |

### Gemini 2.5 Flash Live

The Gemini 2.5 Flash Live model works with the Live API to enable low-latency bidirectional voice and video interactions with Gemini. The model can process text, audio, and video input, and it can provide text and audio output.

[Try in Google AI Studio](https://aistudio.google.com/?model=gemini-live-2.5-flash-preview)

#### Model details

| Property | Description |
| --- | --- |
| Model code | `gemini-live-2.5-flash-preview` |
| Supported data types | **Inputs**  Audio, video, and text  **Output**  Text, and audio |
| Token limits <sup><a href="https://ai.google.dev/gemini-api/docs/#token-size">[*]</a></sup> | **Input token limit**  1,048,576  **Output token limit**  8,192 |
| Capabilities | **Audio generation**  Supported  **Batch API**  Not supported  **Caching**  Not supported  **Code execution**  Supported  **Function calling**  Supported  **Image generation**  Not supported  **Live API**  Supported  **Search grounding**  Supported  **Structured outputs**  Supported  **Thinking**  Not supported  **URL context**  Supported |
| Versions | Read the [model version patterns](https://ai.google.dev/gemini-api/docs/models/gemini#model-versions) for more details. - Preview: `gemini-live-2.5-flash-preview` |
| Latest update | June 2025 |
| Knowledge cutoff | January 2025 |

### Gemini 2.5 Flash Native Audio

Our native audio dialog models, with and without thinking, available through the [Live API](https://ai.google.dev/gemini-api/docs/live). These models provide interactive and unstructured conversational experiences, with style and control prompting.

[Try native audio in Google AI Studio](https://aistudio.google.com/app/live)

#### Model details

| Property | Description |
| --- | --- |
| Model code | `gemini-2.5-flash-native-audio-preview-09-2025` &   `gemini-2.5-flash-exp-native-audio-thinking-dialog` |
| Supported data types | **Inputs**  Audio, video, text  **Output**  Audio and text |
| Token limits <sup><a href="https://ai.google.dev/gemini-api/docs/#token-size">[*]</a></sup> | **Input token limit**  128,000  **Output token limit**  8,000 |
| Capabilities | **Audio generation**  Supported  **Batch API**  Not supported  **Caching**  Not supported  **Code execution**  Not supported  **Function calling**  Supported  **Image generation**  Not supported  **Live API**  Supported  **Search grounding**  Supported  **Structured outputs**  Not supported  **Thinking**  Supported  **URL context**  Not supported |
| Versions | Read the [model version patterns](https://ai.google.dev/gemini-api/docs/models/gemini#model-versions) for more details. - Preview: `gemini-2.5-flash-native-audio-preview-09-2025` - Preview: `gemini-2.5-flash-preview-native-audio-dialog` - Preview: `gemini-2.5-flash-preview-05-20` - Experimental: `gemini-2.5-flash-exp-native-audio-thinking-dialog` |
| Latest update | September 2025 |
| Knowledge cutoff | January 2025 |

### Gemini 2.5 Flash Image Preview

Gemini 2.5 Flash Image Preview is our latest, fastest, and most efficient natively multimodal model that lets you generate and edit images conversationally.

[Try in Google AI Studio](https://aistudio.google.com/?model=gemini-2.5-flash-image-preview)

#### Model details

| Property | Description |
| --- | --- |
| Model code | `gemini-2.5-flash-image-preview` |
| Supported data types | **Inputs**  Images and text  **Output**  Images and text |
| Token limits <sup><a href="https://ai.google.dev/gemini-api/docs/#token-size">[*]</a></sup> | **Input token limit**  32,768  **Output token limit**  32,768 |
| Capabilities | **Audio generation**  Not supported  **Batch API**  Supported  **Caching**  Supported  **Code execution**  Not Supported  **Function calling**  Not supported  **Image generation**  Supported  **Live API**  Not Supported  **Search grounding**  Not Supported  **Structured outputs**  Supported  **Thinking**  Not Supported  **URL context**  Not supported |
| Versions | Read the [model version patterns](https://ai.google.dev/gemini-api/docs/models/gemini#model-versions) for more details. - Preview: `gemini-2.5-flash-image-preview` |
| Latest update | August 2025 |
| Knowledge cutoff | June 2025 |

### Gemini 2.5 Flash Preview Text-to-Speech

Gemini 2.5 Flash Preview TTS is our price-performant text-to-speech model, delivering high control and transparency for structured workflows like podcast generation, audiobooks, customer support, and more. Gemini 2.5 Flash rate limits are more restricted since it is an experimental / preview model.

[Try in Google AI Studio](https://aistudio.google.com/generate-speech)

#### Model details

| Property | Description |
| --- | --- |
| Model code | `gemini-2.5-flash-preview-tts` |
| Supported data types | **Inputs**  Text  **Output**  Audio |
| Token limits <sup><a href="https://ai.google.dev/gemini-api/docs/#token-size">[*]</a></sup> | **Input token limit**  8,000  **Output token limit**  16,000 |
| Capabilities | **Audio generation**  Supported  **Batch API**  Supported  **Caching**  Not supported  **Code execution**  Not supported  **Function calling**  Not supported  **Image generation**  Not supported  **Live API**  Not supported  **Search grounding**  Not supported  **Structured outputs**  Not supported  **Thinking**  Not supported  **URL context**  Not supported |
| Versions | Read the [model version patterns](https://ai.google.dev/gemini-api/docs/models/gemini#model-versions) for more details. - `gemini-2.5-flash-preview-tts` |
| Latest update | May 2025 |

### Gemini 2.5 Pro Preview Text-to-Speech

Gemini 2.5 Pro Preview TTS is our most powerful text-to-speech model, delivering high control and transparency for structured workflows like podcast generation, audiobooks, customer support, and more. Gemini 2.5 Pro rate limits are more restricted since it is an experimental / preview model.

[Try in Google AI Studio](https://aistudio.google.com/generate-speech)

#### Model details

| Property | Description |
| --- | --- |
| Model code | `gemini-2.5-pro-preview-tts` |
| Supported data types | **Inputs**  Text  **Output**  Audio |
| Token limits <sup><a href="https://ai.google.dev/gemini-api/docs/#token-size">[*]</a></sup> | **Input token limit**  8,000  **Output token limit**  16,000 |
| Capabilities | **Audio generation**  Supported  **Batch API**  Supported  **Caching**  Not supported  **Code execution**  Not supported  **Function calling**  Not supported  **Image generation**  Not supported  **Live API**  Not supported  **Search grounding**  Not supported  **Structured outputs**  Not supported  **Thinking**  Not supported  **URL context**  Not supported |
| Versions | Read the [model version patterns](https://ai.google.dev/gemini-api/docs/models/gemini#model-versions) for more details. - `gemini-2.5-pro-preview-tts` |
| Latest update | May 2025 |

### Gemini 2.0 Flash

Gemini 2.0 Flash delivers next-gen features and improved capabilities, including superior speed, native tool use, and a 1M token context window.

[Try in Google AI Studio](https://aistudio.google.com/?model=gemini-2.0-flash-001)

#### Model details

| Property | Description |
| --- | --- |
| Model code | `gemini-2.0-flash` |
| Supported data types | **Inputs**  Audio, images, video, and text  **Output**  Text |
| Token limits <sup><a href="https://ai.google.dev/gemini-api/docs/#token-size">[*]</a></sup> | **Input token limit**  1,048,576  **Output token limit**  8,192 |
| Capabilities | **Audio generation**  Not supported  **Batch API**  Supported  **Caching**  Supported  **Code execution**  Supported  **Function calling**  Supported  **Image generation**  Not supported  **Live API**  Supported  **Search grounding**  Supported  **Structured outputs**  Supported  **Thinking**  Experimental  **URL context**  Not supported |
| Versions | Read the [model version patterns](https://ai.google.dev/gemini-api/docs/models/gemini#model-versions) for more details. - Latest: `gemini-2.0-flash` - Stable: `gemini-2.0-flash-001` - Experimental: `gemini-2.0-flash-exp` |
| Latest update | February 2025 |
| Knowledge cutoff | August 2024 |

### Gemini 2.0 Flash Preview Image Generation

Gemini 2.0 Flash Preview Image Generation delivers improved image generation features, including generating and editing images conversationally.

[Try in Google AI Studio](https://aistudio.google.com/?model=gemini-2.0-flash-preview-image-generation)

#### Model details

| Property | Description |
| --- | --- |
| Model code | `gemini-2.0-flash-preview-image-generation` |
| Supported data types | **Inputs**  Audio, images, video, and text  **Output**  Text and images |
| Token limits <sup><a href="https://ai.google.dev/gemini-api/docs/#token-size">[*]</a></sup> | **Input token limit**  32,000  **Output token limit**  8,192 |
| Capabilities | **Audio generation**  Not supported  **Batch API**  Supported  **Caching**  Supported  **Code execution**  Not Supported  **Function calling**  Not supported  **Image generation**  Supported  **Live API**  Not Supported  **Search grounding**  Not Supported  **Structured outputs**  Supported  **Thinking**  Not Supported  **URL context**  Not supported |
| Versions | Read the [model version patterns](https://ai.google.dev/gemini-api/docs/models/gemini#model-versions) for more details. - Preview: `gemini-2.0-flash-preview-image-generation`  gemini-2.0-flash-preview-image-generation is not currently supported in a number of countries in Europe, Middle East & Africa |
| Latest update | May 2025 |
| Knowledge cutoff | August 2024 |

### Gemini 2.0 Flash-Lite

A Gemini 2.0 Flash model optimized for cost efficiency and low latency.

[Try in Google AI Studio](https://aistudio.google.com/?model=gemini-2.0-flash-lite)

#### Model details

| Property | Description |
| --- | --- |
| Model code | `gemini-2.0-flash-lite` |
| Supported data types | **Inputs**  Audio, images, video, and text  **Output**  Text |
| Token limits <sup><a href="https://ai.google.dev/gemini-api/docs/#token-size">[*]</a></sup> | **Input token limit**  1,048,576  **Output token limit**  8,192 |
| Capabilities | **Audio generation**  Not supported  **Batch API**  Supported  **Caching**  Supported  **Code execution**  Not supported  **Function calling**  Supported  **Image generation**  Not supported  **Live API**  Not supported  **Search grounding**  Not supported  **Structured outputs**  Supported  **Thinking**  Not Supported  **URL context**  Not supported |
| Versions | Read the [model version patterns](https://ai.google.dev/gemini-api/docs/models/gemini#model-versions) for more details. - Latest: `gemini-2.0-flash-lite` - Stable: `gemini-2.0-flash-lite-001` |
| Latest update | February 2025 |
| Knowledge cutoff | August 2024 |

### Gemini 2.0 Flash Live

The Gemini 2.0 Flash Live model works with the Live API to enable low-latency bidirectional voice and video interactions with Gemini. The model can process text, audio, and video input, and it can provide text and audio output.

[Try in Google AI Studio](https://aistudio.google.com/?model=gemini-2.0-flash-live-001)

#### Model details

| Property | Description |
| --- | --- |
| Model code | `gemini-2.0-flash-live-001` |
| Supported data types | **Inputs**  Audio, video, and text  **Output**  Text, and audio |
| Token limits <sup><a href="https://ai.google.dev/gemini-api/docs/#token-size">[*]</a></sup> | **Input token limit**  1,048,576  **Output token limit**  8,192 |
| Capabilities | **Audio generation**  Supported  **Batch API**  Not supported  **Caching**  Not supported  **Code execution**  Supported  **Function calling**  Supported  **Image generation**  Not supported  **Live API**  Supported  **Search grounding**  Supported  **Structured outputs**  Supported  **Thinking**  Not supported  **URL context**  Supported |
| Versions | Read the [model version patterns](https://ai.google.dev/gemini-api/docs/models/gemini#model-versions) for more details. - Preview: `gemini-2.0-flash-live-001` |
| Latest update | April 2025 |
| Knowledge cutoff | August 2024 |

### Gemini 1.5 Flash

Gemini 1.5 Flash is a fast and versatile multimodal model for scaling across diverse tasks.

#### Model details

| Property | Description |
| --- | --- |
| Model code | `gemini-1.5-flash` |
| Supported data types | **Inputs**  Audio, images, video, and text  **Output**  Text |
| Token limits <sup><a href="https://ai.google.dev/gemini-api/docs/#token-size">[*]</a></sup> | **Input token limit**  1,048,576  **Output token limit**  8,192 |
| Audio/visual specs | **Maximum number of images per prompt**  3,600  **Maximum video length**  1 hour  **Maximum audio length**  Approximately 9.5 hours |
| Capabilities | **Adjustable safety settings**  Supported  **Caching**  Supported  **Code execution**  Supported  **Function calling**  Supported  **JSON mode**  Supported  **JSON schema**  Supported  **Live API**  Not supported  **System instructions**  Supported  **Tuning**  Supported |
| Versions | Read the [model version patterns](https://ai.google.dev/gemini-api/docs/models/gemini#model-versions) for more details. - Latest: `gemini-1.5-flash-latest` - Latest stable: `gemini-1.5-flash` - Stable: - `gemini-1.5-flash-001` 	- `gemini-1.5-flash-002` |
| Deprecation date | September 2025 |
| Latest update | September 2024 |

### Gemini 1.5 Flash-8B

Gemini 1.5 Flash-8B is a small model designed for lower intelligence tasks.

#### Model details

| Property | Description |
| --- | --- |
| Model code | `gemini-1.5-flash-8b` |
| Supported data types | **Inputs**  Audio, images, video, and text  **Output**  Text |
| Token limits <sup><a href="https://ai.google.dev/gemini-api/docs/#token-size">[*]</a></sup> | **Input token limit**  1,048,576  **Output token limit**  8,192 |
| Audio/visual specs | **Maximum number of images per prompt**  3,600  **Maximum video length**  1 hour  **Maximum audio length**  Approximately 9.5 hours |
| Capabilities | **Adjustable safety settings**  Supported  **Caching**  Supported  **Code execution**  Supported  **Function calling**  Supported  **JSON mode**  Supported  **JSON schema**  Supported  **Live API**  Not supported  **System instructions**  Supported  **Tuning**  Supported |
| Versions | Read the [model version patterns](https://ai.google.dev/gemini-api/docs/models/gemini#model-versions) for more details. - Latest: `gemini-1.5-flash-8b-latest` - Latest stable: `gemini-1.5-flash-8b` - Stable: - `gemini-1.5-flash-8b-001` |
| Deprecation date | September 2025 |
| Latest update | October 2024 |

### Gemini 1.5 Pro

Try [Gemini 2.5 Pro Preview](https://ai.google.dev/gemini-api/docs/models/experimental-models#available-models), our most advanced Gemini model to date.

Gemini 1.5 Pro is a mid-size multimodal model that is optimized for a wide-range of reasoning tasks. 1.5 Pro can process large amounts of data at once, including 2 hours of video, 19 hours of audio, codebases with 60,000 lines of code, or 2,000 pages of text.

#### Model details

| Property | Description |
| --- | --- |
| Model code | `gemini-1.5-pro` |
| Supported data types | **Inputs**  Audio, images, video, and text  **Output**  Text |
| Token limits <sup><a href="https://ai.google.dev/gemini-api/docs/#token-size">[*]</a></sup> | **Input token limit**  2,097,152  **Output token limit**  8,192 |
| Audio/visual specs | **Maximum number of images per prompt**  7,200  **Maximum video length**  2 hours  **Maximum audio length**  Approximately 19 hours |
| Capabilities | **Adjustable safety settings**  Supported  **Caching**  Supported  **Code execution**  Supported  **Function calling**  Supported  **JSON mode**  Supported  **JSON schema**  Supported  **Live API**  Not supported  **System instructions**  Supported  **Tuning**  Not supported |
| Versions | Read the [model version patterns](https://ai.google.dev/gemini-api/docs/models/gemini#model-versions) for more details. - Latest: `gemini-1.5-pro-latest` - Latest stable: `gemini-1.5-pro` - Stable: - `gemini-1.5-pro-001` 	- `gemini-1.5-pro-002` |
| Deprecation date | September 2025 |
| Latest update | September 2024 |

See the [examples](https://ai.google.dev/examples) to explore the capabilities of these model variations.

\[\*\] A token is equivalent to about 4 characters for Gemini models. 100 tokens are about 60-80 English words.

## Model version name patterns

Gemini models are available in either *stable*, *preview*, or *experimental* versions. In your code, you can use one of the following model name formats to specify which model and version you want to use.

### Latest stable

Points to the most recent stable version released for the specified model generation and variation.

To specify the latest stable version, use the following pattern:`<model>-<generation>-<variation>`. For example, `gemini-2.0-flash`.

### Stable

Points to a specific stable model. Stable models usually don't change. Most production apps should use a specific stable model.

To specify a stable version, use the following pattern:`<model>-<generation>-<variation>-<version>`. For example,`gemini-2.0-flash-001`.

### Preview

Points to a preview model which may not be suitable for production use, come with more restrictive rate limits, but may have billing enabled.

To specify a preview version, use the following pattern:`<model>-<generation>-<variation>-<version>`. For example,`gemini-2.5-pro-preview-06-05`.

Preview models are not stable and availability of model endpoints is subject to change.

### Experimental

Points to an experimental model which may not be suitable for production use and come with more restrictive rate limits. We release experimental models to gather feedback and get our latest updates into the hands of developers quickly.

To specify an experimental version, use the following pattern:`<model>-<generation>-<variation>-<version>`. For example,`gemini-2.0-pro-exp-02-05`.

Experimental models are not stable and availability of model endpoints is subject to change.

## Experimental models

In addition to stable models, the Gemini API offers experimental models which may not be suitable for production use and come with more restrictive rate limits.

We release experimental models to gather feedback, get our latest updates into the hands of developers quickly, and highlight the pace of innovation happening at Google. What we learn from experimental launches informs how we release models more widely. An experimental model can be swapped for another without prior notice. We don't guarantee that an experimental model will become a stable model in the future.

### Previous experimental models

As new versions or stable releases become available, we remove and replace experimental models. You can find the previous experimental models we released in the following section along with the replacement version:

| Model code | Base model | Replacement version |
| --- | --- | --- |
| `gemini-embedding-exp-03-07` | Gemini Embedding | `gemini-embedding-001` |
| `gemini-2.5-flash-preview-04-17` | Gemini 2.5 Flash | `gemini-2.5-flash-preview-05-20` |
| `gemini-2.0-flash-exp-image-generation` | Gemini 2.0 Flash | `gemini-2.0-flash-preview-image-generation` |
| `gemini-2.5-pro-preview-06-05` | Gemini 2.5 Pro | `gemini-2.5-pro` |
| `gemini-2.5-pro-preview-05-06` | Gemini 2.5 Pro | `gemini-2.5-pro` |
| `gemini-2.5-pro-preview-03-25` | Gemini 2.5 Pro | `gemini-2.5-pro` |
| `gemini-2.0-flash-thinking-exp-01-21` | Gemini 2.5 Flash | `gemini-2.5-flash-preview-04-17` |
| `gemini-2.0-pro-exp-02-05` | Gemini 2.0 Pro Experimental | `gemini-2.5-pro-preview-03-25` |
| `gemini-2.0-flash-exp` | Gemini 2.0 Flash | `gemini-2.0-flash` |
| `gemini-exp-1206` | Gemini 2.0 Pro | `gemini-2.0-pro-exp-02-05` |
| `gemini-2.0-flash-thinking-exp-1219` | Gemini 2.0 Flash Thinking | `gemini-2.0-flash-thinking-exp-01-21` |
| `gemini-exp-1121` | Gemini | `gemini-exp-1206` |
| `gemini-exp-1114` | Gemini | `gemini-exp-1206` |
| `gemini-1.5-pro-exp-0827` | Gemini 1.5 Pro | `gemini-exp-1206` |
| `gemini-1.5-pro-exp-0801` | Gemini 1.5 Pro | `gemini-exp-1206` |
| `gemini-1.5-flash-8b-exp-0924` | Gemini 1.5 Flash-8B | `gemini-1.5-flash-8b` |
| `gemini-1.5-flash-8b-exp-0827` | Gemini 1.5 Flash-8B | `gemini-1.5-flash-8b` |

## Supported languages

Gemini models are trained to work with the following languages:

- Arabic (`ar`)
- Bengali (`bn`)
- Bulgarian (`bg`)
- Chinese simplified and traditional (`zh`)
- Croatian (`hr`)
- Czech (`cs`)
- Danish (`da`)
- Dutch (`nl`)
- English (`en`)
- Estonian (`et`)
- Finnish (`fi`)
- French (`fr`)
- German (`de`)
- Greek (`el`)
- Hebrew (`iw`)
- Hindi (`hi`)
- Hungarian (`hu`)
- Indonesian (`id`)
- Italian (`it`)
- Japanese (`ja`)
- Korean (`ko`)
- Latvian (`lv`)
- Lithuanian (`lt`)
- Norwegian (`no`)
- Polish (`pl`)
- Portuguese (`pt`)
- Romanian (`ro`)
- Russian (`ru`)
- Serbian (`sr`)
- Slovak (`sk`)
- Slovenian (`sl`)
- Spanish (`es`)
- Swahili (`sw`)
- Swedish (`sv`)
- Thai (`th`)
- Turkish (`tr`)
- Ukrainian (`uk`)
- Vietnamese (`vi`)

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-09-23 UTC.

The new page has loaded.