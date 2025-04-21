# Daily Sentence

A web application for language learning that helps users practice sentence construction with guided constraints.

## Prerequisites

- Python 3.x
- Poetry for dependency management
- OpenAI API key for ChatGPT integration

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd daily-sentence
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Set up your environment variables in a `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key
```

## Configuration

The application supports the following environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `ENV`: Environment setting
  - Not set or any value: Defaults to development mode (localhost:8085)
  - `production`: Uses production API URL
- `TRANSLATION_API_URL`: (optional) Override the translation API URL

### Environment Setup

#### Development (default)
```env
OPENAI_API_KEY=your_openai_api_key
# ENV and TRANSLATION_API_URL not needed - will use localhost:8085
```

#### Production
```env
OPENAI_API_KEY=your_openai_api_key
ENV=production
# Will use https://ai-translation-api-1f53c7c0c947.herokuapp.com
```

#### Custom API URL (if needed)
```env
OPENAI_API_KEY=your_openai_api_key
TRANSLATION_API_URL=your_custom_url
# Will use your custom URL regardless of ENV setting
```

## Running the Application

1. Activate the Poetry virtual environment:
```bash
poetry shell
```

2. Start the application:
```bash
python -m daily_sentence
```

The application will be available at `http://localhost:8080`

## Project Structure

## Translation System

The application uses [AiTranslationApi](https://github.com/buoren/AiTranslationApi) for handling translations, which provides cached responses for better performance and reduced API calls.

### Language Handling
- UI text translations are handled by the Translation API
- If the Translation API fails, the system falls back to displaying English text
- Sentence analysis (corrections, feedback, etc.) uses direct OpenAI calls and is separate from the Translation API
