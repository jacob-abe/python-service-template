# Base0 Backend

FastAPI backend application with CRUD operations, authentication, logging, and Supabase integration.

## Project Structure

```
b0-backend/
├── app/
│   ├── api/
│   │   └── endpoints/
│   ├── core/
│   ├── middleware/
│   └── main.py
├── tests/
├── env.example
├── requirements.txt
├── pytest.ini
├── render.yaml
└── README.md
```

## Testing

Run all tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app --cov-report=html
```

Run specific test file:
```bash
pytest tests/test_api.py
```

## Environment Variables

- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase API key
- `AUTH_DOMAIN`: Auth provider domain (e.g., Auth0)
- `AUTH_AUDIENCE`: Auth provider audience
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `ENVIRONMENT`: Environment (development, production)

See `env.example` for a complete template.

## License

[MIT]

