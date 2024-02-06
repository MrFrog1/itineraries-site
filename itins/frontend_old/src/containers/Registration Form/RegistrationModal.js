**
 * v0 by Vercel.
 * @see https://v0.dev/t/fY5or456aOt
 */
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import Link from "next/link"

export default function Component() {
  return (
    <div className="mx-auto max-w-[350px] space-y-6">
      <div className="space-y-2 text-center">
        <h1 className="text-3xl font-bold">Register</h1>
        <p className="text-gray-500 dark:text-gray-400">Join our travel community and start exploring</p>
      </div>
      <div>
        <div className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="username">Username</Label>
            <Input id="username" placeholder="Choose a username" required />
          </div>
          <div className="space-y-2">
            <Label htmlFor="name">Name</Label>
            <Input id="name" placeholder="Enter your name" required />
          </div>
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input id="email" placeholder="Enter your email" required type="email" />
          </div>
          <div className="space-y-2">
            <Label htmlFor="phone">Phone Number (Optional)</Label>
            <Input id="phone" placeholder="Enter your phone number" type="tel" />
          </div>
          <Button className="w-full" type="submit">
            Register
          </Button>
        </div>
        <Separator className="my-8" />
        <div className="space-y-4">
          <Button className="w-full" variant="outline">
            Register with Google
          </Button>
          <Button className="w-full" variant="outline">
            Register with Facebook
          </Button>
          <div className="mt-4 text-center text-sm">
            Want to register as an agent?
            <Link className="underline" href="#">
              Click here
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}

s