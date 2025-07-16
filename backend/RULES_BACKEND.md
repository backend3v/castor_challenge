# Backend Rules (Python + Flask)

1. **Best Practices**
   - Follow the official Python (PEP8) and Flask guidelines.
   - Use static typing (type hints) and English docstrings.
   - Organize the project into clear modules and packages.

2. **API Design**
   - Use appropriate design patterns for APIs (Repository, Service, Factory, etc.).
   - Maintain consistency in endpoint, parameter, and response naming.
   - Use standards like HATEOAS for REST APIs.

3. **Style and Structure**
   - Use intuitive and representative URLs, with plural nouns (e.g., /users, /products).
   - Include versioning in the URL (e.g., /api/v1/).
   - Use HTTP methods correctly: GET, POST, PUT, DELETE.
   - Respond with appropriate HTTP status codes (200, 201, 404, 500, etc.).
   - Provide clear and descriptive error messages in English.

4. **Documentation and Testing**
   - Document the API with Swagger/OpenAPI.
   - Implement unit and integration tests (pytest recommended).
   - Use logging and monitoring.

5. **Optimization and Security**
   - Optimize database queries and use caching if necessary.
   - Validate and sanitize all inputs.
   - Consider scalability (load balancing, microservices if applicable). 