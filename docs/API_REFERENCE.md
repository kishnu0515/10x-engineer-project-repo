# API Reference Documentation

Currently, the API does not require any authentication.
## Endpoints

### Health Check
- **Endpoint**: `GET /health`
- **Description**: Check the health status of the API.
- **Response**:
  - **200 OK**: `{ "status": "healthy", "version": "1.0.0" }`
  - **500 Internal Server Error**: `{ "detail": "Health check failed" }`

### Prompts

#### List Prompts
- **Endpoint**: `GET /prompts`
- **Description**: Retrieve a paginated list of prompts with optional filtering.
- **Query Parameters**:
  - `search` (optional): Filter prompts by title.
  - `collection_id` (optional): Filter prompts by collection.
  - `skip` (default: 0): Number of prompts to skip.
  - `limit` (default: 10): Maximum number of prompts to return.
- **Response**:
  - **200 OK**: `{ "prompts": [...], "total": <total_count> }`
  - **500 Internal Server Error**: `{ "detail": "Internal server error" }`

#### Get Prompt
- **Endpoint**: `GET /prompts/{prompt_id}`
- **Description**: Retrieve a specific prompt by its unique identifier.
- **Response**:
  - **200 OK**: `Prompt object`
  - **404 Not Found**: `{ "detail": "Prompt not found" }`
  - **500 Internal Server Error**: `{ "detail": "Internal server error" }`

#### Create Prompt
- **Endpoint**: `POST /prompts`
- **Description**: Create a new prompt.
- **Request Body**: JSON representing `PromptCreate` object.
- **Response**:
  - **201 Created**: `Prompt object`
  - **400 Bad Request**: `{ "detail": "<validation error message>" }`
  - **500 Internal Server Error**: `{ "detail": "Internal server error" }`

#### Update Prompt
- **Endpoint**: `PUT /prompts/{prompt_id}`
- **Description**: Completely replace an existing prompt.
- **Request Body**: JSON representing `PromptUpdate` object.
- **Response**:
  - **200 OK**: `Prompt object`
  - **404 Not Found**: `{ "detail": "Prompt not found" }`
  - **400 Bad Request**: `{ "detail": "<validation error message>" }`
  - **500 Internal Server Error**: `{ "detail": "Internal server error" }`

#### Partial Update Prompt
- **Endpoint**: `PATCH /prompts/{prompt_id}`
- **Description**: Partially update an existing prompt.
- **Request Body**: JSON representing `PromptPartialUpdate` object.
- **Response**:
  - **200 OK**: `Prompt object`
  - **404 Not Found**: `{ "detail": "Prompt not found" }`
  - **400 Bad Request**: `{ "detail": "<validation error message>" }`
  - **500 Internal Server Error**: `{ "detail": "Internal server error" }`

#### Delete Prompt
- **Endpoint**: `DELETE /prompts/{prompt_id}`
- **Description**: Delete a prompt by its unique identifier.
- **Response**:
  - **204 No Content**
  - **404 Not Found**: `{ "detail": "Prompt not found" }`
  - **500 Internal Server Error**: `{ "detail": "Internal server error" }`

### Collections

#### List Collections
- **Endpoint**: `GET /collections`
- **Description**: Retrieve a paginated list of all collections.
- **Query Parameters**:
  - `skip` (default: 0): Number of collections to skip.
  - `limit` (default: 10): Maximum number of collections to return.
- **Response**:
  - **200 OK**: `{ "collections": [...], "total": <total_count> }`
  - **500 Internal Server Error**: `{ "detail": "Internal server error" }`

#### Get Collection
- **Endpoint**: `GET /collections/{collection_id}`
- **Description**: Retrieve a specific collection by its unique identifier.
- **Response**:
  - **200 OK**: `Collection object`
  - **404 Not Found**: `{ "detail": "Collection not found" }`
  - **500 Internal Server Error**: `{ "detail": "Internal server error" }`

#### Create Collection
- **Endpoint**: `POST /collections`
- **Description**: Create a new collection.
- **Request Body**: JSON representing `CollectionCreate` object.
- **Response**:
  - **201 Created**: `Collection object`
  - **400 Bad Request**: `{ "detail": "<validation error message>" }`
  - **500 Internal Server Error**: `{ "detail": "Internal server error" }`

#### Delete Collection
- **Endpoint**: `DELETE /collections/{collection_id}`
- **Description**: Delete a collection by its unique identifier.
  - **Note**: Deleting a collection will orphan prompts that belong to it.
- **Response**:
  - **204 No Content**
  - **404 Not Found**: `{ "detail": "Collection not found" }`
  - **500 Internal Server Error**: `{ "detail": "Internal server error" }`

## Error Response Formats
All error responses follow the format:
- `{ "detail": "<error message>" }`

