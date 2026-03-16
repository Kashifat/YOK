"use client"

import { useEffect, useState } from "react"
import { Header } from "@/components/header"
import { Footer } from "@/components/footer"
import { Eye, EyeOff, Mail, Lock, User, ChevronRight } from "lucide-react"
import Link from "next/link"
import { useAuth } from "@/context/auth-context"

export default function AccountPage() {
  const {
    isAuthenticated,
    user,
    loginWithEmail,
    registerWithEmail,
    startGoogleLogin,
    startFacebookLogin,
  } = useAuth()

  const [activeTab, setActiveTab] = useState<"login" | "register">("login")
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [errorMessage, setErrorMessage] = useState("")
  const [reason, setReason] = useState("")

  const [loginForm, setLoginForm] = useState({ email: "", password: "" })
  const [registerForm, setRegisterForm] = useState({
    firstName: "",
    lastName: "",
    email: "",
    password: "",
    confirmPassword: "",
    newsletter: true,
  })

  useEffect(() => {
    const params = new URLSearchParams(window.location.search)
    setReason(params.get("reason") ?? "")
  }, [])

  const handleLoginSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setErrorMessage("")
    setIsSubmitting(true)

    try {
      await loginWithEmail({
        courriel: loginForm.email,
        mot_de_passe: loginForm.password,
      })
      window.location.href = "/compte/tableau-de-bord"
    } catch (error) {
      const message = error instanceof Error ? error.message : "Connexion impossible pour le moment."
      setErrorMessage(message)
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleRegisterSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setErrorMessage("")

    if (registerForm.password !== registerForm.confirmPassword) {
      setErrorMessage("Les mots de passe ne correspondent pas.")
      return
    }

    setIsSubmitting(true)
    try {
      await registerWithEmail({
        nom_complet: `${registerForm.firstName} ${registerForm.lastName}`.trim(),
        courriel: registerForm.email,
        mot_de_passe: registerForm.password,
      })
      window.location.href = "/compte/tableau-de-bord"
    } catch (error) {
      const message = error instanceof Error ? error.message : "Inscription impossible pour le moment."
      setErrorMessage(message)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <Header />

      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="max-w-md mx-auto">
          {reason && (
            <div className="mb-6 rounded-lg border border-amber-300 bg-amber-50 px-4 py-3 text-sm text-amber-900">
              Pour {reason.toLowerCase()}, vous devez creer un compte ou vous connecter.
            </div>
          )}

          {errorMessage && (
            <div className="mb-6 rounded-lg border border-red-300 bg-red-50 px-4 py-3 text-sm text-red-800">
              {errorMessage}
            </div>
          )}

          {isAuthenticated && (
            <div className="mb-6 rounded-lg border border-emerald-300 bg-emerald-50 px-4 py-3 text-sm text-emerald-800">
              Connecte en tant que {user?.email ?? "utilisateur"}.&nbsp;
              <Link href="/compte/tableau-de-bord" className="underline">
                Aller au tableau de bord
              </Link>
            </div>
          )}

          {/* Tab Switcher */}
          <div className="flex border-b border-border mb-8">
            <button
              onClick={() => setActiveTab("login")}
              className={`flex-1 py-3 text-center font-medium border-b-2 -mb-px transition-colors ${
                activeTab === "login"
                  ? "border-foreground text-foreground"
                  : "border-transparent text-muted-foreground hover:text-foreground"
              }`}
            >
              Connexion
            </button>
            <button
              onClick={() => setActiveTab("register")}
              className={`flex-1 py-3 text-center font-medium border-b-2 -mb-px transition-colors ${
                activeTab === "register"
                  ? "border-foreground text-foreground"
                  : "border-transparent text-muted-foreground hover:text-foreground"
              }`}
            >
              Créer un compte
            </button>
          </div>

          {/* Login Form */}
          {activeTab === "login" && (
            <div>
              <h1 className="text-2xl font-bold mb-2">Bon retour !</h1>
              <p className="text-muted-foreground mb-6">
                Connectez-vous pour accéder à votre compte
              </p>

              <form className="space-y-4" onSubmit={handleLoginSubmit}>
                <div>
                  <label className="block text-sm font-medium mb-2">Email</label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
                    <input
                      type="email"
                      value={loginForm.email}
                      onChange={(e) => setLoginForm({ ...loginForm, email: e.target.value })}
                      placeholder="votre@email.com"
                      className="w-full h-12 pl-10 pr-4 border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-foreground/20"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Mot de passe</label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
                    <input
                      type={showPassword ? "text" : "password"}
                      value={loginForm.password}
                      onChange={(e) => setLoginForm({ ...loginForm, password: e.target.value })}
                      placeholder="Votre mot de passe"
                      className="w-full h-12 pl-10 pr-12 border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-foreground/20"
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                    >
                      {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                    </button>
                  </div>
                </div>

                <div className="flex items-center justify-between">
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input type="checkbox" className="w-4 h-4 accent-foreground" />
                    <span className="text-sm">Se souvenir de moi</span>
                  </label>
                  <Link href="/compte/mot-de-passe-oublie" className="text-sm underline hover:no-underline">
                    Mot de passe oublié ?
                  </Link>
                </div>

                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="w-full h-12 bg-foreground text-background font-medium rounded-lg hover:opacity-90 transition-opacity"
                >
                  {isSubmitting ? "Connexion..." : "Se connecter"}
                </button>
              </form>

              {/* Social Login */}
              <div className="mt-6">
                <div className="relative">
                  <div className="absolute inset-0 flex items-center">
                    <div className="w-full border-t border-border" />
                  </div>
                  <div className="relative flex justify-center text-sm">
                    <span className="bg-background px-4 text-muted-foreground">Ou continuer avec</span>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4 mt-6">
                  <button
                    type="button"
                    onClick={startGoogleLogin}
                    className="h-12 flex items-center justify-center gap-2 border border-border rounded-lg hover:bg-secondary transition-colors"
                  >
                    <svg className="h-5 w-5" viewBox="0 0 24 24">
                      <path
                        fill="currentColor"
                        d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                      />
                      <path
                        fill="currentColor"
                        d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                      />
                      <path
                        fill="currentColor"
                        d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                      />
                      <path
                        fill="currentColor"
                        d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                      />
                    </svg>
                    <span className="text-sm font-medium">Google</span>
                  </button>
                  <button
                    type="button"
                    onClick={startFacebookLogin}
                    className="h-12 flex items-center justify-center gap-2 border border-border rounded-lg hover:bg-secondary transition-colors"
                  >
                    <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12 2C6.477 2 2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.879V14.89h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.989C18.343 21.129 22 16.99 22 12c0-5.523-4.477-10-10-10z" />
                    </svg>
                    <span className="text-sm font-medium">Facebook</span>
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Register Form */}
          {activeTab === "register" && (
            <div>
              <h1 className="text-2xl font-bold mb-2">Créer un compte</h1>
              <p className="text-muted-foreground mb-6">
                Rejoignez-nous et profitez d'avantages exclusifs
              </p>

              <form className="space-y-4" onSubmit={handleRegisterSubmit}>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">Prénom</label>
                    <div className="relative">
                      <User className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
                      <input
                        type="text"
                        value={registerForm.firstName}
                        onChange={(e) => setRegisterForm({ ...registerForm, firstName: e.target.value })}
                        placeholder="Prénom"
                        className="w-full h-12 pl-10 pr-4 border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-foreground/20"
                      />
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-2">Nom</label>
                    <input
                      type="text"
                      value={registerForm.lastName}
                      onChange={(e) => setRegisterForm({ ...registerForm, lastName: e.target.value })}
                      placeholder="Nom"
                      className="w-full h-12 px-4 border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-foreground/20"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Email</label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
                    <input
                      type="email"
                      value={registerForm.email}
                      onChange={(e) => setRegisterForm({ ...registerForm, email: e.target.value })}
                      placeholder="votre@email.com"
                      className="w-full h-12 pl-10 pr-4 border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-foreground/20"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Mot de passe</label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
                    <input
                      type={showPassword ? "text" : "password"}
                      value={registerForm.password}
                      onChange={(e) => setRegisterForm({ ...registerForm, password: e.target.value })}
                      placeholder="Minimum 8 caractères"
                      className="w-full h-12 pl-10 pr-12 border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-foreground/20"
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                    >
                      {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                    </button>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Confirmer le mot de passe</label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
                    <input
                      type={showConfirmPassword ? "text" : "password"}
                      value={registerForm.confirmPassword}
                      onChange={(e) => setRegisterForm({ ...registerForm, confirmPassword: e.target.value })}
                      placeholder="Confirmez votre mot de passe"
                      className="w-full h-12 pl-10 pr-12 border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-foreground/20"
                    />
                    <button
                      type="button"
                      onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                    >
                      {showConfirmPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                    </button>
                  </div>
                </div>

                <label className="flex items-start gap-3 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={registerForm.newsletter}
                    onChange={(e) => setRegisterForm({ ...registerForm, newsletter: e.target.checked })}
                    className="w-4 h-4 mt-0.5 accent-foreground"
                  />
                  <span className="text-sm text-muted-foreground">
                    Je souhaite recevoir les offres exclusives et nouveautés par email
                  </span>
                </label>

                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="w-full h-12 bg-foreground text-background font-medium rounded-lg hover:opacity-90 transition-opacity"
                >
                  {isSubmitting ? "Creation..." : "Creer mon compte"}
                </button>

                <p className="text-xs text-muted-foreground text-center">
                  En créant un compte, vous acceptez nos{" "}
                  <Link href="/conditions" className="underline hover:no-underline">
                    Conditions d'utilisation
                  </Link>{" "}
                  et notre{" "}
                  <Link href="/confidentialite" className="underline hover:no-underline">
                    Politique de confidentialité
                  </Link>
                </p>
              </form>
            </div>
          )}

          {/* Benefits */}
          <div className="mt-12 pt-8 border-t border-border">
            <h3 className="font-semibold mb-4">Avantages membres</h3>
            <ul className="space-y-3">
              {[
                "Accès exclusif aux ventes privées",
                "Livraison gratuite dès 49$",
                "Suivi de vos commandes en temps réel",
                "Retours gratuits sous 35 jours",
                "Points de fidélité à chaque achat",
              ].map((benefit, index) => (
                <li key={index} className="flex items-center gap-2 text-sm text-muted-foreground">
                  <ChevronRight className="h-4 w-4 text-foreground" />
                  {benefit}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  )
}
