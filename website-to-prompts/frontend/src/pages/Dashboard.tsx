import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Card, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { getBlueprints, type Blueprint } from "@/services/api";

export default function Dashboard() {
  const [blueprints, setBlueprints] = useState<Blueprint[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getBlueprints()
      .then(setBlueprints)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {[1, 2, 3].map((i) => (
          <Skeleton key={i} className="h-24 rounded-lg" />
        ))}
      </div>
    );
  }

  if (blueprints.length === 0) {
    return (
      <p className="text-center text-muted-foreground pt-20">
        No blueprints yet. Go to the home page to analyze your first website!
      </p>
    );
  }

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {blueprints.map((bp) => (
        <Link key={bp.id} to={`/blueprint/${bp.id}`}>
          <Card className="hover:shadow-md transition-shadow cursor-pointer">
            <CardHeader>
              <CardTitle className="text-sm truncate">{bp.url}</CardTitle>
              <p className="text-xs text-muted-foreground">{bp.techStack}</p>
            </CardHeader>
          </Card>
        </Link>
      ))}
    </div>
  );
}