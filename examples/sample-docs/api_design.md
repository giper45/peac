# REST API Design Guidelines

## URL Structure

Use nouns for resources, not verbs:
- Good: `/api/users`, `/api/products`
- Bad: `/api/getUsers`, `/api/createProduct`

## HTTP Methods

- GET: Retrieve resources
- POST: Create new resources
- PUT: Update entire resource
- PATCH: Partial update
- DELETE: Remove resource

## Status Codes

Common HTTP status codes:
- 200 OK: Successful GET, PUT, PATCH
- 201 Created: Successful POST
- 204 No Content: Successful DELETE
- 400 Bad Request: Invalid input
- 401 Unauthorized: Missing authentication
- 403 Forbidden: Insufficient permissions
- 404 Not Found: Resource doesn't exist
- 500 Internal Server Error: Server error

## Versioning

Include API version in URL:
- `/api/v1/users`
- `/api/v2/users`

## Response Format

Use consistent JSON structure:
```json
{
  "data": { ... },
  "meta": {
    "timestamp": "2026-01-14T10:00:00Z",
    "version": "1.0"
  },
  "errors": []
}
```

## Pagination

For large datasets, implement pagination:
- Use query parameters: `?page=1&limit=20`
- Include pagination metadata in response
- Provide links to next/previous pages
