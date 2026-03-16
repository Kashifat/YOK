import { useState, useEffect } from 'react'
import { favorisService, panierService } from '../services/apiService'

export default function Favoris() {
  const [favoris, setFavoris] = useState([])
  const [chargement, setChargement] = useState(true)
  const [erreur, setErreur] = useState(null)

  useEffect(() => {
    chargerFavoris()
  }, [])

  async function chargerFavoris() {
    try {
      setChargement(true)
      const data = await favorisService.obtenirMesFavoris()
      setFavoris(data)
    } catch (err) {
      setErreur('Erreur lors du chargement de vos favoris')
      console.error(err)
    } finally {
      setChargement(false)
    }
  }

  async function retirerFavori(produitId) {
    try {
      await favorisService.retirer(produitId)
      setFavoris(favoris.filter(f => f.produit_identifiant !== produitId))
    } catch (err) {
      setErreur('Erreur lors du retrait du favori')
      console.error(err)
    }
  }

  async function ajouterAuPanierDepuisFavori(produitId) {
    try {
      await panierService.ajouterArticle(produitId, 1)
    } catch (err) {
      setErreur(err?.detail || 'Erreur lors de l’ajout au panier')
    }
  }

  if (chargement) return <div className="loading"><div className="spinner"></div></div>

  return (
    <div className="container">
      <h1>Mes Favoris ❤️</h1>

      {erreur && <p className="error">{erreur}</p>}

      {favoris.length === 0 ? (
        <p style={{ textAlign: 'center', marginTop: '40px' }}>Vous n'avez pas de favoris pour le moment</p>
      ) : (
        <>
          <p style={{ marginBottom: '20px' }}>{favoris.length} produit(s) en favori</p>
          <div className="grid">
            {favoris.map(fav => (
              <div key={fav.identifiant} className="card">
                <img 
                  src={'/placeholder.jpg'} 
                  alt={fav.produit_nom}
                  style={{ width: '100%', height: '200px', objectFit: 'cover' }}
                />
                <div style={{ padding: '15px' }}>
                  <h3 style={{ marginBottom: '5px' }}>{fav.produit_nom}</h3>
                  <p style={{ fontSize: '16px', fontWeight: 'bold', color: '#007bff', marginBottom: '10px' }}>
                    {fav.produit_prix_cfa?.toLocaleString()} FCFA
                  </p>
                  <p style={{ fontSize: '12px', color: fav.produit_stock > 0 ? '#28a745' : '#dc3545' }}>
                    Stock: {fav.produit_stock}
                  </p>
                  <div style={{ marginTop: '10px', display: 'flex', gap: '10px' }}>
                    <button className="btn btn-primary" style={{ flex: 1 }} onClick={() => ajouterAuPanierDepuisFavori(fav.produit_identifiant)}>
                      Ajouter au panier
                    </button>
                    <button 
                      className="btn btn-danger"
                      onClick={() => retirerFavori(fav.produit_identifiant)}
                    >
                      Retirer
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  )
}
