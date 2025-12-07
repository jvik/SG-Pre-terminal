import { render, screen, fireEvent } from '@testing-library/svelte';
import { describe, it, expect, vi } from 'vitest';
import Sidebar from './Sidebar.svelte';
import { readable } from 'svelte/store';

// Mock $app/stores
vi.mock('$app/stores', () => {
	return {
		page: {
			subscribe: (fn: (value: any) => void) => {
				fn({ url: { pathname: '/dashboard' } });
				return () => {};
			}
		}
	};
});

describe('Sidebar Component', () => {
	it('renders the sidebar with correct links', () => {
		render(Sidebar);

		expect(screen.getByText('Excelence')).toBeInTheDocument();
		expect(screen.getByText('Dashboard')).toBeInTheDocument();
		expect(screen.getByText('Spreadsheet')).toBeInTheDocument();
		expect(screen.getByText('Settings')).toBeInTheDocument();
	});

	it('highlights the active link based on current path', () => {
		render(Sidebar);
		// We mocked pathname as '/dashboard'
		const dashboardLink = screen.getByText('Dashboard').closest('a');
		expect(dashboardLink).toHaveClass('text-blue-600');
		expect(dashboardLink).toHaveClass('bg-blue-50');

		const settingsLink = screen.getByText('Settings').closest('a');
		// Should not have active classes
		expect(settingsLink).not.toHaveClass('text-blue-600');
		expect(settingsLink).not.toHaveClass('bg-blue-50');
	});

	it('toggles sidebar on mobile when hamburger is clicked', async () => {
		const { container } = render(Sidebar);
		const sidebar = screen.getByLabelText('Sidebar');
		const toggleButton = screen.getByRole('button', { name: /open sidebar/i });

		// Initially closed on mobile (has -translate-x-full)
		expect(sidebar).toHaveClass('-translate-x-full');
		expect(sidebar).not.toHaveClass('translate-x-0');

		// Click to open
		await fireEvent.click(toggleButton);

		// Now open
		expect(sidebar).toHaveClass('translate-x-0');
		expect(sidebar).not.toHaveClass('-translate-x-full');

		// Overlay should be visible
		const overlay = container.querySelector('.fixed.inset-0.z-30');
		expect(overlay).toBeInTheDocument();

		// Click overlay to close
		if (overlay) {
			await fireEvent.click(overlay);
		}
		expect(sidebar).toHaveClass('-translate-x-full');
	});
});
