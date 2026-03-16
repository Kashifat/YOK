import Link from "next/link"
import { Facebook, Instagram, Twitter, Youtube, CreditCard, Smartphone } from "lucide-react"

const footerLinks = {
  aide: [
    { name: "Centre d'aide", href: "/aide" },
    { name: "Suivre ma commande", href: "/suivi" },
    { name: "Retours & Remboursements", href: "/retours" },
    { name: "Livraison", href: "/livraison" },
    { name: "FAQ", href: "/faq" },
  ],
  entreprise: [
    { name: "À propos", href: "/a-propos" },
    { name: "Carrières", href: "/carrieres" },
    { name: "Durabilité", href: "/durabilite" },
    { name: "Presse", href: "/presse" },
    { name: "Affiliés", href: "/affilies" },
  ],
  legal: [
    { name: "Conditions d'utilisation", href: "/conditions" },
    { name: "Politique de confidentialité", href: "/confidentialite" },
    { name: "Politique de cookies", href: "/cookies" },
    { name: "Mentions légales", href: "/mentions-legales" },
  ],
}

const socialLinks = [
  { name: "Facebook", icon: Facebook, href: "https://facebook.com" },
  { name: "Instagram", icon: Instagram, href: "https://instagram.com" },
  { name: "Twitter", icon: Twitter, href: "https://twitter.com" },
  { name: "YouTube", icon: Youtube, href: "https://youtube.com" },
]

export function Footer() {
  return (
    <footer className="bg-foreground text-background">
      {/* Newsletter */}
      <div className="border-b border-background/10">
        <div className="max-w-7xl mx-auto px-4 py-12">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6">
            <div>
              <h3 className="text-xl font-bold mb-2">
                Inscrivez-vous à notre newsletter
              </h3>
              <p className="text-sm opacity-70">
                Recevez 15% de réduction sur votre première commande
              </p>
            </div>
            <div className="flex w-full md:w-auto">
              <input
                type="email"
                placeholder="Votre adresse email"
                className="flex-1 md:w-80 h-12 px-4 bg-background/10 border border-background/20 text-background placeholder:text-background/50 focus:outline-none focus:border-background/40"
              />
              <button className="h-12 px-6 bg-background text-foreground font-medium hover:bg-background/90 transition-colors">
                S'inscrire
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Links */}
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          {/* Company Info */}
          <div>
            <h4 className="text-lg font-bold mb-4">MODESTYLE</h4>
            <p className="text-sm opacity-70 mb-4">
              Votre destination mode pour des vêtements tendance à prix abordables.
            </p>
            <div className="flex gap-3">
              {socialLinks.map((social) => (
                <a
                  key={social.name}
                  href={social.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-10 h-10 flex items-center justify-center border border-background/20 rounded-full hover:bg-background/10 transition-colors"
                  aria-label={social.name}
                >
                  <social.icon className="h-5 w-5" />
                </a>
              ))}
            </div>
          </div>

          {/* Help */}
          <div>
            <h4 className="font-bold mb-4">Aide & Support</h4>
            <ul className="space-y-2">
              {footerLinks.aide.map((link) => (
                <li key={link.name}>
                  <Link
                    href={link.href}
                    className="text-sm opacity-70 hover:opacity-100 transition-opacity"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Company */}
          <div>
            <h4 className="font-bold mb-4">Entreprise</h4>
            <ul className="space-y-2">
              {footerLinks.entreprise.map((link) => (
                <li key={link.name}>
                  <Link
                    href={link.href}
                    className="text-sm opacity-70 hover:opacity-100 transition-opacity"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h4 className="font-bold mb-4">Informations Légales</h4>
            <ul className="space-y-2">
              {footerLinks.legal.map((link) => (
                <li key={link.name}>
                  <Link
                    href={link.href}
                    className="text-sm opacity-70 hover:opacity-100 transition-opacity"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* Payment & App */}
      <div className="border-t border-background/10">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-4">
              <span className="text-sm opacity-70">Paiement sécurisé:</span>
              <div className="flex gap-2">
                <div className="w-10 h-6 bg-background/10 rounded flex items-center justify-center">
                  <CreditCard className="h-4 w-4" />
                </div>
                <div className="w-10 h-6 bg-background/10 rounded flex items-center justify-center text-xs font-bold">
                  VISA
                </div>
                <div className="w-10 h-6 bg-background/10 rounded flex items-center justify-center text-xs font-bold">
                  MC
                </div>
                <div className="w-10 h-6 bg-background/10 rounded flex items-center justify-center text-xs font-bold">
                  PP
                </div>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <Smartphone className="h-5 w-5" />
              <span className="text-sm">Téléchargez notre app</span>
              <div className="flex gap-2">
                <button className="px-3 py-1 text-xs border border-background/20 rounded hover:bg-background/10 transition-colors">
                  App Store
                </button>
                <button className="px-3 py-1 text-xs border border-background/20 rounded hover:bg-background/10 transition-colors">
                  Google Play
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Copyright */}
      <div className="border-t border-background/10">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex flex-col md:flex-row items-center justify-between gap-2 text-xs opacity-50">
            <p>© 2026 MODESTYLE. Tous droits réservés.</p>
            <p>Canada | Français</p>
          </div>
        </div>
      </div>
    </footer>
  )
}
