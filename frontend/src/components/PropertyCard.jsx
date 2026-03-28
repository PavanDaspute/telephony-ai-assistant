/**
 * PropertyCard.jsx
 * Displays a single property listing in a premium dark glass-morphism card.
 */

import React from 'react'

/* ─── Inline styles (scoped via unique class names) ─────────────────────────── */
const styles = {
  card: {
    background: 'linear-gradient(135deg, #1a1d27 0%, #242838 100%)',
    border: '1px solid rgba(255,255,255,0.08)',
    borderRadius: '20px',
    padding: '28px',
    boxShadow: '0 4px 24px rgba(0,0,0,0.4)',
    transition: 'transform 0.22s cubic-bezier(0.4,0,0.2,1), box-shadow 0.22s cubic-bezier(0.4,0,0.2,1)',
    cursor: 'default',
    animation: 'fadeInUp 0.5s ease both',
    display: 'flex',
    flexDirection: 'column',
    gap: '16px',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    gap: '12px',
  },
  title: {
    fontSize: '1.15rem',
    fontWeight: 600,
    color: '#f1f5f9',
    lineHeight: 1.3,
  },
  badge: {
    background: 'rgba(108,99,255,0.18)',
    color: '#8b84ff',
    border: '1px solid rgba(108,99,255,0.35)',
    borderRadius: '99px',
    padding: '4px 12px',
    fontSize: '0.72rem',
    fontWeight: 600,
    whiteSpace: 'nowrap',
    letterSpacing: '0.04em',
    textTransform: 'uppercase',
  },
  locationRow: {
    display: 'flex',
    alignItems: 'center',
    gap: '6px',
    color: '#94a3b8',
    fontSize: '0.88rem',
  },
  divider: {
    height: '1px',
    background: 'rgba(255,255,255,0.06)',
  },
  statsGrid: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '12px',
  },
  statBox: {
    background: 'rgba(255,255,255,0.04)',
    borderRadius: '12px',
    padding: '12px 14px',
  },
  statLabel: {
    fontSize: '0.7rem',
    color: '#64748b',
    textTransform: 'uppercase',
    letterSpacing: '0.08em',
    marginBottom: '4px',
  },
  statValue: {
    fontSize: '1rem',
    fontWeight: 600,
    color: '#f1f5f9',
  },
  amenitiesWrap: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '6px',
  },
  amenityTag: {
    background: 'rgba(34,197,94,0.1)',
    color: '#4ade80',
    border: '1px solid rgba(34,197,94,0.2)',
    borderRadius: '99px',
    padding: '3px 10px',
    fontSize: '0.72rem',
    fontWeight: 500,
  },
  price: {
    fontSize: '1.4rem',
    fontWeight: 700,
    background: 'linear-gradient(90deg, #6c63ff, #a78bfa)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
  },
}

export default function PropertyCard({ property }) {
  const {
    title,
    location,
    price,
    price_in_lakhs,
    carpet_area,
    bedrooms,
    amenities = [],
    description,
  } = property

  return (
    <div
      style={styles.card}
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = 'translateY(-4px)'
        e.currentTarget.style.boxShadow = '0 12px 40px rgba(108,99,255,0.25)'
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = 'translateY(0)'
        e.currentTarget.style.boxShadow = '0 4px 24px rgba(0,0,0,0.4)'
      }}
    >
      {/* Header */}
      <div style={styles.header}>
        <h2 style={styles.title}>{title}</h2>
        <span style={styles.badge}>{bedrooms} BHK</span>
      </div>

      {/* Location */}
      <div style={styles.locationRow}>
        <span>📍</span>
        <span>{location}</span>
      </div>

      <div style={styles.divider} />

      {/* Stats */}
      <div style={styles.statsGrid}>
        <div style={styles.statBox}>
          <div style={styles.statLabel}>Price</div>
          <div style={styles.price}>₹{price_in_lakhs}</div>
        </div>
        <div style={styles.statBox}>
          <div style={styles.statLabel}>Carpet Area</div>
          <div style={styles.statValue}>{carpet_area} sq ft</div>
        </div>
      </div>

      {/* Amenities */}
      {amenities.length > 0 && (
        <div>
          <div style={{ ...styles.statLabel, marginBottom: '8px' }}>Amenities</div>
          <div style={styles.amenitiesWrap}>
            {amenities.slice(0, 5).map((a, i) => (
              <span key={i} style={styles.amenityTag}>{a}</span>
            ))}
            {amenities.length > 5 && (
              <span style={styles.amenityTag}>+{amenities.length - 5} more</span>
            )}
          </div>
        </div>
      )}

      {/* Description */}
      {description && (
        <p style={{ color: '#64748b', fontSize: '0.83rem', lineHeight: 1.6 }}>
          {description.length > 120 ? description.slice(0, 120) + '…' : description}
        </p>
      )}
    </div>
  )
}
