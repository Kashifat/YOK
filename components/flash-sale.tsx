"use client"

import { useState, useEffect } from "react"
import { Zap } from "lucide-react"
import Image from "next/image"
import Link from "next/link"

interface FlashSaleProduct {
  id: string
  name: string
  price: number
  originalPrice: number
  image: string
  soldPercentage: number
}

const flashProducts: FlashSaleProduct[] = [
  {
    id: "f1",
    name: "Set de 5 Éponges Maquillage",
    price: 2.48,
    originalPrice: 9.99,
    image: "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=200&h=200&fit=crop",
    soldPercentage: 78,
  },
  {
    id: "f2",
    name: "Mini Ventilateur USB Rechargeable",
    price: 3.68,
    originalPrice: 12.99,
    image: "https://images.unsplash.com/photo-1586953208270-767889fa9b6f?w=200&h=200&fit=crop",
    soldPercentage: 65,
  },
  {
    id: "f3",
    name: "Bonnet en Satin pour Cheveux",
    price: 1.62,
    originalPrice: 8.99,
    image: "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=200&h=200&fit=crop",
    soldPercentage: 92,
  },
  {
    id: "f4",
    name: "Lot de 7 Bracelets Bohème",
    price: 2.88,
    originalPrice: 11.99,
    image: "https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=200&h=200&fit=crop",
    soldPercentage: 45,
  },
  {
    id: "f5",
    name: "Protecteurs Talon Gel - 20 pcs",
    price: 1.60,
    originalPrice: 7.99,
    image: "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=200&h=200&fit=crop",
    soldPercentage: 88,
  },
]

function CountdownTimer() {
  const [timeLeft, setTimeLeft] = useState({
    hours: 5,
    minutes: 23,
    seconds: 45,
  })

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        let { hours, minutes, seconds } = prev
        seconds--
        if (seconds < 0) {
          seconds = 59
          minutes--
        }
        if (minutes < 0) {
          minutes = 59
          hours--
        }
        if (hours < 0) {
          hours = 23
          minutes = 59
          seconds = 59
        }
        return { hours, minutes, seconds }
      })
    }, 1000)
    return () => clearInterval(timer)
  }, [])

  const formatNumber = (num: number) => num.toString().padStart(2, "0")

  return (
    <div className="flex items-center gap-1">
      <span className="text-sm">Se termine dans</span>
      <div className="flex gap-1">
        <span className="bg-foreground text-background px-2 py-1 text-sm font-mono font-bold rounded">
          {formatNumber(timeLeft.hours)}
        </span>
        <span className="font-bold">:</span>
        <span className="bg-foreground text-background px-2 py-1 text-sm font-mono font-bold rounded">
          {formatNumber(timeLeft.minutes)}
        </span>
        <span className="font-bold">:</span>
        <span className="bg-foreground text-background px-2 py-1 text-sm font-mono font-bold rounded">
          {formatNumber(timeLeft.seconds)}
        </span>
      </div>
    </div>
  )
}

export function FlashSale() {
  return (
    <section className="py-8 bg-gradient-to-r from-rose-50 to-amber-50">
      <div className="max-w-7xl mx-auto px-4">
        {/* Header */}
        <div className="flex flex-col md:flex-row items-center justify-between gap-4 mb-6">
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 bg-red-500 text-white px-4 py-2 rounded-full">
              <Zap className="h-5 w-5 fill-current" />
              <span className="font-bold">VENTE FLASH</span>
            </div>
            <CountdownTimer />
          </div>
          <Link href="/flash-sale" className="text-sm font-medium hover:underline">
            Voir tout →
          </Link>
        </div>

        {/* Products */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
          {flashProducts.map((product) => (
            <Link
              key={product.id}
              href={`/produit/${product.id}`}
              className="bg-background p-4 rounded-lg border border-border hover:shadow-lg transition-shadow"
            >
              <div className="relative aspect-square mb-3 overflow-hidden rounded-md bg-secondary">
                <Image
                  src={product.image}
                  alt={product.name}
                  fill
                  className="object-cover"
                />
                <span className="absolute top-2 left-2 bg-red-500 text-white text-xs font-bold px-2 py-1 rounded">
                  -{Math.round(((product.originalPrice - product.price) / product.originalPrice) * 100)}%
                </span>
              </div>
              <h3 className="text-sm line-clamp-2 mb-2">{product.name}</h3>
              <div className="flex items-center gap-2 mb-2">
                <span className="font-bold text-red-500">
                  CA${product.price.toFixed(2)}
                </span>
                <span className="text-xs text-muted-foreground line-through">
                  CA${product.originalPrice.toFixed(2)}
                </span>
              </div>
              {/* Progress Bar */}
              <div className="relative h-2 bg-secondary rounded-full overflow-hidden">
                <div
                  className="absolute top-0 left-0 h-full bg-red-500 rounded-full"
                  style={{ width: `${product.soldPercentage}%` }}
                />
              </div>
              <p className="text-xs text-muted-foreground mt-1">
                {product.soldPercentage}% vendu
              </p>
            </Link>
          ))}
        </div>
      </div>
    </section>
  )
}
