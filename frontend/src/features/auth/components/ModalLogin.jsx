import React from 'react';
import { useForm } from 'react-hook-form';
import { useLogin } from '../../../hooks/useLogin';
import { LoginErrorMessage } from './LoginErrorMessage';
import { DialogTrigger, DialogTitle, DialogDescription, DialogHeader, DialogFooter, DialogContent, Dialog } from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Link } from 'react-router-dom';

export default function ModalLogin() {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const { login, error, isLoading } = useLogin();

  const onSubmit = (data) => {
    login(data);
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
          </div>
          <LoginErrorMessage error={error} />
          <DialogFooter>
            <Button type="submit" disabled={isLoading}>
              {isLoading ? 'Logging in...' : 'Sign in'}
            </Button>
          </DialogFooter>
          <DialogFooter className="text-center">
            Not Registered? 
            <Link to="/register" className="underline ml-1">
              Subscribe Here
            </Link>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}