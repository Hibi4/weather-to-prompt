import { useState } from "react";
import { useNavigate } from "react-router-dom";
import UrlInput from "@/components/UrlInput";
import BlueprintView from "@/components/BlueprintView";
import { generateBlueprint, type Blueprint } from "@/services/api";

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [blueprint, setBlueprint] = useState<Blueprint | null>(null);
  const navigate = useNavigate();

  const handleAnalyze = async (url: string) => {
    setLoading(true);
    try {
      const result = await generateBlueprint(url);
      setBlueprint(result);
    } catch (error) {
      console.error("Failed to generate blueprint:", error);
      alert("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center gap-10 pt-16">
      <div className="text-center space-y-4">
        <h1 className="text-4xl font-bold tracking-tight">
          Turn any website into AI prompts
        </h1>
        <p className="text-muted-foreground text-lg max-w-xl mx-auto">
          Paste a URL and get a complete set of frontend & backend prompts to
          rebuild the site from scratch.
        </p>
      </div>

      <UrlInput onSubmit={handleAnalyze} isLoading={loading} />

      {loading && (
        <p className="text-muted-foreground animate-pulse">
          Analyzing website... This may take 30–60 seconds.
        </p>
      )}

      {blueprint && <BlueprintView blueprint={blueprint} />}
    </div>
  );
}