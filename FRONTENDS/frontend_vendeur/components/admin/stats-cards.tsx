"use client"

import { DollarSign, ShoppingCart, Users, TrendingUp, ArrowUpRight, ArrowDownRight } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

const stats = [
  {
    title: "Ventes totales",
    value: "12 543,00 $",
    change: "+12,5%",
    trend: "up",
    description: "vs mois dernier",
    icon: DollarSign,
  },
  {
    title: "Commandes",
    value: "156",
    change: "+8,2%",
    trend: "up",
    description: "vs mois dernier",
    icon: ShoppingCart,
  },
  {
    title: "Visiteurs",
    value: "3 425",
    change: "-2,4%",
    trend: "down",
    description: "vs mois dernier",
    icon: Users,
  },
  {
    title: "Taux de conversion",
    value: "4,55%",
    change: "+1,2%",
    trend: "up",
    description: "vs mois dernier",
    icon: TrendingUp,
  },
]

export function StatsCards() {
  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      {stats.map((stat) => (
        <Card key={stat.title} className="bg-card border-border">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              {stat.title}
            </CardTitle>
            <stat.icon className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-foreground">{stat.value}</div>
            <div className="flex items-center gap-1 mt-1">
              {stat.trend === "up" ? (
                <ArrowUpRight className="h-4 w-4 text-primary" />
              ) : (
                <ArrowDownRight className="h-4 w-4 text-destructive" />
              )}
              <span
                className={`text-sm font-medium ${
                  stat.trend === "up" ? "text-primary" : "text-destructive"
                }`}
              >
                {stat.change}
              </span>
              <span className="text-sm text-muted-foreground">{stat.description}</span>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
