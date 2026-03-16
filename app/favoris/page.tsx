"use client"

import { useState } from "react"
import { Header } from "@/components/header"
import { Footer } from "@/components/footer"
import { Heart, ShoppingBag, X, Star, Share2, Grid3X3, LayoutGrid } from "lucide-react"
import Link from "next/link"
import Image from "next/image"
import { useAuth } from "@/context/auth-context"

interface WishlistItem {
  id: string
  name: string
  price: number
  originalPrice?: number
  image: string
  rating: number
  reviews: number
  inStock: boolean
  colors: string[]
  sizes: string[]
}

const initialWishlistItems: WishlistItem[] = [
  {
    id: "1",
    name: "Robe midi à imprimé floral avec ceinture ajustable",
    price: 24.99,
    originalPrice: 45.99,
    image: "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400&h=600&fit=crop",
    rating: 4.5,
    reviews: 1234,
    inStock: true,
    colors: ["#000000", "#D4B896", "#3B82F6"],
    sizes: ["XS", "S", "M", "L", "XL"],
  },
  {
    id: "2",
    name: "Blazer oversize à double boutonnage",
    price: 34.99,
    originalPrice: 59.99,
    image: "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=400&h=600&fit=crop",
    rating: 4.7,
    reviews: 856,
    inStock: true,
    colors: ["#000000", "#FFFFFF", "#9CA3AF"],
    sizes: ["S", "M", "L"],
  },
  {
    id: "3",
    name: "Jean taille haute coupe droite vintage",
    price: 29.99,
    image: "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400&h=600&fit=crop",
    rating: 4.3,
    reviews: 2341,
    inStock: false,
    colors: ["#3B82F6", "#000000"],
    sizes: ["XS", "S", "M", "L", "XL", "XXL"],
  },
  {
    id: "4",
    name: "Top côtelé à manches longues col V",
    price: 12.99,
    originalPrice: 19.99,
    image: "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=400&h=600&fit=crop",
    rating: 4.6,
    reviews: 543,
    inStock: true,
    colors: ["#FFFFFF", "#000000", "#EC4899", "#22C55E"],
    sizes: ["XS", "S", "M", "L"],
  },
  {
    id: "5",
    name: "Jupe plissée mi-longue en satin",
    price: 21.99,
    originalPrice: 35.99,
    image: "https://images.unsplash.com/photo-1583496661160-fb5886a0afe1?w=400&h=600&fit=crop",
    rating: 4.4,
    reviews: 678,
    inStock: true,
    colors: ["#D4B896", "#000000", "#EC4899"],
    sizes: ["S", "M", "L", "XL"],
  },
  {
    id: "6",
    name: "Cardigan en maille torsadée oversize",
    price: 32.99,
    image: "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?w=400&h=600&fit=crop",
    rating: 4.8,
    reviews: 1567,
    inStock: true,
    colors: ["#D4B896", "#FFFFFF", "#9CA3AF"],
    sizes: ["S", "M", "L"],
  },
]

