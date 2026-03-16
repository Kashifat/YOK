import { useState, useEffect } from 'react'

export default function TableauDeBord() {
  const [stats, setStats] = useState({
    ventes: 0,
    revenus: 0,
    produits: 0,
    commandes: 0
  })
  const [chargement, setChargement] = useState(true)

  useEffect(() => {
    chargerStats()
  }, [])

  async function chargerStats() {
    try {
      setChargement(true)
      // TODO: Appel API pour les stats
      setStats({
        ventes: 125,
        revenus: 2500000,
        produits: 48,
        commandes: 35
      })
    } finally {
      setChargement(false)
    }
  }

  if (chargement) return <div>Chargement...</div>

  return (
    <div className="container">
      <h1>Tableau de Bord 📊</h1>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px', marginTop: '30px' }}>
        <div className="card" style={{ padding: '20px', textAlign: 'center' }}>
          <h3 style={{ color: '#666' }}>Ventes du mois</h3>
          <p style={{ fontSize: '32px', fontWeight: 'bold', color: '#28a745', marginTop: '10px' }}>
            {stats.ventes}
          </p>
        </div>

        <div className="card" style={{ padding: '20px', textAlign: 'center' }}>
          <h3 style={{ color: '#666' }}>Revenus</h3>
          <p style={{ fontSize: '32px', fontWeight: 'bold', color: '#007bff', marginTop: '10px' }}>
            {stats.revenus.toLocaleString()} FCFA
          </p>
        </div>

        <div className="card" style={{ padding: '20px', textAlign: 'center' }}>
          <h3 style={{ color: '#666' }}>Produits</h3>
          <p style={{ fontSize: '32px', fontWeight: 'bold', color: '#ffc107', marginTop: '10px' }}>
            {stats.produits}
          </p>
        </div>

        <div className="card" style={{ padding: '20px', textAlign: 'center' }}>
          <h3 style={{ color: '#666' }}>Commandes</h3>
          <p style={{ fontSize: '32px', fontWeight: 'bold', color: '#17a2b8', marginTop: '10px' }}>
            {stats.commandes}
          </p>
        </div>
      </div>

      <section style={{ marginTop: '40px' }}>
        <h2>Actions rapides</h2>
        <div style={{ display: 'flex', gap: '10px', marginTop: '15px', flexWrap: 'wrap' }}>
          <button className="btn btn-primary">Ajouter un produit</button>
          <button className="btn btn-secondary">Voir mes commandes</button>
          <button className="btn btn-secondary">Gérer ma boutique</button>
        </div>
      </section>
    </div>
  )
}
