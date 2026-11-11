import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Code2 } from "lucide-react";

export default function Navbar() {
  return (
    <nav className="border-b bg-background/95 backdrop-blur sticky top-0 z-50">
      <div className="container mx-auto flex h-14 items-center justify-between px-4">
        <Link to="/" className="flex items-center gap-2 font-bold text-lg">
          <Code2 className="h-5 w-5" />
          SiteToPrompts
        </Link>
        <div className="flex gap-2">
          <Link to="/dashboard">
            <Button variant="ghost">Dashboard</Button>
          </Link>
          <Link to="/login">
            <Button>Login</Button>
          </Link>
        </div>
      </div>
    </nav>
  );
}