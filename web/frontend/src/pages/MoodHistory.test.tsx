import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import MoodHistory from './MoodHistory';

vi.mock('../services/api', () => ({
  getMoodHistory: () => Promise.resolve([
    { before: 3, after: 7 }
  ])
}));

describe('MoodHistory page', () => {
  it('shows mood entries', async () => {
    render(<MoodHistory />);
    expect(await screen.findByText('3 → 7')).toBeInTheDocument();
  });
});
