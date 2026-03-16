import { useState, useEffect } from 'react'

export default function Boutiques() {
  const [boutiques, setBoutiques] = useState([])
  const [filtreKYC, setFiltreKYC] = useState(null)
  const [chargement, setChargement] = useState(true)

  useEffect(() => {
    chargerBoutiques()
  }, [filtreKYC])

  async function chargerBoutiques() {
    try {
      setChargement(true)
      // TODO: Appel API pour les boutiques
      setBoutiques([])
    } finally {
      setChargement(false)
    }
  }

  if (chargement) return <div>Chargement...</div>

  return (
    <div className="container">
      <h1>Gestion des boutiques 🏪</h1>

      <div style={{ marginBottom: '20px', display: 'flex', gap: '10px' }}>
        <button 
          className="btn btn-secondary"
          onClick={() => setFiltreKYC(null)}
          style={{ backgroundColor: !filtreKYC ? '#dc3545' : '#6c757d' }}
        >
          Tous
        </button>
        <button 
          className="btn btn-secondary"
          onClick={() => setFiltreKYC('VALIDE')}
          style={{ backgroundColor: filtreKYC === 'VALIDE' ? '#dc3545' : '#6c757d' }}
        >
          Validées
        </button>
        <button 
          className="btn btn-secondary"
          onClick={() => setFiltreKYC('EN_ATTENTE')}
          style={{ backgroundColor: filtreKYC === 'EN_ATTENTE' ? '#dc3545' : '#6c757d' }}
        >
          En attente
        </button>
        <button 
          className="btn btn-secondary"
          onClick={() => setFiltreKYC('REJETEE')}
          style={{ backgroundColor: filtreKYC === 'REJETEE' ? '#dc3545' : '#6c757d' }}
        >
          Rejetées
        </button>
      </div>

      {boutiques.length === 0 ? (
        <p style={{ textAlign: 'center', marginTop: '20px' }}>Aucune boutique trouvée</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Nom</th>
              <th>Propriétaire</th>
              <th>Statut KYC</th>
              <th>CA annuel</th>
              <th>Produits</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {boutiques.map(boutique => (
              <tr key={boutique.id}>
                <td>{boutique.nom}</td>
                <td>{boutique.proprietaire}</td>
                <td>
                  <span className={`badge badge-${boutique.kycValide ? 'success' : 'warning'}`}>
                    {boutique.kycValide ? 'Validée' : 'En attente'}
                  </span>
                </td>
                <td>{boutique.caAnnuel?.toLocaleString() || 0} FCFA</td>
                <td>{boutique.nombreProduits || 0}</td>
                <td>
                  <button className="btn btn-secondary" style={{ padding: '5px 10px' }}>Voir</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}
