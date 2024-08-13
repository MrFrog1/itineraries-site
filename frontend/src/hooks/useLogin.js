// src/hooks/useLogin.js
import { useLoginUserMutation } from '../services/api';
import { useDispatch } from 'react-redux';
import { setUser } from '../features/auth/authSlice';
import { useState } from 'react';

export const useLogin = (navigate) => {
  const [loginUser] = useLoginUserMutation();
  const dispatch = useDispatch();
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isError, setIsError] = useState(false);

  const login = async (credentials) => {
    setIsLoading(true);
    setError(null);
    setIsError(false);

    try {

      const result = await loginUser({
        username: credentials.usernameOrEmail,
        password: credentials.password,
        grant_type: 'password',
        client_id: 'Azi3XQLAUoEXJpYAO9A17FtXATlAK11bIeMlUOmM',
        client_secret: 'pbkdf2_sha256$260000$OVF2LXnBmqlNFA8fgXCqoH$XHwESHTxVcidwk1bT5ZcBm9ulj+2bbO+XD4u5hH3Gko=',
      }).unwrap();


      dispatch(setUser(result));

      if (navigate) {
        navigate('/');
      }
      return true;
    } catch (error) {
      setError(error);
      setIsError(true);
      return false;
    } finally {
      setIsLoading(false);
    }
  };

  return { login, error, isError, isLoading };
};