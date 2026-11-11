import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import BlueprintView from "@/components/BlueprintView";
import { Skeleton } from "@/components/ui/skeleton";
import { getBlueprint, type Blueprint } from "@/services/api";

export default function BlueprintDetail() {
  const { id } = useParams<{ id: string }>();
  const [blueprint, setBlueprint] = useState<Blueprint | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    getBlueprint(id)
      .then(setBlueprint)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <Skeleton className="h-96 w-full rounded-lg" />;
  if (!blueprint) return <p className="text-center pt-20">Blueprint not found.</p>;

  return <BlueprintView blueprint={blueprint} />;
}