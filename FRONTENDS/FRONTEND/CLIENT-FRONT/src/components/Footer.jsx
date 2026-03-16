export default function Footer() {
  return (
    <footer style={{
      backgroundColor: '#343a40',
      color: 'white',
      padding: '40px 20px',
      marginTop: '60px'
    }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '30px', marginBottom: '30px' }}>
          <div>
            <h3>À propos de YOK</h3>
            <p>YOK est la marketplace sénégalaise de référence pour acheter et vendre en ligne.</p>
          </div>
          
          <div>
            <h3>Liens utiles</h3>
            <ul style={{ listStyle: 'none', padding: 0 }}>
              <li><a href="#" style={{ color: '#adb5bd', textDecoration: 'none' }}>Nous contacter</a></li>
              <li><a href="#" style={{ color: '#adb5bd', textDecoration: 'none' }}>Conditions d'utilisation</a></li>
              <li><a href="#" style={{ color: '#adb5bd', textDecoration: 'none' }}>Politique de confidentialité</a></li>
            </ul>
          </div>

          <div>
            <h3>Suivez-nous</h3>
            <div style={{ display: 'flex', gap: '10px' }}>
              <a href="#" style={{ color: '#007bff', textDecoration: 'none', fontSize: '20px' }}>f</a>
              <a href="#" style={{ color: '#007bff', textDecoration: 'none', fontSize: '20px' }}>𝕏</a>
              <a href="#" style={{ color: '#007bff', textDecoration: 'none', fontSize: '20px' }}>📷</a>
            </div>
          </div>
        </div>

        <div style={{ borderTop: '1px solid #495057', paddingTop: '20px', textAlign: 'center' }}>
          <p>&copy; 2026 YOK Marketplace. Tous les droits réservés.</p>
        </div>
      </div>
    </footer>
  )
}
