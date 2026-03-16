"use client"

import { useState } from "react"
import { Header } from "@/components/header"
import { Footer } from "@/components/footer"
import { ProductCard, type Product } from "@/components/product-card"
import { ProductFilters } from "@/components/product-filters"
import { ChevronDown, Grid3X3, LayoutGrid, SlidersHorizontal, X } from "lucide-react"
import Link from "next/link"

const products: Product[] = [
  {
    id: "1",
    name: "Robe midi à imprimé floral avec ceinture ajustable",
    price: 24.99,
    originalPrice: 45.99,
    image: "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400&h=600&fit=crop",
    rating: 4.5,
    reviews: 1234,
    tag: "Nouveau",
    colors: ["#000000", "#D4B896", "#3B82F6"],
  },
  {
    id: "2",
    name: "Blazer oversize à double boutonnage",
    price: 34.99,
    originalPrice: 59.99,
    image: "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=400&h=600&fit=crop",
    rating: 4.7,
    reviews: 856,
    colors: ["#000000", "#FFFFFF", "#9CA3AF"],
  },
  {
    id: "3",
    name: "Jean taille haute coupe droite vintage",
    price: 29.99,
    image: "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400&h=600&fit=crop",
    rating: 4.3,
    reviews: 2341,
    tag: "Best-seller",
    colors: ["#3B82F6", "#000000"],
  },
  {
    id: "4",
    name: "Top côtelé à manches longues col V",
    price: 12.99,
    originalPrice: 19.99,
    image: "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=400&h=600&fit=crop",
    rating: 4.6,
    reviews: 543,
    colors: ["#FFFFFF", "#000000", "#EC4899", "#22C55E"],
  },
  {
    id: "5",
    name: "Jupe plissée mi-longue en satin",
    price: 21.99,
    originalPrice: 35.99,
    image: "https://images.unsplash.com/photo-1583496661160-fb5886a0afe1?w=400&h=600&fit=crop",
    rating: 4.4,
    reviews: 678,
    colors: ["#D4B896", "#000000", "#EC4899"],
  },
  {
    id: "6",
    name: "Chemise en lin à rayures col classique",
    price: 18.99,
    image: "https://images.unsplash.com/photo-1598554747436-c9293d6a588f?w=400&h=600&fit=crop",
    rating: 4.2,
    reviews: 321,
    tag: "Tendance",
    colors: ["#FFFFFF", "#3B82F6"],
  },
  {
    id: "7",
    name: "Pantalon large taille haute avec plis",
    price: 26.99,
    originalPrice: 42.99,
    image: "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=400&h=600&fit=crop",
    rating: 4.5,
    reviews: 892,
    colors: ["#000000", "#D4B896", "#9CA3AF"],
  },
  {
    id: "8",
    name: "Cardigan en maille torsadée oversize",
    price: 32.99,
    image: "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?w=400&h=600&fit=crop",
    rating: 4.8,
    reviews: 1567,
    tag: "Coup de coeur",
    colors: ["#D4B896", "#FFFFFF", "#9CA3AF"],
  },
  {
    id: "9",
    name: "Robe courte à volants et bretelles fines",
    price: 19.99,
    originalPrice: 32.99,
    image: "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=400&h=600&fit=crop",
    rating: 4.4,
    reviews: 445,
    colors: ["#EC4899", "#FFFFFF", "#000000"],
  },
  {
    id: "10",
    name: "Ensemble deux pièces crop top et pantalon",
    price: 38.99,
    originalPrice: 55.99,
    image: "https://images.unsplash.com/photo-1509631179647-0177331693ae?w=400&h=600&fit=crop",
    rating: 4.6,
    reviews: 234,
    tag: "Nouveau",
    colors: ["#000000", "#D4B896"],
  },
  {
    id: "11",
    name: "Veste en cuir synthétique style biker",
    price: 45.99,
    image: "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=600&fit=crop",
    rating: 4.7,
    reviews: 1123,
    colors: ["#000000"],
  },
  {
    id: "12",
    name: "Short en denim taille haute délavé",
    price: 16.99,
    originalPrice: 24.99,
    image: "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=400&h=600&fit=crop",
    rating: 4.3,
    reviews: 765,
    colors: ["#3B82F6", "#000000"],
  },
]

const sortOptions = [
  { label: "Populaires", value: "popular" },
  { label: "Nouveautés", value: "newest" },
  { label: "Prix croissant", value: "price-asc" },
  { label: "Prix décroissant", value: "price-desc" },
  { label: "Meilleures notes", value: "rating" },
]

