import { useContext } from 'react'
import { AuthContext } from '../context/AuthContext'

/**
 * Hook pour accéder au contexte d'authentification
 */
export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth doit être utilisé dans AuthProvider')
  }
  return context
}
