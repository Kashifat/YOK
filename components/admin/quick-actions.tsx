"use client"

import { Plus, Package, Tags, Megaphone } from "lucide-react"
import { Button } from "@/components/ui/button"

const actions = [
  {
    label: "Ajouter un produit",
    icon: Plus,
    variant: "default" as const,
  },
  {
    label: "Gérer l'inventaire",
    icon: Package,
    variant: "outline" as const,
  },
  {
    label: "Créer une remise",
    icon: Tags,
    variant: "outline" as const,
  },
  {
    label: "Lancer une campagne",
    icon: Megaphone,
    variant: "outline" as const,
  },
]

export function QuickActions() {
  return (
    <div className="flex flex-wrap gap-3">
      {actions.map((action) => (
        <Button
          key={action.label}
          variant={action.variant}
          size="sm"
          className="gap-2"
        >
          <action.icon className="h-4 w-4" />
          {action.label}
        </Button>
      ))}
    </div>
  )
}
