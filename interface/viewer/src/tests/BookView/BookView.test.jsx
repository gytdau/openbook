import React from 'react';
import { render, screen } from '@testing-library/react';
import Book from '../../Book/Book';
import axios from 'axios';
import BookResponse from '../fixtures/moby-dick-or-the-whale_32.json'
import { act } from 'react-dom/test-utils';
import { MemoryRouter, useParams } from 'react-router-dom';
import { InView } from 'react-intersection-observer';

jest.mock("axios");
jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useParams: () => ({
    slug: "moby-dick-or-the-whale_32",
    chapterSlug: "moby-dick-or-the-whale"
  })
}));

beforeEach(() => {
  axios.get.mockResolvedValue({ data: BookResponse })

  const mockIntersectionObserver = jest.fn();
  mockIntersectionObserver.mockReturnValue({
    observe: () => null,
    unobserve: () => null,
    disconnect: () => null
  });
  window.IntersectionObserver = mockIntersectionObserver;
});

it("has a title", async () => {
  await act(async () => {
    render(<MemoryRouter><Book /></MemoryRouter>);
    await new Promise(process.nextTick);
  })
  await screen.findAllByText(/Moby Dick; Or, The Whale/);
})

it("allows the Table of Contents to be opened", async () => {
  await act(async () => {
    render(<MemoryRouter><Book /></MemoryRouter>);
    await new Promise(process.nextTick);
  })
  const button = await screen.findByTestId("open-toc");
  expect(button).toBeInTheDocument();
  button.click();
  await screen.findByText(/Table of Contents/);
  const close = await screen.findByTestId("close-toc");
  expect(close).toBeInTheDocument();
  close.click();
  await screen.findAllByText(/Moby Dick; Or, The Whale/);
});