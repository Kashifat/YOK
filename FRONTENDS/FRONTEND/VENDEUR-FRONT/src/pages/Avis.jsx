import { useState, useEffect } from 'react'

export default function Avis() {
  const [avis, setAvis] = useState([])
  const [chargement, setChargement] = useState(true)

  useEffect(() => {
    chargerAvis()
  }, [])

  async function chargerAvis() {
    try {
      setChargement(true)
      // TODO: Appel API pour récupérer les avis
      setAvis([])
    } finally {
      setChargement(false)
    }
  }

  if (chargement) return <div>Chargement...</div>

  return (
    <div className="container">
      <h1>Avis des clients ⭐</h1>

      {avis.length === 0 ? (
        <p style={{ marginTop: '20px', textAlign: 'center' }}>Vous n'avez pas encore reçu d'avis</p>
      ) : (
        <div style={{ marginTop: '20px' }}>
          {avis.map(a => (
            <div key={a.id} className="card" style={{ padding: '15px', marginBottom: '15px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <div>
                  <h3>{a.client}</h3>
                  <p style={{ color: '#666' }}>⭐ {a.note}/5</p>
                </div>
                <p style={{ color: '#999', fontSize: '12px' }}>
                  {new Date(a.date).toLocaleDateString('fr-FR')}
                </p>
              </div>
              <p style={{ marginTop: '10px' }}>{a.texte}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
