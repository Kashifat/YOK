import { useState, useEffect } from 'react'

export default function MesCommandes() {
  const [commandes, setCommandes] = useState([])
  const [chargement, setChargement] = useState(true)

  useEffect(() => {
    chargerCommandes()
  }, [])

  async function chargerCommandes() {
    try {
      setChargement(true)
      // TODO: Appel API pour récupérer les commandes
      setCommandes([])
    } finally {
      setChargement(false)
    }
  }

  if (chargement) return <div>Chargement...</div>

  return (
    <div className="container">
      <h1>Mes Commandes à traiter</h1>

      {commandes.length === 0 ? (
        <p style={{ marginTop: '20px', textAlign: 'center' }}>Vous n'avez pas de commandes à traiter</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Numéro</th>
              <th>Client</th>
              <th>Date</th>
              <th>Montant</th>
              <th>Statut</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {commandes.map(cmd => (
              <tr key={cmd.id}>
                <td>#{cmd.numero}</td>
                <td>{cmd.client}</td>
                <td>{new Date(cmd.date).toLocaleDateString('fr-FR')}</td>
                <td>{cmd.montant} FCFA</td>
                <td>
                  <span style={{ padding: '5px 10px', borderRadius: '4px', backgroundColor: '#ffc107', color: 'white' }}>
                    {cmd.statut}
                  </span>
                </td>
                <td>
                  <button className="btn btn-primary" style={{ padding: '5px 10px' }}>Voir</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}
