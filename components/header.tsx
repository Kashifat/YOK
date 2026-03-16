"use client"

import { useState } from "react"
import { Search, User, Heart, ShoppingBag, Menu, X, ChevronDown, Users } from "lucide-react"
import Link from "next/link"
import { useAuth } from "@/context/auth-context"

const categories = [
  { name: "FEMMES", href: "/femmes", submenu: ["Robes", "Tops", "Pantalons", "Jeans", "Jupes"] },
  { name: "CURVE + GRANDE TAILLE", href: "/curve", submenu: ["Robes", "Tops", "Lingerie"] },
  { name: "ENFANTS", href: "/enfants", submenu: ["Filles", "Garçons", "Bébés"] },
  { name: "HOMMES", href: "/hommes", submenu: ["T-shirts", "Pantalons", "Vestes"] },
  { name: "BEAUTÉ", href: "/beaute", submenu: ["Maquillage", "Soins", "Parfums"] },
  { name: "MAISON", href: "/maison", submenu: ["Décoration", "Literie", "Cuisine"] },
  { name: "SOLDES", href: "/soldes", isRed: true },
]

export function Header() {
  const { isAuthenticated, logout } = useAuth()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")

  return (
    <header className="sticky top-0 z-50 bg-background">
      {/* Top Banner */}
      <div className="bg-foreground text-background text-center py-2 text-sm">
        <p className="font-medium">
          LIVRAISON GRATUITE dès 49$ | Retours gratuits sous 35 jours
        </p>
      </div>

      {/* Main Header */}
      <div className="border-b border-border">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            {/* Mobile Menu Button */}
            <button
              className="lg:hidden p-2"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              aria-label="Menu"
            >
              {mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>

            {/* Logo */}
            <Link href="/" className="flex-shrink-0">
              <h1 className="text-2xl font-bold tracking-tight">MODESTYLE</h1>
            </Link>

            {/* Search Bar - Desktop */}
            <div className="hidden lg:flex flex-1 max-w-xl mx-8">
              <div className="relative w-full">
                <input
                  type="text"
                  placeholder="Rechercher des produits..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full h-10 pl-4 pr-12 border border-border rounded-full bg-secondary text-sm focus:outline-none focus:ring-2 focus:ring-foreground/20"
                />
                <button className="absolute right-0 top-0 h-10 w-10 flex items-center justify-center bg-foreground text-background rounded-full">
                  <Search className="h-4 w-4" />
                </button>
              </div>
            </div>

            {/* Right Icons */}
            <div className="flex items-center gap-4">
              <button className="lg:hidden p-2" aria-label="Rechercher">
                <Search className="h-5 w-5" />
              </button>
              <Link href={isAuthenticated ? "/compte/tableau-de-bord" : "/compte"} className="hidden sm:flex items-center gap-1 text-sm hover:opacity-70 transition-opacity">
                <User className="h-5 w-5" />
                <span className="hidden md:inline">{isAuthenticated ? "Mon compte" : "Compte"}</span>
              </Link>
              <Link href="/favoris" className="flex items-center gap-1 text-sm hover:opacity-70 transition-opacity">
                <Heart className="h-5 w-5" />
                <span className="hidden md:inline">Favoris</span>
              </Link>
              <Link href="/communaute" className="hidden sm:flex items-center gap-1 text-sm hover:opacity-70 transition-opacity">
                <Users className="h-5 w-5" />
                <span className="hidden md:inline">Communauté</span>
              </Link>
              <Link href="/panier" className="flex items-center gap-1 text-sm hover:opacity-70 transition-opacity relative">
                <ShoppingBag className="h-5 w-5" />
                <span className="hidden md:inline">Panier</span>
                <span className="absolute -top-1 -right-1 md:right-auto md:-top-1 md:left-3 bg-red-500 text-white text-xs rounded-full h-4 w-4 flex items-center justify-center">
                  0
                </span>
              </Link>
              {isAuthenticated && (
                <button
                  onClick={logout}
                  className="hidden md:inline text-sm text-muted-foreground hover:text-foreground transition-colors"
                >
                  Deconnexion
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Navigation - Desktop */}
        <nav className="hidden lg:block border-t border-border">
          <div className="max-w-7xl mx-auto px-4">
            <ul className="flex items-center justify-center gap-8 h-12">
              {categories.map((category) => (
                <li key={category.name} className="relative group">
                  <Link
                    href={category.href}
                    className={`flex items-center gap-1 text-sm font-medium hover:opacity-70 transition-opacity ${
                      category.isRed ? "text-red-500" : ""
                    }`}
                  >
                    {category.name}
                    {category.submenu && <ChevronDown className="h-3 w-3" />}
                  </Link>
                  {category.submenu && (
                    <div className="absolute top-full left-0 bg-background border border-border shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 min-w-[180px] z-50">
                      <ul className="py-2">
                        {category.submenu.map((item) => (
                          <li key={item}>
                            <Link
                              href={`${category.href}/${item.toLowerCase()}`}
                              className="block px-4 py-2 text-sm hover:bg-secondary transition-colors"
                            >
                              {item}
                            </Link>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </li>
              ))}
            </ul>
          </div>
        </nav>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="lg:hidden fixed inset-0 top-[104px] bg-background z-40 overflow-y-auto">
          <div className="p-4">
            {/* Mobile Search */}
            <div className="relative mb-4">
              <input
                type="text"
                placeholder="Rechercher des produits..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full h-10 pl-4 pr-12 border border-border rounded-full bg-secondary text-sm focus:outline-none"
              />
              <button className="absolute right-0 top-0 h-10 w-10 flex items-center justify-center bg-foreground text-background rounded-full">
                <Search className="h-4 w-4" />
              </button>
            </div>

            {/* Mobile Navigation */}
            <ul className="space-y-2">
              {categories.map((category) => (
                <li key={category.name}>
                  <Link
                    href={category.href}
                    className={`block py-3 px-4 text-sm font-medium border-b border-border ${
                      category.isRed ? "text-red-500" : ""
                    }`}
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    {category.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </header>
  )
}
