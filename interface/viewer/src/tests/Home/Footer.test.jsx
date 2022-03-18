import React from 'react';
import { render, screen } from '@testing-library/react';
import Footer from '../../Home/Footer';

it('footer renders with credit', async () => {
  render(<Footer />);
  await screen.getByText(/Gytis Daujotas/);
  await screen.getByText(/Sayed Mahmood Alawi/);
});
