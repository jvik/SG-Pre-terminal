import { render, screen } from '@testing-library/svelte';
import { describe, it, expect, vi } from 'vitest';
import SpendingChart from './SpendingChart.svelte';

// Mock Chart.js
vi.mock('chart.js/auto', () => {
  return {
    default: class MockChart {
        data: any;
        constructor(ctx: any, config: any) {
            this.data = config.data;
        }
        update() {}
        destroy() {}
    }
  };
});

describe('SpendingChart Component', () => {
  const mockData = [
      { category_name: 'Food', total_amount: 100 },
      { category_name: 'Transport', total_amount: 50 }
  ];

  it('renders without crashing', () => {
    render(SpendingChart, { chartData: mockData });
    // Since it's a canvas, we can't check for text easily inside the canvas.
    // But we can check if the container renders.
    const canvas = document.querySelector('canvas');
    expect(canvas).toBeInTheDocument();
  });

  it('displays "No expense data" when data is empty', () => {
    render(SpendingChart, { chartData: [] });
    expect(screen.getByText('No expense data')).toBeInTheDocument();
  });
});
