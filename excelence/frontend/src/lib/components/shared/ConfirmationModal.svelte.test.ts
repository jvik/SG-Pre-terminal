import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/svelte';
import userEvent from '@testing-library/user-event';
import ConfirmationModal from './ConfirmationModal.svelte';

describe('ConfirmationModal', () => {
    it('does not render when isOpen is false', () => {
        render(ConfirmationModal, {
            props: {
                isOpen: false,
                message: 'Are you sure?',
                onConfirm: vi.fn(),
                onCancel: vi.fn()
            }
        });

        expect(screen.queryByText('Confirm Action')).not.toBeInTheDocument();
    });

    it('renders correctly when isOpen is true', () => {
        render(ConfirmationModal, {
            props: {
                isOpen: true,
                message: 'Are you sure?',
                onConfirm: vi.fn(),
                onCancel: vi.fn()
            }
        });

        expect(screen.getByText('Confirm Action')).toBeInTheDocument();
        expect(screen.getByText('Are you sure?')).toBeInTheDocument();
        expect(screen.getByText('Confirm')).toBeInTheDocument();
        expect(screen.getByText('Cancel')).toBeInTheDocument();
    });

    it('calls onConfirm when confirm button is clicked', async () => {
        const user = userEvent.setup();
        const onConfirm = vi.fn();
        render(ConfirmationModal, {
            props: {
                isOpen: true,
                message: 'Are you sure?',
                onConfirm,
                onCancel: vi.fn()
            }
        });

        await user.click(screen.getByText('Confirm'));
        expect(onConfirm).toHaveBeenCalled();
    });

    it('calls onCancel when cancel button is clicked', async () => {
        const user = userEvent.setup();
        const onCancel = vi.fn();
        render(ConfirmationModal, {
            props: {
                isOpen: true,
                message: 'Are you sure?',
                onConfirm: vi.fn(),
                onCancel
            }
        });

        await user.click(screen.getByText('Cancel'));
        expect(onCancel).toHaveBeenCalled();
    });
});
