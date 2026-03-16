"use client"

import Image from "next/image"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"

const products = [
  {
    name: "T-shirt Premium",
    image: "/placeholder.svg",
    sales: 245,
    revenue: "4 900 $",
    progress: 85,
  },
  {
    name: "Sneakers Classic",
    image: "/placeholder.svg",
    sales: 189,
    revenue: "7 560 $",
    progress: 72,
  },
  {
    name: "Sac à dos Urban",
    image: "/placeholder.svg",
    sales: 156,
    revenue: "4 680 $",
    progress: 65,
  },
  {
    name: "Casquette Logo",
    image: "/placeholder.svg",
    sales: 134,
    revenue: "2 680 $",
    progress: 52,
  },
  {
    name: "Hoodie Oversize",
    image: "/placeholder.svg",
    sales: 98,
    revenue: "3 920 $",
    progress: 40,
  },
]

export function TopProducts() {
  return (
    <Card className="bg-card border-border h-full">
      <CardHeader>
        <CardTitle className="text-foreground">Produits populaires</CardTitle>
        <CardDescription className="text-muted-foreground">
          Vos meilleurs vendeurs ce mois-ci
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-5">
          {products.map((product, index) => (
            <div key={product.name} className="flex items-center gap-4">
              <span className="text-sm font-medium text-muted-foreground w-4">
                {index + 1}
              </span>
              <div className="h-10 w-10 rounded-lg bg-secondary flex items-center justify-center overflow-hidden">
                <Image
                  src={product.image}
                  alt={product.name}
                  width={40}
                  height={40}
                  className="object-cover"
                />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between mb-1">
                  <p className="text-sm font-medium text-foreground truncate">
                    {product.name}
                  </p>
                  <span className="text-sm font-medium text-foreground ml-2">
                    {product.revenue}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <Progress value={product.progress} className="h-1.5 flex-1" />
                  <span className="text-xs text-muted-foreground whitespace-nowrap">
                    {product.sales} ventes
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
