import Link from "next/link"

const categories = [
  { name: "Robes", image: "👗", href: "/femmes/robes", count: "2,500+" },
  { name: "Tops", image: "👚", href: "/femmes/tops", count: "4,200+" },
  { name: "Pantalons", image: "👖", href: "/femmes/pantalons", count: "1,800+" },
  { name: "Chaussures", image: "👠", href: "/chaussures", count: "3,100+" },
  { name: "Accessoires", image: "👜", href: "/accessoires", count: "5,600+" },
  { name: "Beauté", image: "💄", href: "/beaute", count: "2,900+" },
]

export function CategoryGrid() {
  return (
    <section className="py-12 bg-secondary/50">
      <div className="max-w-7xl mx-auto px-4">
        <h2 className="text-2xl font-bold text-center mb-8">
          Explorez par Catégorie
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {categories.map((category) => (
            <Link
              key={category.name}
              href={category.href}
              className="group flex flex-col items-center p-6 bg-background rounded-lg border border-border hover:shadow-lg transition-shadow"
            >
              <div className="text-5xl mb-3 group-hover:scale-110 transition-transform">
                {category.image}
              </div>
              <h3 className="font-medium text-sm">{category.name}</h3>
              <span className="text-xs text-muted-foreground">
                {category.count} articles
              </span>
            </Link>
          ))}
        </div>
      </div>
    </section>
  )
}
