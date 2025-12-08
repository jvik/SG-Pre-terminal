import { describe, it, expect, vi } from 'vitest';
import { render, fireEvent } from '@testing-library/svelte';
import LoginPage from './+page.svelte';
import { authStore } from '$lib/stores/auth';
import { goto } from '$app/navigation';

// Mock the authStore
vi.mock('$lib/stores/auth', () => {
  return {
    authStore: {
      login: vi.fn(),
      subscribe: vi.fn(() => () => {}), // Mock subscribe to do nothing
    },
  };
});

// Mock the goto function
vi.mock('$app/navigation', () => ({
  goto: vi.fn(),
}));

describe('LoginPage', () => {
  it('renders the login form', () => {
    const { getByLabelText, getByRole } = render(LoginPage);

    expect(getByLabelText('Email')).toBeInTheDocument();
    expect(getByLabelText('Password')).toBeInTheDocument();
    expect(getByRole('button', { name: /login/i })).toBeInTheDocument();
  });

  it('calls authStore.login on form submission with correct credentials', async () => {
    const { getByLabelText, getByRole } = render(LoginPage);

    const emailInput = getByLabelText('Email');
    const passwordInput = getByLabelText('Password');
    const loginButton = getByRole('button', { name: /login/i });

    await fireEvent.input(emailInput, { target: { value: 'test@example.com' } });
    await fireEvent.input(passwordInput, { target: { value: 'password123' } });
    await fireEvent.click(loginButton);

    expect(authStore.login).toHaveBeenCalledWith('test@example.com', 'password123');
  });

  it('redirects to /dashboard on successful login', async () => {
    authStore.login.mockResolvedValueOnce(); // Simulate successful login

    const { getByLabelText, getByRole } = render(LoginPage);

    const emailInput = getByLabelText('Email');
    const passwordInput = getByLabelText('Password');
    const loginButton = getByRole('button', { name: /login/i });

    await fireEvent.input(emailInput, { target: { value: 'test@example.com' } });
    await fireEvent.input(passwordInput, { target: { value: 'password123' } });
    await fireEvent.click(loginButton);

    // Need to wait for the async handleSubmit to complete
    await new Promise((resolve) => setTimeout(resolve, 0));

    expect(goto).toHaveBeenCalledWith('/dashboard');
  });

  it('displays an error message on failed login', async () => {
    const errorMessage = 'Invalid credentials';
    authStore.login.mockRejectedValueOnce(new Error(errorMessage));

    const { getByLabelText, getByRole, findByText } = render(LoginPage);

    const emailInput = getByLabelText('Email');
    const passwordInput = getByLabelText('Password');
    const loginButton = getByRole('button', { name: /login/i });

    await fireEvent.input(emailInput, { target: { value: 'wrong@example.com' } });
    await fireEvent.input(passwordInput, { target: { value: 'wrongpassword' } });
    await fireEvent.click(loginButton);

    const errorElement = await findByText(errorMessage);
    expect(errorElement).toBeInTheDocument();
  });
});
