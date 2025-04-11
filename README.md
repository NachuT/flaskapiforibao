# Flask Astronomy Tutor API

This is a Flask-based backend API for the Astronomy Tutor application. It provides endpoints for asking astronomy-related questions and getting AI-generated responses using the Gemini API.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file:
```bash
cp .env.example .env
```

4. Edit the `.env` file and add your Gemini API key:
```
GEMINI_API_KEY=your_gemini_api_key_here
PORT=5000
```

## Running the Application

1. Start the Flask development server:
```bash
python app.py
```

2. For production, use Gunicorn:
```bash
gunicorn app:app
```

## API Endpoints

### POST /ask
Ask an astronomy-related question.

Request body:
```json
{
    "question": "What is a black hole?"
}
```

Response:
```json
{
    "answer": "A black hole is a region in space where the gravitational pull is so strong that nothing, not even light, can escape from it..."
}
```

### GET /health
Health check endpoint.

Response:
```json
{
    "status": "healthy"
}
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- 400: Invalid request (non-astronomy question)
- 500: Server error (Gemini API error)

## Integration with Flutter

To use this API in your Flutter app:

1. Make sure the backend is running
2. Use the `http` package in Flutter to make requests
3. Example Flutter code:
```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

Future<String> askQuestion(String question) async {
  final response = await http.post(
    Uri.parse('http://your-server:5000/ask'),
    headers: {'Content-Type': 'application/json'},
    body: json.encode({'question': question}),
  );

  if (response.statusCode == 200) {
    return json.decode(response.body)['answer'];
  } else {
    throw Exception('Failed to get answer');
  }
}
``` # flaskapiforibao
