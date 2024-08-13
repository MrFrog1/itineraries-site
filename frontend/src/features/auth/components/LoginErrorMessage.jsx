// src/components/auth/LoginErrorMessage.jsx
import React from 'react';

export const LoginErrorMessage = ({ error }) => {
  if (!error) return null;

  let errorMessage = 'An unexpected error occurred. Please try again.';

  if (error.status === 400) {
    errorMessage = 'Invalid username or password. Please try again.';
  } else if (error.status === 401) {
    errorMessage = 'You are not authorized. Please check your credentials.';
  }

  return <p className="text-red-500 text-sm mt-2">{errorMessage}</p>;
};

