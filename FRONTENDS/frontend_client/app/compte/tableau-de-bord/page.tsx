"use client"

import { useState } from "react"
import { Header } from "@/components/header"
import { Footer } from "@/components/footer"
import { User, Package, Heart, MapPin, CreditCard, Bell, LogOut, ChevronRight, Edit2, Star, MessageSquare } from "lucide-react"
import Link from "next/link"
import Image from "next/image"

const menuItems = [
  { icon: User, label: "Mon profil", href: "#profile", id: "profile" },
  { icon: Package, label: "Mes commandes", href: "#orders", id: "orders" },
  { icon: MessageSquare, label: "Mes avis", href: "#reviews", id: "reviews" },
  { icon: Heart, label: "Mes favoris", href: "/favoris", id: "wishlist" },
  { icon: MapPin, label: "Mes adresses", href: "#addresses", id: "addresses" },
  { icon: CreditCard, label: "Moyens de paiement", href: "#payment", id: "payment" },
  { icon: Bell, label: "Notifications", href: "#notifications", id: "notifications" },
]

const userReviews = [
  {
    id: 1,
    productName: "Robe midi à imprimé floral",
    productImage: "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=200&h=250&fit=crop",
    rating: 5,
    date: "15 janvier 2024",
    comment: "Magnifique robe ! La qualité est vraiment au rendez-vous pour ce prix.",
    helpful: 24,
    status: "published",
  },
  {
    id: 2,
    productName: "Blazer oversize noir",
    productImage: "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=200&h=250&fit=crop",
    rating: 4,
    date: "10 janvier 2024",
    comment: "Très beau blazer, coupe parfaite. Un peu grand aux épaules pour ma morphologie.",
    helpful: 8,
    status: "published",
  },
]

const pendingReviews = [
  {
    id: 1,
    productName: "Jean vintage taille haute",
    productImage: "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=200&h=250&fit=crop",
    orderDate: "8 janvier 2024",
    orderId: "ORD-2024-1198",
  },
]

const orders = [
  {
    id: "ORD-2024-1234",
    date: "15 janvier 2024",
    status: "Livré",
    statusColor: "bg-emerald-100 text-emerald-700",
    total: 89.97,
    items: [
      {
        name: "Robe midi floral",
        image: "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=200&h=250&fit=crop",
        price: 24.99,
        size: "M",
      },
      {
        name: "Blazer oversize",
        image: "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=200&h=250&fit=crop",
        price: 34.99,
        size: "S",
      },
    ],
  },
  {
    id: "ORD-2024-1198",
    date: "8 janvier 2024",
    status: "En transit",
    statusColor: "bg-amber-100 text-amber-700",
    total: 52.98,
    items: [
      {
        name: "Jean vintage",
        image: "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=200&h=250&fit=crop",
        price: 29.99,
        size: "L",
      },
    ],
  },
]

const addresses = [
  {
    id: "1",
    name: "Marie Dupont",
    address: "123 Rue Principale",
    city: "Montréal, QC H2X 1Y6",
    country: "Canada",
    isDefault: true,
  },
  {
    id: "2",
    name: "Marie Dupont",
    address: "456 Avenue des Pins",
    city: "Québec, QC G1R 2H9",
    country: "Canada",
    isDefault: false,
  },
]

