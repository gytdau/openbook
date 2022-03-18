import React from 'react';
import { render, screen } from '@testing-library/react';
import Home from '../../Home/Home';
import axios from 'axios';
import HomepageRecommendations from '../fixtures/homepage_recommendations.json';
import { act } from 'react-dom/test-utils';
import { MemoryRouter } from 'react-router-dom';

jest.mock("axios");

beforeEach(() => {
  axios.get.mockResolvedValue({ data: HomepageRecommendations })
});

it('shows the footer', async () => {
  await act(async () => {
    render(<MemoryRouter><Home /></MemoryRouter>);
    await screen.getByText(/Gytis Daujotas/);
    await screen.getByText(/Sayed Mahmood Alawi/);
  })
});

it('has moby dick', async () => {
  await act(async () => {
    render(<MemoryRouter><Home /></MemoryRouter>);
    await new Promise(process.nextTick);
  })
  await screen.findByText(/Moby Dick; Or, The Whale/);
});

it('links books to the correct location', async () => {
  await act(async () => {
    render(<MemoryRouter><Home /></MemoryRouter>);
    await new Promise(process.nextTick);
  })
  const link = await screen.findByText(/Moby Dick; Or, The Whale/);
  expect(link.closest("a")).toHaveAttribute('href', '/moby-dick-or-the-whale_32');
});

it("has a search bar", async () => {
  await act(async () => {
    render(<MemoryRouter><Home /></MemoryRouter>);
    await new Promise(process.nextTick);
  })
  await screen.findByPlaceholderText(/Search books/);
});



it("has categories displayed", async () => {
  await act(async () => {
    render(<MemoryRouter><Home /></MemoryRouter>);
    await new Promise(process.nextTick);
  })
  await screen.findByText(/Top 5 Books/);
  await screen.findByText(/Most Read/);
  await screen.findByText(/Explore the Harvard Classics/);
});

it("has a masthead", async () => {
  await act(async () => {
    render(<MemoryRouter><Home /></MemoryRouter>);
    await new Promise(process.nextTick);
  })
  await screen.findByText(/Great ideas/);
  await screen.findByText(/Read free books in the public domain./);
});