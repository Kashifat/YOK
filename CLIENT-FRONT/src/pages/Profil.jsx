import { useState, useContext } from 'react'
import { AuthContext } from '../context/AuthContext'

export default function Profil() {
  const { utilisateur, deconnecter } = useContext(AuthContext)
  const [edition, setEdition] = useState(false)

  const handleDeconnexion = () => {
    deconnecter()
    window.location.href = '/'
  }

  return (
    <div className="container">
      <h1>Mon Profil 👤</h1>

      <div style={{ marginTop: '30px', maxWidth: '500px' }}>
        <div className="card" style={{ padding: '20px' }}>
          <div style={{ marginBottom: '20px', textAlign: 'center' }}>
            <div style={{
              width: '100px',
              height: '100px',
              borderRadius: '50%',
              backgroundColor: '#e0e0e0',
              margin: '0 auto 15px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '40px'
            }}>
              👤
            </div>
            <h2>{utilisateur?.nom_complet || 'Utilisateur'}</h2>
            <p style={{ color: '#666' }}>{utilisateur?.courriel}</p>
          </div>

          {!edition ? (
            <>
              <div style={{ marginBottom: '15px' }}>
                <label style={{ fontWeight: 'bold' }}>Identifiant</label>
                <p style={{ backgroundColor: '#f5f5f5', padding: '10px', borderRadius: '4px' }}>
                  {utilisateur?.identifiant || '-'}
                </p>
              </div>

              <div style={{ marginBottom: '15px' }}>
                <label style={{ fontWeight: 'bold' }}>Rôle</label>
                <p style={{ backgroundColor: '#f5f5f5', padding: '10px', borderRadius: '4px' }}>
                  {utilisateur?.role || 'CLIENT'}
                </p>
              </div>

              <div style={{ marginBottom: '15px' }}>
                <label style={{ fontWeight: 'bold' }}>Email</label>
                <p style={{ backgroundColor: '#f5f5f5', padding: '10px', borderRadius: '4px' }}>
                  {utilisateur?.courriel || 'Non disponible (token OAuth)'}
                </p>
              </div>

              <div style={{ marginBottom: '15px' }}>
                <label style={{ fontWeight: 'bold' }}>Nom complet</label>
                <p style={{ backgroundColor: '#f5f5f5', padding: '10px', borderRadius: '4px' }}>
                  {utilisateur?.nom_complet}
                </p>
              </div>

              <div style={{ marginTop: '20px', display: 'flex', gap: '10px' }}>
                <button 
                  className="btn btn-primary"
                  onClick={() => setEdition(true)}
                  style={{ flex: 1 }}
                >
                  Modifier (local)
                </button>
                <button 
                  className="btn btn-danger"
                  onClick={handleDeconnexion}
                  style={{ flex: 1 }}
                >
                  Se déconnecter
                </button>
              </div>
            </>
          ) : (
            <>
              <p style={{ marginBottom: '10px', color: '#666' }}>
                Cette édition est locale (pas encore reliée à un endpoint backend de profil).
              </p>
              <div className="form-group">
                <label>Nom complet</label>
                <input type="text" defaultValue={utilisateur?.nom_complet} />
              </div>

              <div className="form-group">
                <label>Email</label>
                <input type="email" defaultValue={utilisateur?.courriel} />
              </div>

              <div style={{ display: 'flex', gap: '10px' }}>
                <button 
                  className="btn btn-primary"
                  style={{ flex: 1 }}
                >
                  Enregistrer
                </button>
                <button 
                  className="btn btn-secondary"
                  onClick={() => setEdition(false)}
                  style={{ flex: 1 }}
                >
                  Annuler
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
