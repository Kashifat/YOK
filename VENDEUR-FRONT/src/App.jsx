import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'

// Pages
import TableauDeBord from './pages/TableauDeBord'
import AjouterProduit from './pages/AjouterProduit'
import MesProduits from './pages/MesProduits'
import MesCommandes from './pages/MesCommandes'
import Avis from './pages/Avis'
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
              <Route path="/ajouter-produit" element={<AjouterProduit />} />
              <Route path="/mes-produits" element={<MesProduits />} />
              <Route path="/mes-commandes" element={<MesCommandes />} />
              <Route path="/avis" element={<Avis />} />
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
