import Image from "next/image"
import Link from "next/link"
import { TrendingUp } from "lucide-react"

const trends = [
  {
    id: 1,
    tag: "#The Sporty Life",
    image: "https://images.unsplash.com/photo-1518459031867-a89b944bffe4?w=300&h=400&fit=crop",
    price: "20.87",
  },
  {
    id: 2,
    tag: "#SpringBreakOutfit",
    image: "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=300&h=400&fit=crop",
    price: "10.26",
  },
  {
    id: 3,
    tag: "#Vacay Vibes",
    image: "https://images.unsplash.com/photo-1469334031218-e382a71b716b?w=300&h=400&fit=crop",
    price: "2.88",
  },
  {
    id: 4,
    tag: "#Dune Aesthetic",
    image: "https://images.unsplash.com/photo-1509631179647-0177331693ae?w=300&h=400&fit=crop",
    price: "5.22",
  },
  {
    id: 5,
    tag: "#Going Out Outfit",
    image: "https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=300&h=400&fit=crop",
    price: "3.69",
  },
  {
    id: 6,
    tag: "#Casual Style",
    image: "https://images.unsplash.com/photo-1485968579169-a6b459e81c5f?w=300&h=400&fit=crop",
    price: "11.83",
  },
]

export function TrendingSection() {
  return (
    <section className="py-12 bg-secondary/30">
      <div className="max-w-7xl mx-auto px-4">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-3">
            <TrendingUp className="h-6 w-6 text-red-500" />
            <h2 className="text-2xl font-bold">Tendances du Moment</h2>
          </div>
          <Link href="/tendances" className="text-sm font-medium hover:underline">
            Voir plus →
          </Link>
        </div>

        {/* Trend Cards */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {trends.map((trend) => (
            <Link
              key={trend.id}
              href={`/tendance/${trend.tag.replace("#", "").toLowerCase().replace(/\s/g, "-")}`}
              className="group relative aspect-[3/4] rounded-lg overflow-hidden"
            >
              <Image
                src={trend.image}
                alt={trend.tag}
                fill
                className="object-cover group-hover:scale-105 transition-transform duration-300"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />
              <div className="absolute bottom-0 left-0 right-0 p-4 text-white">
                <span className="inline-block bg-foreground/80 text-background text-xs px-2 py-1 rounded mb-2">
                  Peaked
                </span>
                <p className="font-bold text-sm">CA${trend.price}</p>
                <p className="text-xs opacity-80">{trend.tag}</p>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </section>
  )
}
