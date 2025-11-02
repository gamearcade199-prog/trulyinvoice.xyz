"""
API Documentation Generator
FIX #7: Auto-Generated API Documentation

Generate comprehensive API docs with examples, error responses, rate limits
"""

from typing import Dict, List, Optional, Any
from enum import Enum
import json


class HTTPMethod(str, Enum):
    """HTTP methods"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    OPTIONS = "OPTIONS"


class ParameterLocation(str, Enum):
    """Parameter location in request"""
    QUERY = "query"
    PATH = "path"
    BODY = "body"
    HEADER = "header"


class Parameter:
    """API Parameter documentation"""
    
    def __init__(
        self,
        name: str,
        param_type: str,
        location: ParameterLocation,
        required: bool = False,
        description: str = "",
        example: Any = None
    ):
        self.name = name
        self.param_type = param_type
        self.location = location
        self.required = required
        self.description = description
        self.example = example
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "type": self.param_type,
            "location": self.location.value,
            "required": self.required,
            "description": self.description,
            "example": self.example
        }


class Response:
    """API Response documentation"""
    
    def __init__(
        self,
        status_code: int,
        description: str,
        schema: Optional[Dict] = None,
        example: Optional[Dict] = None
    ):
        self.status_code = status_code
        self.description = description
        self.schema = schema
        self.example = example
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "status_code": self.status_code,
            "description": self.description,
            "schema": self.schema,
            "example": self.example
        }


class APIEndpoint:
    """API Endpoint documentation"""
    
    def __init__(
        self,
        path: str,
        method: HTTPMethod,
        summary: str,
        description: str = "",
        tags: List[str] = None
    ):
        self.path = path
        self.method = method
        self.summary = summary
        self.description = description
        self.tags = tags or []
        self.parameters: List[Parameter] = []
        self.responses: List[Response] = []
        self.rate_limit: Optional[str] = None
        self.authentication_required = False
        self.example_request: Optional[Dict] = None
        self.example_response: Optional[Dict] = None
    
    def add_parameter(self, parameter: Parameter) -> "APIEndpoint":
        """Add parameter to endpoint"""
        self.parameters.append(parameter)
        return self
    
    def add_response(self, response: Response) -> "APIEndpoint":
        """Add response to endpoint"""
        self.responses.append(response)
        return self
    
    def set_rate_limit(self, limit: str) -> "APIEndpoint":
        """Set rate limit (e.g., "100 requests per hour")"""
        self.rate_limit = limit
        return self
    
    def require_auth(self) -> "APIEndpoint":
        """Mark endpoint as requiring authentication"""
        self.authentication_required = True
        return self
    
    def set_examples(self, request: Optional[Dict] = None, response: Optional[Dict] = None) -> "APIEndpoint":
        """Set request/response examples"""
        if request:
            self.example_request = request
        if response:
            self.example_response = response
        return self
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "path": self.path,
            "method": self.method.value,
            "summary": self.summary,
            "description": self.description,
            "tags": self.tags,
            "parameters": [p.to_dict() for p in self.parameters],
            "responses": [r.to_dict() for r in self.responses],
            "rate_limit": self.rate_limit,
            "authentication_required": self.authentication_required,
            "example_request": self.example_request,
            "example_response": self.example_response
        }


class APIDocumentation:
    """Complete API documentation"""
    
    def __init__(self, title: str, version: str, description: str = ""):
        self.title = title
        self.version = version
        self.description = description
        self.endpoints: Dict[str, APIEndpoint] = {}
        self.base_url = "https://api.trulyinvoice.com"
        self.authentication_methods: List[str] = ["Bearer Token (JWT)"]
    
    def add_endpoint(self, endpoint: APIEndpoint) -> None:
        """Add endpoint to documentation"""
        key = f"{endpoint.method.value} {endpoint.path}"
        self.endpoints[key] = endpoint
    
    def generate_markdown(self) -> str:
        """Generate Markdown documentation"""
        
        doc = f"""# {self.title} - API Documentation

**Version:** {self.version}

{self.description}

## Authentication

The API requires Bearer token authentication using JWT. Include the token in the Authorization header:

```
Authorization: Bearer YOUR_JWT_TOKEN
```

## Base URL

```
{self.base_url}
```

## Endpoints

