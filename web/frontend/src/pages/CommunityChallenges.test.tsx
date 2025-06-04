import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import CommunityChallenges from './CommunityChallenges';

vi.mock('../services/api', () => ({
  getCommunityChallenges: () => Promise.resolve([
    { id: 1, name: 'Test', target_minutes: 100, start_date: '', end_date: '' }
  ]),
  joinCommunityChallenge: vi.fn()
}));

describe('CommunityChallenges page', () => {
  it('renders list of challenges', async () => {
    render(<CommunityChallenges />);
    expect(await screen.findByText(/Test/)).toBeInTheDocument();
  });
});
