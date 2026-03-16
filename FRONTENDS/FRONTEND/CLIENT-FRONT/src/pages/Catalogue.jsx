import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { catalogueService, favorisService, panierService } from '../services/apiService'

export default function Catalogue() {
  const [produits, setProduits] = useState([])
  const [categories, setCategories] = useState([])
  const [categorieSelectionnee, setCategorieSelectionnee] = useState(null)
  const [recherche, setRecherche] = useState('')
  const [chargement, setChargement] = useState(true)
  const [erreur, setErreur] = useState(null)
  const [message, setMessage] = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    chargerDonnees()
  }, [categorieSelectionnee, recherche])

  async function chargerDonnees() {
    try {
      setChargement(true)
      let data
      
      if (recherche) {
        data = await catalogueService.rechercher(recherche)
      } else {
        data = await catalogueService.obtenirProduits(categorieSelectionnee)
      }
      
      setProduits(data)
      
      if (!categories.length) {
        const cats = await catalogueService.obtenirCategories()
        setCategories(cats)
      }
    } catch (err) {
      setErreur('Erreur lors du chargement du catalogue')
      console.error(err)
    } finally {
      setChargement(false)
    }
  }

  async function ajouterAuxFavoris(produitId) {
    setErreur(null)
    setMessage(null)
    try {
      await favorisService.ajouter(produitId)
      setMessage('Produit ajouté aux favoris')
    } catch (err) {
      if (typeof err?.detail === 'string' && err.detail.toLowerCase().includes('auth')) {
        navigate('/connexion')
        return
      }
      setErreur(err?.detail || 'Impossible d’ajouter aux favoris')
    }
  }

  async function ajouterAuPanier(produitId) {
    setErreur(null)
    setMessage(null)
    try {
      await panierService.ajouterArticle(produitId, 1)
      setMessage('Produit ajouté au panier')
    } catch (err) {
      if (typeof err?.detail === 'string' && err.detail.toLowerCase().includes('auth')) {
        navigate('/connexion')
        return
      }
      setErreur(err?.detail || 'Impossible d’ajouter au panier')
    }
  }

  if (chargement) return <div className="loading"><div className="spinner"></div></div>

  return (
    <div className="container">
      <h1>Catalogue</h1>

      <div style={{ marginBottom: '20px' }}>
        <input
          type="text"
          placeholder="Rechercher un produit..."
          value={recherche}
          onChange={(e) => setRecherche(e.target.value)}
          style={{ 
            width: '100%', 
            padding: '10px', 
            borderRadius: '4px', 
            border: '1px solid #ddd',
            fontSize: '16px'
          }}
        />
      </div>

      <div style={{ marginBottom: '20px' }}>
        <h3>Filtrer par catégorie</h3>
        <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
          <button
            className={`btn ${!categorieSelectionnee ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setCategorieSelectionnee(null)}
          >
            Tous les produits
          </button>
          {categories.map(cat => (
            <button
              key={cat.identifiant}
              className={`btn ${categorieSelectionnee === cat.identifiant ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setCategorieSelectionnee(cat.identifiant)}
            >
              {cat.nom}
            </button>
          ))}
        </div>
      </div>

      {erreur && <p className="error">{erreur}</p>}
      {message && <p className="success">{message}</p>}

      {produits.length === 0 ? (
        <p style={{ textAlign: 'center', marginTop: '40px' }}>Aucun produit trouvé</p>
      ) : (
        <>
          <p style={{ marginBottom: '20px' }}>{produits.length} produit(s) trouvé(s)</p>
          <div className="grid">
            {produits.map(produit => (
              <div key={produit.identifiant} className="card">
                <img 
                  src={'/placeholder.jpg'} 
                  alt={produit.nom}
                  style={{ width: '100%', height: '200px', objectFit: 'cover' }}
                />
                <div style={{ padding: '15px' }}>
                  <h3 style={{ marginBottom: '5px' }}>{produit.nom}</h3>
                  <p style={{ color: '#666', fontSize: '12px', marginBottom: '10px' }}>
                    Vendeur ID: {produit.vendeur_identifiant}
                  </p>
                  <p style={{ fontSize: '16px', fontWeight: 'bold', color: '#007bff', marginBottom: '10px' }}>
                    {produit.prix_cfa?.toLocaleString()} FCFA
                  </p>
                  <p style={{ fontSize: '12px', color: produit.stock > 0 ? '#28a745' : '#dc3545' }}>
                    Stock: {produit.stock}
                  </p>
                  <div style={{ marginTop: '10px', display: 'flex', gap: '10px' }}>
                    <button className="btn btn-primary" style={{ flex: 1 }} onClick={() => ajouterAuPanier(produit.identifiant)}>
                      Ajouter au panier
                    </button>
                    <button className="btn btn-secondary" onClick={() => ajouterAuxFavoris(produit.identifiant)}>❤️</button>
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
