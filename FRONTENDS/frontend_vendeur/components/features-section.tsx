import { Globe, Shield, Headphones } from "lucide-react"

const features = [
  {
    icon: Globe,
    title: "Vendez à l'international en toute simplicité",
    description:
      "Vendez et expédiez à l'international pour atteindre des acheteurs dans le monde entier.",
  },
  {
    icon: Shield,
    title: "Outils de confidentialité et sécurité",
    description:
      "Pour garantir la sécurité de votre entreprise et la conformité aux réglementations telles que le RGPD.",
  },
  {
    icon: Headphones,
    title: "Assistance joignable à tout moment",
    description:
      "Notre équipe d'assistance ainsi que notre Centre d'aide virtuel sont là pour vous accompagner, jour et nuit.",
  },
]

export function FeaturesSection() {
  return (
    <div className="hidden lg:flex flex-col justify-center bg-primary p-12 text-primary-foreground">
      <div className="max-w-lg">
        <h2 className="mb-4 text-3xl font-bold">
          Faites passer votre boutique à la vitesse supérieure
        </h2>
        <p className="mb-10 text-primary-foreground/80">
          Rejoignez des millions d&apos;entrepreneurs qui utilisent notre plateforme pour développer leur activité.
        </p>

        <div className="space-y-8">
          {features.map((feature, index) => (
            <div key={index} className="flex gap-4">
              <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-lg bg-primary-foreground/10">
                <feature.icon className="h-6 w-6" />
              </div>
              <div>
                <h3 className="mb-1 font-semibold">{feature.title}</h3>
                <p className="text-sm text-primary-foreground/70">
                  {feature.description}
                </p>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-12 flex items-center gap-4">
          <div className="flex -space-x-2">
            {[1, 2, 3, 4].map((i) => (
              <div
                key={i}
                className="h-10 w-10 rounded-full border-2 border-primary bg-primary-foreground/20"
                style={{
                  backgroundImage: `url(https://i.pravatar.cc/40?img=${i + 10})`,
                  backgroundSize: "cover",
                }}
              />
            ))}
          </div>
          <div>
            <p className="font-medium">Plus de 1 million</p>
            <p className="text-sm text-primary-foreground/70">de marchands nous font confiance</p>
          </div>
        </div>
      </div>
    </div>
  )
}
