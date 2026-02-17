# Creditro Demo Project - Copilot Instructions

## Project Overview

This is a full-stack application for credit and compliance management:
- **Backend**: .NET 8 Web API (C#)
- **Frontend**: Angular 21 (TypeScript)
- **Purpose**: Manage customers and compliance checks

## General Coding Standards

### Language & Framework
- Backend: C# 12, .NET 8
- Frontend: TypeScript, Angular 21
- Follow official Microsoft and Angular style guides

### Code Style
- Use meaningful variable and method names
- Keep methods small and focused (< 50 lines)
- Add XML documentation comments (C#) or JSDoc (TypeScript)
- Use async/await throughout
- Prefer LINQ and functional patterns in C#
- Use RxJS operators appropriately in Angular

### Error Handling
- Use try-catch blocks in service methods
- Log errors with structured logging
- Return user-friendly error messages
- Never expose stack traces to clients

### Testing
- Write unit tests for all business logic
- Use xUnit for C# (backend)
- Use Jasmine/Karma for TypeScript (frontend)
- Aim for >80% code coverage
- Mock external dependencies

## Architecture Patterns

### Backend
- Clean Architecture / Layered Architecture
- Dependency Injection everywhere
- Repository pattern for data access
- CQRS for complex operations
- MediatR for command/query handling (if needed)

### Frontend
- Component-based architecture
- Services for business logic
- RxJS for state management
- Lazy loading for modules
- Smart/Presentational component pattern

## Security
- All API endpoints require authentication (unless explicitly public)
- Use JWT tokens for authentication
- Validate all input data
- Sanitize output to prevent XSS
- Use HTTPS in production
- Store secrets in environment variables or Azure Key Vault

## Performance
- Use pagination for large datasets
- Implement caching where appropriate
- Optimize database queries (avoid N+1)
- Use CDN for static assets
- Lazy load components and modules

## Git Commit Messages
Follow conventional commits format:
- `feat:` for new features
- `fix:` for bug fixes
- `refactor:` for code refactoring
- `docs:` for documentation
- `test:` for tests
- `chore:` for maintenance

Example: `feat: add customer search endpoint`

## Communication Style
When generating code or responding to questions:
- Be clear and concise
- Explain the "why" behind recommendations
- Provide code examples when helpful
- Follow the project's existing patterns
- Ask clarifying questions if requirements are unclear
