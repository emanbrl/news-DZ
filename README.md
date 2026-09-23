# News DZ 🇩🇿📰

Algerian news aggregation platform that collects, organizes, and categorizes articles from multiple Algerian news sources, with an evolving NLP and AI pipeline.

## Project Goal

News DZ aims to bring news from multiple Algerian sources into one place instead of requiring users to visit different news websites individually.

The project is also designed as an AI Engineering project, progressing from web scraping and data pipelines to databases, NLP, APIs, and eventually deployment.

## Initial Sources

The first version will collect articles from:

* [Algeria Press Service (APS)](https://www.aps.dz/en)
* [Ennahar Online](https://www.ennaharonline.com/fr/)
* [TSA Algérie](https://www.tsa-algerie.com/)

## Initial MVP

The first version will:

* collect recent articles from multiple sources
* extract and normalize article metadata
* store the collected data in a database
* categorize articles
* avoid storing the full article content
* provide a simple way to browse the collected news

The system will be expanded incrementally as new requirements and useful AI features are identified.

## Planned Evolution

```text
News Sources
     ↓
Web Scraping
     ↓
Parsing & Validation
     ↓
Data Pipeline
     ↓
PostgreSQL
     ↓
NLP / ML
     ↓
API
     ↓
News Application
     ↓
Deployment
```

## Potential AI Features

Future versions may explore:

* automatic article categorization
* duplicate and near-duplicate detection
* Arabic and French NLP
* semantic search
* embeddings
* article recommendation
* automatic summarization

These features will be introduced incrementally rather than all at once.

## Current Status

🚧 Early development

The initial APS scraper has been implemented and tested.

Current capabilities:

- Fetch the APS homepage using `requests`
- Parse HTML using BeautifulSoup
- Identify article links
- Remove duplicate article URLs
- Fetch individual article pages
- Extract article titles
- Extract publication dates
- Extract article descriptions
- Handle HTTP/request errors
- Use a persistent HTTP session
- Identify the scraper with a custom User-Agent
- Apply a delay between article requests
- Parse publication dates into Python `datetime` objects

Next steps:

- Normalize the article schema
- Add source and category metadata
- Save collected articles as JSON
- Introduce PostgreSQL
- Implement additional news-source scrapers

## Learning Objectives

This project is intended to strengthen practical AI Engineering skills in:

* Python application development
* HTTP and web scraping
* HTML parsing
* data validation
* data pipelines
* relational databases
* NLP and machine learning
* API development
* software testing
* automation
* Docker and deployment

## Disclaimer

News DZ links back to the original publishers. The project is intended for educational and engineering purposes, and source-specific usage policies, robots.txt directives, and applicable terms will be considered when implementing data collection.