"use client"

import { useState } from "react"
import { Header } from "@/components/header"
import { Footer } from "@/components/footer"
import { ProductCard, type Product } from "@/components/product-card"
import { Heart, ShoppingBag, Star, Truck, RotateCcw, Shield, ChevronLeft, ChevronRight, Minus, Plus, Check, Share2 } from "lucide-react"
import Link from "next/link"
import Image from "next/image"
import { useAuth } from "@/context/auth-context"

const productImages = [
  "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=800&h=1000&fit=crop",
  "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=800&h=1000&fit=crop&sat=-100",
  "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=800&h=1000&fit=crop&flip=h",
  "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=800&h=1000&fit=crop&blur=2",
]

const sizes = ["XS", "S", "M", "L", "XL", "XXL"]
const colors = [
  { name: "Noir", value: "#000000" },
  { name: "Blanc", value: "#FFFFFF" },
  { name: "Rose", value: "#EC4899" },
  { name: "Bleu", value: "#3B82F6" },
]

const reviews = [
  {
    id: 1,
    author: "Marie L.",
    rating: 5,
    date: "Il y a 2 jours",
    size: "M",
    comment: "Magnifique robe ! La qualité est vraiment au rendez-vous pour ce prix. Je recommande vivement.",
    helpful: 24,
    images: ["https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=200&h=200&fit=crop"],
  },
  {
    id: 2,
    author: "Sophie D.",
    rating: 4,
    date: "Il y a 1 semaine",
    size: "S",
    comment: "Très belle robe, conforme aux photos. Je retire une étoile car la livraison a été un peu longue.",
    helpful: 12,
  },
  {
    id: 3,
    author: "Emma B.",
    rating: 5,
    date: "Il y a 2 semaines",
    size: "L",
    comment: "Parfaite pour l'été ! Le tissu est léger et agréable. J'adore le motif floral.",
    helpful: 18,
    images: [
      "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=200&h=200&fit=crop",
      "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=200&h=200&fit=crop&sat=-50",
    ],
  },
]

const relatedProducts: Product[] = [
  {
    id: "2",
    name: "Robe longue à imprimé bohème",
    price: 29.99,
    originalPrice: 49.99,
    image: "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=400&h=600&fit=crop",
    rating: 4.5,
    reviews: 892,
    colors: ["#000000", "#D4B896"],
  },
  {
    id: "3",
    name: "Robe midi plissée élégante",
    price: 34.99,
    image: "https://images.unsplash.com/photo-1583496661160-fb5886a0afe1?w=400&h=600&fit=crop",
    rating: 4.7,
    reviews: 456,
    colors: ["#EC4899", "#3B82F6", "#000000"],
  },
  {
    id: "4",
    name: "Robe courte à volants",
    price: 22.99,
    originalPrice: 35.99,
    image: "https://images.unsplash.com/photo-1509631179647-0177331693ae?w=400&h=600&fit=crop",
    rating: 4.4,
    reviews: 321,
    tag: "Nouveau",
    colors: ["#FFFFFF", "#EC4899"],
  },
  {
    id: "5",
    name: "Robe chemise en lin",
    price: 27.99,
    image: "https://images.unsplash.com/photo-1598554747436-c9293d6a588f?w=400&h=600&fit=crop",
    rating: 4.6,
    reviews: 678,
    colors: ["#D4B896", "#FFFFFF"],
  },
]

