-- ============================================
-- INSERTIONS COMPTES TEST YOK MARKETPLACE
-- ============================================
-- Extension requise pour le hachage
CREATE EXTENSION IF NOT EXISTS pgcrypto;
-- ============ COMPTE ADMINISTRATEUR ============
-- Email: admin@yok.com
-- Mot de passe: AdminPassword123
INSERT INTO utilisateurs (
        identifiant,
        role,
        nom_complet,
        telephone,
        courriel,
        mot_de_passe_hash,
        oauth_provider,
        oauth_id,
        photo_url,
        est_actif
    )
VALUES (
        gen_random_uuid(),
        'ADMINISTRATEUR',
        'Administrateur YOK',
        '+237690000001',
        'admin@yok.com',
        crypt('AdminPassword123', gen_salt('bf', 12)),
        NULL,
        NULL,
        NULL,
        TRUE
    ) ON CONFLICT (courriel) DO NOTHING;
-- ============ COMPTE VENDEUR 1 ============
-- Email: vendeur1@yok.com
-- Mot de passe: VendeurPass123
INSERT INTO utilisateurs (
        identifiant,
        role,
        nom_complet,
        telephone,
        courriel,
        mot_de_passe_hash,
        oauth_provider,
        oauth_id,
        photo_url,
        est_actif
    )
VALUES (
        gen_random_uuid(),
        'VENDEUR',
        'Jean Dupont',
        '+237690000002',
        'vendeur1@yok.com',
        crypt('VendeurPass123', gen_salt('bf', 12)),
        NULL,
        NULL,
        NULL,
        TRUE
    ) ON CONFLICT (courriel) DO NOTHING;
-- Profil vendeur associé
INSERT INTO profils_vendeurs (
        utilisateur_identifiant,
        nom_entreprise,
        nom_contact,
        pays,
        statut_kyc
    )
VALUES (
        (
            SELECT identifiant
            FROM utilisateurs
            WHERE courriel = 'vendeur1@yok.com'
        ),
        'Boutique Tech Pro',
        'Jean Dupont',
        'Cameroun',
        'VALIDEE'
    ) ON CONFLICT (utilisateur_identifiant) DO NOTHING;
-- ============ COMPTE VENDEUR 2 ============
-- Email: vendeur2@yok.com
-- Mot de passe: VendeurPass456
INSERT INTO utilisateurs (
        identifiant,
        role,
        nom_complet,
        telephone,
        courriel,
        mot_de_passe_hash,
        oauth_provider,
        oauth_id,
        photo_url,
        est_actif
    )
VALUES (
        gen_random_uuid(),
        'VENDEUR',
        'Marie Martin',
        '+237690000003',
        'vendeur2@yok.com',
        crypt('VendeurPass456', gen_salt('bf', 12)),
        NULL,
        NULL,
        NULL,
        TRUE
    ) ON CONFLICT (courriel) DO NOTHING;
-- Profil vendeur associé
INSERT INTO profils_vendeurs (
        utilisateur_identifiant,
        nom_entreprise,
        nom_contact,
        pays,
        statut_kyc
    )
VALUES (
        (
            SELECT identifiant
            FROM utilisateurs
            WHERE courriel = 'vendeur2@yok.com'
        ),
        'Fashion Store Africa',
        'Marie Martin',
        'Cameroun',
        'VALIDEE'
    ) ON CONFLICT (utilisateur_identifiant) DO NOTHING;
-- ============================================
-- RÉSUMÉ DES COMPTES DE TEST
-- ============================================
/*
 ADMINISTRATEUR:
 - Email: admin@yok.com
 - Mot de passe: AdminPassword123
 - Accès: panneau admin complet
 
 VENDEUR 1:
 - Email: vendeur1@yok.com
 - Mot de passe: VendeurPass123
 - Boutique: Boutique Tech Pro
 - Statut KYC: VALIDEE
 
 VENDEUR 2:
 - Email: vendeur2@yok.com
 - Mot de passe: VendeurPass456
 - Boutique: Fashion Store Africa
 - Statut KYC: VALIDEE
 
 CLIENTS:
 - Utilisent OAuth uniquement (Google/Facebook)
 - Pas de compte avec mot de passe
 */