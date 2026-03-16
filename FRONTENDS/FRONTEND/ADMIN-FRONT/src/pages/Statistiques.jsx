import { useState } from 'react'

export default function Statistiques() {
  const [periode, setPeriode] = useState('mois')

  return (
    <div className="container">
      <h1>Statistiques 📈</h1>

      <div style={{ marginBottom: '20px', display: 'flex', gap: '10px' }}>
        <button 
          className="btn btn-secondary"
          onClick={() => setPeriode('semaine')}
          style={{ backgroundColor: periode === 'semaine' ? '#dc3545' : '#6c757d' }}
        >
          Cette semaine
        </button>
        <button 
          className="btn btn-secondary"
          onClick={() => setPeriode('mois')}
          style={{ backgroundColor: periode === 'mois' ? '#dc3545' : '#6c757d' }}
        >
          Ce mois
        </button>
        <button 
          className="btn btn-secondary"
          onClick={() => setPeriode('annee')}
          style={{ backgroundColor: periode === 'annee' ? '#dc3545' : '#6c757d' }}
        >
          Cette année
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px', marginTop: '30px' }}>
        <div className="card" style={{ padding: '20px' }}>
          <h3 style={{ color: '#666' }}>Commandes</h3>
          <p style={{ fontSize: '28px', fontWeight: 'bold', color: '#007bff', marginTop: '10px' }}>
            452
          </p>
          <p style={{ color: '#999', fontSize: '12px', marginTop: '5px' }}>+12% vs période précédente</p>
        </div>

        <div className="card" style={{ padding: '20px' }}>
          <h3 style={{ color: '#666' }}>Nouveaux utilisateurs</h3>
          <p style={{ fontSize: '28px', fontWeight: 'bold', color: '#28a745', marginTop: '10px' }}>
            185
          </p>
          <p style={{ color: '#999', fontSize: '12px', marginTop: '5px' }}>+8% vs période précédente</p>
        </div>

        <div className="card" style={{ padding: '20px' }}>
          <h3 style={{ color: '#666' }}>Revenus</h3>
          <p style={{ fontSize: '28px', fontWeight: 'bold', color: '#ffc107', marginTop: '10px' }}>
            12.5M FCFA
          </p>
          <p style={{ color: '#999', fontSize: '12px', marginTop: '5px' }}>+15% vs période précédente</p>
        </div>

        <div className="card" style={{ padding: '20px' }}>
          <h3 style={{ color: '#666' }}>Taux de conversion</h3>
          <p style={{ fontSize: '28px', fontWeight: 'bold', color: '#dc3545', marginTop: '10px' }}>
            3.2%
          </p>
          <p style={{ color: '#999', fontSize: '12px', marginTop: '5px' }}>+0.5pp vs période précédente</p>
        </div>
      </div>

      <section style={{ marginTop: '40px' }}>
        <h2>Produits les plus vendus</h2>
        <table>
          <thead>
            <tr>
              <th>Produit</th>
              <th>Vendeur</th>
              <th>Ventes</th>
              <th>Revenus</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Exemple produit 1</td>
              <td>Vendeur A</td>
              <td>125</td>
              <td>2.5M FCFA</td>
            </tr>
            <tr>
              <td>Exemple produit 2</td>
              <td>Vendeur B</td>
              <td>98</td>
              <td>1.8M FCFA</td>
            </tr>
          </tbody>
        </table>
      </section>
    </div>
  )
}
