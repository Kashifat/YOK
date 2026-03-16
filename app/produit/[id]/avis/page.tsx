"use client"

import { useState } from "react"
import { Header } from "@/components/header"
import { Footer } from "@/components/footer"
import { WriteReviewModal } from "@/components/write-review-modal"
import { Star, ThumbsUp, ChevronDown, Filter, Image as ImageIcon, Check, Camera, SlidersHorizontal } from "lucide-react"
import Link from "next/link"
import Image from "next/image"

const allReviews = [
  {
    id: 1,
    author: "Marie L.",
    avatar: "M",
    rating: 5,
    date: "15 janvier 2024",
    verified: true,
    size: "M",
    fit: "Taille parfaitement",
    title: "Magnifique robe, qualité au top !",
    comment: "Magnifique robe ! La qualité est vraiment au rendez-vous pour ce prix. Le tissu est léger et agréable à porter. Les coutures sont bien faites et le motif floral est superbe. Je recommande vivement ce produit !",
    helpful: 24,
    images: [
      "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400&h=400&fit=crop",
      "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400&h=400&fit=crop&sat=-50",
    ],
    recommend: true,
  },
  {
    id: 2,
    author: "Sophie D.",
    avatar: "S",
    rating: 4,
    date: "12 janvier 2024",
    verified: true,
    size: "S",
    fit: "Taille petit",
    title: "Très belle mais prendre une taille au-dessus",
    comment: "Très belle robe, conforme aux photos. La couleur est exactement comme sur les images. Je retire une étoile car elle taille un peu petit, je conseille de prendre une taille au-dessus. Sinon le tissu est de bonne qualité.",
    helpful: 12,
    recommend: true,
  },
  {
    id: 3,
    author: "Emma B.",
    avatar: "E",
    rating: 5,
    date: "8 janvier 2024",
    verified: true,
    size: "L",
    fit: "Taille parfaitement",
    title: "Parfaite pour l'été !",
    comment: "Parfaite pour l'été ! Le tissu est léger et agréable. J'adore le motif floral, il est très élégant. La ceinture permet d'ajuster parfaitement à la taille. J'ai reçu beaucoup de compliments !",
    helpful: 18,
    images: [
      "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400&h=400&fit=crop",
      "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400&h=400&fit=crop&sat=-50",
      "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400&h=400&fit=crop&flip=h",
    ],
    recommend: true,
  },
  {
    id: 4,
    author: "Julie M.",
    avatar: "J",
    rating: 3,
    date: "5 janvier 2024",
    verified: true,
    size: "M",
    fit: "Taille grand",
    title: "Correct mais quelques défauts",
    comment: "La robe est jolie mais j'ai trouvé quelques petits défauts de finition sur les coutures. Le tissu est correct mais un peu plus fin que ce que j'imaginais. Pour le prix ça reste acceptable.",
    helpful: 8,
    recommend: false,
  },
  {
    id: 5,
    author: "Camille R.",
    avatar: "C",
    rating: 5,
    date: "2 janvier 2024",
    verified: true,
    size: "XS",
    fit: "Taille parfaitement",
    title: "Coup de coeur absolu !",
    comment: "C'est exactement ce que je cherchais ! La robe tombe parfaitement, le tissu est fluide et confortable. Je l'ai portée pour un mariage et j'ai eu énormément de compliments. Je vais sûrement la commander dans une autre couleur.",
    helpful: 31,
    images: [
      "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400&h=400&fit=crop",
    ],
    recommend: true,
  },
  {
    id: 6,
    author: "Laura P.",
    avatar: "L",
    rating: 4,
    date: "28 décembre 2023",
    verified: true,
    size: "S",
    fit: "Taille parfaitement",
    title: "Très satisfaite de mon achat",
    comment: "Belle robe, bien coupée. La livraison a été rapide. Le seul bémol est que le coloris est légèrement différent de la photo, un peu plus foncé. Mais ça reste très joli !",
    helpful: 5,
    recommend: true,
  },
]

const product = {
  id: "1",
  name: "Robe midi à imprimé floral avec ceinture ajustable",
  image: "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400&h=500&fit=crop",
  price: 24.99,
  rating: 4.5,
  totalReviews: 1234,
  ratingBreakdown: {
    5: 802,
    4: 308,
    3: 86,
    2: 25,
    1: 13,
  },
  fitBreakdown: {
    small: 15,
    perfect: 75,
    large: 10,
  },
  recommendPercentage: 92,
}

