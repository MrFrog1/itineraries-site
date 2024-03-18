/**
 * v0 by Vercel.
 * @see https://v0.dev/t/mRPAcGWUZZN
 * Documentation: https://v0.dev/docs#integrating-generated-code-into-your-nextjs-app
 */
import { Input } from "@/components/ui/input"
import { Checkbox } from "@/components/ui/checkbox"
import Link from "next/link"
import { Button } from "@/components/ui/button"

export default function Component() {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
      <div className="bg-white p-8 rounded-lg max-w-md w-full mx-4">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-semibold">Send Me Fascinating Itineraries</h2>
          <button className="text-xl font-semibold">
            <PanelTopCloseIcon className="w-6 h-6" />
          </button>
        </div>
        <form>
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div className="flex flex-col">
              <label className="font-medium" htmlFor="firstName">
                Name
              </label>
              <Input id="firstName" placeholder="Name" />
            </div>
            <div className="flex flex-col">
              <label className="font-medium" htmlFor="email">
                Email Address *
              </label>
              <Input id="email" placeholder="Email Address" type="email" />
            </div>
          </div>
          <div className="flex items-center mb-6">
            <Checkbox id="privacyPolicy" />
            <label className="ml-2 text-sm" htmlFor="privacyPolicy">
              I accept the
              <Link className="text-blue-600" href="#">
                Privacy & Cookie Policy
              </Link>
            </label>
          </div>
          <Button className="w-full">SIGN UP</Button>
        </form>
      </div>
    </div>
  )
}

function PanelTopCloseIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <rect width="18" height="18" x="3" y="3" rx="2" ry="2" />
      <line x1="3" x2="21" y1="9" y2="9" />
      <path d="m9 16 3-3 3 3" />
    </svg>
  )
}
