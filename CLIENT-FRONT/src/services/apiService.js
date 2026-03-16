import { axiosPublic, axiosAuth, API_CONFIG, getApiUrl } from '../config/api'

/**
 * Service d'authentification
 */
export const authService = {
  inscription: async (email, nomComplet, motDePasse, telephone = null) => {
    try {
      const response = await axiosPublic.post(getApiUrl(API_CONFIG.AUTH.BASE_URL, API_CONFIG.AUTH.INSCRIPTION), {
        courriel: email,
        nom_complet: nomComplet,
        mot_de_passe: motDePasse,
        telephone
      })
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  connexion: async (email, motDePasse) => {
    try {
      const response = await axiosPublic.post(getApiUrl(API_CONFIG.AUTH.BASE_URL, API_CONFIG.AUTH.CONNEXION), {
        courriel: email,
        mot_de_passe: motDePasse
      })
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  oauthGoogleUrl: () => getApiUrl(API_CONFIG.AUTH.BASE_URL, API_CONFIG.AUTH.OAUTH_GOOGLE),
  oauthFacebookUrl: () => getApiUrl(API_CONFIG.AUTH.BASE_URL, API_CONFIG.AUTH.OAUTH_FACEBOOK),

  deconnecterApi: async (token) => {
    try {
      const response = await axiosAuth.post(getApiUrl(API_CONFIG.AUTH.BASE_URL, API_CONFIG.AUTH.DECONNEXION), { token })
      return response.data
    } catch (_) {
      return null
    }
  },

  deconnecter: () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
    localStorage.removeItem('refresh_token')
  }
}

/**
 * Service du catalogue
 */
export const catalogueService = {
  obtenirCategories: async () => {
    try {
      const response = await axiosPublic.get(getApiUrl(API_CONFIG.CATALOGUE.BASE_URL, API_CONFIG.CATALOGUE.CATEGORIES))
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  obtenirProduits: async (categorieId = null) => {
    try {
      const params = categorieId ? { categorie_id: categorieId } : {}
      const response = await axiosPublic.get(getApiUrl(API_CONFIG.CATALOGUE.BASE_URL, API_CONFIG.CATALOGUE.PRODUITS), { params })
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  rechercher: async (terme) => {
    try {
      const response = await axiosPublic.get(
        getApiUrl(API_CONFIG.CATALOGUE.BASE_URL, `${API_CONFIG.CATALOGUE.RECHERCHE_PREFIX}/${encodeURIComponent(terme)}`)
      )
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  }
}

/**
 * Service des favoris
 */
export const favorisService = {
  obtenirMesFavoris: async () => {
    try {
      const response = await axiosAuth.get(getApiUrl(API_CONFIG.FAVORIS.BASE_URL, API_CONFIG.FAVORIS.MES_FAVORIS))
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  ajouter: async (produitId) => {
    try {
      const response = await axiosAuth.post(getApiUrl(API_CONFIG.FAVORIS.BASE_URL, API_CONFIG.FAVORIS.AJOUTER), {
        produit_identifiant: produitId
      })
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  retirer: async (produitId) => {
    try {
      await axiosAuth.delete(getApiUrl(API_CONFIG.FAVORIS.BASE_URL, `${API_CONFIG.FAVORIS.RETIRER_PREFIX}/${produitId}`))
      return true
    } catch (error) {
      throw error.response?.data || error.message
    }
  }
}

export const panierService = {
  obtenir: async () => {
    try {
      const response = await axiosAuth.get(getApiUrl(API_CONFIG.COMMANDE.BASE_URL, API_CONFIG.COMMANDE.PANIER))
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  ajouterArticle: async (produitId, quantite = 1) => {
    try {
      const response = await axiosAuth.post(getApiUrl(API_CONFIG.COMMANDE.BASE_URL, API_CONFIG.COMMANDE.PANIER_ARTICLES), {
        produit_identifiant: produitId,
        quantite
      })
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  majQuantite: async (produitId, quantite) => {
    try {
      const response = await axiosAuth.patch(
        getApiUrl(API_CONFIG.COMMANDE.BASE_URL, `${API_CONFIG.COMMANDE.PANIER_ARTICLES}/${produitId}`),
        { quantite }
      )
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  supprimerArticle: async (produitId) => {
    try {
      const response = await axiosAuth.delete(
        getApiUrl(API_CONFIG.COMMANDE.BASE_URL, `${API_CONFIG.COMMANDE.PANIER_ARTICLES}/${produitId}`)
      )
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  vider: async () => {
    try {
      const response = await axiosAuth.delete(getApiUrl(API_CONFIG.COMMANDE.BASE_URL, API_CONFIG.COMMANDE.PANIER))
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  }
}

export const commandeService = {
  listerMesCommandes: async () => {
    try {
      const response = await axiosAuth.get(getApiUrl(API_CONFIG.COMMANDE.BASE_URL, API_CONFIG.COMMANDE.COMMANDES_CLIENT))
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  creerDepuisPanier: async (adresseIdentifiant, remarques = null) => {
    try {
      const response = await axiosAuth.post(getApiUrl(API_CONFIG.COMMANDE.BASE_URL, API_CONFIG.COMMANDE.COMMANDES_CLIENT), {
        adresse_identifiant: adresseIdentifiant,
        remarques
      })
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  annuler: async (commandeId) => {
    try {
      const response = await axiosAuth.delete(
        getApiUrl(API_CONFIG.COMMANDE.BASE_URL, `${API_CONFIG.COMMANDE.COMMANDES_CLIENT}/${commandeId}`)
      )
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  }
}

export const paiementService = {
  initialiser: async (commandeIdentifiant, telephone = null) => {
    try {
      const response = await axiosAuth.post(getApiUrl(API_CONFIG.PAIEMENT.BASE_URL, API_CONFIG.PAIEMENT.INITIALISER), {
        commande_identifiant: commandeIdentifiant,
        telephone,
        canal: 'ALL',
        description: `Paiement commande ${commandeIdentifiant}`
      })
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  }
}

export const factureService = {
  listerMesFactures: async () => {
    try {
      const response = await axiosAuth.get(getApiUrl(API_CONFIG.FACTURE.BASE_URL, API_CONFIG.FACTURE.MES_FACTURES))
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  genererDepuisCommande: async (commandeId) => {
    try {
      const response = await axiosAuth.post(
        getApiUrl(API_CONFIG.FACTURE.BASE_URL, `${API_CONFIG.FACTURE.FACTURE_COMMANDE_PREFIX}/${commandeId}`)
      )
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  telechargerHtml: async (factureId) => {
    try {
      const response = await axiosAuth.get(
        getApiUrl(API_CONFIG.FACTURE.BASE_URL, `/factures/${factureId}${API_CONFIG.FACTURE.TELECHARGER_SUFFIX}`),
        { responseType: 'text' }
      )
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  }
}

export default {
  authService,
  catalogueService,
  favorisService,
  panierService,
  commandeService,
  paiementService,
  factureService
}