type SortOption = "recent" | "helpful" | "highest" | "lowest"
type FilterOption = "all" | "5" | "4" | "3" | "2" | "1" | "with-photos"

export default function ProductReviewsPage() {
  const [sortBy, setSortBy] = useState<SortOption>("helpful")
  const [filterBy, setFilterBy] = useState<FilterOption>("all")
  const [showFilters, setShowFilters] = useState(false)
  const [helpfulReviews, setHelpfulReviews] = useState<number[]>([])
  const [selectedImage, setSelectedImage] = useState<string | null>(null)
  const [showWriteReview, setShowWriteReview] = useState(false)

  const filteredReviews = allReviews
    .filter((review) => {
      if (filterBy === "all") return true
      if (filterBy === "with-photos") return review.images && review.images.length > 0
      return review.rating === parseInt(filterBy)
    })
    .sort((a, b) => {
      if (sortBy === "recent") return new Date(b.date).getTime() - new Date(a.date).getTime()
      if (sortBy === "helpful") return b.helpful - a.helpful
      if (sortBy === "highest") return b.rating - a.rating
      if (sortBy === "lowest") return a.rating - b.rating
      return 0
    })

  const toggleHelpful = (reviewId: number) => {
    setHelpfulReviews((prev) =>
      prev.includes(reviewId)
        ? prev.filter((id) => id !== reviewId)
        : [...prev, reviewId]
    )
  }

  const getPercentage = (count: number) => Math.round((count / product.totalReviews) * 100)

  return (
    <div className="min-h-screen bg-background">
      <Header />

      {/* Breadcrumb */}
      <div className="max-w-7xl mx-auto px-4 py-3 text-sm">
        <nav className="flex items-center gap-2 text-muted-foreground">
          <Link href="/" className="hover:text-foreground transition-colors">Accueil</Link>
          <span>/</span>
          <Link href="/femmes" className="hover:text-foreground transition-colors">Femmes</Link>
          <span>/</span>
          <Link href="/produit/1" className="hover:text-foreground transition-colors">Robe midi floral</Link>
          <span>/</span>
          <span className="text-foreground">Avis</span>
        </nav>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-6">
        <div className="grid lg:grid-cols-4 gap-8">
          {/* Sidebar - Product & Rating Summary */}
          <aside className="lg:col-span-1">
            {/* Product Card */}
            <div className="border border-border rounded-lg p-4 mb-6">
              <Link href="/produit/1" className="flex gap-4">
                <div className="relative w-20 h-24 flex-shrink-0">
                  <Image
                    src={product.image}
                    alt={product.name}
                    fill
                    className="object-cover rounded"
                  />
                </div>
                <div className="flex-1">
                  <h2 className="font-medium text-sm line-clamp-2">{product.name}</h2>
                  <p className="text-lg font-bold mt-1">CA${product.price.toFixed(2)}</p>
                </div>
              </Link>
            </div>

            {/* Rating Summary */}
            <div className="border border-border rounded-lg p-4 mb-6">
              <h3 className="font-semibold mb-4">Résumé des avis</h3>
              
              {/* Overall Rating */}
              <div className="text-center mb-6 pb-6 border-b border-border">
                <div className="text-5xl font-bold mb-2">{product.rating}</div>
                <div className="flex justify-center mb-2">
                  {[...Array(5)].map((_, i) => (
                    <Star
                      key={i}
                      className={`h-5 w-5 ${
                        i < Math.floor(product.rating)
                          ? "fill-amber-400 text-amber-400"
                          : "text-muted-foreground"
                      }`}
                    />
                  ))}
                </div>
                <p className="text-sm text-muted-foreground">
                  Basé sur {product.totalReviews.toLocaleString()} avis
                </p>
              </div>

              {/* Rating Breakdown */}
              <div className="space-y-2 mb-6">
                {[5, 4, 3, 2, 1].map((stars) => {
                  const count = product.ratingBreakdown[stars as keyof typeof product.ratingBreakdown]
                  const percentage = getPercentage(count)
                  return (
                    <button
                      key={stars}
                      onClick={() => setFilterBy(stars.toString() as FilterOption)}
                      className={`w-full flex items-center gap-2 p-1 rounded transition-colors ${
                        filterBy === stars.toString() ? "bg-secondary" : "hover:bg-secondary/50"
                      }`}
                    >
                      <span className="w-4 text-sm">{stars}</span>
                      <Star className="h-3 w-3 fill-amber-400 text-amber-400" />
                      <div className="flex-1 h-2 bg-secondary rounded-full overflow-hidden">
                        <div
                          className="h-full bg-amber-400"
                          style={{ width: `${percentage}%` }}
                        />
                      </div>
                      <span className="w-8 text-xs text-muted-foreground text-right">{count}</span>
                    </button>
                  )
                })}
              </div>

              {/* Fit Breakdown */}
              <div className="mb-6">
                <h4 className="text-sm font-medium mb-3">Taille de l'article</h4>
                <div className="flex items-center gap-1 text-xs">
                  <span>Petit</span>
                  <div className="flex-1 h-2 bg-secondary rounded-full overflow-hidden flex">
                    <div className="h-full bg-foreground/60" style={{ width: `${product.fitBreakdown.small}%` }} />
                    <div className="h-full bg-foreground" style={{ width: `${product.fitBreakdown.perfect}%` }} />
                    <div className="h-full bg-foreground/60" style={{ width: `${product.fitBreakdown.large}%` }} />
                  </div>
                  <span>Grand</span>
                </div>
                <div className="flex justify-between text-xs text-muted-foreground mt-1">
                  <span>{product.fitBreakdown.small}%</span>
                  <span>{product.fitBreakdown.perfect}% parfait</span>
                  <span>{product.fitBreakdown.large}%</span>
                </div>
              </div>

              {/* Recommend */}
              <div className="text-center p-3 bg-emerald-50 rounded-lg">
                <p className="text-2xl font-bold text-emerald-600">{product.recommendPercentage}%</p>
                <p className="text-sm text-emerald-700">recommandent ce produit</p>
              </div>
            </div>

            {/* Write Review CTA */}
            <button
              onClick={() => setShowWriteReview(true)}
              className="w-full py-3 bg-foreground text-background rounded-lg font-medium hover:opacity-90 transition-opacity"
            >
              Donner mon avis
            </button>
          </aside>

          {/* Main Content - Reviews List */}
          <main className="lg:col-span-3">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
              <h1 className="text-2xl font-bold">
                {product.totalReviews.toLocaleString()} avis clients
              </h1>

              <div className="flex items-center gap-3">
                {/* Filter Toggle (Mobile) */}
                <button
                  onClick={() => setShowFilters(!showFilters)}
                  className="sm:hidden flex items-center gap-2 px-4 py-2 border border-border rounded-lg"
                >
                  <SlidersHorizontal className="h-4 w-4" />
                  Filtres
                </button>

                {/* Sort Dropdown */}
                <div className="relative">
                  <select
                    value={sortBy}
                    onChange={(e) => setSortBy(e.target.value as SortOption)}
                    className="appearance-none px-4 py-2 pr-10 border border-border rounded-lg bg-background focus:outline-none focus:border-foreground cursor-pointer"
                  >
                    <option value="helpful">Plus utiles</option>
                    <option value="recent">Plus récents</option>
                    <option value="highest">Note la plus haute</option>
                    <option value="lowest">Note la plus basse</option>
                  </select>
                  <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 pointer-events-none" />
                </div>
              </div>
            </div>

            {/* Filter Pills */}
            <div className={`flex flex-wrap gap-2 mb-6 ${showFilters ? "block" : "hidden sm:flex"}`}>
              <button
                onClick={() => setFilterBy("all")}
                className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                  filterBy === "all"
                    ? "bg-foreground text-background"
                    : "bg-secondary hover:bg-secondary/80"
                }`}
              >
                Tous ({product.totalReviews})
              </button>
              <button
                onClick={() => setFilterBy("with-photos")}
                className={`flex items-center gap-1 px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                  filterBy === "with-photos"
                    ? "bg-foreground text-background"
                    : "bg-secondary hover:bg-secondary/80"
                }`}
              >
                <Camera className="h-4 w-4" />
                Avec photos
              </button>
              {[5, 4, 3, 2, 1].map((stars) => (
                <button
                  key={stars}
                  onClick={() => setFilterBy(stars.toString() as FilterOption)}
                  className={`flex items-center gap-1 px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                    filterBy === stars.toString()
                      ? "bg-foreground text-background"
                      : "bg-secondary hover:bg-secondary/80"
                  }`}
                >
                  {stars}
                  <Star className="h-3 w-3 fill-current" />
                </button>
              ))}
            </div>

            {/* Reviews List */}
            <div className="space-y-6">
              {filteredReviews.map((review) => (
                <article key={review.id} className="border border-border rounded-lg p-6">
                  {/* Review Header */}
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-secondary rounded-full flex items-center justify-center font-medium">
                        {review.avatar}
                      </div>
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="font-medium">{review.author}</span>
                          {review.verified && (
                            <span className="flex items-center gap-1 text-xs text-emerald-600">
                              <Check className="h-3 w-3" />
                              Achat vérifié
                            </span>
                          )}
                        </div>
                        <p className="text-sm text-muted-foreground">{review.date}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="flex">
                        {[...Array(5)].map((_, i) => (
                          <Star
                            key={i}
                            className={`h-4 w-4 ${
                              i < review.rating
                                ? "fill-amber-400 text-amber-400"
                                : "text-muted-foreground"
                            }`}
                          />
                        ))}
                      </div>
                      <p className="text-xs text-muted-foreground mt-1">
                        Taille: {review.size} | {review.fit}
                      </p>
                    </div>
                  </div>

                  {/* Review Content */}
                  {review.title && (
                    <h3 className="font-semibold mb-2">{review.title}</h3>
                  )}
                  <p className="text-muted-foreground leading-relaxed">{review.comment}</p>

                  {/* Review Images */}
                  {review.images && review.images.length > 0 && (
                    <div className="flex gap-2 mt-4">
                      {review.images.map((img, idx) => (
                        <button
                          key={idx}
                          onClick={() => setSelectedImage(img)}
                          className="relative w-20 h-20 overflow-hidden rounded-lg hover:opacity-80 transition-opacity"
                        >
                          <Image
                            src={img}
                            alt={`Photo de ${review.author} ${idx + 1}`}
                            fill
                            className="object-cover"
                          />
                        </button>
                      ))}
                    </div>
                  )}

                  {/* Review Footer */}
                  <div className="flex items-center justify-between mt-4 pt-4 border-t border-border">
                    <div className="flex items-center gap-4">
                      <button
                        onClick={() => toggleHelpful(review.id)}
                        className={`flex items-center gap-2 text-sm transition-colors ${
                          helpfulReviews.includes(review.id)
                            ? "text-foreground font-medium"
                            : "text-muted-foreground hover:text-foreground"
                        }`}
                      >
                        <ThumbsUp className={`h-4 w-4 ${helpfulReviews.includes(review.id) ? "fill-current" : ""}`} />
                        Utile ({review.helpful + (helpfulReviews.includes(review.id) ? 1 : 0)})
                      </button>
                      <button className="text-sm text-muted-foreground hover:text-foreground transition-colors">
                        Signaler
                      </button>
                    </div>
                    {review.recommend !== undefined && (
                      <span className={`text-sm ${review.recommend ? "text-emerald-600" : "text-red-500"}`}>
                        {review.recommend ? "Recommande ce produit" : "Ne recommande pas"}
                      </span>
                    )}
                  </div>
                </article>
              ))}
            </div>

            {/* Load More */}
            <div className="mt-8 text-center">
              <button className="px-8 py-3 border border-border rounded-lg font-medium hover:bg-secondary transition-colors">
                Charger plus d'avis
              </button>
            </div>
          </main>
        </div>
      </div>

      {/* Image Modal */}
      {selectedImage && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/80"
          onClick={() => setSelectedImage(null)}
        >
          <div className="relative max-w-3xl max-h-[90vh] p-4">
            <Image
              src={selectedImage}
              alt="Photo agrandie"
              width={600}
              height={600}
              className="object-contain rounded-lg"
            />
          </div>
        </div>
      )}

      {/* Write Review Modal */}
      <WriteReviewModal
        isOpen={showWriteReview}
        onClose={() => setShowWriteReview(false)}
        product={{
          name: product.name,
          image: product.image,
        }}
      />

      <Footer />
    </div>
  )
}
