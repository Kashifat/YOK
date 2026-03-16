import { createContext, useState, useEffect } from 'react'

export const AuthContext = createContext()

export function AuthProvider({ children }) {
  const [utilisateur, setUtilisateur] = useState(null)
  const [chargement, setChargement] = useState(true)

  useEffect(() => {
    const userStored = localStorage.getItem('user')
    const tokenStored = localStorage.getItem('access_token')
    
    if (userStored && tokenStored) {
      try {
        setUtilisateur(JSON.parse(userStored))
      } catch (e) {
        localStorage.removeItem('user')
      }
    }
    
    setChargement(false)
  }, [])

  const connecter = (user, token) => {
    localStorage.setItem('user', JSON.stringify(user))
    localStorage.setItem('access_token', token)
    setUtilisateur(user)
  }

  const deconnecter = () => {
    localStorage.removeItem('user')
    localStorage.removeItem('access_token')
    setUtilisateur(null)
  }

  return (
    <AuthContext.Provider value={{
      utilisateur,
      chargement,
      connecter,
      deconnecter,
      estConnecte: !!utilisateur
    }}>
      {children}
    </AuthContext.Provider>
  )
}
