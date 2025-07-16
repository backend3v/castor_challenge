# General Project Rules

1. **Clean Code and Comments**
   - Write clean, readable, and maintainable code.
   - Comments must be in English and clearly explain the "why," not just the "what."
   - Remove dead or unused code.

2. **Best Practices**
   - Follow the official best practices for each technology used.
   - Apply SOLID, DRY (Don't Repeat Yourself), and KISS (Keep It Simple, Stupid) principles.
   - Use version control (Git) and branches for new features or fixes.

3. **SOLID Principles**
   - Apply the SOLID principles in all code:
     - **S**ingle Responsibility Principle: Each module/class should have one responsibility.
     - **O**pen/Closed Principle: Software entities should be open for extension, but closed for modification.
     - **L**iskov Substitution Principle: Subtypes must be substitutable for their base types.
     - **I**nterface Segregation Principle: Prefer many specific interfaces over a single general-purpose interface.
     - **D**ependency Inversion Principle: Depend on abstractions, not on concretions.

4. **Integration and Context**
   - Consider backend and frontend integration from the design phase.
   - Define clear contracts (API, data formats, validations).

5. **Architecture**
   - Apply clean architecture, specifically hexagonal (Ports & Adapters).
   - Clearly separate domain, infrastructure, application, and presentation layers.
   - Facilitate scalability, maintainability, and testing. 