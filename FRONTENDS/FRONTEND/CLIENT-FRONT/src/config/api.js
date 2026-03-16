import axios from 'axios'

const env = import.meta.env

export const API_CONFIG = {
  AUTH: {
    BASE_URL: env.VITE_API_AUTH || 'http://localhost:8001',
    INSCRIPTION: '/auth/inscription',
    CONNEXION: '/auth/connexion',
    RENEW: '/auth/renouveler',
    DECONNEXION: '/auth/deconnecter',
    OAUTH_GOOGLE: '/auth/oauth/google',
    OAUTH_FACEBOOK: '/auth/oauth/facebook'
  },
  CATALOGUE: {
    BASE_URL: env.VITE_API_CATALOGUE || 'http://localhost:8002',
    PRODUITS: '/catalogue/public/produits',
    CATEGORIES: '/catalogue/public/categories',
    RECHERCHE_PREFIX: '/catalogue/public/produits/recherche'
  },
  FAVORIS: {
    BASE_URL: env.VITE_API_FAVORIS || 'http://localhost:8005',
    MES_FAVORIS: '/favoris/mes-favoris',
    AJOUTER: '/favoris/ajouter',
    RETIRER_PREFIX: '/favoris/retirer'
  },
  COMMANDE: {
    BASE_URL: env.VITE_API_COMMANDE || 'http://localhost:8003',
    PANIER: '/panier',
    PANIER_ARTICLES: '/panier/articles',
    COMMANDES_CLIENT: '/commandes/client'
  },
  PAIEMENT: {
    BASE_URL: env.VITE_API_PAIEMENT_CLIENTS || 'http://localhost:8007',
    INITIALISER: '/paiements/initialiser'
  },
  FACTURE: {
    BASE_URL: env.VITE_API_FACTURE || 'http://localhost:8006',
    MES_FACTURES: '/factures/mes-factures',
    FACTURE_COMMANDE_PREFIX: '/factures/commande',
    TELECHARGER_SUFFIX: '/telecharger'
  }
}

export const axiosPublic = axios.create({ timeout: 15000 })

export const axiosAuth = axios.create({ timeout: 20000 })

axiosAuth.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers = config.headers || {}
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export function getApiUrl(baseUrl, path) {
  return `${baseUrl}${path}`
}

export default API_CONFIG
