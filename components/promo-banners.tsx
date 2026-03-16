import Link from "next/link"
import { Truck, RotateCcw, ShieldCheck, Headphones } from "lucide-react"

const promos = [
  {
    id: 1,
    title: "Offres Maman",
    subtitle: "Cadeaux parfaits",
    discount: "-40%",
    href: "/fete-des-meres",
    bgColor: "bg-rose-100",
  },
  {
    id: 2,
    title: "Mega Soldes Maison",
    subtitle: "Tout pour la maison",
    discount: "-60%",
    href: "/maison",
    bgColor: "bg-amber-100",
  },
  {
    id: 3,
    title: "Liquidation",
    subtitle: "Dernières pièces",
    discount: "-70%",
    href: "/liquidation",
    bgColor: "bg-sky-100",
  },
]

const features = [
  {
    icon: Truck,
    title: "Livraison Gratuite",
    description: "Dès 49$ d'achat",
  },
  {
    icon: RotateCcw,
    title: "Retours Gratuits",
    description: "Sous 35 jours",
  },
  {
    icon: ShieldCheck,
    title: "Paiement Sécurisé",
    description: "100% protégé",
  },
  {
    icon: Headphones,
    title: "Support 24/7",
    description: "À votre écoute",
  },
]

export function PromoBanners() {
  return (
    <section className="py-12">
      <div className="max-w-7xl mx-auto px-4">
        {/* Promo Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-12">
          {promos.map((promo) => (
            <Link
              key={promo.id}
              href={promo.href}
              className={`${promo.bgColor} p-8 rounded-lg hover:shadow-lg transition-shadow`}
            >
              <span className="inline-block bg-red-500 text-white text-sm font-bold px-3 py-1 rounded-full mb-4">
                {promo.discount}
              </span>
              <h3 className="text-2xl font-bold mb-2">{promo.title}</h3>
              <p className="text-muted-foreground">{promo.subtitle}</p>
              <span className="inline-block mt-4 text-sm font-medium underline">
                Voir les offres →
              </span>
            </Link>
          ))}
        </div>

        {/* Features */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          {features.map((feature) => (
            <div
              key={feature.title}
              className="flex flex-col items-center text-center p-6"
            >
              <div className="w-12 h-12 flex items-center justify-center bg-secondary rounded-full mb-4">
                <feature.icon className="h-6 w-6" />
              </div>
              <h4 className="font-medium mb-1">{feature.title}</h4>
              <p className="text-sm text-muted-foreground">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
