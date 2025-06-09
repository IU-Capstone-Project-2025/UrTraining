import React from 'react';
import './App.css'

const App: React.FC = () => {
  return (
    <div style={styles.container}>
      <h1 style={styles.message}>We are in progress...</h1>
    </div>
  );
};

const styles: Record<string, React.CSSProperties> = {
  container: {
    height: '100vh',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    background: '#fff',
  },
  message: {
    fontSize: '2.5rem',
    lineHeight: 12,
    fontWeight: '700',
    letterSpacing: '0.1em',
    background: 'linear-gradient(135deg, #667eea, #764ba2)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    backgroundClip: 'text',
    color: 'transparent',
    animation: 'fadeInOut 3s ease-in-out infinite',
  },
};

export default App;


