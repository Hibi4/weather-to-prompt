import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import PromptCard from "./PromptCard";
import type { Blueprint } from "@/services/api";

interface BlueprintViewProps {
  blueprint: Blueprint;
}

export default function BlueprintView({ blueprint }: BlueprintViewProps) {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold">{blueprint.url}</h2>
        <p className="text-muted-foreground mt-1">
          Recommended stack: <span className="font-medium">{blueprint.techStack}</span>
        </p>
      </div>

      <Tabs defaultValue="frontend" className="w-full">
        <TabsList>
          <TabsTrigger value="frontend">
            Frontend ({blueprint.frontendPrompts.length})
          </TabsTrigger>
          <TabsTrigger value="backend">
            Backend ({blueprint.backendPrompts.length})
          </TabsTrigger>
        </TabsList>

        <TabsContent value="frontend" className="space-y-4 mt-4">
          {blueprint.frontendPrompts.map((p) => (
            <PromptCard key={p.step} prompt={p} />
          ))}
        </TabsContent>

        <TabsContent value="backend" className="space-y-4 mt-4">
          {blueprint.backendPrompts.map((p) => (
            <PromptCard key={p.step} prompt={p} />
          ))}
        </TabsContent>
      </Tabs>
    </div>
  );
}