import { Link } from "react-router-dom";
import { useSelector, useDispatch } from 'react-redux';
import { logoutUser } from '../../features/auth/authSlice';
import ModalLogin from '../../features/auth/components/ModalLogin';
import { Button } from "@/components/ui/button";

export default function Header({ onSelectLabel }) {
  const { user } = useSelector((state) => state.auth);
  const dispatch = useDispatch();
  const isLoggedIn = Boolean(user);


  return (
    <header className="flex items-center h-24 px-4 border-b border-gray-200 backdrop-filter backdrop-blur-sm justify-between dark:border-gray-800">
      <div className="flex items-center space-x-4 flex-1 justify-end">
        {isLoggedIn ? (
          <>
            <Link to="/profile" className="flex items-center p-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800">
              <UserIcon className="h-6 w-6" />
            </Link>
            <Link to="/messages" className="flex items-center p-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800">
              <MessageSquareIcon className="h-6 w-6" />
            </Link>
            <Link to="/settings" className="flex items-center p-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800">
              <SettingsIcon className="h-6 w-6" />
            </Link>
            <Button
              onClick={() => dispatch(logoutUser())}
              className="flex items-center p-2 rounded-md bg-[#F6EEE3] font-optimaroman text-[#A7252A]"
            >
              Logout
            </Button>
          </>
        ) : (
          <ModalLogin className="font-optimaroman text-[#A7252A]" />
        )}
      </div>
    </header>
  );
}

// ... (Icon components remain the same)
function HomeIcon(props) {
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
      <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
      <polyline points="9 22 9 12 15 12 15 22" />
    </svg>
  )
}


function MessageSquareIcon(props) {
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
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
    </svg>
  )
}


function SettingsIcon(props) {
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
      <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z" />
      <circle cx="12" cy="12" r="3" />
    </svg>
  )
}


function UserIcon(props) {
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
      <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2" />
      <circle cx="12" cy="7" r="4" />
    </svg>
  )
}