"""
        
        # Group endpoints by tag
        endpoints_by_tag = {}
        for endpoint in self.endpoints.values():
            for tag in endpoint.tags or ["General"]:
                if tag not in endpoints_by_tag:
                    endpoints_by_tag[tag] = []
                endpoints_by_tag[tag].append(endpoint)
        
        # Generate documentation for each tag
        for tag, endpoints in sorted(endpoints_by_tag.items()):
            doc += f"\n### {tag}\n"
            
            for endpoint in endpoints:
                doc += self._generate_endpoint_markdown(endpoint)
        
        return doc
    
    def _generate_endpoint_markdown(self, endpoint: APIEndpoint) -> str:
        """Generate Markdown for single endpoint"""
        
        auth_badge = "🔐 **Requires Authentication**" if endpoint.authentication_required else ""
        
        markdown = f"""
#### {endpoint.method.value} {endpoint.path}

{endpoint.summary}

{auth_badge}

**Description:** {endpoint.description}

"""
        
        # Parameters
        if endpoint.parameters:
            markdown += "**Parameters:**\n\n"
            for param in endpoint.parameters:
                required = "✓ Required" if param.required else "Optional"
                markdown += f"- `{param.name}` ({param.param_type}, {required}): {param.description}"
                if param.example:
                    markdown += f"\n  Example: `{param.example}`"
                markdown += "\n"
            markdown += "\n"
        
        # Rate Limit
        if endpoint.rate_limit:
            markdown += f"**Rate Limit:** {endpoint.rate_limit}\n\n"
        
        # Request Example
        if endpoint.example_request:
            markdown += f"""**Request Example:**

```json
{json.dumps(endpoint.example_request, indent=2)}
```

"""
        
        # Responses
        if endpoint.responses:
            markdown += "**Responses:**\n\n"
            for response in endpoint.responses:
                markdown += f"- **{response.status_code}** - {response.description}\n"
                if response.example:
                    markdown += f"  ```json\n  {json.dumps(response.example, indent=2)}\n  ```\n"
            markdown += "\n"
        
        # Response Example
        if endpoint.example_response:
            markdown += f"""**Response Example:**

```json
{json.dumps(endpoint.example_response, indent=2)}
```

"""
        
        return markdown
    
    def generate_openapi_json(self) -> Dict:
        """Generate OpenAPI 3.0 specification"""
        
        paths = {}
        for endpoint in self.endpoints.values():
            if endpoint.path not in paths:
                paths[endpoint.path] = {}
            
            method_spec = {
                "summary": endpoint.summary,
                "description": endpoint.description,
                "tags": endpoint.tags,
                "parameters": [
                    {
                        "name": p.name,
                        "in": p.location.value,
                        "required": p.required,
                        "schema": {"type": p.param_type},
                        "description": p.description,
                        "example": p.example
                    }
                    for p in endpoint.parameters
                ],
                "responses": {
                    str(r.status_code): {
                        "description": r.description,
                        "content": {
                            "application/json": {
                                "schema": r.schema or {"type": "object"}
                            }
                        }
                    }
                    for r in endpoint.responses
                }
            }
            
            if endpoint.authentication_required:
                method_spec["security"] = [{"bearerAuth": []}]
            
            paths[endpoint.path][endpoint.method.value.lower()] = method_spec
        
        return {
            "openapi": "3.0.0",
            "info": {
                "title": self.title,
                "version": self.version,
                "description": self.description
            },
            "servers": [{"url": self.base_url}],
            "paths": paths,
            "components": {
                "securitySchemes": {
                    "bearerAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT"
                    }
                }
            }
        }
    
    def to_json(self) -> str:
        """Export as JSON"""
        return json.dumps(self.generate_openapi_json(), indent=2)


# Initialize API documentation
def create_api_docs() -> APIDocumentation:
    """Create complete API documentation"""
    
    docs = APIDocumentation(
        title="TrulyInvoice API",
        version="1.0.0",
        description="Professional invoice processing and management API"
    )
    
    # Example: Payment Endpoints
    create_order_endpoint = (
        APIEndpoint("/api/v1/payments/create-order", HTTPMethod.POST, "Create Payment Order")
        .set_examples(
            request={"amount": 9999, "currency": "INR"},
            response={"order_id": "order_12345"}
        )
        .require_auth()
        .set_rate_limit("10 requests per minute")
        .add_response(Response(200, "Order created successfully"))
        .add_response(Response(400, "Invalid request"))
        .add_response(Response(401, "Unauthorized"))
    )
    docs.add_endpoint(create_order_endpoint)
    
    return docs


if __name__ == "__main__":
    # Generate documentation
    docs = create_api_docs()
    
    print("📚 Generating API Documentation\n")
    print(docs.generate_markdown()[:500] + "...\n")
    print("✅ API documentation generated successfully!")