export default function ProductDetailPage() {
  const { requireAuth } = useAuth()
  const [selectedImage, setSelectedImage] = useState(0)
  const [selectedSize, setSelectedSize] = useState<string | null>(null)
  const [selectedColor, setSelectedColor] = useState(colors[0])
  const [quantity, setQuantity] = useState(1)
  const [isWishlisted, setIsWishlisted] = useState(false)
  const [activeTab, setActiveTab] = useState<"description" | "details" | "reviews">("description")

  const product = {
    name: "Robe midi à imprimé floral avec ceinture ajustable",
    price: 24.99,
    originalPrice: 45.99,
    rating: 4.5,
    reviews: 1234,
    sku: "SKU: MS-DRESS-001",
  }

  const discountPercentage = Math.round(
    ((product.originalPrice - product.price) / product.originalPrice) * 100
  )

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
          <Link href="/femmes/robes" className="hover:text-foreground transition-colors">Robes</Link>
          <span>/</span>
          <span className="text-foreground">Robe midi floral</span>
        </nav>
      </div>

      {/* Product Section */}
      <section className="max-w-7xl mx-auto px-4 py-6">
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Image Gallery */}
          <div className="flex flex-col-reverse lg:flex-row gap-4">
            {/* Thumbnails */}
            <div className="flex lg:flex-col gap-2 overflow-x-auto lg:overflow-y-auto lg:max-h-[600px]">
              {productImages.map((img, index) => (
                <button
                  key={index}
                  onClick={() => setSelectedImage(index)}
                  className={`flex-shrink-0 w-16 h-20 lg:w-20 lg:h-24 relative border-2 transition-colors ${
                    selectedImage === index ? "border-foreground" : "border-transparent hover:border-muted-foreground"
                  }`}
                >
                  <Image src={img} alt={`Vue ${index + 1}`} fill className="object-cover" />
                </button>
              ))}
            </div>

            {/* Main Image */}
            <div className="relative flex-1 aspect-[3/4] bg-secondary">
              <Image
                src={productImages[selectedImage]}
                alt={product.name}
                fill
                className="object-cover"
              />
              {/* Navigation Arrows */}
              <button
                onClick={() => setSelectedImage((prev) => (prev > 0 ? prev - 1 : productImages.length - 1))}
                className="absolute left-2 top-1/2 -translate-y-1/2 w-10 h-10 flex items-center justify-center bg-background/80 rounded-full hover:bg-background transition-colors"
                aria-label="Image précédente"
              >
                <ChevronLeft className="h-5 w-5" />
              </button>
              <button
                onClick={() => setSelectedImage((prev) => (prev < productImages.length - 1 ? prev + 1 : 0))}
                className="absolute right-2 top-1/2 -translate-y-1/2 w-10 h-10 flex items-center justify-center bg-background/80 rounded-full hover:bg-background transition-colors"
                aria-label="Image suivante"
              >
                <ChevronRight className="h-5 w-5" />
              </button>
              {/* Discount Badge */}
              <span className="absolute top-4 left-4 px-3 py-1 bg-red-500 text-white text-sm font-medium">
                -{discountPercentage}%
              </span>
            </div>
          </div>

          {/* Product Info */}
          <div className="space-y-6">
            {/* Title & Rating */}
            <div>
              <h1 className="text-2xl font-bold mb-2 text-balance">{product.name}</h1>
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-1">
                  {[...Array(5)].map((_, i) => (
                    <Star
                      key={i}
                      className={`h-4 w-4 ${
                        i < Math.floor(product.rating)
                          ? "fill-amber-400 text-amber-400"
                          : "text-muted-foreground"
                      }`}
                    />
                  ))}
                  <span className="ml-1 text-sm font-medium">{product.rating}</span>
                </div>
                <span className="text-sm text-muted-foreground">
                  ({product.reviews.toLocaleString()} avis)
                </span>
                <span className="text-sm text-muted-foreground">{product.sku}</span>
              </div>
            </div>

            {/* Price */}
            <div className="flex items-baseline gap-3">
              <span className="text-3xl font-bold">CA${product.price.toFixed(2)}</span>
              <span className="text-xl text-muted-foreground line-through">
                CA${product.originalPrice.toFixed(2)}
              </span>
              <span className="text-red-500 font-medium">-{discountPercentage}%</span>
            </div>

            {/* Color Selection */}
            <div>
              <div className="flex items-center gap-2 mb-3">
                <span className="font-medium">Couleur:</span>
                <span>{selectedColor.name}</span>
              </div>
              <div className="flex gap-2">
                {colors.map((color) => (
                  <button
                    key={color.value}
                    onClick={() => setSelectedColor(color)}
                    className={`w-10 h-10 rounded-full border-2 flex items-center justify-center transition-all ${
                      selectedColor.value === color.value
                        ? "border-foreground scale-110"
                        : "border-border hover:border-muted-foreground"
                    }`}
                    style={{ backgroundColor: color.value }}
                    title={color.name}
                  >
                    {selectedColor.value === color.value && (
                      <Check className={`h-5 w-5 ${color.value === "#FFFFFF" ? "text-foreground" : "text-white"}`} />
                    )}
                  </button>
                ))}
              </div>
            </div>

            {/* Size Selection */}
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="font-medium">Taille:</span>
                <button className="text-sm underline text-muted-foreground hover:text-foreground transition-colors">
                  Guide des tailles
                </button>
              </div>
              <div className="flex flex-wrap gap-2">
                {sizes.map((size) => (
                  <button
                    key={size}
                    onClick={() => setSelectedSize(size)}
                    className={`min-w-[48px] h-10 px-4 border text-sm font-medium transition-colors ${
                      selectedSize === size
                        ? "bg-foreground text-background border-foreground"
                        : "border-border hover:border-foreground"
                    }`}
                  >
                    {size}
                  </button>
                ))}
              </div>
            </div>

            {/* Quantity */}
            <div>
              <span className="font-medium mb-3 block">Quantité:</span>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setQuantity((prev) => Math.max(1, prev - 1))}
                  className="w-10 h-10 flex items-center justify-center border border-border hover:border-foreground transition-colors"
                  aria-label="Diminuer la quantité"
                >
                  <Minus className="h-4 w-4" />
                </button>
                <span className="w-12 text-center font-medium">{quantity}</span>
                <button
                  onClick={() => setQuantity((prev) => prev + 1)}
                  className="w-10 h-10 flex items-center justify-center border border-border hover:border-foreground transition-colors"
                  aria-label="Augmenter la quantité"
                >
                  <Plus className="h-4 w-4" />
                </button>
              </div>
            </div>

            {/* Actions */}
            <div className="flex gap-3">
              <button
                className="flex-1 flex items-center justify-center gap-2 h-12 bg-foreground text-background font-medium hover:opacity-90 transition-opacity"
                onClick={() => {
                  requireAuth("passer commande")
                }}
              >
                <ShoppingBag className="h-5 w-5" />
                Ajouter au panier
              </button>
              <button
                onClick={() => {
                  if (!requireAuth("ajouter des produits aux favoris")) {
                    return
                  }
                  setIsWishlisted(!isWishlisted)
                }}
                className={`w-12 h-12 flex items-center justify-center border transition-colors ${
                  isWishlisted
                    ? "border-red-500 text-red-500"
                    : "border-border hover:border-foreground"
                }`}
                aria-label={isWishlisted ? "Retirer des favoris" : "Ajouter aux favoris"}
              >
                <Heart className={`h-5 w-5 ${isWishlisted ? "fill-red-500" : ""}`} />
              </button>
              <button
                className="w-12 h-12 flex items-center justify-center border border-border hover:border-foreground transition-colors"
                aria-label="Partager"
              >
                <Share2 className="h-5 w-5" />
              </button>
            </div>

            {/* Benefits */}
            <div className="grid grid-cols-3 gap-4 py-4 border-t border-b border-border">
              <div className="flex flex-col items-center text-center gap-2">
                <Truck className="h-6 w-6" />
                <span className="text-xs">Livraison gratuite dès 49$</span>
              </div>
              <div className="flex flex-col items-center text-center gap-2">
                <RotateCcw className="h-6 w-6" />
                <span className="text-xs">Retours gratuits 35 jours</span>
              </div>
              <div className="flex flex-col items-center text-center gap-2">
                <Shield className="h-6 w-6" />
                <span className="text-xs">Paiement sécurisé</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Tabs Section */}
      <section className="max-w-7xl mx-auto px-4 py-8">
        {/* Tab Headers */}
        <div className="flex border-b border-border">
          {[
            { id: "description", label: "Description" },
            { id: "details", label: "Détails & Entretien" },
            { id: "reviews", label: `Avis (${product.reviews})` },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as typeof activeTab)}
              className={`px-6 py-3 text-sm font-medium border-b-2 -mb-px transition-colors ${
                activeTab === tab.id
                  ? "border-foreground text-foreground"
                  : "border-transparent text-muted-foreground hover:text-foreground"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Tab Content */}
        <div className="py-6">
          {activeTab === "description" && (
            <div className="prose max-w-none">
              <p className="text-muted-foreground leading-relaxed">
                Cette magnifique robe midi à imprimé floral est parfaite pour toutes les occasions estivales. 
                Confectionnée dans un tissu léger et fluide, elle offre un confort optimal tout au long de la journée. 
                Sa coupe flatteuse met en valeur la silhouette tandis que la ceinture ajustable permet de définir la taille.
              </p>
              <ul className="mt-4 space-y-2 text-muted-foreground">
                <li>Coupe midi élégante arrivant sous le genou</li>
                <li>Imprimé floral exclusif aux couleurs vives</li>
                <li>Ceinture amovible pour un ajustement personnalisé</li>
                <li>Col en V flatteur</li>
                <li>Manches courtes évasées</li>
              </ul>
            </div>
          )}

          {activeTab === "details" && (
            <div className="grid md:grid-cols-2 gap-8">
              <div>
                <h3 className="font-semibold mb-4">Composition</h3>
                <ul className="space-y-2 text-muted-foreground">
                  <li>100% Polyester</li>
                  <li>Doublure: 100% Polyester</li>
                </ul>
              </div>
              <div>
                <h3 className="font-semibold mb-4">Entretien</h3>
                <ul className="space-y-2 text-muted-foreground">
                  <li>Lavage en machine à 30°C maximum</li>
                  <li>Ne pas utiliser de sèche-linge</li>
                  <li>Repasser à basse température</li>
                  <li>Ne pas nettoyer à sec</li>
                </ul>
              </div>
            </div>
          )}

          {activeTab === "reviews" && (
            <div>
              {/* Rating Summary */}
              <div className="flex flex-col md:flex-row gap-8 mb-8 pb-8 border-b border-border">
                <div className="text-center">
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
                  <p className="text-sm text-muted-foreground">{product.reviews} avis</p>
                  <button
                    className="mt-3 px-4 py-2 text-sm font-medium bg-foreground text-background rounded hover:opacity-90 transition-opacity"
                    onClick={() => {
                      requireAuth("publier un avis")
                    }}
                  >
                    Donner mon avis
                  </button>
                </div>
                <div className="flex-1 space-y-2">
                  {[5, 4, 3, 2, 1].map((stars) => (
                    <div key={stars} className="flex items-center gap-2">
                      <span className="w-8 text-sm">{stars}</span>
                      <Star className="h-4 w-4 fill-amber-400 text-amber-400" />
                      <div className="flex-1 h-2 bg-secondary rounded-full overflow-hidden">
                        <div
                          className="h-full bg-amber-400"
                          style={{ width: stars === 5 ? "65%" : stars === 4 ? "25%" : stars === 3 ? "7%" : "2%" }}
                        />
                      </div>
                      <span className="w-12 text-sm text-muted-foreground text-right">
                        {stars === 5 ? "65%" : stars === 4 ? "25%" : stars === 3 ? "7%" : "2%"}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Reviews List */}
              <div className="space-y-6">
                {reviews.map((review) => (
                  <div key={review.id} className="border-b border-border pb-6">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-3">
                        <span className="font-medium">{review.author}</span>
                        <span className="text-sm text-muted-foreground">Taille: {review.size}</span>
                      </div>
                      <span className="text-sm text-muted-foreground">{review.date}</span>
                    </div>
                    <div className="flex mb-2">
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
                    <p className="text-muted-foreground mb-3">{review.comment}</p>
                    {review.images && (
                      <div className="flex gap-2 mb-3">
                        {review.images.map((img, idx) => (
                          <div key={idx} className="relative w-20 h-20">
                            <Image src={img} alt={`Photo client ${idx + 1}`} fill className="object-cover rounded" />
                          </div>
                        ))}
                      </div>
                    )}
                    <button className="text-sm text-muted-foreground hover:text-foreground transition-colors">
                      Utile ({review.helpful})
                    </button>
                  </div>
                ))}
              </div>

              <div className="mt-6 flex gap-4">
                <Link
                  href="/produit/1/avis"
                  className="px-6 py-2 border border-foreground text-foreground font-medium hover:bg-foreground hover:text-background transition-colors"
                >
                  Voir tous les {product.reviews} avis
                </Link>
                <button
                  className="px-6 py-2 bg-foreground text-background font-medium hover:opacity-90 transition-opacity"
                  onClick={() => {
                    requireAuth("publier un avis")
                  }}
                >
                  Donner mon avis
                </button>
              </div>
            </div>
          )}
        </div>
      </section>

      {/* Related Products */}
      <section className="max-w-7xl mx-auto px-4 py-8">
        <h2 className="text-2xl font-bold mb-6">Vous aimerez aussi</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {relatedProducts.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </section>

      <Footer />
    </div>
  )
}
