import { Header } from "@/components/header"
import { HeroBanner } from "@/components/hero-banner"
import { CategoryGrid } from "@/components/category-grid"
import { FlashSale } from "@/components/flash-sale"
import { TrendingSection } from "@/components/trending-section"
import { ProductGrid } from "@/components/product-grid"
import { PromoBanners } from "@/components/promo-banners"
import { Footer } from "@/components/footer"

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-1">
        <HeroBanner />
        <CategoryGrid />
        <FlashSale />
        <TrendingSection />
        <ProductGrid title="Nouveautés" />
        <PromoBanners />
        <ProductGrid title="Les Plus Vendus" showViewAll={true} />
      </main>
      <Footer />
    </div>
  )
}
