"use client"

import { useState } from "react"
import { X, Star, Camera, Upload } from "lucide-react"
import Image from "next/image"

interface WriteReviewModalProps {
  isOpen: boolean
  onClose: () => void
  product: {
    name: string
    image: string
    size?: string
    color?: string
  }
}

export function WriteReviewModal({ isOpen, onClose, product }: WriteReviewModalProps) {
  const [rating, setRating] = useState(0)
  const [hoverRating, setHoverRating] = useState(0)
  const [title, setTitle] = useState("")
  const [comment, setComment] = useState("")
  const [fit, setFit] = useState<"small" | "perfect" | "large" | null>(null)
  const [images, setImages] = useState<string[]>([])
  const [recommend, setRecommend] = useState<boolean | null>(null)

  if (!isOpen) return null

  const handleImageUpload = () => {
    // Simule l'ajout d'une image
    const newImage = "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=200&h=200&fit=crop"
    if (images.length < 5) {
      setImages([...images, newImage])
    }
  }

  const removeImage = (index: number) => {
    setImages(images.filter((_, i) => i !== index))
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // Submit logic here
    onClose()
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Overlay */}
      <div 
        className="absolute inset-0 bg-black/50"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="relative bg-background w-full max-w-2xl max-h-[90vh] overflow-y-auto mx-4 rounded-lg shadow-xl">
        {/* Header */}
        <div className="sticky top-0 bg-background border-b border-border px-6 py-4 flex items-center justify-between">
          <h2 className="text-xl font-semibold">Donnez votre avis</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-secondary rounded-full transition-colors"
            aria-label="Fermer"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {/* Product Info */}
          <div className="flex gap-4 p-4 bg-secondary/50 rounded-lg">
            <div className="relative w-16 h-20 flex-shrink-0">
              <Image
                src={product.image}
                alt={product.name}
                fill
                className="object-cover rounded"
              />
            </div>
            <div>
              <p className="font-medium">{product.name}</p>
              {product.size && (
                <p className="text-sm text-muted-foreground">Taille: {product.size}</p>
              )}
              {product.color && (
                <p className="text-sm text-muted-foreground">Couleur: {product.color}</p>
              )}
            </div>
          </div>

          {/* Rating */}
          <div>
            <label className="block font-medium mb-2">Note globale *</label>
            <div className="flex gap-1">
              {[1, 2, 3, 4, 5].map((star) => (
                <button
                  key={star}
                  type="button"
                  onClick={() => setRating(star)}
                  onMouseEnter={() => setHoverRating(star)}
                  onMouseLeave={() => setHoverRating(0)}
                  className="p-1"
                >
                  <Star
                    className={`h-8 w-8 transition-colors ${
                      star <= (hoverRating || rating)
                        ? "fill-amber-400 text-amber-400"
                        : "text-muted-foreground"
                    }`}
                  />
                </button>
              ))}
            </div>
            <p className="text-sm text-muted-foreground mt-1">
              {rating === 0 && "Cliquez pour noter"}
              {rating === 1 && "Très insatisfait"}
              {rating === 2 && "Insatisfait"}
              {rating === 3 && "Correct"}
              {rating === 4 && "Satisfait"}
              {rating === 5 && "Très satisfait"}
            </p>
          </div>

          {/* Fit */}
          <div>
            <label className="block font-medium mb-2">Comment taille cet article ?</label>
            <div className="flex gap-2">
              {[
                { value: "small", label: "Taille petit" },
                { value: "perfect", label: "Taille parfaitement" },
                { value: "large", label: "Taille grand" },
              ].map((option) => (
                <button
                  key={option.value}
                  type="button"
                  onClick={() => setFit(option.value as typeof fit)}
                  className={`flex-1 py-2 px-4 border rounded-lg text-sm font-medium transition-colors ${
                    fit === option.value
                      ? "border-foreground bg-foreground text-background"
                      : "border-border hover:border-foreground"
                  }`}
                >
                  {option.label}
                </button>
              ))}
            </div>
          </div>

          {/* Title */}
          <div>
            <label className="block font-medium mb-2">Titre de votre avis</label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Résumez votre avis en quelques mots"
              className="w-full px-4 py-3 border border-border rounded-lg focus:outline-none focus:border-foreground transition-colors"
              maxLength={100}
            />
            <p className="text-xs text-muted-foreground mt-1 text-right">{title.length}/100</p>
          </div>

          {/* Comment */}
          <div>
            <label className="block font-medium mb-2">Votre avis *</label>
            <textarea
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              placeholder="Partagez votre expérience avec ce produit. Qu'est-ce qui vous a plu ou déplu ?"
              className="w-full px-4 py-3 border border-border rounded-lg focus:outline-none focus:border-foreground transition-colors resize-none"
              rows={4}
              minLength={20}
              maxLength={1000}
            />
            <p className="text-xs text-muted-foreground mt-1 text-right">{comment.length}/1000</p>
          </div>

          {/* Photos */}
          <div>
            <label className="block font-medium mb-2">Ajouter des photos (optionnel)</label>
            <p className="text-sm text-muted-foreground mb-3">
              Ajoutez jusqu'à 5 photos pour illustrer votre avis
            </p>
            <div className="flex flex-wrap gap-3">
              {images.map((img, index) => (
                <div key={index} className="relative w-20 h-20">
                  <Image
                    src={img}
                    alt={`Photo ${index + 1}`}
                    fill
                    className="object-cover rounded-lg"
                  />
                  <button
                    type="button"
                    onClick={() => removeImage(index)}
                    className="absolute -top-2 -right-2 w-6 h-6 bg-foreground text-background rounded-full flex items-center justify-center"
                  >
                    <X className="h-4 w-4" />
                  </button>
                </div>
              ))}
              {images.length < 5 && (
                <button
                  type="button"
                  onClick={handleImageUpload}
                  className="w-20 h-20 border-2 border-dashed border-border rounded-lg flex flex-col items-center justify-center gap-1 hover:border-foreground transition-colors"
                >
                  <Camera className="h-5 w-5 text-muted-foreground" />
                  <span className="text-xs text-muted-foreground">Ajouter</span>
                </button>
              )}
            </div>
          </div>

          {/* Recommend */}
          <div>
            <label className="block font-medium mb-2">Recommanderiez-vous ce produit ?</label>
            <div className="flex gap-3">
              <button
                type="button"
                onClick={() => setRecommend(true)}
                className={`flex-1 py-3 border rounded-lg font-medium transition-colors ${
                  recommend === true
                    ? "border-emerald-500 bg-emerald-50 text-emerald-700"
                    : "border-border hover:border-foreground"
                }`}
              >
                Oui, je recommande
              </button>
              <button
                type="button"
                onClick={() => setRecommend(false)}
                className={`flex-1 py-3 border rounded-lg font-medium transition-colors ${
                  recommend === false
                    ? "border-red-500 bg-red-50 text-red-700"
                    : "border-border hover:border-foreground"
                }`}
              >
                Non, je ne recommande pas
              </button>
            </div>
          </div>

          {/* Submit */}
          <div className="flex gap-3 pt-4 border-t border-border">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 py-3 border border-border rounded-lg font-medium hover:bg-secondary transition-colors"
            >
              Annuler
            </button>
            <button
              type="submit"
              disabled={rating === 0 || comment.length < 20}
              className="flex-1 py-3 bg-foreground text-background rounded-lg font-medium hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Publier mon avis
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
