# 💰 Wallet Vendeur - Architecture Complète

## 📋 Modèle de données (PostgreSQL)

Trois tables centrales :

### **1. wallet_vendeurs**

```sql
CREATE TABLE wallet_vendeurs (
  vendeur_identifiant UUID PRIMARY KEY,
  solde_disponible_cfa INTEGER,        -- ✅ Argent libre, prêt au retrait
  solde_en_attente_cfa INTEGER,        -- ⏳ Argent bloqué en attente
  date_creation TIMESTAMPTZ,
  date_mise_a_jour TIMESTAMPTZ
);
```

**Invariant:** `solde_disponible + solde_en_attente = argent total du vendeur`

---

### **2. wallet_reservations_commandes**

Chaque commande contenant des articles du vendeur crée une **réservation** :

```sql
CREATE TABLE wallet_reservations_commandes (
  identifiant UUID PRIMARY KEY,
  vendeur_identifiant UUID,
  commande_identifiant UUID UNIQUE,
  montant_total_net_cfa INTEGER,          -- Prix après 10% commission
  montant_en_attente_restant_cfa INTEGER, -- Argent qui attend tranches
  montant_avance_debloque_cfa INTEGER,    -- 20% libéré à EXPEDIE_PAR_VENDEUR
  montant_solde_debloque_cfa INTEGER,     -- 80% libéré à RECU_PAR_AGENT
  statut ENUM('EN_ATTENTE', 'PARTIELLEMENT_LIBEREE', 'LIBEREE', 'ANNULEE'),
  date_creation TIMESTAMPTZ
);
```

**Statuts:**

- `EN_ATTENTE` → Commande payée, argent bloqué (100%)
- `PARTIELLEMENT_LIBEREE` → 20% débloqué (après EXPEDIE_PAR_VENDEUR)
- `LIBEREE` → 100% débloqué (après RECU_PAR_AGENT)
- `ANNULEE` → Commande annulée/remboursée

---

### **3. transactions_wallet**

**Audit trail** de chaque mouvement d'argent :

```sql
CREATE TABLE transactions_wallet (
  identifiant UUID PRIMARY KEY,
  vendeur_identifiant UUID,
  commande_identifiant UUID,
  type ENUM('CREDIT_ATTENTE', 'DEBIT_ATTENTE', 'CREDIT_DISPONIBLE', 'PAIEMENT_EFFECTUE'),
  montant_cfa INTEGER,
  commentaire TEXT,
  date_creation TIMESTAMPTZ
);
```

---

## 🔄 Flux d'argent - Modèle V2 (20% + 80%)

### **Exemple concret : Commande de 100 000 FCFA**

```
ÉTAPE 1: Commande PAYEE (Client a payé)
┌─────────────────────────────────────────┐
│ Montant brut vendeur: 100 000 FCFA      │
│ Commission plateforme (10%): -10 000    │
│ Montant net: 90 000 FCFA                │
└─────────────────────────────────────────┘
                    ↓
Wallet création/maj:
  solde_en_attente_cfa += 90 000
  solde_en_attente_cfa = 90 000
  solde_disponible_cfa = 0
                    ↓
Réservation:
  montant_total_net_cfa = 90 000
  montant_en_attente_restant = 90 000  ← Le "pool" à débloquer
  montant_avance_debloque = 0
  montant_solde_debloque = 0
  statut = EN_ATTENTE
                    ↓
Transactions:
  ✓ CREDIT_ATTENTE (+90 000 FCFA, "Commande payée: crédit en attente")


ÉTAPE 2: Vendeur expédie + Tracking valide (EXPEDIE_PAR_VENDEUR)
┌─────────────────────────────────────────┐
│ Tranche 1: 20% de 90 000 = 18 000 FCFA │
│ Reste: 72 000 FCFA en attente           │
└─────────────────────────────────────────┘
                    ↓
Wallet maj:
  solde_en_attente -= 18 000  → 72 000
  solde_disponible += 18 000  → 18 000  ✅ VENDEUR PEUT RETIRER
                    ↓
Réservation maj:
  montant_en_attente_restant = 72 000  ← Réduit
  montant_avance_debloque = 18 000  ← DÉBLOQUÉ
  statut = PARTIELLEMENT_LIBEREE
                    ↓
Transactions:
  ✓ DEBIT_ATTENTE (-18 000, "Expédition vendeur: déblocage avance 20%")
  ✓ CREDIT_DISPONIBLE (+18 000, "Avance 20% disponible après tracking")
  ✓ NOTIFICATION: "Avance de 18 000 FCFA débloquée"


ÉTAPE 3: Agent vérifie produit (RECU_PAR_AGENT) - QUALITÉ VALIDÉE ✓
┌─────────────────────────────────────────┐
│ Tranche 2: 80% de 90 000 = 72 000 FCFA │
│ PAIEMENT COMPLET                        │
└─────────────────────────────────────────┘
                    ↓
Wallet maj:
  solde_en_attente -= 72 000  → 0
  solde_disponible += 72 000  → 90 000  ✅ COMPLET
                    ↓
Réservation maj:
  montant_en_attente_restant = 0  ← Épuisé
  montant_solde_debloque = 72 000  ← DÉBLOQUÉ
  statut = LIBEREE  ← TERMINAL
                    ↓
Transactions:
  ✓ DEBIT_ATTENTE (-72 000, "Vérification agent: déblocage solde 80%")
  ✓ CREDIT_DISPONIBLE (+72 000, "Solde 80% disponible après vérification")
  ✓ NOTIFICATION: "Solde final de 72 000 FCFA débloqué"
```

