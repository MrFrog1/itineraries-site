import React from 'react';
import { useForm, Controller } from 'react-hook-form';
import countries from './countries'; // Ensure this path is correct
import interests from './interests'; // Ensure this path is correct
import { Card, CardHeader, CardContent, CardTitle, CardDescription } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select";
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem } from "@/components/ui/dropdown-menu";
import { useRegisterUserMutation } from '../../../services/api'; // Ensure this path is correct
import { useNavigate } from 'react-router-dom';

export default function SubscribeForm() {
    const { register, handleSubmit, control, watch, formState: { errors } } = useForm();
    const [registerUser, { isLoading }] = useRegisterUserMutation();
    const navigate = useNavigate();
    const password = watch('password'); // Watch the password value to compare with confirmation

    const onSubmit = async (data) => {
        const { passwordConfirm, ...formData } = data; // Exclude passwordConfirm from data sent to backend
        try {
            const result = await registerUser(formData).unwrap();
            console.log('Registration successful', result);
            navigate('/login');
        } catch (error) {
            console.error('Registration failed', error);
        }
    };

    return (
        <Card className="w-full max-w-md mx-auto">
            <form onSubmit={handleSubmit(onSubmit)}>
                <CardHeader className="text-center">
                    <CardTitle>Subscribe</CardTitle>
                    <CardDescription>
                        Want to register as an agent? Email us at 
                        <a href="mailto:theindusrivercamp@gmail.com" className="underline"> here</a>.
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="space-y-2">
                        <Label htmlFor="username">Username</Label>
                        <Input id="username" placeholder="Username" {...register("username", { required: "Username is required", validate: value => !value.includes('@') })} />
                        {errors.username && <p className="text-red-500">{errors.username.message}</p>}
                    </div>
                    <div className="space-y-2">
                        <Label htmlFor="email">Email</Label>
                        <Input id="email" placeholder="Email" {...register("email", { required: "Email is required", pattern: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i })} />
                        {errors.email && <p className="text-red-500">{errors.email.message}</p>}
                    </div>
                    <div className="space-y-2">
                        <Label htmlFor="password">Password</Label>
                        <Input id="password" placeholder="Password" type="password" {...register("password", { required: "Password is required", minLength: { value: 8, message: "Password must be at least 8 characters" } })} />
                        {errors.password && <p className="text-red-500">{errors.password.message}</p>}
                    </div>
                    <div className="space-y-2">
                        <Label htmlFor="passwordConfirm">Retype Password</Label>
                        <Input id="passwordConfirm" placeholder="Retype Password" type="password" {...register("passwordConfirm", { 
                            validate: value => value === password || "Passwords do not match" 
                        })} />
                        {errors.passwordConfirm && <p className="text-red-500">{errors.passwordConfirm.message}</p>}
                    </div>

                    {/* Country and Interests components remain unchanged */}
                    <div className="space-y-2">
                        <Label>Country</Label>
                        <Controller
                            name="country"
                            control={control}
                            rules={{ required: 'Country is required' }}
                            render={({ field: { onChange, value, ref } }) => (
                                <Select onValueChange={val => onChange(val)} value={value} ref={ref}>
                                    <SelectTrigger>
                                        <SelectValue placeholder="Select country" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        {countries.map((country, index) => (
                                            <SelectItem key={index} value={country}>
                                                {country}
                                            </SelectItem>
                                        ))}
                                    </SelectContent>
                                </Select>
                            )}
                        />
                        {errors.country && <p className="text-red-500">{errors.country.message}</p>}
                    </div>
                    {/* Interests section remains unchanged */}
                    <Button className="w-full" type="submit" disabled={isLoading}>
                        {isLoading ? 'Subscribing...' : 'Subscribe'}
                    </Button>
                </CardContent>
            </form>
        </Card>
    );
}
