import React from 'react';
import { Toaster } from "@/components/ui/toaster"

const Layout = ({ children }) => {
  return (
    <div className="min-h-screen font-body">
      {children}
        <Toaster />
    </div>
  );
};

export default Layout;