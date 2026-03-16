"use client"

import { useState } from "react"
import { Header } from "@/components/header"
import { Footer } from "@/components/footer"
import { ProductCard, type Product } from "@/components/product-card"
import { Trash2, Minus, Plus, Tag, Truck, ShieldCheck, ChevronRight, X } from "lucide-react"
import Link from "next/link"
import Image from "next/image"
import { useAuth } from "@/context/auth-context"

interface CartItem {
  id: string
  name: string
  price: number
  originalPrice?: number
  image: string
  size: string
  color: string
  colorValue: string
  quantity: number
}

const initialCartItems: CartItem[] = [
  {
    id: "1",
    name: "Robe midi à imprimé floral avec ceinture ajustable",
    price: 24.99,
    originalPrice: 45.99,
    image: "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400&h=600&fit=crop",
    size: "M",
    color: "Noir",
    colorValue: "#000000",
    quantity: 1,
  },
  {
    id: "2",
    name: "Blazer oversize à double boutonnage",
    price: 34.99,
    originalPrice: 59.99,
    image: "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=400&h=600&fit=crop",
    size: "S",
    color: "Gris",
    colorValue: "#9CA3AF",
    quantity: 2,
  },
  {
    id: "3",
    name: "Jean taille haute coupe droite vintage",
    price: 29.99,
    image: "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400&h=600&fit=crop",
    size: "L",
    color: "Bleu",
    colorValue: "#3B82F6",
    quantity: 1,
  },
]

const suggestedProducts: Product[] = [
  {
    id: "10",
    name: "Top côtelé à manches longues col V",
    price: 12.99,
    originalPrice: 19.99,
    image: "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=400&h=600&fit=crop",
    rating: 4.6,
    reviews: 543,
    colors: ["#FFFFFF", "#000000", "#EC4899"],
  },
  {
    id: "11",
    name: "Cardigan en maille torsadée",
    price: 32.99,
    image: "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?w=400&h=600&fit=crop",
    rating: 4.8,
    reviews: 321,
    tag: "Coup de coeur",
    colors: ["#D4B896", "#FFFFFF"],
  },
  {
    id: "12",
    name: "Écharpe en cachemire doux",
    price: 18.99,
    image: "https://images.unsplash.com/photo-1584030373081-f37b7bb4fa8e?w=400&h=600&fit=crop",
    rating: 4.5,
    reviews: 892,
    colors: ["#D4B896", "#9CA3AF", "#000000"],
  },
  {
    id: "13",
    name: "Sac à main en cuir synthétique",
    price: 24.99,
    originalPrice: 39.99,
    image: "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400&h=600&fit=crop",
    rating: 4.4,
    reviews: 456,
    colors: ["#000000", "#D4B896"],
  },
]

