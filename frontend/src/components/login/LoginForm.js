import { useForm } from 'react-hook-form';
import { CardTitle, CardDescription, CardHeader, CardContent, CardFooter, Card } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useDispatch } from 'react-redux';
import { loginUser } from '../features/auth/authSlice'; // Update the import path according to your project structure

export default function LoginComponent() {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const dispatch = useDispatch();

  const onSubmit = data => {
    // Dispatch the login action
    dispatch(loginUser(data));
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <form onSubmit={handleSubmit(onSubmit)}>
        <CardHeader className="space-y-2">
          <CardTitle className="text-3xl font-bold">Login</CardTitle>
          <CardDescription>Enter your email and password below to login to your account.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input id="email" placeholder="m@example.com" required type="email" {...register("email", { required: true })} />
            {errors.email && <p className="text-red-500">Email is required</p>}
          </div>
          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input id="password" required type="password" {...register("password", { required: true })} />
            {errors.password && <p className="text-red-500">Password is required</p>}
          </div>
        </CardContent>
        <CardFooter className="flex">
          <Button type="submit" className="ml-auto">Sign in</Button>
        </CardFooter>
      </form>
    </Card>
  );
}