---
title: "Rate limits  |  Gemini API"
source: "https://ai.google.dev/gemini-api/docs/rate-limits"
author:
  - "[[Google AI for Developers]]"
published:
created: 2025-09-23
description:
tags:
  - "clippings"
---
Rate limits regulate the number of requests you can make to the Gemini API within a given timeframe. These limits help maintain fair usage, protect against abuse, and help maintain system performance for all users.

## How rate limits work

Rate limits are usually measured across three dimensions:

- Requests per minute (**RPM**)
- Tokens per minute (input) (**TPM**)
- Requests per day (**RPD**)

Your usage is evaluated against each limit, and exceeding any of them will trigger a rate limit error. For example, if your RPM limit is 20, making 21 requests within a minute will result in an error, even if you haven't exceeded your TPM or other limits.

Rate limits are applied per project, not per API key.

Requests per day (**RPD**) quotas reset at midnight Pacific time.

Limits vary depending on the specific model being used, and some limits only apply to specific models. For example, Images per minute, or IPM, is only calculated for models capable of generating images (Imagen 3), but is conceptually similar to TPM. Other models might have a token per day limit (TPD).

Rate limits are more restricted for experimental and preview models.

## Usage tiers

Rate limits are tied to the project's usage tier. As your API usage and spending increase, you'll have an option to upgrade to a higher tier with increased rate limits.

The qualifications for Tiers 2 and 3 are based on the total cumulative spending on Google Cloud services (including, but not limited to, the Gemini API) for the billing account linked to your project.

