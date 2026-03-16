import { useState, useEffect } from 'react'

export default function Produits() {
  const [produits, setProduits] = useState([])
  const [filtreStatut, setFiltreStatut] = useState(null)
  const [chargement, setChargement] = useState(true)

  useEffect(() => {
    chargerProduits()
  }, [filtreStatut])

  async function chargerProduits() {
    try {
      setChargement(true)
      // TODO: Appel API pour les produits
      setProduits([])
    } finally {
      setChargement(false)
    }
  }

  if (chargement) return <div>Chargement...</div>

  return (
    <div className="container">
      <h1>Modération des produits 📦</h1>

      <div style={{ marginBottom: '20px', display: 'flex', gap: '10px' }}>
        <button 
          className="btn btn-secondary"
          onClick={() => setFiltreStatut(null)}
          style={{ backgroundColor: !filtreStatut ? '#dc3545' : '#6c757d' }}
        >
          Tous
        </button>
        <button 
          className="btn btn-secondary"
          onClick={() => setFiltreStatut('ACTIF')}
          style={{ backgroundColor: filtreStatut === 'ACTIF' ? '#dc3545' : '#6c757d' }}
        >
          Actifs
        </button>
        <button 
          className="btn btn-secondary"
          onClick={() => setFiltreStatut('EN_ATTENTE')}
          style={{ backgroundColor: filtreStatut === 'EN_ATTENTE' ? '#dc3545' : '#6c757d' }}
        >
          En attente
        </button>
        <button 
          className="btn btn-secondary"
          onClick={() => setFiltreStatut('REJETEE')}
          style={{ backgroundColor: filtreStatut === 'REJETEE' ? '#dc3545' : '#6c757d' }}
        >
          Rejetés
        </button>
      </div>

      {produits.length === 0 ? (
        <p style={{ textAlign: 'center', marginTop: '20px' }}>Aucun produit à modérer</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Nom</th>
              <th>Vendeur</th>
              <th>Prix</th>
              <th>Statut</th>
              <th>Date de création</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {produits.map(prod => (
              <tr key={prod.id}>
                <td>{prod.nom}</td>
                <td>{prod.vendeur}</td>
                <td>{prod.prix?.toLocaleString()} FCFA</td>
                <td>
                  <span className={`badge badge-${prod.statut === 'ACTIF' ? 'success' : prod.statut === 'EN_ATTENTE' ? 'warning' : 'danger'}`}>
                    {prod.statut}
                  </span>
                </td>
                <td>{new Date(prod.dateCreation).toLocaleDateString('fr-FR')}</td>
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
