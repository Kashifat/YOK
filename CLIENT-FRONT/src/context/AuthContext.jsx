import { createContext, useState, useEffect } from 'react'

/**
 * Context pour l'authentification
 */
export const AuthContext = createContext()

function decodeJwt(token) {
  if (!token) return null
  try {
    const payload = token.split('.')[1]
    if (!payload) return null
    return JSON.parse(atob(payload))
  } catch (_) {
    return null
  }
}

function buildUserFromToken(token, userStored = null) {
  const payload = decodeJwt(token)
  if (!payload) return userStored

  return {
    identifiant: payload.sub,
    role: payload.role || userStored?.role || null,
    nom_complet: userStored?.nom_complet || 'Client',
    courriel: userStored?.courriel || ''
  }
}

export function AuthProvider({ children }) {
  const [utilisateur, setUtilisateur] = useState(null)
  const [chargement, setChargement] = useState(true)
  const [erreur, setErreur] = useState(null)

  useEffect(() => {
    // Callback OAuth: backend renvoie les tokens en query params
    const params = new URLSearchParams(window.location.search)
    const oauthAccess = params.get('access_token')
    const oauthRefresh = params.get('refresh_token')

    if (oauthAccess) {
      localStorage.setItem('access_token', oauthAccess)
      if (oauthRefresh) {
        localStorage.setItem('refresh_token', oauthRefresh)
      }
      const built = buildUserFromToken(oauthAccess)
      if (built) {
        localStorage.setItem('user', JSON.stringify(built))
        setUtilisateur(built)
      }
      window.history.replaceState({}, document.title, window.location.pathname)
      setChargement(false)
      return
    }

    // Vérifier si l'utilisateur est déjà connecté
    const userStored = localStorage.getItem('user')
    const tokenStored = localStorage.getItem('access_token')
    
    if (userStored && tokenStored) {
      try {
        const parsed = JSON.parse(userStored)
        const user = buildUserFromToken(tokenStored, parsed)
        setUtilisateur(user)
        localStorage.setItem('user', JSON.stringify(user))
      } catch (e) {
        console.error('Erreur lors de la restauration de l\'utilisateur:', e)
        localStorage.removeItem('user')
      }
    } else if (tokenStored) {
      const user = buildUserFromToken(tokenStored)
      if (user) {
        setUtilisateur(user)
        localStorage.setItem('user', JSON.stringify(user))
      }
    }
    
    setChargement(false)
  }, [])

  const connecter = (user, token, refreshToken = null) => {
    const finalUser = buildUserFromToken(token, user)
    localStorage.setItem('user', JSON.stringify(finalUser))
    localStorage.setItem('access_token', token)
    if (refreshToken) {
      localStorage.setItem('refresh_token', refreshToken)
    }
    setUtilisateur(finalUser)
    setErreur(null)
  }

  const deconnecter = () => {
    localStorage.removeItem('user')
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    setUtilisateur(null)
  }

  const estConnecte = () => {
    return !!utilisateur && !!localStorage.getItem('access_token')
  }

  return (
    <AuthContext.Provider value={{
      utilisateur,
      chargement,
      erreur,
      setErreur,
      connecter,
      deconnecter,
      estConnecte
    }}>
      {children}
    </AuthContext.Provider>
  )
}