export default function WishlistPage() {
  const { isAuthenticated, requireAuth } = useAuth()
  const [wishlistItems, setWishlistItems] = useState(initialWishlistItems)
  const [gridCols, setGridCols] = useState<2 | 4>(4)
  const [selectedSizes, setSelectedSizes] = useState<Record<string, string>>({})

  const removeItem = (id: string) => {
    if (!requireAuth("gerer vos favoris")) {
      return
    }
    setWishlistItems((items) => items.filter((item) => item.id !== id))
  }

  const selectSize = (itemId: string, size: string) => {
    if (!requireAuth("ajouter des produits au panier")) {
      return
    }
    setSelectedSizes((prev) => ({ ...prev, [itemId]: size }))
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-background">
        <Header />
        <div className="max-w-7xl mx-auto px-4 py-16 text-center">
          <div className="max-w-md mx-auto">
            <div className="w-24 h-24 mx-auto mb-6 bg-secondary rounded-full flex items-center justify-center">
              <Heart className="w-12 h-12 text-muted-foreground" />
            </div>
            <h1 className="text-2xl font-bold mb-2">Connexion requise</h1>
            <p className="text-muted-foreground mb-6">
              Connectez-vous pour consulter et gerer vos favoris.
            </p>
            <Link
              href="/compte?reason=gerer%20vos%20favoris"
              className="inline-block px-8 py-3 bg-foreground text-background font-medium hover:opacity-90 transition-opacity"
            >
              Creer un compte / Se connecter
            </Link>
          </div>
        </div>
        <Footer />
      </div>
    )
  }

  if (wishlistItems.length === 0) {
    return (
      <div className="min-h-screen bg-background">
        <Header />
        <div className="max-w-7xl mx-auto px-4 py-16 text-center">
          <div className="max-w-md mx-auto">
            <div className="w-24 h-24 mx-auto mb-6 bg-secondary rounded-full flex items-center justify-center">
              <Heart className="w-12 h-12 text-muted-foreground" />
            </div>
            <h1 className="text-2xl font-bold mb-2">Votre liste de favoris est vide</h1>
            <p className="text-muted-foreground mb-6">
              Explorez notre collection et ajoutez vos articles préférés en cliquant sur le coeur.
            </p>
            <Link
              href="/femmes"
              className="inline-block px-8 py-3 bg-foreground text-background font-medium hover:opacity-90 transition-opacity"
            >
              Découvrir nos produits
            </Link>
          </div>
        </div>
        <Footer />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      <Header />

      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Page Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
          <div>
            <h1 className="text-2xl font-bold">Mes favoris</h1>
            <p className="text-muted-foreground">{wishlistItems.length} article(s)</p>
          </div>
          <div className="flex items-center gap-4">
            <button className="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors">
              <Share2 className="h-4 w-4" />
              Partager ma liste
            </button>
            <div className="flex items-center gap-2 border-l border-border pl-4">
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

        {/* Wishlist Grid */}
        <div className={`grid gap-4 ${gridCols === 2 ? "grid-cols-1 sm:grid-cols-2" : "grid-cols-2 md:grid-cols-3 lg:grid-cols-4"}`}>
          {wishlistItems.map((item) => {
            const discountPercentage = item.originalPrice
              ? Math.round(((item.originalPrice - item.price) / item.originalPrice) * 100)
              : 0

            return (
              <div key={item.id} className="group relative bg-background border border-border rounded-lg overflow-hidden">
                {/* Image */}
                <Link href={`/produit/${item.id}`} className="block relative aspect-[3/4] overflow-hidden bg-secondary">
                  <Image
                    src={item.image}
                    alt={item.name}
                    fill
                    className={`object-cover group-hover:scale-105 transition-transform duration-300 ${!item.inStock ? "opacity-50" : ""}`}
                  />
                  
                  {/* Tags */}
                  <div className="absolute top-2 left-2 flex flex-col gap-1">
                    {discountPercentage > 0 && (
                      <span className="px-2 py-1 text-xs font-medium bg-red-500 text-white">
                        -{discountPercentage}%
                      </span>
                    )}
                    {!item.inStock && (
                      <span className="px-2 py-1 text-xs font-medium bg-foreground/80 text-background">
                        Rupture de stock
                      </span>
                    )}
                  </div>

                  {/* Remove Button */}
                  <button
                    onClick={(e) => {
                      e.preventDefault()
                      removeItem(item.id)
                    }}
                    className="absolute top-2 right-2 w-8 h-8 flex items-center justify-center bg-background rounded-full hover:bg-red-50 transition-colors group/btn"
                    aria-label="Retirer des favoris"
                  >
                    <X className="h-4 w-4 group-hover/btn:text-red-500 transition-colors" />
                  </button>
                </Link>

                {/* Product Info */}
                <div className="p-3">
                  {/* Colors */}
                  <div className="flex gap-1 mb-2">
                    {item.colors.slice(0, 4).map((color, index) => (
                      <span
                        key={index}
                        className="w-4 h-4 rounded-full border border-border"
                        style={{ backgroundColor: color }}
                      />
                    ))}
                    {item.colors.length > 4 && (
                      <span className="text-xs text-muted-foreground">
                        +{item.colors.length - 4}
                      </span>
                    )}
                  </div>

                  {/* Name */}
                  <Link href={`/produit/${item.id}`}>
                    <h3 className="text-sm line-clamp-2 hover:underline mb-1">
                      {item.name}
                    </h3>
                  </Link>

                  {/* Rating */}
                  <div className="flex items-center gap-1 mb-2">
                    <div className="flex">
                      {[...Array(5)].map((_, i) => (
                        <Star
                          key={i}
                          className={`h-3 w-3 ${
                            i < Math.floor(item.rating)
                              ? "fill-amber-400 text-amber-400"
                              : "text-muted-foreground"
                          }`}
                        />
                      ))}
                    </div>
                    <span className="text-xs text-muted-foreground">
                      ({item.reviews})
                    </span>
                  </div>

                  {/* Price */}
                  <div className="flex items-center gap-2 mb-3">
                    <span className="font-bold text-foreground">
                      CA${item.price.toFixed(2)}
                    </span>
                    {item.originalPrice && (
                      <span className="text-sm text-muted-foreground line-through">
                        CA${item.originalPrice.toFixed(2)}
                      </span>
                    )}
                  </div>

                  {/* Size Selection */}
                  {item.inStock && (
                    <div className="mb-3">
                      <p className="text-xs text-muted-foreground mb-1.5">Sélectionnez une taille:</p>
                      <div className="flex flex-wrap gap-1">
                        {item.sizes.map((size) => (
                          <button
                            key={size}
                            onClick={() => selectSize(item.id, size)}
                            className={`min-w-[32px] h-7 px-2 text-xs border transition-colors ${
                              selectedSizes[item.id] === size
                                ? "bg-foreground text-background border-foreground"
                                : "border-border hover:border-foreground"
                            }`}
                          >
                            {size}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Add to Cart Button */}
                  <button
                    disabled={!item.inStock || !selectedSizes[item.id]}
                    onClick={() => {
                      requireAuth("ajouter des produits au panier")
                    }}
                    className={`w-full flex items-center justify-center gap-2 h-10 text-sm font-medium transition-colors ${
                      item.inStock && selectedSizes[item.id]
                        ? "bg-foreground text-background hover:opacity-90"
                        : "bg-secondary text-muted-foreground cursor-not-allowed"
                    }`}
                  >
                    <ShoppingBag className="h-4 w-4" />
                    {!item.inStock 
                      ? "Indisponible" 
                      : !selectedSizes[item.id] 
                        ? "Choisir une taille" 
                        : "Ajouter au panier"
                    }
                  </button>
                </div>
              </div>
            )
          })}
        </div>

        {/* Actions */}
        <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-4">
          <button
            className="w-full sm:w-auto px-8 py-3 bg-foreground text-background font-medium hover:opacity-90 transition-opacity flex items-center justify-center gap-2"
            onClick={() => {
              requireAuth("ajouter des produits au panier")
            }}
          >
            <ShoppingBag className="h-5 w-5" />
            Tout ajouter au panier
          </button>
          <Link
            href="/femmes"
            className="w-full sm:w-auto px-8 py-3 border border-foreground text-foreground font-medium hover:bg-foreground hover:text-background transition-colors text-center"
          >
            Continuer mes achats
          </Link>
        </div>
      </div>

      <Footer />
    </div>
  )
}