---

## 🎯 Statuts et transitions

```
EN_ATTENTE (100% bloqué)
     ↓
     └─→ EXPEDIE_PAR_VENDEUR → PARTIELLEMENT_LIBEREE (20% disponible, 80% attente)
               ↓
               └─→ RECU_PAR_AGENT → LIBEREE (100% disponible)

Alternative:
EN_ATTENTE ↓
           └─→ ANNULEE (remboursé client)
     ou
PARTIELLEMENT_LIBEREE ↓
                      └─→ ANNULEE (cas exceptionnel)
```

---

## 📊 Vues + Endpoints

### **1. GET `/vendeur/wallet` - Mon wallet (vue vendeur)**

```json
{
  "wallet": {
    "solde_disponible_cfa": 150000, // Peut retirer
    "solde_en_attente_cfa": 180000, // Attend tranches
    "total_cfa": 330000
  },
  "reservations": [
    {
      "commande_identifiant": "cmd-123",
      "montant_total_net_cfa": 90000,
      "montant_en_attente_restant": 72000,
      "montant_avance_debloque": 18000,
      "montant_solde_debloque": 0,
      "statut": "PARTIELLEMENT_LIBEREE",
      "progression": "20%" // 18/90
    },
    {
      "commande_identifiant": "cmd-456",
      "montant_total_net_cfa": 100000,
      "montant_en_attente_restant": 100000,
      "montant_avance_debloque": 0,
      "montant_solde_debloque": 0,
      "statut": "EN_ATTENTE",
      "progression": "0%"
    }
  ],
  "transactions_recentes": [
    {
      "type": "CREDIT_DISPONIBLE",
      "montant_cfa": 18000,
      "commentaire": "Avance 20% disponible après tracking",
      "date": "2026-03-15T14:32:00Z"
    }
  ]
}
```

---

## 🔐 Règles de sécurité

| Règle                                              | Raison               | Implémentation                                                      |
| -------------------------------------------------- | -------------------- | ------------------------------------------------------------------- |
| **Montant net = Prix brut × (1 - 10% commission)** | Platform prend 10%   | `wallet_service._credit_en_attente_si_absent()`                     |
| **Avance uniquement si tracking valide**           | Prouver l'expédition | `logistique_service.signaler_expedition_vendeur()` → wallet trigger |
| **Solde uniquement si RECU_PAR_AGENT**             | Agent = quality gate | `logistique_service.confirmer_reception_agent()` → wallet trigger   |
| **Pas de double débit/crédit**                     | Idempotence          | `if reservation.montant_avance_debloque_cfa > 0: continue`          |
| **Solde en attente jamais négatif**                | Précision            | `max(0, solde_en_attente - montant)`                                |

---

## 🛠️ Code clé (wallet_service.py)

### **Création/initialisation à la commande payée**

```python
def _credit_en_attente_si_absent(self, commande: Commande):
    """Crée la réservation + crédite solde_en_attente au paiement."""
    for vendeur_id, brut in groupes.items():
        net = brut * 0.90  # 10% commission
        wallet = self._get_or_create_wallet(vendeur_id)
        wallet.solde_en_attente_cfa += net

        reservation = WalletReservationCommande(
            montant_total_net_cfa=net,
            montant_en_attente_restant_cfa=net,
            statut=EN_ATTENTE
        )
```

### **Déblocage avance (20%) à l'expédition**

