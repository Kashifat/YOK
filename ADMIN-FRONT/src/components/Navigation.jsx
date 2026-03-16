import { Link } from 'react-router-dom'

export default function Navigation() {
  return (
    <nav style={{
      backgroundColor: '#f8f9fa',
      borderBottom: '1px solid #dee2e6',
      padding: '10px 0'
    }}>
      <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '0 20px', display: 'flex', gap: '30px' }}>
        <Link to="/" style={{ textDecoration: 'none', color: '#333', fontWeight: '500', padding: '10px 0' }}>
          Tableau de bord
        </Link>
        <Link to="/utilisateurs" style={{ textDecoration: 'none', color: '#333', fontWeight: '500', padding: '10px 0' }}>
          Utilisateurs
        </Link>
        <Link to="/boutiques" style={{ textDecoration: 'none', color: '#333', fontWeight: '500', padding: '10px 0' }}>
          Boutiques
        </Link>
        <Link to="/produits" style={{ textDecoration: 'none', color: '#333', fontWeight: '500', padding: '10px 0' }}>
          Produits
        </Link>
        <Link to="/statistiques" style={{ textDecoration: 'none', color: '#333', fontWeight: '500', padding: '10px 0' }}>
          Statistiques
        </Link>
      </div>
    </nav>
  )
}
