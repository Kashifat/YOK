import { Link } from 'react-router-dom'

export default function Navigation() {
  return (
    <nav style={{
      backgroundColor: '#f8f9fa',
      borderBottom: '1px solid #dee2e6',
      padding: '10px 0'
    }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 20px', display: 'flex', gap: '30px' }}>
        <Link to="/" style={{ textDecoration: 'none', color: '#333', fontWeight: '500', padding: '10px 0' }}>
          Accueil
        </Link>
        <Link to="/catalogue" style={{ textDecoration: 'none', color: '#333', fontWeight: '500', padding: '10px 0' }}>
          Catalogue
        </Link>
        <Link to="/favoris" style={{ textDecoration: 'none', color: '#333', fontWeight: '500', padding: '10px 0' }}>
          Favoris ❤️
        </Link>
        <Link to="/panier" style={{ textDecoration: 'none', color: '#333', fontWeight: '500', padding: '10px 0' }}>
          Panier 🛒
        </Link>
        <Link to="/mes-commandes" style={{ textDecoration: 'none', color: '#333', fontWeight: '500', padding: '10px 0' }}>
          Mes commandes
        </Link>
        <Link to="/profil" style={{ textDecoration: 'none', color: '#333', fontWeight: '500', padding: '10px 0' }}>
          Profil
        </Link>
      </div>
    </nav>
  )
}
