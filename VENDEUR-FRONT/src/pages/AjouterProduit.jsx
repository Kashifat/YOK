import { useState } from 'react'

export default function AjouterProduit() {
  const [formData, setFormData] = useState({
    nom: '',
    description: '',
    prix: '',
    stock: '',
    categorie: '',
    tailles: '',
    couleurs: ''
  })

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    // TODO: Appel API pour créer le produit
    console.log('Produit:', formData)
  }

  return (
    <div className="container" style={{ maxWidth: '800px' }}>
      <h1>Ajouter un produit</h1>

      <form onSubmit={handleSubmit} style={{ marginTop: '30px' }}>
        <div className="form-group">
          <label>Nom du produit</label>
          <input
            type="text"
            name="nom"
            value={formData.nom}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Description</label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows="4"
            required
          ></textarea>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
          <div className="form-group">
            <label>Prix (FCFA)</label>
            <input
              type="number"
              name="prix"
              value={formData.prix}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label>Stock</label>
            <input
              type="number"
              name="stock"
              value={formData.stock}
              onChange={handleChange}
              required
            />
          </div>
        </div>

        <div className="form-group">
          <label>Catégorie</label>
          <select
            name="categorie"
            value={formData.categorie}
            onChange={handleChange}
            required
          >
            <option value="">Sélectionner une catégorie</option>
            <option value="electronique">Électronique</option>
            <option value="mode">Mode</option>
            <option value="maison">Maison</option>
            <option value="sport">Sport</option>
            <option value="beaute">Beauté</option>
            <option value="alimentation">Alimentation</option>
            <option value="livres">Livres</option>
            <option value="jouets">Jouets</option>
          </select>
        </div>

        <div className="form-group">
          <label>Tailles (séparées par des virgules)</label>
          <input
            type="text"
            name="tailles"
            placeholder="XS, S, M, L, XL"
            value={formData.tailles}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <label>Couleurs (séparées par des virgules)</label>
          <input
            type="text"
            name="couleurs"
            placeholder="Noir, Blanc, Bleu, Rouge"
            value={formData.couleurs}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <label>Images</label>
          <input type="file" multiple accept="image/*" />
        </div>

        <button type="submit" className="btn btn-primary" style={{ marginTop: '20px' }}>
          Créer le produit
        </button>
      </form>
    </div>
  )
}
