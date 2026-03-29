/**
 * Home.jsx
 * Landing page — hero section explaining the voice assistant + property listings.
 */

import React from 'react'
import PropertyList from '../components/PropertyList'
import VoiceCall from '../components/VoiceCall'

const styles = {
  page: {
    minHeight: '100vh',
    background: 'linear-gradient(160deg, #0f1117 0%, #131622 60%, #0d1020 100%)',
    padding: '0 0 80px',
  },

  hero: {
    maxWidth: '860px',
    margin: '0 auto',
    padding: '80px 24px 48px',
    textAlign: 'center',
  },

  heroTag: {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '8px',
    background: 'rgba(108,99,255,0.12)',
    border: '1px solid rgba(108,99,255,0.3)',
    borderRadius: '99px',
    padding: '6px 18px',
    fontSize: '0.78rem',
    fontWeight: 600,
    color: '#a78bfa',
    letterSpacing: '0.06em',
    textTransform: 'uppercase',
    marginBottom: '24px',
  },

  heroTitle: {
    fontSize: 'clamp(2rem, 5vw, 3.2rem)',
    fontWeight: 700,
    lineHeight: 1.18,
    marginBottom: '18px',
    background: 'linear-gradient(135deg, #f1f5f9 30%, #a78bfa 100%)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
  },

  heroSub: {
    color: '#94a3b8',
    fontSize: '1.05rem',
    lineHeight: 1.7,
    maxWidth: '560px',
    margin: '0 auto 40px',
  },

  infoBanner: {
    display: 'flex',
    justifyContent: 'center',
    gap: '16px',
    flexWrap: 'wrap',
    marginBottom: '16px',
  },

  infoChip: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    background: 'rgba(255,255,255,0.04)',
    border: '1px solid rgba(255,255,255,0.08)',
    borderRadius: '99px',
    padding: '8px 18px',
    fontSize: '0.83rem',
    color: '#94a3b8',
  },

  sectionWrap: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '0 24px',
  },

  sectionTitle: {
    fontSize: '1.5rem',
    fontWeight: 700,
    color: '#f1f5f9',
    marginBottom: '8px',
  },

  sectionSub: {
    color: '#64748b',
    fontSize: '0.88rem',
    marginBottom: '32px',
  },

  divider: {
    height: '1px',
    background: 'linear-gradient(90deg, transparent, rgba(108,99,255,0.3), transparent)',
    margin: '0 auto 64px',
    maxWidth: '600px',
  },
}

export default function Home() {
  return (
    <div style={styles.page}>
      {/* ── Hero ─────────────────────────────────────── */}
      <header style={styles.hero}>
        <div style={styles.heroTag}>
          <span>🎙️</span>
          <span>AI Voice Telephony Assistant</span>
        </div>

        <h1 style={styles.heroTitle}>
          Find Your Perfect Property<br />— Just Ask
        </h1>

        <p style={styles.heroSub}>
          Call our dedicated number and ask anything about price, location, area, or
          amenities. Our AI assistant answers instantly using live data.
        </p>

        <div style={styles.infoBanner}>
          {[
            { icon: '📞', label: 'Twilio Voice Integration' },
            { icon: '🧠', label: 'Intent-Driven AI' },
            { icon: '🏠', label: 'Live DB Answers' },
            { icon: '🗣️', label: 'Indian English TTS' },
          ].map(({ icon, label }) => (
            <div key={label} style={styles.infoChip}>
              <span>{icon}</span>
              <span>{label}</span>
            </div>
          ))}
        </div>
      </header>

      <VoiceCall />

      <div style={styles.divider} />

      {/* ── Listings ─────────────────────────────────── */}
      <main style={styles.sectionWrap}>
        <h2 style={styles.sectionTitle}>Available Properties</h2>
        <p style={styles.sectionSub}>Browse all listings — or call to ask our AI agent.</p>
        <PropertyList />
      </main>
    </div>
  )
}
