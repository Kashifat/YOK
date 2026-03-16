import { StatsCards } from "@/components/admin/stats-cards"
import { RecentOrders } from "@/components/admin/recent-orders"
import { SalesChart } from "@/components/admin/sales-chart"
import { TopProducts } from "@/components/admin/top-products"
import { QuickActions } from "@/components/admin/quick-actions"

export default function AdminDashboard() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-foreground">Bonjour, Admin</h1>
          <p className="text-sm text-muted-foreground">
            Voici ce qui se passe dans votre boutique aujourd&apos;hui.
          </p>
        </div>
      </div>

      <QuickActions />

      <StatsCards />

      <div className="grid gap-6 lg:grid-cols-7">
        <div className="lg:col-span-4">
          <SalesChart />
        </div>
        <div className="lg:col-span-3">
          <TopProducts />
        </div>
      </div>

      <RecentOrders />
    </div>
  )
}
