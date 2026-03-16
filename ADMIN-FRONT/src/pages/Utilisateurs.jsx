import { useState, useEffect } from 'react'

export default function Utilisateurs() {
  const [utilisateurs, setUtilisateurs] = useState([])
  const [filtreRole, setFiltreRole] = useState(null)
  const [chargement, setChargement] = useState(true)

  useEffect(() => {
    chargerUtilisateurs()
  }, [filtreRole])

  async function chargerUtilisateurs() {
    try {
      setChargement(true)
      // TODO: Appel API pour les utilisateurs
      setUtilisateurs([])
    } finally {
      setChargement(false)
    }
  }

  if (chargement) return <div>Chargement...</div>

  return (
    <div className="container">
      <h1>Gestion des utilisateurs 👥</h1>

      <div style={{ marginBottom: '20px', display: 'flex', gap: '10px' }}>
        <button 
          className="btn btn-secondary"
          onClick={() => setFiltreRole(null)}
          style={{ backgroundColor: !filtreRole ? '#dc3545' : '#6c757d' }}
        >
          Tous
        </button>
        <button 
          className="btn btn-secondary"
          onClick={() => setFiltreRole('CLIENT')}
          style={{ backgroundColor: filtreRole === 'CLIENT' ? '#dc3545' : '#6c757d' }}
        >
          Clients
        </button>
        <button 
          className="btn btn-secondary"
          onClick={() => setFiltreRole('VENDEUR')}
          style={{ backgroundColor: filtreRole === 'VENDEUR' ? '#dc3545' : '#6c757d' }}
        >
          Vendeurs
        </button>
      </div>

      {utilisateurs.length === 0 ? (
        <p style={{ textAlign: 'center', marginTop: '20px' }}>Aucun utilisateur trouvé</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Email</th>
              <th>Nom</th>
              <th>Rôle</th>
              <th>Statut</th>
              <th>Date d'inscription</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {utilisateurs.map(user => (
              <tr key={user.id}>
                <td>{user.email}</td>
                <td>{user.nom}</td>
                <td>{user.role}</td>
                <td>
                  <span className={`badge ${user.actif ? 'badge-success' : 'badge-warning'}`}>
                    {user.actif ? 'Actif' : 'Inactif'}
                  </span>
                </td>
                <td>{new Date(user.dateInscription).toLocaleDateString('fr-FR')}</td>
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
