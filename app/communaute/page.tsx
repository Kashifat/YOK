"use client"

import { useState } from "react"
import Image from "next/image"
import Link from "next/link"
import { Header } from "@/components/header"
import { Footer } from "@/components/footer"
import { 
  Heart, 
  MessageCircle, 
  Share2, 
  Bookmark, 
  Camera, 
  X, 
  MoreHorizontal,
  ImagePlus,
  AtSign,
  ShoppingBag,
  TrendingUp,
  Users,
  Sparkles
} from "lucide-react"

const posts = [
  {
    id: 1,
    user: {
      name: "Marie L.",
      avatar: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&h=100&fit=crop",
      isVerified: true,
    },
    images: [
      "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=600&h=800&fit=crop",
    ],
    caption: "Obsédée par cette robe ! Parfaite pour les fêtes de fin d'année ✨ @MODESTYLE #ModestyleStyle #OOTD",
    products: [
      { id: 1, name: "Robe midi satin", price: 45.99, image: "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=100&h=100&fit=crop" }
    ],
    likes: 342,
    comments: 28,
    timeAgo: "2h",
    isLiked: false,
    isSaved: false,
  },
  {
    id: 2,
    user: {
      name: "Sophie D.",
      avatar: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&h=100&fit=crop",
      isVerified: false,
    },
    images: [
      "https://images.unsplash.com/photo-1509631179647-0177331693ae?w=600&h=800&fit=crop",
      "https://images.unsplash.com/photo-1485968579580-b6d095142e6e?w=600&h=800&fit=crop",
    ],
    caption: "Mon haul MODESTYLE est arrivé ! Tout est parfait, je recommande à 100% 🛍️ #ModestyleHaul #Mode",
    products: [
      { id: 2, name: "Blazer oversize", price: 52.99, image: "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=100&h=100&fit=crop" },
      { id: 3, name: "Pantalon large", price: 34.99, image: "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=100&h=100&fit=crop" }
    ],
    likes: 567,
    comments: 45,
    timeAgo: "5h",
    isLiked: true,
    isSaved: true,
  },
  {
    id: 3,
    user: {
      name: "Camille R.",
      avatar: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&h=100&fit=crop",
      isVerified: true,
    },
    images: [
      "https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=600&h=800&fit=crop",
    ],
    caption: "Look du jour avec ma nouvelle jupe @MODESTYLE ! Vous aimez ? 💕 #StyleDuJour #ModestyleLook",
    products: [
      { id: 4, name: "Jupe plissée midi", price: 29.99, image: "https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?w=100&h=100&fit=crop" }
    ],
    likes: 891,
    comments: 72,
    timeAgo: "8h",
    isLiked: false,
    isSaved: false,
  },
  {
    id: 4,
    user: {
      name: "Emma B.",
      avatar: "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=100&h=100&fit=crop",
      isVerified: false,
    },
    images: [
      "https://images.unsplash.com/photo-1539109136881-3be0616acf4b?w=600&h=800&fit=crop",
      "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=600&h=800&fit=crop",
      "https://images.unsplash.com/photo-1469334031218-e382a71b716b?w=600&h=800&fit=crop",
    ],
    caption: "3 façons de porter ce cardigan cozy pour l'hiver ❄️ @MODESTYLE #ModestyleInspo #WinterStyle",
    products: [
      { id: 5, name: "Cardigan oversize", price: 39.99, image: "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=100&h=100&fit=crop" }
    ],
    likes: 1243,
    comments: 98,
    timeAgo: "12h",
    isLiked: true,
    isSaved: false,
  },
]

const trendingHashtags = [
  { tag: "#ModestyleStyle", posts: "12.5K" },
  { tag: "#OOTD", posts: "8.2K" },
  { tag: "#ModestyleHaul", posts: "5.7K" },
  { tag: "#WinterStyle", posts: "4.1K" },
  { tag: "#StyleDuJour", posts: "3.8K" },
]

