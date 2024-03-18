/**
 * v0 by Vercel.
 * @see https://v0.dev/t/9xYI7gWNXf5
 * Documentation: https://v0.dev/docs#integrating-generated-code-into-your-nextjs-app
 */
export default function Component() {
  return (
    <div className="w-full py-6 bg-cream-texture">
      <div className="container grid md:gap-6 px-4 md:px-6">
        <div className="grid gap-6 lg:grid-cols-2 xl:gap-12">
          <div className="flex flex-col gap-4">
            <div className="flex flex-col gap-2">
              <h1 className="text-3xl font-bold tracking-tighter sm:text-5xl text-maroon dark:text-blue-400 border-b border-gray-200 dark:border-gray-800 pb-2">
                Emily Parker
              </h1>
              <div className="flex items-center gap-2">
                <CalendarIcon className="h-4 w-4 text-green-500" />
                <span className="text-sm text-gray-500 dark:text-gray-400">Joined in August 2019</span>
              </div>
              <div className="flex items-center gap-2">
                <BriefcaseIcon className="h-4 w-4 text-blue-500" />
                <span className="text-sm text-gray-500 dark:text-gray-400">Sustainable Travel Co.</span>
              </div>
              <div className="flex items-center gap-2">
                <StarIcon className="h-4 w-4 text-yellow-500" />
                <span className="text-sm text-gray-500 dark:text-gray-400">4.5 (23 reviews)</span>
              </div>
              <div className="flex items-center gap-2">
                <LinkIcon className="h-4 w-4 text-purple-500" />
                <a
                  className="text-sm text-blue-600 dark:text-blue-400 underline"
                  href="#"
                  rel="noopener noreferrer"
                  target="_blank"
                >
                  Website
                </a>
              </div>
              <div className="flex items-center gap-2">
                <InstagramIcon className="h-4 w-4 text-pink-500" />
                <a
                  className="text-sm text-blue-600 dark:text-blue-400 underline"
                  href="#"
                  rel="noopener noreferrer"
                  target="_blank"
                >
                  Instagram
                </a>
              </div>
            </div>
            <div className="grid gap-2">
              <div className="inline-block rounded-lg bg-yellow-100 px-3 py-1 text-sm dark:bg-gray-800 w-1/2">
                Sustainable Travel Expert
              </div>
              <div className="inline-block rounded-lg bg-yellow-100 px-3 py-1 text-sm dark:bg-gray-800 w-1/2">
                Adventure Enthusiast
              </div>
            </div>
            <div className="grid gap-4 md:gap-8">
              <div className="space-y-2 text-base/relaxed">
                <p>
                  Emily is passionate about sustainable travel and eco-tourism. She believes that travel can be a force
                  for good and works with local communities to create authentic experiences that benefit both travelers
                  and the destinations.
                </p>
              </div>
              <div className="space-y-2 text-base/relaxed">
                <p>
                  Emily Parker is a sustainable travel expert with over a decade of experience in the tourism industry.
                  She has explored remote corners of the world and is dedicated to promoting responsible and ethical
                  travel practices.
                </p>
              </div>
            </div>
            <details>
              <summary className="text-blue-600 cursor-pointer dark:text-blue-400">Read More</summary>
              <div className="grid gap-4 md:gap-8">
                <div className="space-y-2 text-base/relaxed">
                  <p>
                    Emily is passionate about sustainable travel and eco-tourism. She believes that travel can be a
                    force for good and works with local communities to create authentic experiences that benefit both
                    travelers and the destinations.
                  </p>
                </div>
                <div className="space-y-2 text-base/relaxed">
                  <p>
                    Emily Parker is a sustainable travel expert with over a decade of experience in the tourism
                    industry. She has explored remote corners of the world and is dedicated to promoting responsible and
                    ethical travel practices.
                  </p>
                </div>
              </div>
            </details>
          </div>
          <div className="flex items-start">
            <span className="w-full max-w-sm border aspect-video rounded-md bg-muted" />
          </div>
        </div>
        <div className="grid gap-6 md:grid-cols-2">
          <div className="flex flex-col gap-2">
            <h3 className="text-2xl font-bold tracking-tighter sm:text-3xl border-b border-gray-200 dark:border-gray-800 pb-2">
              Itineraries
            </h3>
            <div className="flex gap-6">
              <div className="flex items-center gap-4">
                <img
                  alt="Image"
                  className="rounded-lg object-cover"
                  height="100"
                  src="/placeholder.svg"
                  style={{
                    aspectRatio: "100/100",
                    objectFit: "cover",
                  }}
                  width="100"
                />
                <div className="flex flex-col gap-1">
                  <h4 className="font-semibold tracking-tighter">Serene Seaside Escape</h4>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    Experience the beauty of the coast with this relaxing itinerary. From charming beachfront cottages
                    to sunset cruises, this trip is all about unwinding by the sea.
                  </p>
                  <p className="text-sm font-semibold">$ - $$$</p>
                </div>
              </div>
              <div className="flex items-center gap-4">
                <img
                  alt="Image"
                  className="rounded-lg object-cover"
                  height="100"
                  src="/placeholder.svg"
                  style={{
                    aspectRatio: "100/100",
                    objectFit: "cover",
                  }}
                  width="100"
                />
                <div className="flex flex-col gap-1">
                  <h4 className="font-semibold tracking-tighter">Cultural Immersion Tour</h4>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    Dive into the local culture with this immersive itinerary. You'll visit traditional villages, sample
                    authentic cuisine, and meet artisans preserving age-old crafts.
                  </p>
                  <p className="text-sm font-semibold">$$ - $$$</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="grid gap-6 md:grid-cols-2">
          <div className="flex flex-col gap-2">
            <h3 className="text-2xl font-bold tracking-tighter sm:text-3xl border-b border-gray-200 dark:border-gray-800 pb-2">
              Sustainability Practices
            </h3>
            <ul className="grid gap-2">
              <li>
                <CheckIcon className="mr-2 inline-block h-4 w-4 text-green-500" />
                Partnering with local communities to support sustainable tourism initiatives.
              </li>
              <li>
                <CheckIcon className="mr-2 inline-block h-4 w-4 text-green-500" />
                Offsetting carbon emissions from travel by investing in reforestation projects.
              </li>
              <li>
                <CheckIcon className="mr-2 inline-block h-4 w-4 text-green-500" />
                Encouraging travelers to reduce single-use plastics and minimize their environmental impact.
              </li>
              <li>
                <CheckIcon className="mr-2 inline-block h-4 w-4 text-green-500" />
                Promoting wildlife conservation and responsible animal encounters.
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

function BriefcaseIcon(props) {
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
      <rect width="20" height="14" x="2" y="7" rx="2" ry="2" />
      <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16" />
    </svg>
  )
}


function CalendarIcon(props) {
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
      <rect width="18" height="18" x="3" y="4" rx="2" ry="2" />
      <line x1="16" x2="16" y1="2" y2="6" />
      <line x1="8" x2="8" y1="2" y2="6" />
      <line x1="3" x2="21" y1="10" y2="10" />
    </svg>
  )
}


function CheckIcon(props) {
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
      <polyline points="20 6 9 17 4 12" />
    </svg>
  )
}


function InstagramIcon(props) {
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
      <rect width="20" height="20" x="2" y="2" rx="5" ry="5" />
      <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z" />
      <line x1="17.5" x2="17.51" y1="6.5" y2="6.5" />
    </svg>
  )
}


function LinkIcon(props) {
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
      <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71" />
      <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71" />
    </svg>
  )
}


function StarIcon(props) {
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
      <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
    </svg>
  )
}
