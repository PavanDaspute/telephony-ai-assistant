/**
 * PropertyList.jsx
 * Fetches all properties from the Django API and renders them in a responsive grid.
 * Includes loading skeleton state, error feedback, and live search filtering.
 */

import React, { useEffect, useState } from 'react'
import { fetchProperties } from '../services/api'
import PropertyCard from './PropertyCard'

const styles = {
  container: { width: '100%' },

  searchBar: {
    width: '100%',
    padding: '14px 20px',
    background: 'rgba(255,255,255,0.05)',
    border: '1px solid rgba(255,255,255,0.1)',
    borderRadius: '99px',
    color: '#f1f5f9',
    fontSize: '0.95rem',
    outline: 'none',
    marginBottom: '32px',
    transition: 'border-color 0.2s, box-shadow 0.2s',
    fontFamily: 'inherit',
  },

  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
    gap: '24px',
  },

  skeleton: {
    background: 'linear-gradient(90deg, #1a1d27 25%, #242838 50%, #1a1d27 75%)',
    backgroundSize: '800px 100%',
    animation: 'shimmer 1.5s infinite',
    borderRadius: '20px',
    height: '320px',
  },

  errorBox: {
    background: 'rgba(239,68,68,0.1)',
    border: '1px solid rgba(239,68,68,0.3)',
    borderRadius: '14px',
    padding: '20px 24px',
    color: '#fca5a5',
    fontSize: '0.9rem',
    textAlign: 'center',
  },

  emptyState: {
    gridColumn: '1 / -1',
    textAlign: 'center',
    color: '#64748b',
    padding: '60px 0',
    fontSize: '1rem',
  },

  count: {
    color: '#64748b',
    fontSize: '0.85rem',
    marginBottom: '20px',
  },
}

export default function PropertyList() {
  const [properties, setProperties] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [search, setSearch] = useState('')

  useEffect(() => {
    const loadProperties = async () => {
      try {
        setLoading(true)
        const response = await fetchProperties(search ? { search } : {})
        // Handle DRF pagination (results field) or plain array
        const data = response.data?.results ?? response.data
        setProperties(Array.isArray(data) ? data : [])
      } catch (err) {
        console.error('Failed to fetch properties:', err)
        setError('Failed to load properties. Make sure the backend is running.')
      } finally {
        setLoading(false)
      }
    }

    // Debounce search input by 400 ms
    const timer = setTimeout(loadProperties, 400)
    return () => clearTimeout(timer)
  }, [search])

  return (
    <div style={styles.container}>
      {/* Search bar */}
      <input
        id="property-search"
        type="search"
        placeholder="🔍  Search by title, area, or description…"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        style={styles.searchBar}
        onFocus={(e) => {
          e.target.style.borderColor = '#6c63ff'
          e.target.style.boxShadow = '0 0 0 3px rgba(108,99,255,0.2)'
        }}
        onBlur={(e) => {
          e.target.style.borderColor = 'rgba(255,255,255,0.1)'
          e.target.style.boxShadow = 'none'
        }}
      />

      {/* Error state */}
      {error && <div style={styles.errorBox}>⚠️ {error}</div>}

      {/* Result count */}
      {!loading && !error && (
        <p style={styles.count}>
          {properties.length === 0
            ? 'No properties found'
            : `${properties.length} propert${properties.length === 1 ? 'y' : 'ies'} found`}
        </p>
      )}

      {/* Grid */}
      <div style={styles.grid}>
        {loading
          ? Array.from({ length: 3 }).map((_, i) => (
              <div key={i} style={styles.skeleton} />
            ))
          : properties.length === 0 && !error
          ? <div style={styles.emptyState}>No properties match your search.</div>
          : properties.map((prop) => (
              <PropertyCard key={prop.id} property={prop} />
            ))}
      </div>
    </div>
  )
}