export default function DashboardPage() {
  const [activeSection, setActiveSection] = useState("profile")

  const user = {
    name: "Marie Dupont",
    email: "marie.dupont@email.com",
    phone: "+1 514 555 0123",
    memberSince: "Janvier 2023",
    points: 1250,
  }

  return (
    <div className="min-h-screen bg-background">
      <Header />

      <div className="max-w-7xl mx-auto px-4 py-8">
        <h1 className="text-2xl font-bold mb-8">Mon compte</h1>

        <div className="grid lg:grid-cols-4 gap-8">
          {/* Sidebar */}
          <aside className="lg:col-span-1">
            <div className="border border-border rounded-lg p-4 mb-4">
              <div className="flex items-center gap-3 mb-4 pb-4 border-b border-border">
                <div className="w-12 h-12 bg-secondary rounded-full flex items-center justify-center">
                  <User className="h-6 w-6 text-muted-foreground" />
                </div>
                <div>
                  <p className="font-medium">{user.name}</p>
                  <p className="text-sm text-muted-foreground">{user.points} points</p>
                </div>
              </div>

              <nav className="space-y-1">
                {menuItems.map((item) => (
                  <button
                    key={item.id}
                    onClick={() => setActiveSection(item.id)}
                    className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors ${
                      activeSection === item.id
                        ? "bg-secondary font-medium"
                        : "hover:bg-secondary/50"
                    }`}
                  >
                    <item.icon className="h-5 w-5" />
                    {item.label}
                  </button>
                ))}
              </nav>
            </div>

            <button className="w-full flex items-center gap-3 px-4 py-3 text-sm text-red-500 hover:bg-red-50 rounded-lg transition-colors">
              <LogOut className="h-5 w-5" />
              Déconnexion
            </button>
          </aside>

          {/* Main Content */}
          <main className="lg:col-span-3">
            {/* Profile Section */}
            {activeSection === "profile" && (
              <div className="border border-border rounded-lg p-6">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-lg font-semibold">Informations personnelles</h2>
                  <button className="flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground transition-colors">
                    <Edit2 className="h-4 w-4" />
                    Modifier
                  </button>
                </div>

                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <label className="text-sm text-muted-foreground">Nom complet</label>
                    <p className="font-medium">{user.name}</p>
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground">Email</label>
                    <p className="font-medium">{user.email}</p>
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground">Téléphone</label>
                    <p className="font-medium">{user.phone}</p>
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground">Membre depuis</label>
                    <p className="font-medium">{user.memberSince}</p>
                  </div>
                </div>

                {/* Points Card */}
                <div className="mt-8 p-4 bg-gradient-to-r from-foreground to-foreground/80 text-background rounded-lg">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm opacity-80">Points de fidélité</p>
                      <p className="text-3xl font-bold">{user.points.toLocaleString()}</p>
                      <p className="text-sm opacity-80 mt-1">= CA${(user.points * 0.01).toFixed(2)} de réduction</p>
                    </div>
                    <div className="text-right">
                      <Star className="h-8 w-8 inline-block" />
                      <p className="text-sm mt-1">Membre Gold</p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Orders Section */}
            {activeSection === "orders" && (
              <div className="space-y-4">
                <h2 className="text-lg font-semibold mb-4">Mes commandes</h2>
                
                {orders.map((order) => (
                  <div key={order.id} className="border border-border rounded-lg p-4">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4 pb-4 border-b border-border">
                      <div>
                        <p className="font-medium">{order.id}</p>
                        <p className="text-sm text-muted-foreground">{order.date}</p>
                      </div>
                      <div className="flex items-center gap-3">
                        <span className={`px-3 py-1 rounded-full text-xs font-medium ${order.statusColor}`}>
                          {order.status}
                        </span>
                        <span className="font-bold">CA${order.total.toFixed(2)}</span>
                      </div>
                    </div>

                    <div className="space-y-3">
                      {order.items.map((item, idx) => (
                        <div key={idx} className="flex gap-3">
                          <div className="relative w-16 h-20 flex-shrink-0">
                            <Image
                              src={item.image}
                              alt={item.name}
                              fill
                              className="object-cover rounded"
                            />
                          </div>
                          <div className="flex-1">
                            <p className="font-medium">{item.name}</p>
                            <p className="text-sm text-muted-foreground">Taille: {item.size}</p>
                            <p className="text-sm">CA${item.price.toFixed(2)}</p>
                          </div>
                        </div>
                      ))}
                    </div>

                    <div className="mt-4 pt-4 border-t border-border flex gap-3">
                      <button className="px-4 py-2 text-sm font-medium border border-border rounded hover:bg-secondary transition-colors">
                        Voir les détails
                      </button>
                      <button className="px-4 py-2 text-sm font-medium border border-border rounded hover:bg-secondary transition-colors">
                        Suivre la livraison
                      </button>
                    </div>
                  </div>
                ))}

                <Link
                  href="/compte/commandes"
                  className="flex items-center justify-center gap-2 py-3 text-sm font-medium border border-border rounded-lg hover:bg-secondary transition-colors"
                >
                  Voir toutes mes commandes
                  <ChevronRight className="h-4 w-4" />
                </Link>
              </div>
            )}

            {/* Addresses Section */}
            {activeSection === "addresses" && (
              <div>
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-lg font-semibold">Mes adresses</h2>
                  <button className="px-4 py-2 text-sm font-medium bg-foreground text-background rounded hover:opacity-90 transition-opacity">
                    Ajouter une adresse
                  </button>
                </div>

                <div className="grid md:grid-cols-2 gap-4">
                  {addresses.map((address) => (
                    <div key={address.id} className="border border-border rounded-lg p-4 relative">
                      {address.isDefault && (
                        <span className="absolute top-2 right-2 px-2 py-0.5 bg-foreground text-background text-xs rounded">
                          Par défaut
                        </span>
                      )}
                      <p className="font-medium">{address.name}</p>
                      <p className="text-sm text-muted-foreground mt-1">{address.address}</p>
                      <p className="text-sm text-muted-foreground">{address.city}</p>
                      <p className="text-sm text-muted-foreground">{address.country}</p>
                      <div className="mt-4 flex gap-2">
                        <button className="text-sm text-muted-foreground hover:text-foreground transition-colors">
                          Modifier
                        </button>
                        <span className="text-muted-foreground">|</span>
                        <button className="text-sm text-red-500 hover:text-red-600 transition-colors">
                          Supprimer
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Payment Section */}
            {activeSection === "payment" && (
              <div>
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-lg font-semibold">Moyens de paiement</h2>
                  <button className="px-4 py-2 text-sm font-medium bg-foreground text-background rounded hover:opacity-90 transition-opacity">
                    Ajouter une carte
                  </button>
                </div>

                <div className="border border-border rounded-lg p-4">
                  <div className="flex items-center gap-4">
                    <div className="w-16 h-10 bg-gradient-to-r from-blue-600 to-blue-800 rounded flex items-center justify-center text-white text-xs font-bold">
                      VISA
                    </div>
                    <div className="flex-1">
                      <p className="font-medium">**** **** **** 4532</p>
                      <p className="text-sm text-muted-foreground">Expire 12/26</p>
                    </div>
                    <span className="px-2 py-0.5 bg-foreground text-background text-xs rounded">
                      Par défaut
                    </span>
                  </div>
                  <div className="mt-4 flex gap-2">
                    <button className="text-sm text-muted-foreground hover:text-foreground transition-colors">
                      Modifier
                    </button>
                    <span className="text-muted-foreground">|</span>
                    <button className="text-sm text-red-500 hover:text-red-600 transition-colors">
                      Supprimer
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* Reviews Section */}
            {activeSection === "reviews" && (
              <div className="space-y-6">
                {/* Pending Reviews */}
                {pendingReviews.length > 0 && (
                  <div className="border border-amber-200 bg-amber-50 rounded-lg p-4">
                    <h3 className="font-semibold text-amber-800 mb-3">
                      Produits en attente d'avis ({pendingReviews.length})
                    </h3>
                    <p className="text-sm text-amber-700 mb-4">
                      Partagez votre expérience et gagnez 50 points par avis !
                    </p>
                    {pendingReviews.map((product) => (
                      <div key={product.id} className="flex items-center gap-4 p-3 bg-background rounded-lg">
                        <div className="relative w-16 h-20 flex-shrink-0">
                          <Image
                            src={product.productImage}
                            alt={product.productName}
                            fill
                            className="object-cover rounded"
                          />
                        </div>
                        <div className="flex-1">
                          <p className="font-medium">{product.productName}</p>
                          <p className="text-sm text-muted-foreground">
                            Commande {product.orderId} - {product.orderDate}
                          </p>
                        </div>
                        <button className="px-4 py-2 bg-foreground text-background text-sm font-medium rounded hover:opacity-90 transition-opacity">
                          Donner mon avis
                        </button>
                      </div>
                    ))}
                  </div>
                )}

                {/* My Reviews */}
                <div>
                  <h2 className="text-lg font-semibold mb-4">Mes avis publiés ({userReviews.length})</h2>
                  <div className="space-y-4">
                    {userReviews.map((review) => (
                      <div key={review.id} className="border border-border rounded-lg p-4">
                        <div className="flex gap-4">
                          <div className="relative w-20 h-24 flex-shrink-0">
                            <Image
                              src={review.productImage}
                              alt={review.productName}
                              fill
                              className="object-cover rounded"
                            />
                          </div>
                          <div className="flex-1">
                            <div className="flex items-start justify-between mb-2">
                              <div>
                                <h3 className="font-medium">{review.productName}</h3>
                                <p className="text-sm text-muted-foreground">{review.date}</p>
                              </div>
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
                            </div>
                            <p className="text-sm text-muted-foreground line-clamp-2">{review.comment}</p>
                            <div className="flex items-center gap-4 mt-3">
                              <span className="text-sm text-muted-foreground">
                                {review.helpful} personnes ont trouvé cet avis utile
                              </span>
                              <button className="text-sm text-muted-foreground hover:text-foreground transition-colors">
                                Modifier
                              </button>
                              <button className="text-sm text-red-500 hover:text-red-600 transition-colors">
                                Supprimer
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Stats */}
                <div className="grid grid-cols-3 gap-4">
                  <div className="border border-border rounded-lg p-4 text-center">
                    <p className="text-3xl font-bold">{userReviews.length}</p>
                    <p className="text-sm text-muted-foreground">Avis publiés</p>
                  </div>
                  <div className="border border-border rounded-lg p-4 text-center">
                    <p className="text-3xl font-bold">{userReviews.reduce((acc, r) => acc + r.helpful, 0)}</p>
                    <p className="text-sm text-muted-foreground">Votes utiles</p>
                  </div>
                  <div className="border border-border rounded-lg p-4 text-center">
                    <p className="text-3xl font-bold">{userReviews.length * 50}</p>
                    <p className="text-sm text-muted-foreground">Points gagnés</p>
                  </div>
                </div>
              </div>
            )}

            {/* Notifications Section */}
            {activeSection === "notifications" && (
              <div>
                <h2 className="text-lg font-semibold mb-4">Préférences de notification</h2>

                <div className="border border-border rounded-lg divide-y divide-border">
                  {[
                    { label: "Promotions et offres spéciales", description: "Recevez nos meilleures offres par email" },
                    { label: "Nouveautés", description: "Soyez informé des dernières tendances" },
                    { label: "Suivi de commande", description: "Notifications sur l'état de vos commandes" },
                    { label: "Rappels panier", description: "Rappels pour les articles dans votre panier" },
                  ].map((notification, index) => (
                    <div key={index} className="flex items-center justify-between p-4">
                      <div>
                        <p className="font-medium">{notification.label}</p>
                        <p className="text-sm text-muted-foreground">{notification.description}</p>
                      </div>
                      <label className="relative inline-flex items-center cursor-pointer">
                        <input type="checkbox" defaultChecked={index < 3} className="sr-only peer" />
                        <div className="w-11 h-6 bg-secondary rounded-full peer peer-checked:bg-foreground peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-background after:rounded-full after:h-5 after:w-5 after:transition-all"></div>
                      </label>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </main>
        </div>
      </div>

      <Footer />
    </div>
  )
}
