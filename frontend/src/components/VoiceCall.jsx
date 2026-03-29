import React, { useState, useEffect, useRef } from 'react';
import { Device } from '@twilio/voice-sdk';

const styles = {
  container: {
    padding: '24px',
    background: 'rgba(255,255,255,0.03)',
    border: '1px solid rgba(255,255,255,0.08)',
    borderRadius: '16px',
    maxWidth: '400px',
    margin: '0 auto 40px',
    textAlign: 'center',
  },
  status: {
    fontSize: '0.9rem',
    color: '#94a3b8',
    marginBottom: '20px',
    fontWeight: 500,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '8px',
  },
  statusDot: (color) => ({
    width: '8px',
    height: '8px',
    borderRadius: '50%',
    backgroundColor: color,
    boxShadow: `0 0 8px ${color}`,
  }),
  buttonContainer: {
    display: 'flex',
    gap: '12px',
    justifyContent: 'center',
  },
  btn: {
    padding: '12px 24px',
    borderRadius: '99px',
    border: 'none',
    fontSize: '0.95rem',
    fontWeight: 600,
    cursor: 'pointer',
    transition: 'all 0.2s',
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
  },
  btnCall: {
    background: '#22c55e',
    color: '#fff',
    boxShadow: '0 4px 14px rgba(34, 197, 94, 0.3)',
  },
  btnCallDisabled: {
    background: 'rgba(255,255,255,0.1)',
    color: '#64748b',
    cursor: 'not-allowed',
  },
  btnEnd: {
    background: '#ef4444',
    color: '#fff',
    boxShadow: '0 4px 14px rgba(239, 68, 68, 0.3)',
  },
  error: {
    marginTop: '16px',
    color: '#f87171',
    fontSize: '0.85rem',
    background: 'rgba(239,68,68,0.1)',
    padding: '8px',
    borderRadius: '8px',
  }
};

export default function VoiceCall() {
  const [device, setDevice] = useState(null);
  const [status, setStatus] = useState('Initializing...');
  const [callState, setCallState] = useState('idle'); // idle, connecting, active
  const [error, setError] = useState(null);

  // Keep track of the active call
  const callRef = useRef(null);

  useEffect(() => {
    async function setupDevice() {
      try {
        // Fetch token from Django backend
        const response = await fetch('http://localhost:8000/api/token/');
        if (!response.ok) throw new Error('Failed to fetch token. Is the backend running and configured?');
        const data = await response.json();

        // Initialize Twilio Device
        const twilioDevice = new Device(data.token, {
          logLevel: 1, // Warnings and errors only
          codecPreferences: ['opus', 'pcmu'],
        });

        // Register event listeners
        twilioDevice.on('registered', () => {
          setStatus('Ready to call');
        });

        twilioDevice.on('error', (twilioError) => {
          console.error('Twilio Error:', twilioError);
          setError(twilioError?.message || String(twilioError));
          setStatus('Error');
          setCallState('idle');
        });

        // Outgoing call events
        twilioDevice.on('disconnect', () => {
          setStatus('Ready to call');
          setCallState('idle');
          callRef.current = null;
        });

        await twilioDevice.register();
        setDevice(twilioDevice);
      } catch (err) {
        console.error('Setup error:', err);
        setError(err?.message || (err ? String(err) : 'Unknown setup error'));
        setStatus('Error');
      }
    }

    setupDevice();

    return () => {
      // Cleanup device on unmount
      if (device) {
        device.destroy();
      }
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleStartCall = async () => {
    if (!device) return;
    setError(null);
    setStatus('Connecting...');
    setCallState('connecting');

    try {
      // Initiate outgoing call to our Django webhook handler
      const call = await device.connect({
        params: { To: "browser_user" }
      });

      callRef.current = call;

      call.on('accept', () => {
        setStatus('Call Active');
        setCallState('active');
      });

      call.on('disconnect', () => {
        setStatus('Ready to call');
        setCallState('idle');
        callRef.current = null;
      });

      call.on('error', (err) => {
        setError(err?.message || String(err));
        setStatus('Error');
        setCallState('idle');
        callRef.current = null;
      });

    } catch (err) {
      console.error('Call failed:', err);
      setError('Could not start call: ' + (err?.message || (err ? String(err) : 'Unknown error')));
      setStatus('Ready to call');
      setCallState('idle');
    }
  };

  const handleEndCall = () => {
    if (device) {
      device.disconnectAll();
    }
  };

  // Determine indicator color based on status
  let indicatorColor = '#64748b'; // default gray
  if (status === 'Ready to call') indicatorColor = '#3b82f6'; // blue
  if (callState === 'connecting') indicatorColor = '#eab308'; // yellow
  if (callState === 'active') indicatorColor = '#22c55e'; // green
  if (status === 'Error') indicatorColor = '#ef4444'; // red

  return (
    <div style={styles.container}>
      <div style={styles.status}>
        <div style={styles.statusDot(indicatorColor)}></div>
        {status}
      </div>

      <div style={styles.buttonContainer}>
        <button
          style={{ ...styles.btn, ...(callState === 'idle' && device ? styles.btnCall : styles.btnCallDisabled) }}
          onClick={handleStartCall}
          disabled={callState !== 'idle' || !device}
        >
          📞 Start Call
        </button>

        <button
          //style={{...styles.btn, ...styles.btnEnd}}
          onClick={handleEndCall}
          disabled={callState === 'idle'}
          style={callState === 'idle' ? { ...styles.btn, ...styles.btnCallDisabled } : { ...styles.btn, ...styles.btnEnd }}
        >
          🛑 End Call
        </button>
      </div>

      {error && <div style={styles.error}>{error}</div>}
    </div>
  );
}
