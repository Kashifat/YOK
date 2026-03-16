import { ProductCard, type Product } from "./product-card"

const products: Product[] = [
  {
    id: "1",
    name: "Robe Longue Florale à Manches Courtes Style Bohème",
    price: 24.99,
    originalPrice: 39.99,
    image: "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400&h=600&fit=crop",
    rating: 4.5,
    reviews: 1234,
    tag: "BEST SELLER",
    colors: ["#f5f5dc", "#e6d5c3", "#d4a574", "#8b7355"],
  },
  {
    id: "2",
    name: "Blazer Oversize Élégant pour Femme",
    price: 45.99,
    originalPrice: 69.99,
    image: "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=400&h=600&fit=crop",
    rating: 4.8,
    reviews: 892,
    colors: ["#000000", "#8b7355", "#f5f5f5"],
  },
  {
    id: "3",
    name: "Jean Mom Taille Haute Délavé Vintage",
    price: 32.50,
    image: "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400&h=600&fit=crop",
    rating: 4.3,
    reviews: 567,
    tag: "NOUVEAU",
    colors: ["#6b8e9f", "#4a6670", "#8fa8b3"],
  },
  {
    id: "4",
    name: "Top Crop en Maille Côtelée",
    price: 12.99,
    originalPrice: 19.99,
    image: "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=400&h=600&fit=crop",
    rating: 4.6,
    reviews: 2341,
    colors: ["#ffffff", "#000000", "#ffc0cb", "#87ceeb"],
  },
  {
    id: "5",
    name: "Ensemble 2 Pièces Casual Loungewear",
    price: 28.99,
    originalPrice: 45.00,
    image: "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=400&h=600&fit=crop",
    rating: 4.7,
    reviews: 1089,
    tag: "-36%",
    colors: ["#d3d3d3", "#ffd1dc", "#e6e6fa"],
  },
  {
    id: "6",
    name: "Chemise en Lin Oversize Décontractée",
    price: 21.50,
    image: "https://images.unsplash.com/photo-1564257631407-4deb1f99d992?w=400&h=600&fit=crop",
    rating: 4.4,
    reviews: 445,
    colors: ["#f5f5f5", "#e6d5c3", "#87ceeb"],
  },
  {
    id: "7",
    name: "Mini Jupe Plissée Style Preppy",
    price: 18.99,
    originalPrice: 25.99,
    image: "https://images.unsplash.com/photo-1583496661160-fb5886a0uj5u?w=400&h=600&fit=crop",
    rating: 4.2,
    reviews: 678,
    colors: ["#000000", "#1a2456", "#8b0000"],
  },
  {
    id: "8",
    name: "Cardigan Long en Maille Douce",
    price: 35.99,
    image: "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=400&h=600&fit=crop",
    rating: 4.9,
    reviews: 1567,
    tag: "TENDANCE",
    colors: ["#f5f5dc", "#d2b48c", "#8b7355", "#2f4f4f"],
  },
]

interface ProductGridProps {
  title?: string
  showViewAll?: boolean
}

export function ProductGrid({ title = "Nouveautés", showViewAll = true }: ProductGridProps) {
  return (
    <section className="py-12">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex items-center justify-between mb-8">
          <h2 className="text-2xl font-bold">{title}</h2>
          {showViewAll && (
            <a
              href="/nouveautes"
              className="text-sm font-medium hover:underline"
            >
              Voir tout →
            </a>
          )}
        </div>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">
          {products.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </div>
    </section>
  )
}
