/**
 * App.jsx — Root component.
 * Renders the navigation bar and the Home page.
 */

import React from 'react'
import Home from './pages/Home'

const styles = {
  nav: {
    position: 'sticky',
    top: 0,
    zIndex: 100,
    background: 'rgba(15,17,23,0.85)',
    backdropFilter: 'blur(16px)',
    WebkitBackdropFilter: 'blur(16px)',
    borderBottom: '1px solid rgba(255,255,255,0.06)',
    padding: '0 32px',
    height: '60px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
  },

  logo: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    fontWeight: 700,
    fontSize: '1.05rem',
    color: '#f1f5f9',
    textDecoration: 'none',
  },

  logoDot: {
    width: '10px',
    height: '10px',
    borderRadius: '50%',
    background: '#6c63ff',
    boxShadow: '0 0 8px #6c63ff',
    animation: 'pulse-ring 2s ease-in-out infinite',
  },

  navRight: {
    display: 'flex',
    alignItems: 'center',
    gap: '24px',
    fontSize: '0.85rem',
    color: '#64748b',
  },

  statusDot: {
    display: 'flex',
    alignItems: 'center',
    gap: '6px',
  },

  greenDot: {
    width: '7px',
    height: '7px',
    borderRadius: '50%',
    background: '#22c55e',
    boxShadow: '0 0 6px #22c55e',
  },
}

export default function App() {
  return (
    <>
      {/* Navigation bar */}
      <nav style={styles.nav}>
        <a href="/" style={styles.logo}>
          <div style={styles.logoDot} />
          PropertyVoice AI
        </a>
        <div style={styles.navRight}>
          <span style={styles.statusDot}>
            <div style={styles.greenDot} />
            Live
          </span>
          <span>Powered by Twilio + Django</span>
        </div>
      </nav>

      {/* Main content */}
      <Home />
    </>
  )
}
