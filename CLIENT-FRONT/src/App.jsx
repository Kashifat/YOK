import './App.css'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, AuthContext } from './context/AuthContext'
import { useContext } from 'react'

// Pages
import Accueil from './pages/Accueil'
import Catalogue from './pages/Catalogue'
import Favoris from './pages/Favoris'
import Panier from './pages/Panier'
import Commandes from './pages/Commandes'
import Profil from './pages/Profil'
import Connexion from './pages/Connexion'

// Composants
import Header from './components/Header'
import Navigation from './components/Navigation'
import Footer from './components/Footer'

function AppRoutes() {
  const { estConnecte } = useContext(AuthContext)

  return (
    <Router>
      <div className="app">
        <Header />
        <Navigation />
        
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Accueil />} />
            <Route path="/catalogue" element={<Catalogue />} />
            <Route path="/connexion" element={<Connexion />} />
            
            {/* Routes protégées */}
            <Route 
              path="/favoris" 
              element={estConnecte() ? <Favoris /> : <Navigate to="/connexion" />} 
            />
            <Route 
              path="/panier" 
              element={estConnecte() ? <Panier /> : <Navigate to="/connexion" />} 
            />
            <Route 
              path="/mes-commandes" 
              element={estConnecte() ? <Commandes /> : <Navigate to="/connexion" />} 
            />
            <Route 
              path="/profil" 
              element={estConnecte() ? <Profil /> : <Navigate to="/connexion" />} 
            />
            
            {/* Route par défaut */}
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </main>

        <Footer />
      </div>
    </Router>
  )
}

function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  )
}

export default App