```python
def _liberer_avance_expedition_vendeur(self, commande_id, reception_id=None):
    """Libère 20% après EXPEDIE_PAR_VENDEUR. Appelé par logistique."""
    for reservation in self.repo.lister_reservations_commande(commande_id):
        avance = int(reservation.montant_total_net_cfa * 0.20)  # 20%
        wallet.solde_en_attente -= avance
        wallet.solde_disponible += avance

        reservation.montant_avance_debloque = avance
        reservation.montant_en_attente_restant -= avance
        reservation.statut = PARTIELLEMENT_LIBEREE

        self._notifier_vendeur_wallet(
            "Avance débloquée",
            f"{avance} FCFA disponible après tracking"
        )
```

### **Déblocage solde (80%) à la vérification agent**

```python
def _liberer_solde_verification_agent(self, commande_id):
    """Libère 80% après RECU_PAR_AGENT. Appelé par logistique."""
    for reservation in self.repo.lister_reservations_commande(commande_id):
        restant = reservation.montant_en_attente_restant
        wallet.solde_en_attente -= restant
        wallet.solde_disponible += restant

        reservation.montant_solde_debloque = restant
        reservation.montant_en_attente_restant = 0
        reservation.statut = LIBEREE

        self._notifier_vendeur_wallet(
            "Solde débloqué",
            f"{restant} FCFA disponible après vérification"
        )
```

---

## 📈 Exemples multiples vendeurs dans 1 commande

**Cas:** Commande contenant articles de 3 vendeurs

```
Commande total: 300 000 FCFA

Articles:
  - Vendeur A: 100 000 FCFA (net: 90 000)
  - Vendeur B: 100 000 FCFA (net: 90 000)
  - Vendeur C: 100 000 FCFA (net: 90 000)
```

**À PAYEE:**

```
Wallet A: solde_en_attente += 90 000
Wallet B: solde_en_attente += 90 000
Wallet C: solde_en_attente += 90 000

Réservation A: montant_total=90k, en_attente=90k
Réservation B: montant_total=90k, en_attente=90k
Réservation C: montant_total=90k, en_attente=90k
```

**À EXPEDIE_PAR_VENDEUR (chacun expédie ses articles indépendamment):**

```
Si Vendeur A expédie:
  Wallet A: en_attente: 90k → 72k, disponible: 0 → 18k
  Réservation A: avance=18k, en_attente=72k

Si Vendeur B NE FAIT RIEN:
  Wallet B: en_attente: 90k (inchangé)
  Réservation B: EN_ATTENTE (inchangé)

Si Vendeur C expédie:
  Wallet C: en_attente: 90k → 72k, disponible: 0 → 18k
  Réservation C: avance=18k, en_attente=72k
```

---

## 🚀 Points clés du design V2

✅ **Verify-then-pay** : Agent logistique est le quality gate (pas de paiement sans vérification)  
✅ **Tranches progressives** : Revenu additionnel vendeur dès l'expédition (20%), pas d'attente complète  
✅ **Plateforme protégée** : Fonds gelés jusqu'à preuve de qualité (80% en sécurité)  
✅ **Audit trail** : Toutes les transactions sont loggées  
✅ **Notifications en temps réel** : Vendeur sait exactement quand l'argent est disponible  
✅ **Pas de charge service** : Wallet est purement de tracking, pas de frais additionnels

---

## 🔗 Configuration (PAIEMENT_VENDEURS/config.py)

```python
commission_percent: float = 0.10  # 10% commission plateforme

# Modèle partiel V2 : avance à l'expédition (20%), solde à la vérification (80%)
avance_percent_expedition_vendeur: float = 0.20  # 20% after shipment
solde_percent_verification_agent: float = 0.80   # 80% after verification
```

---

## 📞 Questions fréquentes

**Q: Quand le vendeur peut-il retirer l'argent ?**
A: Immédiatement après déverrouillage (20% + 80%). Pas de délai supplémentaire après déblocage.

**Q: Que se passe-t-il si l'agent signale un problème ?**
A: Le dossier passe à PROBLEME_RECEPTION. L'argent reste bloqué. L'admin intervient.

**Q: La commission (10%) s'applique-t-elle avant ou après les tranches ?**
A: La commission s'applique d'abord. Les % (20/80) s'appliquent au montant net.

**Q: Peut-on modifier les % 20/80 après lancement ?**
A: Oui, dans config.py. Les nouvelles commandes utilisent les nouveaux %. Les anciennes conservent leurs paramètres.

**Q: Support multi-devise ?**
A: Actuellement XOF (FCFA) uniquement. Peut être étendu via devise parameter dans config.
