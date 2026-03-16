import { useState, useEffect } from 'react'

export default function MesProduits() {
  const [produits, setProduits] = useState([])
  const [chargement, setChargement] = useState(true)

  useEffect(() => {
    chargerProduits()
  }, [])

  async function chargerProduits() {
    try {
      setChargement(true)
      // TODO: Appel API pour récupérer les produits
      setProduits([])
    } finally {
      setChargement(false)
    }
  }

  if (chargement) return <div>Chargement...</div>

  return (
    <div className="container">
      <h1>Mes Produits</h1>

      {produits.length === 0 ? (
        <p style={{ marginTop: '20px', textAlign: 'center' }}>
          Vous n'avez pas encore ajouté de produits.{' '}
          <a href="/ajouter-produit">Ajouter un produit</a>
        </p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Nom</th>
              <th>Prix</th>
              <th>Stock</th>
              <th>Ventes</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {produits.map(prod => (
              <tr key={prod.id}>
                <td>{prod.nom}</td>
                <td>{prod.prix} FCFA</td>
                <td>{prod.stock}</td>
                <td>{prod.ventes || 0}</td>
                <td>
                  <button className="btn btn-secondary" style={{ padding: '5px 10px' }}>Éditer</button>
                  <button className="btn btn-danger" style={{ padding: '5px 10px', marginLeft: '5px' }}>Supprimer</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}
