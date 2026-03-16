"use client"

import { useState, useEffect } from "react"
import { ChevronLeft, ChevronRight } from "lucide-react"
import Link from "next/link"

const banners = [
  {
    id: 1,
    title: "NOUVELLE COLLECTION",
    subtitle: "Printemps 2026",
    description: "Découvrez les dernières tendances",
    cta: "ACHETER MAINTENANT",
    href: "/nouveautes",
    bgColor: "bg-rose-100",
    textColor: "text-foreground",
  },
  {
    id: 2,
    title: "SOLDES FLASH",
    subtitle: "Jusqu'à -70%",
    description: "Offres limitées dans le temps",
    cta: "VOIR LES OFFRES",
    href: "/soldes",
    bgColor: "bg-amber-100",
    textColor: "text-foreground",
  },
  {
    id: 3,
    title: "LIVRAISON GRATUITE",
    subtitle: "Dès 49$ d'achat",
    description: "Partout au Canada",
    cta: "EN PROFITER",
    href: "/livraison",
    bgColor: "bg-sky-100",
    textColor: "text-foreground",
  },
]

export function HeroBanner() {
  const [currentSlide, setCurrentSlide] = useState(0)

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % banners.length)
    }, 5000)
    return () => clearInterval(timer)
  }, [])

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % banners.length)
  }

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + banners.length) % banners.length)
  }

  return (
    <section className="relative overflow-hidden">
      <div
        className="flex transition-transform duration-500 ease-out"
        style={{ transform: `translateX(-${currentSlide * 100}%)` }}
      >
        {banners.map((banner) => (
          <div
            key={banner.id}
            className={`min-w-full ${banner.bgColor} ${banner.textColor}`}
          >
            <div className="max-w-7xl mx-auto px-4 py-16 md:py-24 flex flex-col items-center text-center">
              <span className="text-sm font-medium tracking-wider uppercase mb-2">
                {banner.subtitle}
              </span>
              <h2 className="text-4xl md:text-6xl font-bold tracking-tight mb-4 text-balance">
                {banner.title}
              </h2>
              <p className="text-lg md:text-xl mb-8 opacity-80">
                {banner.description}
              </p>
              <Link
                href={banner.href}
                className="inline-flex items-center justify-center px-8 py-3 bg-foreground text-background font-medium text-sm hover:opacity-90 transition-opacity"
              >
                {banner.cta}
              </Link>
            </div>
          </div>
        ))}
      </div>

      {/* Navigation Arrows */}
      <button
        onClick={prevSlide}
        className="absolute left-4 top-1/2 -translate-y-1/2 w-10 h-10 flex items-center justify-center bg-background/80 hover:bg-background border border-border rounded-full transition-colors"
        aria-label="Slide précédente"
      >
        <ChevronLeft className="h-5 w-5" />
      </button>
      <button
        onClick={nextSlide}
        className="absolute right-4 top-1/2 -translate-y-1/2 w-10 h-10 flex items-center justify-center bg-background/80 hover:bg-background border border-border rounded-full transition-colors"
        aria-label="Slide suivante"
      >
        <ChevronRight className="h-5 w-5" />
      </button>

      {/* Dots */}
      <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2">
        {banners.map((_, index) => (
          <button
            key={index}
            onClick={() => setCurrentSlide(index)}
            className={`w-2 h-2 rounded-full transition-colors ${
              index === currentSlide ? "bg-foreground" : "bg-foreground/30"
            }`}
            aria-label={`Aller à la slide ${index + 1}`}
          />
        ))}
      </div>
    </section>
  )
}