| Tier | Qualifications |
| --- | --- |
| Free | Users in [eligible countries](https://ai.google.dev/gemini-api/docs/available-regions) |
| Tier 1 | Billing account [linked to the project](https://ai.google.dev/gemini-api/docs/billing#enable-cloud-billing) |
| Tier 2 | Total spend: > $250 and at least 30 days since successful payment |
| Tier 3 | Total spend: > $1,000 and at least 30 days since successful payment |

When you request an upgrade, our automated abuse protection system performs additional checks. While meeting the stated qualification criteria is generally sufficient for approval, in rare cases an upgrade request may be denied based on other factors identified during the review process.

This system helps maintain the security and integrity of the Gemini API platform for all users.

## Standard API rate limits

The following table lists the rate limits for all standard Gemini API calls.

<table><thead><tr><th>Model</th><th>RPM</th><th>TPM</th><th>RPD</th></tr></thead><tbody><tr><th colspan="4">Text-out models</th></tr><tr><td>Gemini 2.5 Pro</td><td>5</td><td>250,000</td><td>100</td></tr><tr><td>Gemini 2.5 Flash</td><td>10</td><td>250,000</td><td>250</td></tr><tr><td>Gemini 2.5 Flash-Lite</td><td>15</td><td>250,000</td><td>1,000</td></tr><tr><td>Gemini 2.0 Flash</td><td>15</td><td>1,000,000</td><td>200</td></tr><tr><td>Gemini 2.0 Flash-Lite</td><td>30</td><td>1,000,000</td><td>200</td></tr><tr><th colspan="4">Live API</th></tr><tr><td>Gemini 2.5 Flash Live</td><td>3 sessions</td><td>1,000,000</td><td>*</td></tr><tr><td>Gemini 2.5 Flash Preview Native Audio</td><td>1 session</td><td>25,000</td><td>5</td></tr><tr><td>Gemini 2.5 Flash Experimental Native Audio Thinking</td><td>1 session</td><td>10,000</td><td>5</td></tr><tr><td>Gemini 2.0 Flash Live</td><td>3 sessions</td><td>1,000,000</td><td>*</td></tr><tr><th colspan="4">Multi-modal generation models</th></tr><tr><td>Gemini 2.5 Flash Preview TTS</td><td>3</td><td>10,000</td><td>15</td></tr><tr><td>Gemini 2.0 Flash Preview Image Generation</td><td>10</td><td>200,000</td><td>100</td></tr><tr><th colspan="4">Other models</th></tr><tr><td>Gemma 3 &amp; 3n</td><td>30</td><td>15,000</td><td>14,400</td></tr><tr><td>Gemini Embedding</td><td>100</td><td>30,000</td><td>1,000</td></tr><tr><th colspan="4">Deprecated models</th></tr><tr><td>Gemini 1.5 Flash (Deprecated)</td><td>15</td><td>250,000</td><td>50</td></tr><tr><td>Gemini 1.5 Flash-8B (Deprecated)</td><td>15</td><td>250,000</td><td>50</td></tr></tbody></table>

<table><thead><tr><th>Model</th><th>RPM</th><th>TPM</th><th>RPD</th><th>Batch Enqueued Tokens</th></tr></thead><tbody><tr><th colspan="5">Text-out models</th></tr><tr><td>Gemini 2.5 Pro</td><td>150</td><td>2,000,000</td><td>10,000</td><td>5,000,000</td></tr><tr><td>Gemini 2.5 Flash</td><td>1,000</td><td>1,000,000</td><td>10,000</td><td>3,000,000</td></tr><tr><td>Gemini 2.5 Flash-Lite</td><td>4,000</td><td>4,000,000</td><td>*</td><td>10,000,000</td></tr><tr><td>Gemini 2.0 Flash</td><td>2,000</td><td>4,000,000</td><td>*</td><td>10,000,000</td></tr><tr><td>Gemini 2.0 Flash-Lite</td><td>4,000</td><td>4,000,000</td><td>*</td><td>10,000,000</td></tr><tr><th colspan="5">Live API</th></tr><tr><td>Gemini 2.5 Flash Live</td><td>50 sessions</td><td>4,000,000</td><td>*</td><td>*</td></tr><tr><td>Gemini 2.5 Flash Preview Native Audio</td><td>3 sessions</td><td>50,000</td><td>50</td><td>*</td></tr><tr><td>Gemini 2.5 Flash Experimental Native Audio Thinking</td><td>1 session</td><td>25,000</td><td>50</td><td>*</td></tr><tr><td>Gemini 2.0 Flash Live</td><td>50 sessions</td><td>4,000,000</td><td>*</td><td>*</td></tr><tr><th colspan="5">Multi-modal generation models</th></tr><tr><td>Gemini 2.5 Flash Preview TTS</td><td>10</td><td>10,000</td><td>100</td><td>*</td></tr><tr><td>Gemini 2.5 Pro Preview TTS</td><td>10</td><td>10,000</td><td>50</td><td>*</td></tr><tr><td>Gemini 2.5 Flash Image Preview</td><td>500</td><td>500,000</td><td>2,000</td><td>*</td></tr><tr><td>Gemini 2.0 Flash Preview Image Generation</td><td>1,000</td><td>1,000,000</td><td>10,000</td><td>*</td></tr><tr><td>Imagen 4 Standard/Fast</td><td>10</td><td>*</td><td>70</td><td>*</td></tr><tr><td>Imagen 4 Ultra</td><td>5</td><td>*</td><td>30</td><td>*</td></tr><tr><td>Imagen 3</td><td>20</td><td>*</td><td>*</td><td>*</td></tr><tr><td>Veo 3</td><td>2</td><td>*</td><td>10</td><td>*</td></tr><tr><td>Veo 3 Fast</td><td>2</td><td>*</td><td>10</td><td>*</td></tr><tr><td>Veo 2</td><td>2</td><td>*</td><td>50</td><td>*</td></tr><tr><th colspan="5">Other models</th></tr><tr><td>Gemma 3 &amp; 3n</td><td>30</td><td>15,000</td><td>14,400</td><td>*</td></tr><tr><td>Gemini Embedding</td><td>3,000</td><td>1,000,000</td><td>*</td><td>*</td></tr><tr><th colspan="5">Deprecated models</th></tr><tr><td>Gemini 1.5 Flash (Deprecated)</td><td>2,000</td><td>4,000,000</td><td>*</td><td>*</td></tr><tr><td>Gemini 1.5 Flash-8B (Deprecated)</td><td>4,000</td><td>4,000,000</td><td>*</td><td>*</td></tr><tr><td>Gemini 1.5 Pro (Deprecated)</td><td>1,000</td><td>4,000,000</td><td>*</td><td>*</td></tr></tbody></table>

<table><thead><tr><th>Model</th><th>RPM</th><th>TPM</th><th>RPD</th><th>Batch Enqueued Tokens</th></tr></thead><tbody><tr><th colspan="5">Text-out models</th></tr><tr><td>Gemini 2.5 Pro</td><td>1,000</td><td>5,000,000</td><td>50,000</td><td>500,000,000</td></tr><tr><td>Gemini 2.5 Flash</td><td>2,000</td><td>3,000,000</td><td>100,000</td><td>400,000,000</td></tr><tr><td>Gemini 2.5 Flash-Lite</td><td>10,000</td><td>10,000,000</td><td>*</td><td>500,000,000</td></tr><tr><td>Gemini 2.0 Flash</td><td>10,000</td><td>10,000,000</td><td>*</td><td>1,000,000,000</td></tr><tr><td>Gemini 2.0 Flash-Lite</td><td>20,000</td><td>10,000,000</td><td>*</td><td>1,000,000,000</td></tr><tr><th colspan="5">Live API</th></tr><tr><td>Gemini 2.5 Flash Live</td><td>1,000 sessions</td><td>10,000,000</td><td>*</td><td>*</td></tr><tr><td>Gemini 2.5 Flash Preview Native Audio</td><td>100 sessions</td><td>1,000,000</td><td>*</td><td>*</td></tr><tr><td>Gemini 2.5 Flash Experimental Native Audio Thinking</td><td>1 session</td><td>25,000</td><td>50</td><td>*</td></tr><tr><td>Gemini 2.0 Flash Live</td><td>1,000 sessions</td><td>10,000,000</td><td>*</td><td>*</td></tr><tr><th colspan="5">Multi-modal generation models</th></tr><tr><td>Gemini 2.5 Flash Preview TTS</td><td>1,000</td><td>100,000</td><td>10,000</td><td>*</td></tr><tr><td>Gemini 2.5 Pro Preview TTS</td><td>100</td><td>25,000</td><td>1,000</td><td>*</td></tr><tr><td>Gemini 2.5 Flash Image Preview</td><td>2,000</td><td>1,500,000</td><td>50,000</td><td>*</td></tr><tr><td>Gemini 2.0 Flash Preview Image Generation</td><td>2,000</td><td>3,000,000</td><td>100,000</td><td>*</td></tr><tr><td>Imagen 4 Standard/Fast</td><td>15</td><td>*</td><td>1000</td><td>*</td></tr><tr><td>Imagen 4 Ultra</td><td>10</td><td>*</td><td>400</td><td>*</td></tr><tr><td>Imagen 3</td><td>20</td><td>*</td><td>*</td><td>*</td></tr><tr><td>Veo 3</td><td>4</td><td>*</td><td>50</td><td>*</td></tr><tr><td>Veo 3 Fast</td><td>4</td><td>*</td><td>50</td><td>*</td></tr><tr><td>Veo 2</td><td>2</td><td>*</td><td>50</td><td>*</td></tr><tr><th colspan="5">Other models</th></tr><tr><td>Gemma 3 &amp; 3n</td><td>30</td><td>15,000</td><td>14,400</td><td>*</td></tr><tr><td>Gemini Embedding</td><td>5,000</td><td>5,000,000</td><td>*</td><td>*</td></tr><tr><th colspan="5">Deprecated models</th></tr><tr><td>Gemini 1.5 Flash (Deprecated)</td><td>2,000</td><td>4,000,000</td><td>*</td><td>*</td></tr><tr><td>Gemini 1.5 Flash-8B (Deprecated)</td><td>4,000</td><td>4,000,000</td><td>*</td><td>*</td></tr><tr><td>Gemini 1.5 Pro (Deprecated)</td><td>1,000</td><td>4,000,000</td><td>*</td><td>*</td></tr></tbody></table>

<table><thead><tr><th>Model</th><th>RPM</th><th>TPM</th><th>RPD</th><th>Batch Enqueued Tokens</th></tr></thead><tbody><tr><th colspan="5">Text-out models</th></tr><tr><td>Gemini 2.5 Pro</td><td>2,000</td><td>8,000,000</td><td>*</td><td>1,000,000,000</td></tr><tr><td>Gemini 2.5 Flash</td><td>10,000</td><td>8,000,000</td><td>*</td><td>1,000,000,000</td></tr><tr><td>Gemini 2.5 Flash-Lite</td><td>30,000</td><td>30,000,000</td><td>*</td><td>1,000,000,000</td></tr><tr><td>Gemini 2.0 Flash</td><td>30,000</td><td>30,000,000</td><td>*</td><td>5,000,000,000</td></tr><tr><td>Gemini 2.0 Flash-Lite</td><td>30,000</td><td>30,000,000</td><td>*</td><td>5,000,000,000</td></tr><tr><th colspan="5">Live API</th></tr><tr><td>Gemini 2.5 Flash Live</td><td>1,000 sessions</td><td>10,000,000</td><td>*</td><td>*</td></tr><tr><td>Gemini 2.5 Flash Preview Native Audio</td><td>100 sessions</td><td>1,000,000</td><td>*</td><td>*</td></tr><tr><td>Gemini 2.5 Flash Experimental Native Audio Thinking</td><td>1 session</td><td>25,000</td><td>50</td><td>*</td></tr><tr><td>Gemini 2.0 Flash Live</td><td>1,000 sessions</td><td>10,000,000</td><td>*</td><td>*</td></tr><tr><th colspan="5">Multi-modal generation models</th></tr><tr><td>Gemini 2.5 Flash Preview TTS</td><td>1,000</td><td>1,000,000</td><td>*</td><td>*</td></tr><tr><td>Gemini 2.5 Pro Preview TTS</td><td>100</td><td>1,000,000</td><td>*</td><td>*</td></tr><tr><td>Gemini 2.5 Flash Image Preview</td><td>5,000</td><td>5,000,000</td><td>*</td><td>*</td></tr><tr><td>Gemini 2.0 Flash Preview Image Generation</td><td>5,000</td><td>5,000,000</td><td>*</td><td>*</td></tr><tr><td>Imagen 4 Standard/Fast</td><td>20</td><td>*</td><td>15,000</td><td>*</td></tr><tr><td>Imagen 4 Ultra</td><td>15</td><td>*</td><td>5,000</td><td>*</td></tr><tr><td>Imagen 3</td><td>20</td><td>*</td><td>*</td><td>*</td></tr><tr><td>Veo 3</td><td>10</td><td>*</td><td>500</td><td>*</td></tr><tr><td>Veo 3 Fast</td><td>10</td><td>*</td><td>500</td><td>*</td></tr><tr><td>Veo 2</td><td>2</td><td>*</td><td>50</td><td>*</td></tr><tr><th colspan="5">Other models</th></tr><tr><td>Gemma 3 &amp; 3n</td><td>30</td><td>15,000</td><td>14,400</td><td>*</td></tr><tr><td>Gemini Embedding</td><td>10,000</td><td>10,000,000</td><td>*</td><td>*</td></tr><tr><th colspan="5">Deprecated models</th></tr><tr><td>Gemini 1.5 Flash (Deprecated)</td><td>2,000</td><td>4,000,000</td><td>*</td><td>*</td></tr><tr><td>Gemini 1.5 Flash-8B (Deprecated)</td><td>4,000</td><td>4,000,000</td><td>*</td><td>*</td></tr><tr><td>Gemini 1.5 Pro (Deprecated)</td><td>1,000</td><td>4,000,000</td><td>*</td><td>*</td></tr></tbody></table>

Specified rate limits are not guaranteed and actual capacity may vary.

## Batch API rate limits

[Batch API](https://ai.google.dev/gemini-api/docs/batch-api) requests are subject to their own rate limits, separate from the non-batch API calls.

- **Concurrent batch requests:** 100
- **Input file size limit:** 2GB
- **File storage limit:** 20GB
- **Enqueued tokens per model:** The **Batch Enqueued Tokens** column in the rate limits table lists the maximum number of tokens that can be enqueued for batch processing across all your active batch jobs for a given model. See in the [standard API rate limits table](https://ai.google.dev/gemini-api/docs/#current-rate-limits).

The Gemini API uses Cloud Billing for all billing services. To transition from the Free tier to a paid tier, you must first enable Cloud Billing for your Google Cloud project.

Once your project meets the specified criteria, it becomes eligible for an upgrade to the next tier. To request an upgrade, follow these steps:

- Navigate to the [API keys page](https://aistudio.google.com/app/apikey) in AI Studio.
- Locate the project you want to upgrade and click "Upgrade". The "Upgrade" option will only show up for projects that meet [next tier qualifications](https://ai.google.dev/gemini-api/docs/rate-limits#usage-tiers).

After a quick validation, the project will be upgraded to the next tier.

## Request a rate limit increase

Each model variation has an associated rate limit (requests per minute, RPM). For details on those rate limits, see [Gemini models](https://ai.google.dev/models/gemini).

[Request paid tier rate limit increase](https://forms.gle/ETzX94k8jf7iSotH9)

We offer no guarantees about increasing your rate limit, but we'll do our best to review your request.

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-09-23 UTC.