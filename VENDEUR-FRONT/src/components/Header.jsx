import { Link, useNavigate } from 'react-router-dom'
import { useContext } from 'react'
import { AuthContext } from '../context/AuthContext'

export default function Header() {
  const { utilisateur, deconnecter } = useContext(AuthContext)
  const navigate = useNavigate()

  const handleDeconnexion = () => {
    deconnecter()
    navigate('/connexion')
  }

  return (
    <header style={{
      backgroundColor: '#28a745',
      color: 'white',
      padding: '15px 0',
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
    }}>
      <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '0 20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Link to="/" style={{ textDecoration: 'none', color: 'white', fontSize: '24px', fontWeight: 'bold' }}>
          🏪 YOK Vendeur
        </Link>

        <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
          <span>Bienvenue, {utilisateur?.nom_complet || 'Vendeur'}</span>
          <button 
            onClick={handleDeconnexion}
            style={{
              background: 'none',
              border: 'none',
              color: 'white',
              cursor: 'pointer',
              textDecoration: 'underline'
            }}
          >
            Déconnexion
          </button>
        </div>
      </div>
    </header>
  )
}
