import React from 'react';
import { useForm } from 'react-hook-form';
import { useLoginUserMutation } from '../../../services/api'; // Correct path as necessary
import { useDispatch } from 'react-redux';
import { setUser } from '../authSlice'; // Correct path as necessary
import { DialogTrigger, DialogTitle, DialogDescription, DialogHeader, DialogFooter, DialogContent, Dialog } from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Link } from 'react-router-dom';

export default function ModalLogin() {
    const { register, handleSubmit, formState: { errors } } = useForm();
    const [loginUser, { isLoading, isError, error }] = useLoginUserMutation();
    const dispatch = useDispatch();

    const onSubmit = async (data) => {
        const { email, password } = data;
        const credentials = {
            password,
            ...(email.includes('@') ? { email } : { username: email }),
        };

        try {
            const result = await loginUser(credentials).unwrap();
            const { access, ...userInfo } = result; // Extract user info and access token
            dispatch(setUser({
                user: userInfo,
                token: access, // Only the access token is needed if you're using it client-side for API requests
            }));
        } catch (error) {
            console.error('Login failed', error);
        }
    };

    return (
        <Dialog>
            <DialogTrigger asChild>
                <Button variant="outline">Login</Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
                <form onSubmit={handleSubmit(onSubmit)}>
                    <DialogHeader>
                        <DialogTitle>Login</DialogTitle>
                        <DialogDescription>Enter your details below to login to your account.</DialogDescription>
                    </DialogHeader>
                    <div className="grid gap-4 py-4">
                        <div className="space-y-2">
                            <Label htmlFor="email">Username or Email</Label>
                            <Input id="email" 
                                placeholder="Username or email@example.com" 
                                {...register("email", {
                                    required: "Username or Email is required",
                                    pattern: {
                                        value: /^(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])|[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$/,
                                        message: "Invalid username or email"
                                    }
                                })}
                            />
                            {errors.email && <p className="text-red-500">{errors.email.message}</p>}
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="password">Password</Label>
                            <Input id="password" 
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
                    </div>
                    <DialogFooter>
                        <Button type="submit" disabled={isLoading}>
                            {isLoading ? 'Logging in...' : 'Sign in'}
                        </Button>
                    </DialogFooter>
                    {isError && (
                        <DialogFooter className="text-red-500">
                            {error?.data?.detail || 'Failed to login. Please try again.'}
                        </DialogFooter>
                    )}
                    <DialogFooter className="text-center">
                        Not Registered? 
                        <Link to="/register" className="underline">
                            Subscribe Here
                        </Link>
                    </DialogFooter>
                </form>
            </DialogContent>
        </Dialog>
    );
}
