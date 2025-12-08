import { render, fireEvent, screen, waitFor } from '@testing-library/svelte';
import Register from './+page.svelte';
import { describe, it, expect, vi, beforeEach } from 'vitest';

// Mock the $app/navigation module
vi.mock('$app/navigation', () => ({
  goto: vi.fn(),
}));

// Mock the API service
vi.mock('$lib/services/api', () => ({
  registerUser: vi.fn(),
}));

describe('Register Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders the registration form', () => {
    render(Register);
    expect(screen.getByLabelText('Email')).toBeInTheDocument();
    expect(screen.getByLabelText('Password')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Register' })).toBeInTheDocument();
  });

  it('shows an error message for short passwords', async () => {
    render(Register);

    const emailInput = screen.getByLabelText('Email');
    const passwordInput = screen.getByLabelText('Password');

    await fireEvent.input(emailInput, { target: { value: 'test@example.com' } });
    await fireEvent.input(passwordInput, { target: { value: 'short' } });

    const form = screen.getByRole('button', { name: 'Register' }).closest('form');
    await fireEvent.submit(form!);

    await waitFor(() => {
      expect(screen.getByText('Password must be at least 8 characters long.')).toBeInTheDocument();
    });
  });
});
