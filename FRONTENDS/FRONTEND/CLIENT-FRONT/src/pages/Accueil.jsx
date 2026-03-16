import { useState, useEffect } from 'react'
import { catalogueService } from '../services/apiService'

export default function Accueil() {
  const [produits, setProduits] = useState([])
  const [categories, setCategories] = useState([])
  const [chargement, setChargement] = useState(true)
  const [erreur, setErreur] = useState(null)

  useEffect(() => {
    chargerDonnees()
  }, [])

  async function chargerDonnees() {
    try {
      setChargement(true)
      const [produitsData, categoriesData] = await Promise.all([
        catalogueService.obtenirProduits(),
        catalogueService.obtenirCategories()
      ])
      setProduits((produitsData || []).slice(0, 8))
      setCategories(categoriesData)
    } catch (err) {
      setErreur('Erreur lors du chargement des données')
      console.error(err)
    } finally {
      setChargement(false)
    }
  }

  if (chargement) return <div className="loading"><div className="spinner"></div></div>

  return (
    <div className="container">
      <h1>Bienvenue sur YOK 🌍</h1>
      <p>La marketplace sénégalaise de référence</p>

      <section style={{ marginTop: '40px' }}>
        <h2>Catégories</h2>
        <div className="grid" style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(150px, 1fr))' }}>
          {categories.map(cat => (
            <div key={cat.identifiant} className="card" style={{ padding: '15px', textAlign: 'center' }}>
              <h3>{cat.nom}</h3>
              <p style={{ fontSize: '12px', color: '#666' }}>{cat.description || 'Catégorie active'}</p>
            </div>
          ))}
        </div>
      </section>

      <section style={{ marginTop: '40px' }}>
        <h2>Produits en vedette</h2>
        {erreur && <p className="error">{erreur}</p>}
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
                <p style={{ color: '#666', fontSize: '14px', marginBottom: '10px' }}>
                  {produit.description?.substring(0, 100)}...
                </p>
                <p style={{ fontSize: '18px', fontWeight: 'bold', color: '#007bff', marginBottom: '10px' }}>
                  {produit.prix_cfa?.toLocaleString()} FCFA
                </p>
                <p style={{ fontSize: '12px', color: produit.stock > 0 ? '#28a745' : '#dc3545' }}>
                  Stock: {produit.stock}
                </p>
                <button className="btn btn-primary" style={{ width: '100%', marginTop: '10px' }}>
                  Voir détails
                </button>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}
