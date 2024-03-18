
export default function LoadingPlaceholder() {
  return (
    <div className="flex space-x-8">
      {[1, 2, 3].map((index) => (
        <div key={index} className="flex flex-col items-center space-y-4">
          <div className="h-[300px] w-[300px] rounded-lg bg-gray-200 animate-pulse"></div>
          <div className="h-4 w-32 bg-gray-200 rounded animate-pulse"></div>
          <div className="h-4 w-48 bg-gray-200 rounded animate-pulse"></div>
          <div className="h-4 w-40 bg-gray-200 rounded animate-pulse"></div>
          <div className="h-10 w-32 bg-gray-200 rounded animate-pulse"></div>
        </div>
      ))}
    </div>
  );
}
