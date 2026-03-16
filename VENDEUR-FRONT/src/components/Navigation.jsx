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
        <Link to="/ajouter-produit" style={{ textDecoration: 'none', color: '#333', fontWeight: '500', padding: '10px 0' }}>
          Ajouter produit
        </Link>
        <Link to="/mes-produits" style={{ textDecoration: 'none', color: '#333', fontWeight: '500', padding: '10px 0' }}>
          Mes produits
        </Link>
        <Link to="/mes-commandes" style={{ textDecoration: 'none', color: '#333', fontWeight: '500', padding: '10px 0' }}>
          Commandes
        </Link>
        <Link to="/avis" style={{ textDecoration: 'none', color: '#333', fontWeight: '500', padding: '10px 0' }}>
          Avis clients
        </Link>
      </div>
    </nav>
  )
}
