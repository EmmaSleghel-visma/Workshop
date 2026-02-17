using Xunit;
using Moq;
using FluentAssertions;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace CreditroDemo.API.Tests.Controllers
{
    public class {ControllerName}Tests
    {
        private readonly Mock<I{ServiceName}> _mockService;
        private readonly Mock<ILogger<{ControllerName}>> _mockLogger;
        private readonly {ControllerName} _controller;

        public {ControllerName}Tests()
        {
            _mockService = new Mock<I{ServiceName}>();
            _mockLogger = new Mock<ILogger<{ControllerName}>>();
            _controller = new {ControllerName}(_mockService.Object, _mockLogger.Object);
        }

        #region GET Tests

        [Fact]
        public async Task GetAll_ReturnsOkResult_WithListOfItems()
        {
            // Arrange
            var expectedItems = new List<{ModelName}>
            {
                new {ModelName} { Id = Guid.NewGuid(), /* properties */ },
                new {ModelName} { Id = Guid.NewGuid(), /* properties */ }
            };
            _mockService
                .Setup(x => x.GetAllAsync())
                .ReturnsAsync(expectedItems);

            // Act
            var result = await _controller.GetAll();

            // Assert
            var okResult = result.Result.Should().BeOfType<OkObjectResult>().Subject;
            var returnedItems = okResult.Value.Should().BeAssignableTo<List<{ModelName}>>().Subject;
            returnedItems.Should().HaveCount(expectedItems.Count);
            _mockService.Verify(x => x.GetAllAsync(), Times.Once);
        }

        [Fact]
        public async Task GetById_ValidId_ReturnsOkResult_WithItem()
        {
            // Arrange
            var id = Guid.NewGuid();
            var expectedItem = new {ModelName} { Id = id, /* properties */ };
            _mockService
                .Setup(x => x.GetByIdAsync(id))
                .ReturnsAsync(expectedItem);

            // Act
            var result = await _controller.GetById(id);

            // Assert
            var okResult = result.Result.Should().BeOfType<OkObjectResult>().Subject;
            var returnedItem = okResult.Value.Should().BeAssignableTo<{ModelName}>().Subject;
            returnedItem.Id.Should().Be(id);
        }

        [Fact]
        public async Task GetById_NonExistentId_ReturnsNotFound()
        {
            // Arrange
            var id = Guid.NewGuid();
            _mockService
                .Setup(x => x.GetByIdAsync(id))
                .ReturnsAsync(({ModelName}?)null);

            // Act
            var result = await _controller.GetById(id);

            // Assert
            result.Result.Should().BeOfType<NotFoundResult>();
        }

        #endregion

        #region POST Tests

        [Fact]
        public async Task Create_ValidRequest_ReturnsCreatedResult()
        {
            // Arrange
            var request = new Create{ModelName}Request
            {
                // Set properties
            };
            var createdItem = new {ModelName}
            {
                Id = Guid.NewGuid(),
                // Map from request
            };
            _mockService
                .Setup(x => x.CreateAsync(It.IsAny<Create{ModelName}Request>()))
                .ReturnsAsync(createdItem);

            // Act
            var result = await _controller.Create(request);

            // Assert
            var createdResult = result.Result.Should().BeOfType<CreatedAtActionResult>().Subject;
            createdResult.ActionName.Should().Be(nameof(_controller.GetById));
            var returnedItem = createdResult.Value.Should().BeAssignableTo<{ModelName}>().Subject;
            returnedItem.Id.Should().Be(createdItem.Id);
        }

        [Fact]
        public async Task Create_InvalidModelState_ReturnsBadRequest()
        {
            // Arrange
            _controller.ModelState.AddModelError("Property", "Error message");
            var request = new Create{ModelName}Request();

            // Act
            var result = await _controller.Create(request);

            // Assert
            result.Result.Should().BeOfType<BadRequestObjectResult>();
        }

        #endregion

        #region PUT Tests

        [Fact]
        public async Task Update_ValidRequest_ReturnsOkResult()
        {
            // Arrange
            var id = Guid.NewGuid();
            var request = new Update{ModelName}Request
            {
                // Set properties
            };
            var updatedItem = new {ModelName}
            {
                Id = id,
                // Map from request
            };
            _mockService
                .Setup(x => x.UpdateAsync(id, It.IsAny<Update{ModelName}Request>()))
                .ReturnsAsync(updatedItem);

            // Act
            var result = await _controller.Update(id, request);

            // Assert
            var okResult = result.Result.Should().BeOfType<OkObjectResult>().Subject;
            var returnedItem = okResult.Value.Should().BeAssignableTo<{ModelName}>().Subject;
            returnedItem.Id.Should().Be(id);
        }

        [Fact]
        public async Task Update_NonExistentId_ReturnsNotFound()
        {
            // Arrange
            var id = Guid.NewGuid();
            var request = new Update{ModelName}Request();
            _mockService
                .Setup(x => x.UpdateAsync(id, It.IsAny<Update{ModelName}Request>()))
                .ReturnsAsync(({ModelName}?)null);

            // Act
            var result = await _controller.Update(id, request);

            // Assert
            result.Result.Should().BeOfType<NotFoundResult>();
        }

        #endregion

        #region DELETE Tests

        [Fact]
        public async Task Delete_ValidId_ReturnsNoContent()
        {
            // Arrange
            var id = Guid.NewGuid();
            _mockService
                .Setup(x => x.DeleteAsync(id))
                .ReturnsAsync(true);

            // Act
            var result = await _controller.Delete(id);

            // Assert
            result.Should().BeOfType<NoContentResult>();
        }

        [Fact]
        public async Task Delete_NonExistentId_ReturnsNotFound()
        {
            // Arrange
            var id = Guid.NewGuid();
            _mockService
                .Setup(x => x.DeleteAsync(id))
                .ReturnsAsync(false);

            // Act
            var result = await _controller.Delete(id);

            // Assert
            result.Should().BeOfType<NotFoundResult>();
        }

        #endregion

        #region Exception Handling Tests

        [Fact]
        public async Task GetAll_ServiceThrowsException_ReturnsInternalServerError()
        {
            // Arrange
            _mockService
                .Setup(x => x.GetAllAsync())
                .ThrowsAsync(new Exception("Database error"));

            // Act
            Func<Task> act = async () => await _controller.GetAll();

            // Assert
            await act.Should().ThrowAsync<Exception>();
            _mockLogger.Verify(
                x => x.Log(
                    LogLevel.Error,
                    It.IsAny<EventId>(),
                    It.IsAny<It.IsAnyType>(),
                    It.IsAny<Exception>(),
                    It.IsAny<Func<It.IsAnyType, Exception?, string>>()),
                Times.Once);
        }

        #endregion
    }
}