const topCreators = [
  { name: "Marie L.", avatar: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&h=100&fit=crop", followers: "15.2K" },
  { name: "Camille R.", avatar: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&h=100&fit=crop", followers: "12.8K" },
  { name: "Léa M.", avatar: "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?w=100&h=100&fit=crop", followers: "9.5K" },
]

export default function CommunautePage() {
  const [activeTab, setActiveTab] = useState<"feed" | "trending" | "following">("feed")
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [postsState, setPostsState] = useState(posts)
  const [selectedImageIndex, setSelectedImageIndex] = useState<{[key: number]: number}>({})

  const toggleLike = (postId: number) => {
    setPostsState(prev => prev.map(post => 
      post.id === postId 
        ? { ...post, isLiked: !post.isLiked, likes: post.isLiked ? post.likes - 1 : post.likes + 1 }
        : post
    ))
  }

  const toggleSave = (postId: number) => {
    setPostsState(prev => prev.map(post => 
      post.id === postId 
        ? { ...post, isSaved: !post.isSaved }
        : post
    ))
  }

  const nextImage = (postId: number, totalImages: number) => {
    setSelectedImageIndex(prev => ({
      ...prev,
      [postId]: ((prev[postId] || 0) + 1) % totalImages
    }))
  }

  const prevImage = (postId: number, totalImages: number) => {
    setSelectedImageIndex(prev => ({
      ...prev,
      [postId]: ((prev[postId] || 0) - 1 + totalImages) % totalImages
    }))
  }

  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Hero Section */}
        <div className="text-center mb-8">
          <h1 className="text-3xl md:text-4xl font-bold mb-3">Communauté MODESTYLE</h1>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Partagez vos looks, inspirez la communauté et découvrez les tendances de nos membres
          </p>
        </div>

        {/* Stats Bar */}
        <div className="grid grid-cols-3 gap-4 mb-8">
          <div className="bg-secondary rounded-lg p-4 text-center">
            <div className="flex items-center justify-center gap-2 mb-1">
              <Users className="h-5 w-5 text-muted-foreground" />
              <span className="text-2xl font-bold">125K</span>
            </div>
            <p className="text-sm text-muted-foreground">Membres actifs</p>
          </div>
          <div className="bg-secondary rounded-lg p-4 text-center">
            <div className="flex items-center justify-center gap-2 mb-1">
              <Camera className="h-5 w-5 text-muted-foreground" />
              <span className="text-2xl font-bold">48K</span>
            </div>
            <p className="text-sm text-muted-foreground">Publications</p>
          </div>
          <div className="bg-secondary rounded-lg p-4 text-center">
            <div className="flex items-center justify-center gap-2 mb-1">
              <TrendingUp className="h-5 w-5 text-muted-foreground" />
              <span className="text-2xl font-bold">2.1M</span>
            </div>
            <p className="text-sm text-muted-foreground">Interactions</p>
          </div>
        </div>

        {/* Create Post CTA */}
        <div className="bg-gradient-to-r from-rose-50 to-amber-50 rounded-xl p-6 mb-8 border border-rose-100">
          <div className="flex flex-col md:flex-row items-center gap-4">
            <div className="flex-1 text-center md:text-left">
              <h2 className="text-xl font-semibold mb-2">Partagez votre style !</h2>
              <p className="text-muted-foreground text-sm">
                Postez vos looks MODESTYLE et gagnez jusqu'à 100 points bonus par publication
              </p>
            </div>
            <button 
              onClick={() => setShowCreateModal(true)}
              className="flex items-center gap-2 px-6 py-3 bg-foreground text-background font-medium rounded-full hover:opacity-90 transition-opacity"
            >
              <Camera className="h-5 w-5" />
              Créer une publication
            </button>
          </div>
        </div>

        <div className="flex flex-col lg:flex-row gap-8">
          {/* Main Feed */}
          <div className="flex-1">
            {/* Tabs */}
            <div className="flex gap-4 mb-6 border-b border-border">
              <button 
                onClick={() => setActiveTab("feed")}
                className={`pb-3 px-2 text-sm font-medium border-b-2 transition-colors ${
                  activeTab === "feed" 
                    ? "border-foreground text-foreground" 
                    : "border-transparent text-muted-foreground hover:text-foreground"
                }`}
              >
                Pour toi
              </button>
              <button 
                onClick={() => setActiveTab("trending")}
                className={`pb-3 px-2 text-sm font-medium border-b-2 transition-colors ${
                  activeTab === "trending" 
                    ? "border-foreground text-foreground" 
                    : "border-transparent text-muted-foreground hover:text-foreground"
                }`}
              >
                Tendances
              </button>
              <button 
                onClick={() => setActiveTab("following")}
                className={`pb-3 px-2 text-sm font-medium border-b-2 transition-colors ${
                  activeTab === "following" 
                    ? "border-foreground text-foreground" 
                    : "border-transparent text-muted-foreground hover:text-foreground"
                }`}
              >
                Abonnements
              </button>
            </div>

            {/* Posts */}
            <div className="space-y-6">
              {postsState.map((post) => (
                <article key={post.id} className="bg-background border border-border rounded-xl overflow-hidden">
                  {/* Post Header */}
                  <div className="flex items-center justify-between p-4">
                    <div className="flex items-center gap-3">
                      <div className="relative w-10 h-10">
                        <Image
                          src={post.user.avatar}
                          alt={post.user.name}
                          fill
                          className="object-cover rounded-full"
                        />
                      </div>
                      <div>
                        <div className="flex items-center gap-1">
                          <span className="font-medium text-sm">{post.user.name}</span>
                          {post.user.isVerified && (
                            <Sparkles className="h-4 w-4 text-amber-500" />
                          )}
                        </div>
                        <span className="text-xs text-muted-foreground">{post.timeAgo}</span>
                      </div>
                    </div>
                    <button className="p-2 hover:bg-secondary rounded-full transition-colors">
                      <MoreHorizontal className="h-5 w-5 text-muted-foreground" />
                    </button>
                  </div>

                  {/* Post Images */}
                  <div className="relative aspect-[4/5] bg-secondary">
                    <Image
                      src={post.images[selectedImageIndex[post.id] || 0]}
                      alt="Post image"
                      fill
                      className="object-cover"
                    />
                    {post.images.length > 1 && (
                      <>
                        <button 
                          onClick={() => prevImage(post.id, post.images.length)}
                          className="absolute left-2 top-1/2 -translate-y-1/2 w-8 h-8 bg-background/80 rounded-full flex items-center justify-center hover:bg-background transition-colors"
                        >
                          <span className="sr-only">Précédent</span>
                          ‹
                        </button>
                        <button 
                          onClick={() => nextImage(post.id, post.images.length)}
                          className="absolute right-2 top-1/2 -translate-y-1/2 w-8 h-8 bg-background/80 rounded-full flex items-center justify-center hover:bg-background transition-colors"
                        >
                          <span className="sr-only">Suivant</span>
                          ›
                        </button>
                        <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-1">
                          {post.images.map((_, idx) => (
                            <span 
                              key={idx}
                              className={`w-2 h-2 rounded-full ${
                                (selectedImageIndex[post.id] || 0) === idx 
                                  ? "bg-background" 
                                  : "bg-background/50"
                              }`}
                            />
                          ))}
                        </div>
                      </>
                    )}
                  </div>

                  {/* Post Actions */}
                  <div className="p-4">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-4">
                        <button 
                          onClick={() => toggleLike(post.id)}
                          className="flex items-center gap-1 hover:opacity-70 transition-opacity"
                        >
                          <Heart className={`h-6 w-6 ${post.isLiked ? "fill-red-500 text-red-500" : ""}`} />
                        </button>
                        <button className="flex items-center gap-1 hover:opacity-70 transition-opacity">
                          <MessageCircle className="h-6 w-6" />
                        </button>
                        <button className="flex items-center gap-1 hover:opacity-70 transition-opacity">
                          <Share2 className="h-6 w-6" />
                        </button>
                      </div>
                      <button 
                        onClick={() => toggleSave(post.id)}
                        className="hover:opacity-70 transition-opacity"
                      >
                        <Bookmark className={`h-6 w-6 ${post.isSaved ? "fill-foreground" : ""}`} />
                      </button>
                    </div>

                    <p className="font-medium text-sm mb-1">{post.likes.toLocaleString()} j'aime</p>
                    <p className="text-sm mb-2">
                      <span className="font-medium">{post.user.name}</span>{" "}
                      {post.caption}
                    </p>
                    <button className="text-sm text-muted-foreground hover:text-foreground transition-colors">
                      Voir les {post.comments} commentaires
                    </button>

                    {/* Tagged Products */}
                    {post.products.length > 0 && (
                      <div className="mt-4 pt-4 border-t border-border">
                        <p className="text-xs text-muted-foreground mb-2 flex items-center gap-1">
                          <ShoppingBag className="h-3 w-3" />
                          Produits mentionnés
                        </p>
                        <div className="flex gap-2 overflow-x-auto pb-2">
                          {post.products.map((product) => (
                            <Link
                              key={product.id}
                              href={`/produit/${product.id}`}
                              className="flex items-center gap-2 p-2 border border-border rounded-lg hover:bg-secondary transition-colors flex-shrink-0"
                            >
                              <div className="relative w-10 h-10">
                                <Image
                                  src={product.image}
                                  alt={product.name}
                                  fill
                                  className="object-cover rounded"
                                />
                              </div>
                              <div>
                                <p className="text-xs font-medium line-clamp-1">{product.name}</p>
                                <p className="text-xs text-muted-foreground">{product.price}$</p>
                              </div>
                            </Link>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </article>
              ))}
            </div>

            {/* Load More */}
            <div className="text-center mt-8">
              <button className="px-8 py-3 border border-foreground text-foreground font-medium hover:bg-foreground hover:text-background transition-colors">
                Charger plus
              </button>
            </div>
          </div>

          {/* Sidebar */}
          <aside className="w-full lg:w-80 space-y-6">
            {/* Trending Hashtags */}
            <div className="border border-border rounded-xl p-4">
              <h3 className="font-semibold mb-4 flex items-center gap-2">
                <TrendingUp className="h-5 w-5" />
                Hashtags tendances
              </h3>
              <div className="space-y-3">
                {trendingHashtags.map((hashtag, idx) => (
                  <Link
                    key={hashtag.tag}
                    href={`/communaute/hashtag/${hashtag.tag.slice(1)}`}
                    className="flex items-center justify-between hover:bg-secondary p-2 rounded-lg transition-colors"
                  >
                    <div className="flex items-center gap-3">
                      <span className="text-muted-foreground text-sm">{idx + 1}</span>
                      <span className="font-medium text-sm">{hashtag.tag}</span>
                    </div>
                    <span className="text-xs text-muted-foreground">{hashtag.posts} posts</span>
                  </Link>
                ))}
              </div>
            </div>

            {/* Top Creators */}
            <div className="border border-border rounded-xl p-4">
              <h3 className="font-semibold mb-4 flex items-center gap-2">
                <Sparkles className="h-5 w-5" />
                Créateurs populaires
              </h3>
              <div className="space-y-3">
                {topCreators.map((creator) => (
                  <div key={creator.name} className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="relative w-10 h-10">
                        <Image
                          src={creator.avatar}
                          alt={creator.name}
                          fill
                          className="object-cover rounded-full"
                        />
                      </div>
                      <div>
                        <p className="font-medium text-sm">{creator.name}</p>
                        <p className="text-xs text-muted-foreground">{creator.followers} abonnés</p>
                      </div>
                    </div>
                    <button className="px-3 py-1 text-xs font-medium border border-foreground rounded-full hover:bg-foreground hover:text-background transition-colors">
                      Suivre
                    </button>
                  </div>
                ))}
              </div>
            </div>

            {/* Guidelines */}
            <div className="bg-secondary rounded-xl p-4">
              <h3 className="font-semibold mb-2">Règles de la communauté</h3>
              <ul className="text-sm text-muted-foreground space-y-1">
                <li>• Publiez uniquement vos propres photos</li>
                <li>• Mentionnez les produits MODESTYLE</li>
                <li>• Restez respectueux et bienveillant</li>
                <li>• Pas de contenu inapproprié</li>
              </ul>
            </div>
          </aside>
        </div>
      </main>

      {/* Create Post Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-foreground/50">
          <div className="bg-background rounded-xl w-full max-w-lg max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between p-4 border-b border-border">
              <h2 className="text-lg font-semibold">Créer une publication</h2>
              <button 
                onClick={() => setShowCreateModal(false)}
                className="p-2 hover:bg-secondary rounded-full transition-colors"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
            
            <div className="p-4 space-y-4">
              {/* Image Upload */}
              <div className="border-2 border-dashed border-border rounded-xl p-8 text-center hover:border-foreground/50 transition-colors cursor-pointer">
                <ImagePlus className="h-12 w-12 mx-auto text-muted-foreground mb-3" />
                <p className="font-medium mb-1">Ajouter des photos</p>
                <p className="text-sm text-muted-foreground">Glissez-déposez ou cliquez pour sélectionner</p>
                <p className="text-xs text-muted-foreground mt-2">Maximum 10 photos</p>
              </div>

              {/* Caption */}
              <div>
                <label className="block text-sm font-medium mb-2">Description</label>
                <textarea
                  rows={4}
                  placeholder="Partagez votre look avec la communauté..."
                  className="w-full p-3 border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-foreground/20 resize-none"
                />
              </div>

              {/* Tag Products */}
              <div>
                <label className="block text-sm font-medium mb-2 flex items-center gap-2">
                  <AtSign className="h-4 w-4" />
                  Identifier des produits
                </label>
                <div className="relative">
                  <input
                    type="text"
                    placeholder="Rechercher un produit..."
                    className="w-full p-3 border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-foreground/20"
                  />
                </div>
                <p className="text-xs text-muted-foreground mt-1">
                  Identifiez les produits MODESTYLE que vous portez
                </p>
              </div>

              {/* Hashtags Suggestions */}
              <div>
                <label className="block text-sm font-medium mb-2">Hashtags suggérés</label>
                <div className="flex flex-wrap gap-2">
                  {["#ModestyleStyle", "#OOTD", "#ModestyleHaul", "#StyleDuJour"].map((tag) => (
                    <button
                      key={tag}
                      className="px-3 py-1 text-sm border border-border rounded-full hover:bg-secondary transition-colors"
                    >
                      {tag}
                    </button>
                  ))}
                </div>
              </div>

              {/* Submit */}
              <div className="flex gap-3 pt-4">
                <button
                  onClick={() => setShowCreateModal(false)}
                  className="flex-1 py-3 border border-border font-medium rounded-lg hover:bg-secondary transition-colors"
                >
                  Annuler
                </button>
                <button className="flex-1 py-3 bg-foreground text-background font-medium rounded-lg hover:opacity-90 transition-opacity">
                  Publier
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      <Footer />
    </div>
  )
}