export default function CartPage() {
  const { requireAuth } = useAuth()
  const [cartItems, setCartItems] = useState(initialCartItems)
  const [promoCode, setPromoCode] = useState("")
  const [promoApplied, setPromoApplied] = useState(false)
  const [promoDiscount, setPromoDiscount] = useState(0)

  const updateQuantity = (id: string, newQuantity: number) => {
    if (newQuantity < 1) return
    setCartItems((items) =>
      items.map((item) => (item.id === id ? { ...item, quantity: newQuantity } : item))
    )
  }

  const removeItem = (id: string) => {
    setCartItems((items) => items.filter((item) => item.id !== id))
  }

  const applyPromoCode = () => {
    if (promoCode.toLowerCase() === "save10") {
      setPromoApplied(true)
      setPromoDiscount(10)
    }
  }

  const removePromo = () => {
    setPromoApplied(false)
    setPromoDiscount(0)
    setPromoCode("")
  }

  const subtotal = cartItems.reduce((sum, item) => sum + item.price * item.quantity, 0)
  const savings = cartItems.reduce(
    (sum, item) => sum + ((item.originalPrice || item.price) - item.price) * item.quantity,
    0
  )
  const promoSavings = promoApplied ? (subtotal * promoDiscount) / 100 : 0
  const shipping = subtotal >= 49 ? 0 : 6.99
  const total = subtotal - promoSavings + shipping

  if (cartItems.length === 0) {
    return (
      <div className="min-h-screen bg-background">
        <Header />
        <div className="max-w-7xl mx-auto px-4 py-16 text-center">
          <div className="max-w-md mx-auto">
            <div className="w-24 h-24 mx-auto mb-6 bg-secondary rounded-full flex items-center justify-center">
              <svg
                className="w-12 h-12 text-muted-foreground"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={1.5}
                  d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"
                />
              </svg>
            </div>
            <h1 className="text-2xl font-bold mb-2">Votre panier est vide</h1>
            <p className="text-muted-foreground mb-6">
              Découvrez nos dernières tendances et ajoutez vos articles préférés.
            </p>
            <Link
              href="/femmes"
              className="inline-block px-8 py-3 bg-foreground text-background font-medium hover:opacity-90 transition-opacity"
            >
              Continuer mes achats
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

      {/* Free Shipping Banner */}
      {subtotal < 49 && (
        <div className="bg-amber-50 border-b border-amber-200">
          <div className="max-w-7xl mx-auto px-4 py-3 text-center">
            <p className="text-sm text-amber-800">
              <Truck className="inline h-4 w-4 mr-1" />
              Plus que <strong>CA${(49 - subtotal).toFixed(2)}</strong> pour la livraison gratuite !
            </p>
            <div className="mt-2 h-1.5 bg-amber-200 rounded-full max-w-xs mx-auto overflow-hidden">
              <div
                className="h-full bg-amber-500 transition-all duration-300"
                style={{ width: `${Math.min((subtotal / 49) * 100, 100)}%` }}
              />
            </div>
          </div>
        </div>
      )}

      <div className="max-w-7xl mx-auto px-4 py-8">
        <h1 className="text-2xl font-bold mb-2">Mon panier</h1>
        <p className="text-muted-foreground mb-8">{cartItems.length} article(s)</p>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Cart Items */}
          <div className="lg:col-span-2 space-y-4">
            {cartItems.map((item) => (
              <div
                key={item.id}
                className="flex gap-4 p-4 border border-border rounded-lg"
              >
                {/* Product Image */}
                <Link href={`/produit/${item.id}`} className="flex-shrink-0">
                  <div className="relative w-24 h-32 sm:w-32 sm:h-40">
                    <Image
                      src={item.image}
                      alt={item.name}
                      fill
                      className="object-cover rounded"
                    />
                  </div>
                </Link>

                {/* Product Details */}
                <div className="flex-1 flex flex-col">
                  <div className="flex justify-between gap-2">
                    <Link href={`/produit/${item.id}`}>
                      <h3 className="font-medium hover:underline line-clamp-2">{item.name}</h3>
                    </Link>
                    <button
                      onClick={() => removeItem(item.id)}
                      className="flex-shrink-0 p-1 text-muted-foreground hover:text-foreground transition-colors"
                      aria-label="Supprimer"
                    >
                      <Trash2 className="h-5 w-5" />
                    </button>
                  </div>

                  <div className="flex items-center gap-3 mt-2 text-sm text-muted-foreground">
                    <span className="flex items-center gap-1">
                      <span
                        className="w-4 h-4 rounded-full border border-border"
                        style={{ backgroundColor: item.colorValue }}
                      />
                      {item.color}
                    </span>
                    <span>|</span>
                    <span>Taille: {item.size}</span>
                  </div>

                  <div className="mt-auto pt-4 flex items-center justify-between">
                    {/* Quantity */}
                    <div className="flex items-center border border-border rounded">
                      <button
                        onClick={() => updateQuantity(item.id, item.quantity - 1)}
                        className="w-8 h-8 flex items-center justify-center hover:bg-secondary transition-colors"
                        aria-label="Diminuer"
                      >
                        <Minus className="h-4 w-4" />
                      </button>
                      <span className="w-8 text-center text-sm font-medium">{item.quantity}</span>
                      <button
                        onClick={() => updateQuantity(item.id, item.quantity + 1)}
                        className="w-8 h-8 flex items-center justify-center hover:bg-secondary transition-colors"
                        aria-label="Augmenter"
                      >
                        <Plus className="h-4 w-4" />
                      </button>
                    </div>

                    {/* Price */}
                    <div className="text-right">
                      <span className="font-bold">CA${(item.price * item.quantity).toFixed(2)}</span>
                      {item.originalPrice && (
                        <span className="block text-sm text-muted-foreground line-through">
                          CA${(item.originalPrice * item.quantity).toFixed(2)}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Order Summary */}
          <div className="lg:col-span-1">
            <div className="sticky top-[120px] border border-border rounded-lg p-6">
              <h2 className="text-lg font-bold mb-4">Résumé de la commande</h2>

              {/* Promo Code */}
              <div className="mb-4 pb-4 border-b border-border">
                {promoApplied ? (
                  <div className="flex items-center justify-between bg-emerald-50 p-3 rounded">
                    <div className="flex items-center gap-2 text-emerald-700">
                      <Tag className="h-4 w-4" />
                      <span className="font-medium">{promoCode.toUpperCase()}</span>
                      <span className="text-sm">(-{promoDiscount}%)</span>
                    </div>
                    <button
                      onClick={removePromo}
                      className="text-emerald-700 hover:text-emerald-800"
                      aria-label="Supprimer le code"
                    >
                      <X className="h-4 w-4" />
                    </button>
                  </div>
                ) : (
                  <div className="flex gap-2">
                    <input
                      type="text"
                      placeholder="Code promo"
                      value={promoCode}
                      onChange={(e) => setPromoCode(e.target.value)}
                      className="flex-1 h-10 px-3 border border-border rounded text-sm focus:outline-none focus:ring-1 focus:ring-foreground"
                    />
                    <button
                      onClick={applyPromoCode}
                      className="px-4 h-10 border border-foreground text-sm font-medium hover:bg-foreground hover:text-background transition-colors"
                    >
                      Appliquer
                    </button>
                  </div>
                )}
              </div>

              {/* Price Breakdown */}
              <div className="space-y-3 text-sm mb-4 pb-4 border-b border-border">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Sous-total</span>
                  <span>CA${subtotal.toFixed(2)}</span>
                </div>
                {savings > 0 && (
                  <div className="flex justify-between text-emerald-600">
                    <span>Économies</span>
                    <span>-CA${savings.toFixed(2)}</span>
                  </div>
                )}
                {promoSavings > 0 && (
                  <div className="flex justify-between text-emerald-600">
                    <span>Réduction promo</span>
                    <span>-CA${promoSavings.toFixed(2)}</span>
                  </div>
                )}
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Livraison</span>
                  <span className={shipping === 0 ? "text-emerald-600" : ""}>
                    {shipping === 0 ? "GRATUIT" : `CA$${shipping.toFixed(2)}`}
                  </span>
                </div>
              </div>

              {/* Total */}
              <div className="flex justify-between items-center mb-6">
                <span className="font-bold text-lg">Total</span>
                <span className="font-bold text-xl">CA${total.toFixed(2)}</span>
              </div>

              {/* Checkout Button */}
              <button
                className="w-full h-12 bg-foreground text-background font-medium hover:opacity-90 transition-opacity flex items-center justify-center gap-2"
                onClick={() => {
                  requireAuth("passer commande")
                }}
              >
                Passer la commande
                <ChevronRight className="h-5 w-5" />
              </button>

              {/* Trust Badges */}
              <div className="mt-4 pt-4 border-t border-border space-y-2">
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <ShieldCheck className="h-4 w-4" />
                  <span>Paiement 100% sécurisé</span>
                </div>
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <Truck className="h-4 w-4" />
                  <span>Livraison en 5-10 jours ouvrables</span>
                </div>
              </div>

              {/* Payment Methods */}
              <div className="mt-4 flex items-center justify-center gap-2">
                {["Visa", "Mastercard", "PayPal", "Apple Pay"].map((method) => (
                  <div
                    key={method}
                    className="w-10 h-6 bg-secondary rounded flex items-center justify-center text-[8px] text-muted-foreground"
                  >
                    {method}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Suggested Products */}
        <section className="mt-12 pt-8 border-t border-border">
          <h2 className="text-xl font-bold mb-6">Complétez votre look</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {suggestedProducts.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        </section>
      </div>

      <Footer />
    </div>
  )
}
