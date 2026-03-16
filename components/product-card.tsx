"use client"

import { useState } from "react"
import { Heart, ShoppingBag, Star } from "lucide-react"
import Link from "next/link"
import Image from "next/image"
import { useAuth } from "@/context/auth-context"

export interface Product {
  id: string
  name: string
  price: number
  originalPrice?: number
  image: string
  rating: number
  reviews: number
  discount?: number
  tag?: string
  colors?: string[]
}

interface ProductCardProps {
  product: Product
}

export function ProductCard({ product }: ProductCardProps) {
  const { requireAuth } = useAuth()
  const [isWishlisted, setIsWishlisted] = useState(false)
  const [isHovered, setIsHovered] = useState(false)

  const discountPercentage = product.originalPrice
    ? Math.round(((product.originalPrice - product.price) / product.originalPrice) * 100)
    : 0

  return (
    <div
      className="group relative bg-background"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* Image Container */}
      <Link href={`/produit/${product.id}`} className="block relative aspect-[3/4] overflow-hidden bg-secondary">
        <Image
          src={product.image}
          alt={product.name}
          fill
          className="object-cover group-hover:scale-105 transition-transform duration-300"
        />
        
        {/* Tags */}
        <div className="absolute top-2 left-2 flex flex-col gap-1">
          {product.tag && (
            <span className="px-2 py-1 text-xs font-medium bg-foreground text-background">
              {product.tag}
            </span>
          )}
          {discountPercentage > 0 && (
            <span className="px-2 py-1 text-xs font-medium bg-red-500 text-white">
              -{discountPercentage}%
            </span>
          )}
        </div>

        {/* Wishlist Button */}
        <button
          onClick={(e) => {
            e.preventDefault()
            if (!requireAuth("ajouter des produits aux favoris")) {
              return
            }
            setIsWishlisted(!isWishlisted)
          }}
          className="absolute top-2 right-2 w-8 h-8 flex items-center justify-center bg-background/80 rounded-full hover:bg-background transition-colors"
          aria-label={isWishlisted ? "Retirer des favoris" : "Ajouter aux favoris"}
        >
          <Heart
            className={`h-4 w-4 transition-colors ${
              isWishlisted ? "fill-red-500 text-red-500" : "text-foreground"
            }`}
          />
        </button>

        {/* Quick Add Button */}
        <div
          className={`absolute bottom-0 left-0 right-0 bg-foreground text-background py-3 text-center text-sm font-medium transition-all duration-200 ${
            isHovered ? "opacity-100 translate-y-0" : "opacity-0 translate-y-full"
          }`}
        >
          <button
            className="flex items-center justify-center gap-2 w-full"
            onClick={(e) => {
              e.preventDefault()
              requireAuth("ajouter des produits au panier")
            }}
          >
            <ShoppingBag className="h-4 w-4" />
            Ajouter au panier
          </button>
        </div>
      </Link>

      {/* Product Info */}
      <div className="p-3">
        {/* Colors */}
        {product.colors && product.colors.length > 0 && (
          <div className="flex gap-1 mb-2">
            {product.colors.slice(0, 4).map((color, index) => (
              <span
                key={index}
                className="w-4 h-4 rounded-full border border-border"
                style={{ backgroundColor: color }}
              />
            ))}
            {product.colors.length > 4 && (
              <span className="text-xs text-muted-foreground">
                +{product.colors.length - 4}
              </span>
            )}
          </div>
        )}

        {/* Name */}
        <Link href={`/produit/${product.id}`}>
          <h3 className="text-sm line-clamp-2 hover:underline">
            {product.name}
          </h3>
        </Link>

        {/* Rating */}
        <div className="flex items-center gap-1 mt-1">
          <div className="flex">
            {[...Array(5)].map((_, i) => (
              <Star
                key={i}
                className={`h-3 w-3 ${
                  i < Math.floor(product.rating)
                    ? "fill-amber-400 text-amber-400"
                    : "text-muted-foreground"
                }`}
              />
            ))}
          </div>
          <span className="text-xs text-muted-foreground">
            ({product.reviews})
          </span>
        </div>

        {/* Price */}
        <div className="flex items-center gap-2 mt-2">
          <span className="font-bold text-foreground">
            CA${product.price.toFixed(2)}
          </span>
          {product.originalPrice && (
            <span className="text-sm text-muted-foreground line-through">
              CA${product.originalPrice.toFixed(2)}
            </span>
          )}
        </div>
      </div>
    </div>
  )
}