export default function FemmesPage() {
  const [filtersOpen, setFiltersOpen] = useState(false)
  const [sortOpen, setSortOpen] = useState(false)
  const [selectedSort, setSelectedSort] = useState(sortOptions[0])
  const [gridCols, setGridCols] = useState<2 | 4>(4)

  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      {/* Breadcrumb */}
      <div className="max-w-7xl mx-auto px-4 py-3 text-sm">
        <nav className="flex items-center gap-2 text-muted-foreground">
          <Link href="/" className="hover:text-foreground transition-colors">Accueil</Link>
          <span>/</span>
          <span className="text-foreground font-medium">Femmes</span>
        </nav>
      </div>

      {/* Page Header */}
      <div className="max-w-7xl mx-auto px-4 pb-6">
        <h1 className="text-3xl font-bold mb-2">Mode Femme</h1>
        <p className="text-muted-foreground">
          {products.length.toLocaleString()} articles
        </p>
      </div>

      {/* Toolbar */}
      <div className="sticky top-[104px] z-30 bg-background border-y border-border">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex items-center justify-between h-12">
            {/* Left - Filters */}
            <button
              onClick={() => setFiltersOpen(true)}
              className="lg:hidden flex items-center gap-2 text-sm font-medium"
            >
              <SlidersHorizontal className="h-4 w-4" />
              Filtres
            </button>

            {/* Center - Sort */}
            <div className="relative">
              <button
                onClick={() => setSortOpen(!sortOpen)}
                className="flex items-center gap-2 text-sm font-medium"
              >
                Trier par: {selectedSort.label}
                <ChevronDown className={`h-4 w-4 transition-transform ${sortOpen ? "rotate-180" : ""}`} />
              </button>
              {sortOpen && (
                <>
                  <div className="fixed inset-0 z-10" onClick={() => setSortOpen(false)} />
                  <div className="absolute top-full left-0 mt-1 bg-background border border-border shadow-lg rounded-md z-20 min-w-[180px]">
                    {sortOptions.map((option) => (
                      <button
                        key={option.value}
                        onClick={() => {
                          setSelectedSort(option)
                          setSortOpen(false)
                        }}
                        className={`block w-full text-left px-4 py-2 text-sm hover:bg-secondary transition-colors ${
                          selectedSort.value === option.value ? "bg-secondary font-medium" : ""
                        }`}
                      >
                        {option.label}
                      </button>
                    ))}
                  </div>
                </>
              )}
            </div>

            {/* Right - Grid Toggle */}
            <div className="flex items-center gap-2">
              <button
                onClick={() => setGridCols(2)}
                className={`p-1.5 rounded transition-colors ${gridCols === 2 ? "bg-secondary" : "hover:bg-secondary"}`}
                aria-label="2 colonnes"
              >
                <LayoutGrid className="h-4 w-4" />
              </button>
              <button
                onClick={() => setGridCols(4)}
                className={`p-1.5 rounded transition-colors ${gridCols === 4 ? "bg-secondary" : "hover:bg-secondary"}`}
                aria-label="4 colonnes"
              >
                <Grid3X3 className="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 py-6">
        <div className="flex gap-8">
          {/* Sidebar Filters - Desktop */}
          <div className="hidden lg:block w-64 flex-shrink-0">
            <ProductFilters />
          </div>

          {/* Product Grid */}
          <div className="flex-1">
            <div className={`grid gap-4 ${gridCols === 2 ? "grid-cols-2" : "grid-cols-2 md:grid-cols-3 lg:grid-cols-4"}`}>
              {products.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>

            {/* Load More */}
            <div className="mt-8 text-center">
              <button className="px-8 py-3 border border-foreground text-foreground font-medium hover:bg-foreground hover:text-background transition-colors">
                Voir plus de produits
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Mobile Filters Drawer */}
      {filtersOpen && (
        <>
          <div
            className="fixed inset-0 bg-foreground/50 z-40 lg:hidden"
            onClick={() => setFiltersOpen(false)}
          />
          <div className="fixed inset-y-0 left-0 w-full max-w-sm bg-background z-50 lg:hidden overflow-y-auto">
            <ProductFilters isMobile onClose={() => setFiltersOpen(false)} />
          </div>
        </>
      )}

      <Footer />
    </div>
  )
}
