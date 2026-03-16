import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'

// Pages
import TableauDeBord from './pages/TableauDeBord'
import Utilisateurs from './pages/Utilisateurs'
import Boutiques from './pages/Boutiques'
import Produits from './pages/Produits'
import Statistiques from './pages/Statistiques'
import Connexion from './pages/Connexion'

// Composants
import Header from './components/Header'
import Navigation from './components/Navigation'
import Footer from './components/Footer'

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="app">
          <Header />
          <Navigation />
          
          <main className="main-content">
            <Routes>
              <Route path="/connexion" element={<Connexion />} />
              <Route path="/" element={<TableauDeBord />} />
              <Route path="/utilisateurs" element={<Utilisateurs />} />
              <Route path="/boutiques" element={<Boutiques />} />
              <Route path="/produits" element={<Produits />} />
              <Route path="/statistiques" element={<Statistiques />} />
              <Route path="*" element={<Navigate to="/" />} />
            </Routes>
          </main>

          <Footer />
        </div>
      </Router>
    </AuthProvider>
  )
}

export default App
