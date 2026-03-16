import { useState, useEffect } from 'react'

export default function TableauDeBord() {
  const [stats, setStats] = useState({
    utilisateurs: 0,
    boutiques: 0,
    produits: 0,
    commandes: 0,
    revenus: 0
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
        utilisateurs: 1250,
        boutiques: 45,
        produits: 3200,
        commandes: 850,
        revenus: 25000000
      })
    } finally {
      setChargement(false)
    }
  }

  if (chargement) return <div>Chargement...</div>

  return (
    <div className="container">
      <h1>Tableau de Bord Administrateur 🔧</h1>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px', marginTop: '30px' }}>
        <div className="card" style={{ padding: '20px', textAlign: 'center' }}>
          <h3 style={{ color: '#666' }}>Utilisateurs</h3>
          <p style={{ fontSize: '32px', fontWeight: 'bold', color: '#007bff', marginTop: '10px' }}>
            {stats.utilisateurs.toLocaleString()}
          </p>
        </div>

        <div className="card" style={{ padding: '20px', textAlign: 'center' }}>
          <h3 style={{ color: '#666' }}>Boutiques</h3>
          <p style={{ fontSize: '32px', fontWeight: 'bold', color: '#28a745', marginTop: '10px' }}>
            {stats.boutiques}
          </p>
        </div>

        <div className="card" style={{ padding: '20px', textAlign: 'center' }}>
          <h3 style={{ color: '#666' }}>Produits</h3>
          <p style={{ fontSize: '32px', fontWeight: 'bold', color: '#ffc107', marginTop: '10px' }}>
            {stats.produits.toLocaleString()}
          </p>
        </div>

        <div className="card" style={{ padding: '20px', textAlign: 'center' }}>
          <h3 style={{ color: '#666' }}>Commandes</h3>
          <p style={{ fontSize: '32px', fontWeight: 'bold', color: '#17a2b8', marginTop: '10px' }}>
            {stats.commandes.toLocaleString()}
          </p>
        </div>

        <div className="card" style={{ padding: '20px', textAlign: 'center' }}>
          <h3 style={{ color: '#666' }}>Revenus totaux</h3>
          <p style={{ fontSize: '32px', fontWeight: 'bold', color: '#dc3545', marginTop: '10px' }}>
            {stats.revenus.toLocaleString()} FCFA
          </p>
        </div>
      </div>

      <section style={{ marginTop: '40px' }}>
        <h2>Gestion rapide</h2>
        <div style={{ display: 'flex', gap: '10px', marginTop: '15px', flexWrap: 'wrap' }}>
          <button className="btn btn-primary">Valider boutiques</button>
          <button className="btn btn-secondary">Modérer produits</button>
          <button className="btn btn-secondary">Gérer utilisateurs</button>
          <button className="btn btn-secondary">Voir statistiques</button>
        </div>
      </section>
    </div>
  )
}
