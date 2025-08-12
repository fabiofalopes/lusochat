# SearXNG Web Search Integration

This directory contains the configuration files for SearXNG, which provides web search capabilities for Lusochat.

## Files

- `settings.yml` - Main SearXNG configuration
- `uwsgi.ini` - UWSGI server configuration
- `limiter.toml` - Rate limiting configuration

## Features

- **Privacy-focused**: No tracking, no ads, no data collection
- **Multi-engine**: Aggregates results from multiple search engines
- **JSON API**: Provides structured results for RAG integration
- **Customizable**: Easy to configure search engines and behavior

## Access

- SearXNG web interface: http://localhost:8083
- API endpoint: http://localhost:8083/search?q=your-query&format=json

## Configuration

The web search is configured in the main `.env` file:

```env
ENABLE_RAG_WEB_SEARCH=True
RAG_WEB_SEARCH_ENGINE=searxng
RAG_WEB_SEARCH_RESULT_COUNT=3
RAG_WEB_SEARCH_CONCURRENT_REQUESTS=10
SEARXNG_QUERY_URL=http://searxng:8080/search?q=<query>
```

## Usage in Lusochat

Once enabled, users can:
1. Ask questions that require web search
2. Use the web search tool in conversations
3. Get real-time information from the internet

The AI will automatically decide when to use web search based on the query context.