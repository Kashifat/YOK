import { useState, useContext } from 'react'
import { useNavigate } from 'react-router-dom'
import { AuthContext } from '../context/AuthContext'

export default function Connexion() {
  const navigate = useNavigate()
  const { connecter, estConnecte } = useContext(AuthContext)
  const [formData, setFormData] = useState({
    email: '',
    motDePasse: ''
  })
  const [erreur, setErreur] = useState(null)
  const [chargement, setChargement] = useState(false)

  if (estConnecte) {
    navigate('/')
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setErreur(null)
    setChargement(true)

    try {
      // TODO: Appel API pour connexion admin
      console.log('Connexion admin:', formData)
    } catch (err) {
      setErreur('Erreur de connexion')
    } finally {
      setChargement(false)
    }
  }

  return (
    <div style={{ maxWidth: '400px', margin: '50px auto' }}>
      <div className="card" style={{ padding: '30px' }}>
        <h1 style={{ marginBottom: '30px', textAlign: 'center' }}>Connexion Administrateur</h1>

        {erreur && <p style={{ color: '#dc3545', marginBottom: '15px' }}>{erreur}</p>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label>Mot de passe</label>
            <input
              type="password"
              name="motDePasse"
              value={formData.motDePasse}
              onChange={handleChange}
              required
            />
          </div>

          <button 
            type="submit" 
            className="btn btn-primary"
            style={{ width: '100%', marginTop: '20px' }}
            disabled={chargement}
          >
            {chargement ? 'Connexion en cours...' : 'Se connecter'}
          </button>
        </form>
      </div>
    </div>
  )
}
