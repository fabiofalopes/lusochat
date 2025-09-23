---
title: "Google AI Studio"
source: "https://aistudio.google.com/apikey"
author:
  - "[[AI Studio]]"
published:
created: 2025-09-23
description: "The fastest path from prompt to production with Gemini"
tags:
  - "clippings"
---
## Chaves de API

#### Testar rapidamente a API Gemini

[Guia de início rápido da API](https://ai.google.dev/gemini-api/docs/quickstart?lang=python)

Code

```
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent" \
  -H 'Content-Type: application/json' \
  -H 'X-goog-api-key: GEMINI_API_KEY' \
  -X POST \
  -d '{
    "contents": [
      {
        "parts": [
          {
            "text": "Explain how AI works in a few words"
          }
        ]
      }
    ]
  }'
```

Suas chaves de API estão listadas abaixo. Também é possível visualizar e gerenciar seu projeto e as chaves de API no Google Cloud.

Número do projeto

Nome do projeto

Chave de API

Criação

Plano

...2732

My Project 27121

...oz5k...B8w4

14 de mai. de 2025

2 de jul. de 2024

Free tier Configurar o faturamento Ver dados de uso

Use as chaves de API com segurança. Não as compartilhe nem as incorpore em códigos públicos. O uso da API Gemini em um projeto com faturamento ativado está sujeito aos [preços do modelo de pagamento por uso](https://ai.google.dev/gemini-api/docs/pricing).