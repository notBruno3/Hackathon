// tests/App.spec.js
import { describe, it, expect } from 'vitest';

describe('App.vue', () => {
  it('dummy test: 1 + 3 === 4', () => {
    // Arrange
    const a = 1;
    const b = 3;

    // Act
    const result = a + b;

    // Assert
    expect(result).toBe(4);
  });
});
