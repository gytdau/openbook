import React from 'react';
import { render, screen } from '@testing-library/react';
import Home from '../../Home/Home';
import axios from 'axios';
import HomepageRecommendations from '../fixtures/homepage_recommendations.json';
import { act } from 'react-dom/test-utils';
import { MemoryRouter } from 'react-router-dom';

jest.mock("axios");

it('shows the footer', async () => {
  axios.get.mockResolvedValue({ data: HomepageRecommendations })
  await act(async () => {
    render(<MemoryRouter><Home /></MemoryRouter>);
    await screen.getByText(/Gytis Daujotas/);
    await screen.getByText(/Sayed Mahmood Alawi/);
  })
});

it('has moby dick', async () => {
  axios.get.mockResolvedValue({ data: HomepageRecommendations })
  await act(async () => {
    render(<MemoryRouter><Home /></MemoryRouter>);
    await new Promise(process.nextTick);
  })
  await screen.findByText(/Moby Dick; Or, The Whale/);
});
