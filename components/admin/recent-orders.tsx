"use client"

import { MoreHorizontal, ExternalLink } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

const orders = [
  {
    id: "#1042",
    customer: "Marie Dupont",
    email: "marie.dupont@email.com",
    status: "En cours",
    date: "Il y a 2 heures",
    total: "125,00 $",
    items: 3,
  },
  {
    id: "#1041",
    customer: "Jean Martin",
    email: "jean.martin@email.com",
    status: "Expédiée",
    date: "Il y a 5 heures",
    total: "89,99 $",
    items: 1,
  },
  {
    id: "#1040",
    customer: "Sophie Bernard",
    email: "sophie.b@email.com",
    status: "Livrée",
    date: "Hier",
    total: "234,50 $",
    items: 4,
  },
  {
    id: "#1039",
    customer: "Pierre Leroy",
    email: "p.leroy@email.com",
    status: "En attente",
    date: "Hier",
    total: "56,00 $",
    items: 2,
  },
  {
    id: "#1038",
    customer: "Claire Moreau",
    email: "claire.m@email.com",
    status: "Livrée",
    date: "Il y a 2 jours",
    total: "178,00 $",
    items: 3,
  },
]

const statusStyles: Record<string, string> = {
  "En cours": "bg-chart-4/20 text-chart-4 border-chart-4/30",
  "Expédiée": "bg-chart-2/20 text-chart-2 border-chart-2/30",
  "Livrée": "bg-primary/20 text-primary border-primary/30",
  "En attente": "bg-muted text-muted-foreground border-border",
  "Annulée": "bg-destructive/20 text-destructive border-destructive/30",
}

export function RecentOrders() {
  return (
    <Card className="bg-card border-border">
      <CardHeader className="flex flex-row items-center justify-between">
        <div>
          <CardTitle className="text-foreground">Commandes récentes</CardTitle>
          <CardDescription className="text-muted-foreground">
            Vous avez 156 commandes ce mois-ci
          </CardDescription>
        </div>
        <Button variant="outline" size="sm" className="gap-2">
          Voir toutes les commandes
          <ExternalLink className="h-4 w-4" />
        </Button>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow className="border-border hover:bg-transparent">
              <TableHead className="text-muted-foreground">Commande</TableHead>
              <TableHead className="text-muted-foreground">Client</TableHead>
              <TableHead className="text-muted-foreground">Statut</TableHead>
              <TableHead className="text-muted-foreground">Date</TableHead>
              <TableHead className="text-muted-foreground text-right">Total</TableHead>
              <TableHead className="w-10"></TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {orders.map((order) => (
              <TableRow key={order.id} className="border-border">
                <TableCell className="font-medium text-foreground">
                  {order.id}
                </TableCell>
                <TableCell>
                  <div>
                    <div className="font-medium text-foreground">{order.customer}</div>
                    <div className="text-sm text-muted-foreground">{order.email}</div>
                  </div>
                </TableCell>
                <TableCell>
                  <Badge
                    variant="outline"
                    className={statusStyles[order.status]}
                  >
                    {order.status}
                  </Badge>
                </TableCell>
                <TableCell className="text-muted-foreground">{order.date}</TableCell>
                <TableCell className="text-right font-medium text-foreground">
                  {order.total}
                </TableCell>
                <TableCell>
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="ghost" size="icon" className="h-8 w-8">
                        <MoreHorizontal className="h-4 w-4" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem>Voir les détails</DropdownMenuItem>
                      <DropdownMenuItem>Modifier la commande</DropdownMenuItem>
                      <DropdownMenuSeparator />
                      <DropdownMenuItem>Imprimer le reçu</DropdownMenuItem>
                      <DropdownMenuItem className="text-destructive">
                        Annuler la commande
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  )
}
