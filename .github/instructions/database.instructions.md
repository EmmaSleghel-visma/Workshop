---
paths:
  - 'backend/CreditroDemo.API/Models/**'
  - 'backend/CreditroDemo.API/Data/**'
  - '**/DbContext.cs'
---

# Database & Models Instructions

## Entity Design

### Models
- Use record types for DTOs and request/response models
- Use classes for entity models
- Add validation attributes on properties
- Use nullable reference types appropriately

Example:
```csharp
public class Customer
{
    public Guid Id { get; set; }

    [Required]
    [MaxLength(100)]
    public string Name { get; set; } = string.Empty;

    [Required]
    [EmailAddress]
    [MaxLength(200)]
    public string Email { get; set; } = string.Empty;

    [Phone]
    public string? Phone { get; set; }

    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    public DateTime? UpdatedAt { get; set; }

    // Navigation properties
    public ICollection<ComplianceCheck> ComplianceChecks { get; set; } = new List<ComplianceCheck>();
}
```

### Request/Response DTOs
- Use record types for immutability
- Include validation attributes
- Keep DTOs separate from entities

Example:
```csharp
public record CreateCustomerRequest(
    [Required][MaxLength(100)] string Name,
    [Required][EmailAddress] string Email,
    [Phone] string? Phone
);

public record CustomerResponse(
    Guid Id,
    string Name,
    string Email,
    string? Phone,
    DateTime CreatedAt
);
```

## DbContext Configuration

### Entity Configuration
- Use Fluent API for complex configurations
- Configure relationships explicitly
- Set up indexes for frequently queried fields
- Define cascade delete behaviors

Example:
```csharp
public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options)
    {
    }

    public DbSet<Customer> Customers { get; set; } = null!;
    public DbSet<ComplianceCheck> ComplianceChecks { get; set; } = null!;

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        // Customer configuration
        modelBuilder.Entity<Customer>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.HasIndex(e => e.Email).IsUnique();
            entity.Property(e => e.Name).IsRequired().HasMaxLength(100);
            entity.Property(e => e.Email).IsRequired().HasMaxLength(200);

            // Relationships
            entity.HasMany(e => e.ComplianceChecks)
                  .WithOne(c => c.Customer)
                  .HasForeignKey(c => c.CustomerId)
                  .OnDelete(DeleteBehavior.Cascade);
        });

        // ComplianceCheck configuration
        modelBuilder.Entity<ComplianceCheck>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.HasIndex(e => e.CustomerId);
            entity.Property(e => e.Status).IsRequired().HasMaxLength(50);
        });
    }
}
```

## Query Patterns

### Best Practices
- Always use async methods (ToListAsync, FirstOrDefaultAsync, etc.)
- Use Include() for eager loading related entities
- Use AsNoTracking() for read-only queries
- Implement pagination with Skip() and Take()
- Use projections (Select) to load only needed data

Example - Good Query:
```csharp
public async Task<List<CustomerResponse>> GetCustomersAsync(int page, int pageSize)
{
    return await _context.Customers
        .AsNoTracking()
        .OrderBy(c => c.Name)
        .Skip((page - 1) * pageSize)
        .Take(pageSize)
        .Select(c => new CustomerResponse(
            c.Id,
            c.Name,
            c.Email,
            c.Phone,
            c.CreatedAt
        ))
        .ToListAsync();
}
```

Example - Query with Related Data:
```csharp
public async Task<Customer?> GetCustomerWithChecksAsync(Guid id)
{
    return await _context.Customers
        .Include(c => c.ComplianceChecks)
        .FirstOrDefaultAsync(c => c.Id == id);
}
```

## Migrations

### When to Create Migrations
- After adding/modifying entity models
- After changing DbContext configuration
- Before deploying to any environment

### Commands
```bash
# Add migration
dotnet ef migrations add MigrationName

# Update database
dotnet ef database update

# Remove last migration (if not applied)
dotnet ef migrations remove
```

### Migration Best Practices
- Use descriptive migration names (e.g., "AddCustomerEmailIndex")
- Review generated migration code before applying
- Test migrations on development environment first
- Never modify applied migrations

## Data Seeding

### Seed Data Example
```csharp
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    base.OnModelCreating(modelBuilder);

    // Seed initial data
    modelBuilder.Entity<Customer>().HasData(
        new Customer
        {
            Id = Guid.Parse("00000000-0000-0000-0000-000000000001"),
            Name = "Test Customer",
            Email = "test@example.com",
            CreatedAt = DateTime.UtcNow
        }
    );
}
```

## Connection Strings

### Development
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost;Database=CreditroDemo;Trusted_Connection=True;TrustServerCertificate=True"
  }
}
```

### Production
- Use Azure Key Vault or environment variables
- Never commit connection strings to source control
- Use managed identities when possible
