-- ============================================
-- BASE YOK (MARKETPLACE) - SIMPLE & PROPRE
-- PostgreSQL
-- ============================================
-- UUID
CREATE EXTENSION IF NOT EXISTS pgcrypto;
-- ============ ENUMS ============
DO $$ BEGIN CREATE TYPE role_utilisateur AS ENUM ('CLIENT', 'VENDEUR', 'ADMINISTRATEUR');
EXCEPTION
WHEN duplicate_object THEN NULL;
END $$;
DO $$ BEGIN CREATE TYPE statut_kyc AS ENUM (
  'EN_ATTENTE',
  'VALIDEE',
  'REJETEE',
  'EN_REVISION'
);
EXCEPTION
WHEN duplicate_object THEN NULL;
END $$;
DO $$ BEGIN CREATE TYPE statut_commande AS ENUM (
  'EN_ATTENTE_PAIEMENT',
  'PAYEE',
  'EN_PREPARATION',
  'EXPEDIEE',
  'LIVREE',
  'ANNULEE',
  'REMBOURSEE'
);
EXCEPTION
WHEN duplicate_object THEN NULL;
END $$;
-- ============ UTILISATEURS ============
CREATE TABLE IF NOT EXISTS utilisateurs (
  identifiant UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  role role_utilisateur NOT NULL,
  nom_complet TEXT NOT NULL,
  telephone TEXT UNIQUE,
  courriel TEXT UNIQUE NOT NULL,
  mot_de_passe_hash TEXT,
  oauth_provider TEXT,
  oauth_id TEXT UNIQUE,
  photo_url TEXT,
  est_actif BOOLEAN DEFAULT TRUE,
  date_creation TIMESTAMPTZ DEFAULT NOW(),
  CONSTRAINT check_auth_method CHECK (
    (
      mot_de_passe_hash IS NOT NULL
      AND oauth_provider IS NULL
    )
    OR (
      mot_de_passe_hash IS NULL
      AND oauth_provider IS NOT NULL
    )
  )
);
CREATE INDEX IF NOT EXISTS idx_utilisateurs_courriel ON utilisateurs(courriel);
CREATE INDEX IF NOT EXISTS idx_utilisateurs_role ON utilisateurs(role);
CREATE INDEX IF NOT EXISTS idx_utilisateurs_oauth ON utilisateurs(oauth_provider, oauth_id);
-- ============ ADRESSES ============
CREATE TABLE IF NOT EXISTS adresses (
  identifiant UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  utilisateur_identifiant UUID NOT NULL REFERENCES utilisateurs(identifiant) ON DELETE CASCADE,
  ville TEXT NOT NULL,
  quartier TEXT,
  adresse_complete TEXT NOT NULL,
  telephone TEXT,
  par_defaut BOOLEAN DEFAULT FALSE,
  date_creation TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_adresses_utilisateur ON adresses(utilisateur_identifiant);
-- ============ PROFIL VENDEUR (KYC) ============
CREATE TABLE IF NOT EXISTS profils_vendeurs (
  utilisateur_identifiant UUID PRIMARY KEY REFERENCES utilisateurs(identifiant) ON DELETE CASCADE,
  nom_entreprise TEXT NOT NULL,
  nom_contact TEXT,
  pays TEXT DEFAULT 'Chine',
  statut_kyc statut_kyc DEFAULT 'EN_ATTENTE',
  date_creation TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_profils_vendeurs_kyc ON profils_vendeurs(statut_kyc);
-- ============ CATEGORIES ============
CREATE TABLE IF NOT EXISTS categories (
  identifiant UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  nom TEXT NOT NULL UNIQUE,
  parent_identifiant UUID REFERENCES categories(identifiant) ON DELETE
  SET NULL,
    description TEXT,
    est_actif BOOLEAN DEFAULT TRUE,
    date_creation TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_categories_nom ON categories(nom);
CREATE INDEX IF NOT EXISTS idx_categories_parent ON categories(parent_identifiant);
-- ============ PRODUITS ============
CREATE TABLE IF NOT EXISTS produits (
  identifiant UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  vendeur_identifiant UUID NOT NULL REFERENCES utilisateurs(identifiant) ON DELETE CASCADE,
  categorie_identifiant UUID NOT NULL REFERENCES categories(identifiant),
  nom TEXT NOT NULL,
  description TEXT,
  prix_cfa INTEGER NOT NULL CHECK (prix_cfa > 0),
  stock INTEGER DEFAULT 0 CHECK (stock >= 0),
  tailles TEXT [] DEFAULT '{}',
  couleurs TEXT [] DEFAULT '{}',
  est_actif BOOLEAN DEFAULT TRUE,
  date_creation TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_produits_vendeur ON produits(vendeur_identifiant);
CREATE INDEX IF NOT EXISTS idx_produits_categorie ON produits(categorie_identifiant);
CREATE INDEX IF NOT EXISTS idx_produits_nom ON produits(nom);
-- Images produits
CREATE TABLE IF NOT EXISTS images_produits (
  identifiant UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  produit_identifiant UUID NOT NULL REFERENCES produits(identifiant) ON DELETE CASCADE,
  url_image TEXT NOT NULL,
  couleur TEXT,
  position INTEGER DEFAULT 0,
  date_creation TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_images_produits_produit ON images_produits(produit_identifiant);
CREATE INDEX IF NOT EXISTS idx_images_produits_couleur ON images_produits(couleur);
-- Vidéos produits
CREATE TABLE IF NOT EXISTS videos_produits (
  identifiant UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  produit_identifiant UUID NOT NULL REFERENCES produits(identifiant) ON DELETE CASCADE,
  url_video TEXT NOT NULL,
  position INTEGER DEFAULT 0,
  date_creation TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_videos_produits_produit ON videos_produits(produit_identifiant);
-- ============ PANIERS ============
CREATE TABLE IF NOT EXISTS paniers (
  identifiant UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  utilisateur_identifiant UUID UNIQUE NOT NULL REFERENCES utilisateurs(identifiant) ON DELETE CASCADE,
  date_mise_a_jour TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_paniers_utilisateur ON paniers(utilisateur_identifiant);
CREATE TABLE IF NOT EXISTS panier_articles (
  identifiant UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  panier_identifiant UUID NOT NULL REFERENCES paniers(identifiant) ON DELETE CASCADE,
  produit_identifiant UUID NOT NULL REFERENCES produits(identifiant) ON DELETE CASCADE,
  quantite INTEGER NOT NULL CHECK (quantite > 0),
  date_creation TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE (panier_identifiant, produit_identifiant)
);
CREATE INDEX IF NOT EXISTS idx_panier_articles_panier ON panier_articles(panier_identifiant);
CREATE INDEX IF NOT EXISTS idx_panier_articles_produit ON panier_articles(produit_identifiant);
-- ============ COMMANDES ============
CREATE TABLE IF NOT EXISTS commandes (
  identifiant UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  client_identifiant UUID NOT NULL REFERENCES utilisateurs(identifiant) ON DELETE CASCADE,
  adresse_identifiant UUID NOT NULL REFERENCES adresses(identifiant),
  statut statut_commande DEFAULT 'EN_ATTENTE_PAIEMENT',
  total_cfa INTEGER DEFAULT 0 CHECK (total_cfa >= 0),
  remarques TEXT,
  date_creation TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_commandes_client ON commandes(client_identifiant);
CREATE INDEX IF NOT EXISTS idx_commandes_statut ON commandes(statut);
-- Lignes de commande (important pour multi-vendeur)
CREATE TABLE IF NOT EXISTS commande_articles (
  identifiant UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  commande_identifiant UUID NOT NULL REFERENCES commandes(identifiant) ON DELETE CASCADE,
  produit_identifiant UUID NOT NULL REFERENCES produits(identifiant),
  vendeur_identifiant UUID NOT NULL REFERENCES utilisateurs(identifiant),
  prix_unitaire_cfa INTEGER NOT NULL CHECK (prix_unitaire_cfa > 0),
  quantite INTEGER NOT NULL CHECK (quantite > 0),
  total_ligne_cfa INTEGER NOT NULL CHECK (total_ligne_cfa >= 0),
  statut statut_commande DEFAULT 'EN_ATTENTE_PAIEMENT',
  date_creation TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_commande_articles_commande ON commande_articles(commande_identifiant);
CREATE INDEX IF NOT EXISTS idx_commande_articles_vendeur ON commande_articles(vendeur_identifiant);
-- ============ AVIS ============
CREATE TABLE IF NOT EXISTS avis (
  identifiant UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  produit_identifiant UUID NOT NULL REFERENCES produits(identifiant) ON DELETE CASCADE,
  client_identifiant UUID NOT NULL REFERENCES utilisateurs(identifiant) ON DELETE CASCADE,
  note INTEGER NOT NULL CHECK (
    note BETWEEN 1 AND 5
  ),
  titre TEXT,
  commentaire TEXT,
  date_creation TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE (produit_identifiant, client_identifiant)
);
CREATE INDEX IF NOT EXISTS idx_avis_produit ON avis(produit_identifiant);
CREATE INDEX IF NOT EXISTS idx_avis_client ON avis(client_identifiant);
-- Photos d'avis (le client peut prouver ce qu’il a reçu)
CREATE TABLE IF NOT EXISTS images_avis (
  identifiant UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  avis_identifiant UUID NOT NULL REFERENCES avis(identifiant) ON DELETE CASCADE,
  url_image TEXT NOT NULL,
  position INTEGER DEFAULT 0,
  date_creation TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_images_avis_avis ON images_avis(avis_identifiant);
-- ============ FAVORIS ============
CREATE TABLE IF NOT EXISTS favoris (
  identifiant UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  utilisateur_identifiant UUID NOT NULL REFERENCES utilisateurs(identifiant) ON DELETE CASCADE,
  produit_identifiant UUID NOT NULL REFERENCES produits(identifiant) ON DELETE CASCADE,
  date_creation TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE (utilisateur_identifiant, produit_identifiant)
);
CREATE INDEX IF NOT EXISTS idx_favoris_utilisateur ON favoris(utilisateur_identifiant);
CREATE INDEX IF NOT EXISTS idx_favoris_produit ON favoris(produit_identifiant);
-- ============ FACTURES ============
DO $$ BEGIN CREATE TYPE statut_facture_paiement AS ENUM (
  'EN_ATTENTE',
  'PAYEE',
  'ECHOUE',
  'REMBOURSEE'
);
EXCEPTION
WHEN duplicate_object THEN NULL;
END $$;
CREATE TABLE IF NOT EXISTS factures (
  identifiant UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  numero_facture TEXT NOT NULL UNIQUE,
  commande_identifiant UUID NOT NULL UNIQUE REFERENCES commandes(identifiant) ON DELETE CASCADE,
  client_identifiant UUID NOT NULL REFERENCES utilisateurs(identifiant) ON DELETE CASCADE,
  montant_total_cfa INTEGER NOT NULL CHECK (montant_total_cfa >= 0),
  statut_paiement statut_facture_paiement NOT NULL DEFAULT 'EN_ATTENTE',
  mode_paiement TEXT,
  reference_paiement TEXT,
  date_emission TIMESTAMPTZ DEFAULT NOW(),
  date_paiement TIMESTAMPTZ,
  notes TEXT
);
CREATE INDEX IF NOT EXISTS idx_factures_client ON factures(client_identifiant);
CREATE INDEX IF NOT EXISTS idx_factures_statut ON factures(statut_paiement);
CREATE INDEX IF NOT EXISTS idx_factures_commande ON factures(commande_identifiant);
CREATE TABLE IF NOT EXISTS facture_paiement_suivis (
  identifiant UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  facture_identifiant UUID NOT NULL REFERENCES factures(identifiant) ON DELETE CASCADE,
  ancien_statut statut_facture_paiement,
  nouveau_statut statut_facture_paiement NOT NULL,
  commentaire TEXT,
  acteur_identifiant UUID REFERENCES utilisateurs(identifiant),
  date_evenement TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_facture_suivis_facture ON facture_paiement_suivis(facture_identifiant);
CREATE INDEX IF NOT EXISTS idx_facture_suivis_date ON facture_paiement_suivis(date_evenement);
-- ============ PAIEMENTS ============
DO $$ BEGIN CREATE TYPE fournisseur_paiement AS ENUM ('CINETPAY');
EXCEPTION
WHEN duplicate_object THEN NULL;
END $$;
DO $$ BEGIN CREATE TYPE statut_paiement_transaction AS ENUM (
  'EN_ATTENTE',
  'EN_COURS',
  'PAYEE',
  'ECHOUE',
  'ANNULEE'
);
EXCEPTION
WHEN duplicate_object THEN NULL;
END $$;
CREATE TABLE IF NOT EXISTS paiements (
  identifiant UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  commande_identifiant UUID NOT NULL UNIQUE REFERENCES commandes(identifiant) ON DELETE CASCADE,
  utilisateur_identifiant UUID NOT NULL REFERENCES utilisateurs(identifiant) ON DELETE CASCADE,
  montant_cfa INTEGER NOT NULL CHECK (montant_cfa >= 0),
  devise TEXT NOT NULL DEFAULT 'XOF',
  fournisseur fournisseur_paiement NOT NULL DEFAULT 'CINETPAY',
  statut statut_paiement_transaction NOT NULL DEFAULT 'EN_ATTENTE',
  provider_transaction_id TEXT UNIQUE,
  provider_payment_url TEXT,
  methode TEXT,
  description TEXT,
  payload_initialisation JSONB,
  payload_webhook JSONB,
  date_confirmation TIMESTAMPTZ,
  date_creation TIMESTAMPTZ DEFAULT NOW(),
  date_mise_a_jour TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_paiements_commande ON paiements(commande_identifiant);
CREATE INDEX IF NOT EXISTS idx_paiements_utilisateur ON paiements(utilisateur_identifiant);
CREATE INDEX IF NOT EXISTS idx_paiements_statut ON paiements(statut);
CREATE INDEX IF NOT EXISTS idx_paiements_provider_tx ON paiements(provider_transaction_id);
CREATE TABLE IF NOT EXISTS paiement_evenements (
  identifiant UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  paiement_identifiant UUID NOT NULL REFERENCES paiements(identifiant) ON DELETE CASCADE,
  type_evenement TEXT NOT NULL,
  source TEXT NOT NULL,
  ancien_statut statut_paiement_transaction,
  nouveau_statut statut_paiement_transaction NOT NULL,
  payload JSONB,
  commentaire TEXT,
  date_evenement TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_paiement_evenements_paiement ON paiement_evenements(paiement_identifiant);
CREATE INDEX IF NOT EXISTS idx_paiement_evenements_date ON paiement_evenements(date_evenement DESC);
-- ============ PAIEMENT VENDEURS (WALLET LEDGER) ============
DO $$ BEGIN CREATE TYPE type_transaction_wallet AS ENUM (
  'CREDIT_ATTENTE',
  'DEBIT_ATTENTE',
  'CREDIT_DISPONIBLE',
  'PAIEMENT_EFFECTUE'
);
EXCEPTION
WHEN duplicate_object THEN NULL;
END $$;
DO $$ BEGIN CREATE TYPE statut_reservation_wallet AS ENUM (
  'EN_ATTENTE',
  'PARTIELLEMENT_LIBEREE',
  'LIBEREE',
  'ANNULEE'
);
EXCEPTION
WHEN duplicate_object THEN NULL;
END $$;
CREATE TABLE IF NOT EXISTS wallet_vendeurs (
  vendeur_identifiant UUID PRIMARY KEY REFERENCES utilisateurs(identifiant) ON DELETE CASCADE,
  solde_disponible_cfa INTEGER NOT NULL DEFAULT 0 CHECK (solde_disponible_cfa >= 0),
  solde_en_attente_cfa INTEGER NOT NULL DEFAULT 0 CHECK (solde_en_attente_cfa >= 0),
  date_creation TIMESTAMPTZ DEFAULT NOW(),
  date_mise_a_jour TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS wallet_reservations_commandes (
  identifiant UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  vendeur_identifiant UUID NOT NULL REFERENCES utilisateurs(identifiant) ON DELETE CASCADE,
  commande_identifiant UUID NOT NULL REFERENCES commandes(identifiant) ON DELETE CASCADE,
  montant_total_net_cfa INTEGER NOT NULL CHECK (montant_total_net_cfa >= 0),
  montant_en_attente_restant_cfa INTEGER NOT NULL CHECK (montant_en_attente_restant_cfa >= 0),
  montant_avance_debloque_cfa INTEGER NOT NULL DEFAULT 0 CHECK (montant_avance_debloque_cfa >= 0),
  montant_solde_debloque_cfa INTEGER NOT NULL DEFAULT 0 CHECK (montant_solde_debloque_cfa >= 0),
  statut statut_reservation_wallet NOT NULL DEFAULT 'EN_ATTENTE',
  date_creation TIMESTAMPTZ DEFAULT NOW(),
  date_mise_a_jour TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE (vendeur_identifiant, commande_identifiant)
);
CREATE INDEX IF NOT EXISTS idx_wallet_reservations_commande ON wallet_reservations_commandes(commande_identifiant);
CREATE INDEX IF NOT EXISTS idx_wallet_reservations_vendeur ON wallet_reservations_commandes(vendeur_identifiant);
CREATE INDEX IF NOT EXISTS idx_wallet_reservations_statut ON wallet_reservations_commandes(statut);
CREATE TABLE IF NOT EXISTS transactions_wallet (
  identifiant UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  vendeur_identifiant UUID NOT NULL REFERENCES utilisateurs(identifiant) ON DELETE CASCADE,
  commande_identifiant UUID REFERENCES commandes(identifiant) ON DELETE
  SET NULL,
    type type_transaction_wallet NOT NULL,
    montant_cfa INTEGER NOT NULL CHECK (montant_cfa >= 0),
    commentaire TEXT,
    date_creation TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_transactions_wallet_vendeur ON transactions_wallet(vendeur_identifiant);
CREATE INDEX IF NOT EXISTS idx_transactions_wallet_commande ON transactions_wallet(commande_identifiant);
CREATE INDEX IF NOT EXISTS idx_transactions_wallet_type ON transactions_wallet(type);
CREATE INDEX IF NOT EXISTS idx_transactions_wallet_date ON transactions_wallet(date_creation DESC);
-- ============ LIVRAISONS ============
DO $$ BEGIN CREATE TYPE statut_livraison AS ENUM (
  'CREEE',
  'ASSIGNEE',
  'EN_TRANSIT',
  'ARRIVEE_ENTREPOT_ABIDJAN',
  'LIVREE_CLIENT',
  'ANNULEE'
);
EXCEPTION
WHEN duplicate_object THEN NULL;
END $$;
DO $$ BEGIN ALTER TYPE statut_livraison
ADD VALUE IF NOT EXISTS 'ASSIGNEE';
EXCEPTION
WHEN duplicate_object THEN NULL;
END $$;
DO $$ BEGIN ALTER TYPE statut_livraison
ADD VALUE IF NOT EXISTS 'ARRIVEE_ENTREPOT_ABIDJAN';
EXCEPTION
WHEN duplicate_object THEN NULL;
END $$;
CREATE TABLE IF NOT EXISTS livraisons (
  identifiant UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  commande_identifiant UUID NOT NULL UNIQUE REFERENCES commandes(identifiant) ON DELETE CASCADE,
  statut statut_livraison NOT NULL DEFAULT 'CREEE',
  livreur_nom TEXT,
  livreur_telephone TEXT,
  preuve_livraison_url TEXT,
  commentaire TEXT,
  date_creation TIMESTAMPTZ DEFAULT NOW(),
  date_mise_a_jour TIMESTAMPTZ DEFAULT NOW(),
  date_ramassage TIMESTAMPTZ,
  date_verification_entrepot TIMESTAMPTZ,
  date_livraison TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS idx_livraisons_commande ON livraisons(commande_identifiant);
CREATE INDEX IF NOT EXISTS idx_livraisons_statut ON livraisons(statut);
CREATE TABLE IF NOT EXISTS livraison_evenements (
  identifiant UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  livraison_identifiant UUID NOT NULL REFERENCES livraisons(identifiant) ON DELETE CASCADE,
  statut_avant statut_livraison,
  statut_apres statut_livraison NOT NULL,
  acteur_identifiant UUID REFERENCES utilisateurs(identifiant) ON DELETE
  SET NULL,
    commentaire TEXT,
    date_evenement TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_livraison_evenements_livraison ON livraison_evenements(livraison_identifiant);
CREATE INDEX IF NOT EXISTS idx_livraison_evenements_date ON livraison_evenements(date_evenement DESC);
-- ============ RESEAU SOCIAUX ============
DO $$ BEGIN CREATE TYPE statut_moderation_post AS ENUM ('ACTIF', 'MASQUE', 'SUPPRIME');
EXCEPTION
WHEN duplicate_object THEN NULL;
END $$;
DO $$ BEGIN CREATE TYPE statut_moderation_commentaire AS ENUM ('ACTIF', 'MASQUE', 'SUPPRIME');
EXCEPTION
WHEN duplicate_object THEN NULL;
END $$;
CREATE TABLE IF NOT EXISTS reseau_posts (
  identifiant UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  auteur_identifiant UUID NOT NULL REFERENCES utilisateurs(identifiant) ON DELETE CASCADE,
  contenu TEXT NOT NULL,
  statut_moderation statut_moderation_post NOT NULL DEFAULT 'ACTIF',
  date_creation TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_reseau_posts_auteur ON reseau_posts(auteur_identifiant);
CREATE INDEX IF NOT EXISTS idx_reseau_posts_date ON reseau_posts(date_creation DESC);
CREATE TABLE IF NOT EXISTS reseau_post_images (
  identifiant UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  post_identifiant UUID NOT NULL REFERENCES reseau_posts(identifiant) ON DELETE CASCADE,
  url_image TEXT NOT NULL,
  position INTEGER DEFAULT 0,
  date_creation TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_reseau_post_images_post ON reseau_post_images(post_identifiant);
CREATE TABLE IF NOT EXISTS reseau_post_tags_produits (
  identifiant UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  post_identifiant UUID NOT NULL REFERENCES reseau_posts(identifiant) ON DELETE CASCADE,
  produit_identifiant UUID NOT NULL REFERENCES produits(identifiant),
  boutique_identifiant UUID NOT NULL REFERENCES utilisateurs(identifiant),
  UNIQUE (post_identifiant, produit_identifiant)
);
CREATE INDEX IF NOT EXISTS idx_reseau_tags_post ON reseau_post_tags_produits(post_identifiant);
CREATE INDEX IF NOT EXISTS idx_reseau_tags_produit ON reseau_post_tags_produits(produit_identifiant);
CREATE INDEX IF NOT EXISTS idx_reseau_tags_boutique ON reseau_post_tags_produits(boutique_identifiant);
CREATE TABLE IF NOT EXISTS reseau_commentaires (
  identifiant UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  post_identifiant UUID NOT NULL REFERENCES reseau_posts(identifiant) ON DELETE CASCADE,
  auteur_identifiant UUID NOT NULL REFERENCES utilisateurs(identifiant) ON DELETE CASCADE,
  contenu TEXT NOT NULL,
  statut_moderation statut_moderation_commentaire NOT NULL DEFAULT 'ACTIF',
  date_creation TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_reseau_commentaires_post ON reseau_commentaires(post_identifiant);
CREATE INDEX IF NOT EXISTS idx_reseau_commentaires_auteur ON reseau_commentaires(auteur_identifiant);
CREATE INDEX IF NOT EXISTS idx_reseau_commentaires_statut ON reseau_commentaires(statut_moderation);
CREATE TABLE IF NOT EXISTS reseau_commentaire_likes (
  identifiant UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  commentaire_identifiant UUID NOT NULL REFERENCES reseau_commentaires(identifiant) ON DELETE CASCADE,
  utilisateur_identifiant UUID NOT NULL REFERENCES utilisateurs(identifiant) ON DELETE CASCADE,
  date_creation TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE (commentaire_identifiant, utilisateur_identifiant)
);
CREATE INDEX IF NOT EXISTS idx_reseau_commentaire_likes_commentaire ON reseau_commentaire_likes(commentaire_identifiant);
CREATE INDEX IF NOT EXISTS idx_reseau_commentaire_likes_utilisateur ON reseau_commentaire_likes(utilisateur_identifiant);
CREATE TABLE IF NOT EXISTS reseau_likes (
  identifiant UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  post_identifiant UUID NOT NULL REFERENCES reseau_posts(identifiant) ON DELETE CASCADE,
  utilisateur_identifiant UUID NOT NULL REFERENCES utilisateurs(identifiant) ON DELETE CASCADE,
  date_creation TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE (post_identifiant, utilisateur_identifiant)
);
CREATE INDEX IF NOT EXISTS idx_reseau_likes_post ON reseau_likes(post_identifiant);
CREATE INDEX IF NOT EXISTS idx_reseau_likes_utilisateur ON reseau_likes(utilisateur_identifiant);
CREATE TABLE IF NOT EXISTS reseau_partages (
  identifiant UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  post_identifiant UUID NOT NULL REFERENCES reseau_posts(identifiant) ON DELETE CASCADE,
  utilisateur_identifiant UUID NOT NULL REFERENCES utilisateurs(identifiant) ON DELETE CASCADE,
  plateforme TEXT,
  date_creation TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_reseau_partages_post ON reseau_partages(post_identifiant);
CREATE INDEX IF NOT EXISTS idx_reseau_partages_utilisateur ON reseau_partages(utilisateur_identifiant);