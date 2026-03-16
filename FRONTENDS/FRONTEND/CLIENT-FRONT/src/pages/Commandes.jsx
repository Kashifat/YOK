import { useState, useEffect } from 'react'
import { commandeService, paiementService, factureService } from '../services/apiService'

export default function Commandes() {
  const [commandes, setCommandes] = useState([])
  const [factures, setFactures] = useState([])
  const [chargement, setChargement] = useState(true)
  const [erreur, setErreur] = useState(null)
  const [message, setMessage] = useState(null)
  const [adresseId, setAdresseId] = useState('')
  const [remarques, setRemarques] = useState('')

  useEffect(() => {
    chargerCommandes()
  }, [])

  async function chargerCommandes() {
    try {
      setChargement(true)
      const [cmds, facts] = await Promise.all([
        commandeService.listerMesCommandes(),
        factureService.listerMesFactures()
      ])
      setCommandes(cmds)
      setFactures(facts)
      setErreur(null)
    } catch (err) {
      setErreur(err?.detail || 'Erreur lors du chargement des commandes')
    } finally {
      setChargement(false)
    }
  }

  async function creerCommande() {
    if (!adresseId.trim()) {
      setErreur('Renseigne un identifiant d’adresse (UUID)')
      return
    }
    try {
      const created = await commandeService.creerDepuisPanier(adresseId.trim(), remarques.trim() || null)
      setMessage(`Commande créée: ${created.identifiant}`)
      setErreur(null)
      setRemarques('')
      await chargerCommandes()
    } catch (err) {
      setErreur(err?.detail || 'Impossible de créer la commande')
    }
  }

  async function annulerCommande(commandeId) {
    try {
      await commandeService.annuler(commandeId)
      setMessage('Commande annulée')
      await chargerCommandes()
    } catch (err) {
      setErreur(err?.detail || 'Annulation impossible')
    }
  }

  async function initierPaiement(commandeId) {
    const telephone = window.prompt('Numéro téléphone paiement (optionnel):', '') || null
    try {
      const data = await paiementService.initialiser(commandeId, telephone)
      setMessage('Paiement initialisé, ouverture du lien CinetPay')
      if (data?.payment_url) {
        window.open(data.payment_url, '_blank')
      }
      await chargerCommandes()
    } catch (err) {
      setErreur(err?.detail || 'Initialisation paiement impossible')
    }
  }

  async function genererFacture(commandeId) {
    try {
      await factureService.genererDepuisCommande(commandeId)
      setMessage('Facture générée')
      await chargerCommandes()
    } catch (err) {
      setErreur(err?.detail || 'Génération facture impossible')
    }
  }

  async function telechargerFacture(factureId) {
    try {
      const html = await factureService.telechargerHtml(factureId)
      const blob = new Blob([html], { type: 'text/html' })
      const url = window.URL.createObjectURL(blob)
      window.open(url, '_blank')
    } catch (err) {
      setErreur(err?.detail || 'Téléchargement facture impossible')
    }
  }

  if (chargement) return <div className="loading"><div className="spinner"></div></div>

  return (
    <div className="container">
      <h1>Mes Commandes 📦</h1>

      {erreur && <p className="error" style={{ marginTop: '10px' }}>{erreur}</p>}
      {message && <p className="success" style={{ marginTop: '10px' }}>{message}</p>}

      <div className="card" style={{ marginTop: '20px', padding: '15px' }}>
        <h3>Créer une commande depuis le panier</h3>
        <div className="form-group" style={{ marginTop: '10px' }}>
          <label>Adresse identifiant (UUID)</label>
          <input value={adresseId} onChange={(e) => setAdresseId(e.target.value)} placeholder="UUID adresse" />
        </div>
        <div className="form-group">
          <label>Remarques (optionnel)</label>
          <input value={remarques} onChange={(e) => setRemarques(e.target.value)} placeholder="Instruction de livraison" />
        </div>
        <button className="btn btn-primary" onClick={creerCommande}>Créer commande</button>
      </div>

      {commandes.length === 0 ? (
        <p style={{ textAlign: 'center', marginTop: '40px' }}>Vous n'avez pas encore passé de commande</p>
      ) : (
        <div>
          {commandes.map(cmd => (
            <div key={cmd.identifiant} className="card" style={{ marginBottom: '15px', padding: '15px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <h3>Commande #{cmd.identifiant}</h3>
                  <p style={{ color: '#666', fontSize: '14px' }}>
                    Passée le {new Date(cmd.date_creation).toLocaleDateString('fr-FR')}
                  </p>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <p style={{ fontSize: '18px', fontWeight: 'bold', color: '#007bff' }}>
                    {cmd.total_cfa} FCFA
                  </p>
                  <p style={{ color: '#28a745', fontWeight: 'bold' }}>
                    {cmd.statut}
                  </p>
                </div>
              </div>
              <p style={{ marginTop: '10px', color: '#555' }}>Articles: {(cmd.articles || []).length}</p>
              <div style={{ display: 'flex', gap: '10px', marginTop: '10px', flexWrap: 'wrap' }}>
                <button className="btn btn-primary" onClick={() => initierPaiement(cmd.identifiant)}>Payer</button>
                <button className="btn btn-secondary" onClick={() => genererFacture(cmd.identifiant)}>Générer facture</button>
                <button className="btn btn-danger" onClick={() => annulerCommande(cmd.identifiant)}>Annuler</button>
              </div>
            </div>
          ))}

          <div className="card" style={{ marginTop: '25px', padding: '15px' }}>
            <h3>Mes Factures</h3>
            {factures.length === 0 ? (
              <p style={{ marginTop: '10px' }}>Aucune facture disponible.</p>
            ) : (
              <div style={{ marginTop: '10px' }}>
                {factures.map(f => (
                  <div key={f.identifiant} style={{ borderBottom: '1px solid #eee', padding: '10px 0' }}>
                    <p><strong>{f.numero_facture}</strong> - {f.montant_total_cfa} FCFA - {f.statut_paiement}</p>
                    <button className="btn btn-secondary" onClick={() => telechargerFacture(f.identifiant)}>Télécharger HTML</button>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
