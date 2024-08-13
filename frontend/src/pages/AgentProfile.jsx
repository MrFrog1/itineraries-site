import { useGetAgentQuery, useGetAllAgentsQuery  } from '../services/api.js'
import { InstagramIcon, LinkIcon, LoadingIcon, StarIcon, CheckIcon, CalendarIcon, BriefcaseIcon} from '../components/ui/icons';


const AgentProfile =  ({ agentId}) => {

  const { data: agent, isLoading: isAgentLoading } = useGetAllAgentsQuery(agentId);


 if (isAgentLoading) {
    return <div>{LoadingIcon}</div>;
  }


  return (


    <div className="w-full py-6 bg-cream-texture">
        <div className="container grid md:gap-6 px-4 md:px-6">
            <div className="grid gap-6 lg:grid-cols-2 xl:gap-12">
            <div className="flex flex-col gap-4">
                <div className="flex flex-col gap-2">
                <h1 className="text-3xl font-bold tracking-tighter sm:text-5xl text-maroon dark:text-blue-400 border-b border-gray-200 dark:border-gray-800 pb-2">
                    {agent.name}
                </h1>
                <div className="flex items-center gap-2">
                    <CalendarIcon className="h-4 w-4 text-green-500" />
                    <span className="text-sm text-gray-500 dark:text-gray-400">
                        Joined in {new Date(agent.agent_profile.join_date).toLocaleDateString('en-US', { month: 'long', year: 'numeric' })}
                    </span>
                </div>
                <div className="flex items-center gap-2">
                    <BriefcaseIcon className="h-4 w-4 text-blue-500" />
                    <span className="text-sm text-gray-500 dark:text-gray-400"> {agent.agent_profile.business_name}</span>
                </div>
                <div className="flex items-center gap-2">
                    <StarIcon className="h-4 w-4 text-yellow-500" />
                        <span className="text-sm text-gray-500 dark:text-gray-400">{agent.agent_profile.review_rating} ({agent.agent_profile.review_count} reviews)</span>
                </div>
                <div className="flex items-center gap-2">
                    <LinkIcon className="h-4 w-4 text-purple-500" />
                    <a
                    className="text-sm text-blue-600 dark:text-blue-400 underline"
                    href= {agent.agent_profile.website}
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
                    href= {agent.agent_profile.instagram_link}
                    rel="noopener noreferrer"
                    target="_blank"
                    >
                    Instagram
                    </a>
                </div>
                </div>

                <div className="grid gap-2">
                {agent.agent_profile.expertise_categories.map((category) => (
                    <div key={category} className="inline-block rounded-lg bg-yellow-100 px-3 py-1 text-sm dark:bg-gray-800 w-1/2">
                    {category}
                    </div>
                ))}
                </div>

                <div className="grid gap-4 md:gap-8">
                <div className="space-y-2 text-base/relaxed">
                    <p> {agent.agent_profile.short_bio} </p>
                </div>
                <div className="space-y-2 text-base/relaxed">
                    <p> {agent.agent_profile.short_bio} </p>
                </div>
                </div>
                <details>
                <summary className="text-blue-600 cursor-pointer dark:text-blue-400">Read More</summary>
                <div className="grid gap-4 md:gap-8">
                    <div className="space-y-2 text-base/relaxed">
                    <p> {agent.agent_profile.bio} </p>
                    </div>
                    <div className="space-y-2 text-base/relaxed">
                        <p> {agent.agent_profile.bio} </p>
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
                {agent.agent_profile.itineraries.map((itinerary) => (
                    <div key={itinerary.id} className="flex items-center gap-4">
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
                        <h4 className="font-semibold tracking-tighter">{itinerary.name}</h4>
                        <p className="text-sm text-gray-500 dark:text-gray-400">{itinerary.visible_description}</p>
                        <p className="text-sm font-semibold">${itinerary.cost_for_1_pax} - ${itinerary.cost_for_4_pax}</p>
                    </div>
                    </div>
                ))}            
            </div>
            </div>
            <div className="grid gap-6 md:grid-cols-2">
                <div className="flex flex-col gap-2">
                <h3 className="text-2xl font-bold tracking-tighter sm:text-3xl border-b border-gray-200 dark:border-gray-800 pb-2">
                    Sustainability Practices
                </h3>
                <p>{agent.agent_profile.sustainability_practices}</p>
                </div>          
            </div>
        </div>
        </div>
    )
}



export default AgentProfile; 