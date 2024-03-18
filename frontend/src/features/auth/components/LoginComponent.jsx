import React from 'react';
import { useForm } from 'react-hook-form';
import { useLoginUserMutation } from '../../../services/api'; // Correct path as necessary
import { useNavigate, useLocation } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { setUser } from '../authSlice'; // Correct path as necessary
import { Card, CardHeader, CardContent, CardFooter, CardTitle, CardDescription } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export default function LoginComponent() {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const [loginUser, { isLoading, isError, error }] = useLoginUserMutation(); // Ensure isError is being correctly destructured here
  const navigate = useNavigate();
  const location = useLocation();
  const dispatch = useDispatch();

  const from = location.state?.from?.pathname || '/';
    const onSubmit = async (data) => {
    const { usernameOrEmail, password } = data;
    const credentials = {
        password,
        ...(usernameOrEmail.includes('@') ? { email: usernameOrEmail } : { username: usernameOrEmail }),
    };

    try {
        const result = await loginUser(credentials).unwrap();

        // Extract user info; the backend should handle tokens
        // Since we're not using the tokens on the client-side directly, except for the access token if necessary.
        const { access, ...userInfo } = result; // Assuming 'access' is your access token

        // Dispatch setUser action with user info. Assuming your backend returns user info separately from tokens
        dispatch(setUser({
            user: userInfo, // Contains all user details excluding tokens
            token: access, // Only the access token is needed if you're using it client-side for API requests
        }));

        // Redirect after successful login
        navigate(from, { replace: true });
    } catch (error) {
        console.error('Login failed', error);
        // Here you could handle specific login errors, show messages to the user, etc.
    }
};

  return (
    <Card className="w-full max-w-md mx-auto">
      <form onSubmit={handleSubmit(onSubmit)}>
        <CardHeader className="space-y-2">
          <CardTitle className="text-3xl font-bold">Login</CardTitle>
          <CardDescription>
            Not Registered? Subscribe&nbsp;
            <span className="underline">Here</span>
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="usernameOrEmail">Username or Email</Label>
            <Input 
              id="usernameOrEmail" 
              placeholder="Username or email@example.com" 
              {...register("usernameOrEmail", {
                required: "Username or Email is required",
                pattern: {
                  value: /^(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])|[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$/,
                  message: "Invalid username or email"
                }
              })}
            />
            {errors.usernameOrEmail && <p className="text-red-500">{errors.usernameOrEmail.message}</p>}
          </div>
          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input 
              id="password" 
              type="password" 
              {...register("password", {
                required: "Password is required",
                minLength: {
                  value: 3,
                  message: "Password must be at least 3 characters"
                }
              })}
            />
            {errors.password && <p className="text-red-500">{errors.password.message}</p>}
          </div>
        </CardContent>
        <CardFooter className="flex justify-center">
          <Button type="submit" disabled={isLoading}>
            {isLoading ? 'Logging in...' : 'Sign in'}
          </Button>
        </CardFooter>
        {isError && (
          <CardFooter className="text-red-500 text-center">
            {error?.data?.detail || 'Failed to login. Please try again.'}
          </CardFooter>
        )}
      </form>
    </Card>
  );
}
