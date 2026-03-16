import { useState, useContext } from 'react'
import { useNavigate } from 'react-router-dom'
import { AuthContext } from '../context/AuthContext'
import { authService } from '../services/apiService'

export default function Connexion() {
  const navigate = useNavigate()
  const { connecter, estConnecte } = useContext(AuthContext)
  const [mode, setMode] = useState('connexion') // connexion ou inscription
  const [chargement, setChargement] = useState(false)
  const [erreur, setErreur] = useState(null)
  const [formData, setFormData] = useState({
    email: '',
    motDePasse: '',
    nomComplet: '',
    telephone: ''
  })

  // Redirection si déjà connecté
  if (estConnecte()) {
    navigate('/')
  }

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleConnexion = async (e) => {
    e.preventDefault()
    setErreur(null)
    setChargement(true)

    try {
      const response = await authService.connexion(formData.email, formData.motDePasse)
      connecter(
        {
          nom_complet: formData.email.split('@')[0] || 'Client',
          courriel: formData.email
        },
        response.access_token,
        response.refresh_token
      )
      navigate('/')
    } catch (err) {
      setErreur(err.detail || 'Erreur de connexion')
      console.error(err)
    } finally {
      setChargement(false)
    }
  }

  const handleInscription = async (e) => {
    e.preventDefault()
    setErreur(null)
    setChargement(true)

    try {
      await authService.inscription(
        formData.email,
        formData.nomComplet,
        formData.motDePasse,
        formData.telephone || null
      )

      const login = await authService.connexion(formData.email, formData.motDePasse)
      connecter(
        {
          nom_complet: formData.nomComplet,
          courriel: formData.email
        },
        login.access_token,
        login.refresh_token
      )
      navigate('/')
    } catch (err) {
      setErreur(err.detail || 'Erreur lors de l\'inscription')
      console.error(err)
    } finally {
      setChargement(false)
    }
  }

  return (
    <div className="container" style={{ maxWidth: '400px', margin: '50px auto' }}>
      {mode === 'connexion' ? (
        <div className="card" style={{ padding: '30px' }}>
          <h1 style={{ marginBottom: '30px', textAlign: 'center' }}>Connexion</h1>

          {erreur && <p className="error" style={{ marginBottom: '15px' }}>{erreur}</p>}

          <form onSubmit={handleConnexion}>
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="form-group">
              <label>Mot de passe</label>
              <input
                type="password"
                name="motDePasse"
                value={formData.motDePasse}
                onChange={handleInputChange}
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

            <button
              type="button"
              className="btn btn-secondary"
              style={{ width: '100%', marginTop: '10px' }}
              onClick={() => {
                window.location.href = authService.oauthGoogleUrl()
              }}
            >
              Continuer avec Google
            </button>

            <button
              type="button"
              className="btn btn-secondary"
              style={{ width: '100%', marginTop: '10px' }}
              onClick={() => {
                window.location.href = authService.oauthFacebookUrl()
              }}
            >
              Continuer avec Facebook
            </button>
          </form>

          <p style={{ textAlign: 'center', marginTop: '15px' }}>
            Pas encore de compte?{' '}
            <button 
              onClick={() => setMode('inscription')}
              style={{ background: 'none', border: 'none', color: '#007bff', cursor: 'pointer', textDecoration: 'underline' }}
            >
              S'inscrire
            </button>
          </p>
        </div>
      ) : (
        <div className="card" style={{ padding: '30px' }}>
          <h1 style={{ marginBottom: '30px', textAlign: 'center' }}>S'inscrire</h1>

          {erreur && <p className="error" style={{ marginBottom: '15px' }}>{erreur}</p>}

          <form onSubmit={handleInscription}>
            <div className="form-group">
              <label>Nom complet</label>
              <input
                type="text"
                name="nomComplet"
                value={formData.nomComplet}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="form-group">
              <label>Téléphone (optionnel)</label>
              <input
                type="tel"
                name="telephone"
                value={formData.telephone}
                onChange={handleInputChange}
              />
            </div>

            <div className="form-group">
              <label>Mot de passe</label>
              <input
                type="password"
                name="motDePasse"
                value={formData.motDePasse}
                onChange={handleInputChange}
                required
              />
            </div>

            <button 
              type="submit" 
              className="btn btn-primary"
              style={{ width: '100%', marginTop: '20px' }}
              disabled={chargement}
            >
              {chargement ? 'Inscription en cours...' : 'S\'inscrire'}
            </button>
          </form>

          <p style={{ textAlign: 'center', marginTop: '15px' }}>
            Déjà inscrit?{' '}
            <button 
              onClick={() => setMode('connexion')}
              style={{ background: 'none', border: 'none', color: '#007bff', cursor: 'pointer', textDecoration: 'underline' }}
            >
              Se connecter
            </button>
          </p>
        </div>
      )}
    </div>
  )
}
