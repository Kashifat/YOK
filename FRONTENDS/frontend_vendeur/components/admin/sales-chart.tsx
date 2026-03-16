"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Area, AreaChart, CartesianGrid, XAxis, YAxis, ResponsiveContainer, Tooltip } from "recharts"

const data = [
  { name: "Lun", ventes: 2400, commandes: 24 },
  { name: "Mar", ventes: 1398, commandes: 13 },
  { name: "Mer", ventes: 3200, commandes: 32 },
  { name: "Jeu", ventes: 2780, commandes: 28 },
  { name: "Ven", ventes: 4890, commandes: 49 },
  { name: "Sam", ventes: 3390, commandes: 34 },
  { name: "Dim", ventes: 2490, commandes: 25 },
]

export function SalesChart() {
  return (
    <Card className="bg-card border-border">
      <CardHeader>
        <CardTitle className="text-foreground">Aperçu des ventes</CardTitle>
        <CardDescription className="text-muted-foreground">
          Ventes des 7 derniers jours
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
              <defs>
                <linearGradient id="colorVentes" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="oklch(0.65 0.18 145)" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="oklch(0.65 0.18 145)" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="oklch(0.28 0.005 260)" vertical={false} />
              <XAxis
                dataKey="name"
                stroke="oklch(0.65 0 0)"
                fontSize={12}
                tickLine={false}
                axisLine={false}
              />
              <YAxis
                stroke="oklch(0.65 0 0)"
                fontSize={12}
                tickLine={false}
                axisLine={false}
                tickFormatter={(value) => `${value} $`}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: "oklch(0.18 0.005 260)",
                  border: "1px solid oklch(0.28 0.005 260)",
                  borderRadius: "8px",
                  color: "oklch(0.95 0 0)",
                }}
                labelStyle={{ color: "oklch(0.65 0 0)" }}
                formatter={(value: number) => [`${value} $`, "Ventes"]}
              />
              <Area
                type="monotone"
                dataKey="ventes"
                stroke="oklch(0.65 0.18 145)"
                strokeWidth={2}
                fillOpacity={1}
                fill="url(#colorVentes)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  )
}
