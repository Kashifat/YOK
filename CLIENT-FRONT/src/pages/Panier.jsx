import { useEffect, useState } from 'react'
import { panierService } from '../services/apiService'

export default function Panier() {
  const [panier, setPanier] = useState(null)
  const [chargement, setChargement] = useState(true)
  const [erreur, setErreur] = useState(null)

  useEffect(() => {
    chargerPanier()
  }, [])

  async function chargerPanier() {
    try {
      setChargement(true)
      setErreur(null)
      const data = await panierService.obtenir()
      setPanier(data)
    } catch (err) {
      setErreur(err?.detail || 'Impossible de charger le panier')
    } finally {
      setChargement(false)
    }
  }

  async function modifierQuantite(produitId, quantite) {
    try {
      await panierService.majQuantite(produitId, quantite)
      await chargerPanier()
    } catch (err) {
      setErreur(err?.detail || 'Impossible de modifier la quantité')
    }
  }

  async function retirer(produitId) {
    try {
      await panierService.supprimerArticle(produitId)
      await chargerPanier()
    } catch (err) {
      setErreur(err?.detail || 'Impossible de retirer cet article')
    }
  }

  async function vider() {
    try {
      await panierService.vider()
      await chargerPanier()
    } catch (err) {
      setErreur(err?.detail || 'Impossible de vider le panier')
    }
  }

  const articles = panier?.articles || []

  if (chargement) return <div className="loading"><div className="spinner"></div></div>

  return (
    <div className="container">
      <h1>Mon Panier 🛒</h1>

      {erreur && <p className="error" style={{ marginTop: '10px' }}>{erreur}</p>}

      {articles.length === 0 ? (
        <p style={{ textAlign: 'center', marginTop: '40px' }}>Votre panier est vide</p>
      ) : (
        <div>
          <div style={{ marginBottom: '10px', display: 'flex', justifyContent: 'space-between' }}>
            <p><strong>{articles.length}</strong> article(s)</p>
            <button className="btn btn-danger" onClick={vider}>Vider le panier</button>
          </div>

          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ backgroundColor: '#f5f5f5' }}>
                <th style={{ padding: '10px', textAlign: 'left', borderBottom: '1px solid #ddd' }}>Produit ID</th>
                <th style={{ padding: '10px', textAlign: 'center', borderBottom: '1px solid #ddd' }}>Quantité</th>
                <th style={{ padding: '10px', textAlign: 'center', borderBottom: '1px solid #ddd' }}>Action</th>
              </tr>
            </thead>
            <tbody>
              {articles.map(item => (
                <tr key={item.identifiant} style={{ borderBottom: '1px solid #ddd' }}>
                  <td style={{ padding: '10px' }}>{item.produit_identifiant}</td>
                  <td style={{ padding: '10px', textAlign: 'center' }}>
                    <input
                      type="number"
                      value={item.quantite}
                      min="1"
                      style={{ width: '65px' }}
                      onChange={(e) => {
                        const qte = Number(e.target.value)
                        if (qte > 0) {
                          modifierQuantite(item.produit_identifiant, qte)
                        }
                      }}
                    />
                  </td>
                  <td style={{ padding: '10px', textAlign: 'center' }}>
                    <button className="btn btn-danger" onClick={() => retirer(item.produit_identifiant)}>Retirer</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          <div style={{ marginTop: '20px', textAlign: 'right' }}>
            <h3>Étape suivante: créer une commande depuis la page « Mes commandes »</h3>
          </div>
        </div>
      )}
    </div>
  )
}
