-- ============================================
-- INSERTION CATÉGORIES DE BASE
-- ============================================
-- Catégories principales
INSERT INTO categories (identifiant, nom, description, est_actif)
VALUES (
        gen_random_uuid(),
        'Électronique',
        'Smartphones, ordinateurs, accessoires tech',
        TRUE
    ),
    (
        gen_random_uuid(),
        'Mode',
        'Vêtements, chaussures, accessoires',
        TRUE
    ),
    (
        gen_random_uuid(),
        'Maison',
        'Meubles, décoration, électroménager',
        TRUE
    ),
    (
        gen_random_uuid(),
        'Sport',
        'Équipements sportifs, vêtements de sport',
        TRUE
    ),
    (
        gen_random_uuid(),
        'Beauté',
        'Cosmétiques, parfums, soins',
        TRUE
    ),
    (
        gen_random_uuid(),
        'Alimentation',
        'Produits alimentaires, boissons',
        TRUE
    ),
    (
        gen_random_uuid(),
        'Livres',
        'Livres, magazines, BD',
        TRUE
    ),
    (
        gen_random_uuid(),
        'Jouets',
        'Jouets pour enfants, jeux',
        TRUE
    ) ON CONFLICT (nom) DO NOTHING;
-- Message de confirmation
SELECT 'Catégories insérées avec succès!' as message;
SELECT nom,
    description
FROM categories
WHERE est_actif = TRUE
ORDER BY nom;