import React from 'react';
import StatsPanel from './StatsPanel';

const ControlPanel = ({ onSpawn, onToggleMode, mode, stats, environment, onSetSpeed }) => {
    const isZen = mode === 'Zen';

    return (
        <div className={`glass-panel`} style={{
            position: 'relative', // Changed from absolute
            height: '100vh',
            width: isZen ? '0px' : '300px',
            padding: isZen ? '0' : '24px',
            overflow: 'hidden',
            display: 'flex',
            flexDirection: 'column',
            gap: '20px',
            opacity: isZen ? 0 : 1,
            pointerEvents: isZen ? 'none' : 'auto',
            transition: 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)',
            borderLeft: '1px solid var(--glass-border)',
            borderRadius: 0, // Remove radius for sidebar
            boxSizing: 'border-box'
        }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h3>Control Panel</h3>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <span className="text-muted">Mode</span>
                <button onClick={onToggleMode} className="btn-premium btn-primary" style={{ fontSize: '0.8em', padding: '6px 12px' }}>
                    {mode}
                </button>
            </div>

            <hr style={{ width: '100%', borderColor: 'var(--glass-border)', margin: 0 }} />

            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                <h4 className="text-muted" style={{ fontSize: '0.85em', textTransform: 'uppercase', letterSpacing: '0.1em' }}>Simulation</h4>

                {/* Telemetry */}
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9em' }}>
                    <span className="text-muted">Ticks</span>
                    <span>{environment?.total_ticks || 0}</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9em' }}>
                    <span className="text-muted">Tick Time</span>
                    <span>{environment?.last_tick_duration ? environment.last_tick_duration.toFixed(2) : 0} ms</span>
                </div>

                {/* Speed Controls */}
                <div style={{ display: 'flex', gap: '5px', marginTop: '5px' }}>
                    <button onClick={() => onSetSpeed(0)} className="btn-premium" style={{ flex: 1, padding: '4px', fontSize: '0.8em' }}>⏸</button>
                    <button onClick={() => onSetSpeed(10)} className="btn-premium" style={{ flex: 1, padding: '4px', fontSize: '0.8em' }}>1x</button>
                    <button onClick={() => onSetSpeed(20)} className="btn-premium" style={{ flex: 1, padding: '4px', fontSize: '0.8em' }}>2x</button>
                    <button onClick={() => onSetSpeed(50)} className="btn-premium" style={{ flex: 1, padding: '4px', fontSize: '0.8em' }}>5x</button>
                    <button onClick={() => onSetSpeed(100)} className="btn-premium" style={{ flex: 1, padding: '4px', fontSize: '0.8em' }}>Max</button>
                </div>
            </div>

            <hr style={{ width: '100%', borderColor: 'var(--glass-border)', margin: 0 }} />

            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                <h4 className="text-muted" style={{ fontSize: '0.85em', textTransform: 'uppercase', letterSpacing: '0.1em' }}>Spawn Agents</h4>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                    <button onClick={() => onSpawn('plant')} className="btn-premium btn-success">
                        Plant
                    </button>
                    <button onClick={() => onSpawn('animal')} className="btn-premium btn-danger">
                        Animal
                    </button>
                </div>
            </div>

            <hr style={{ width: '100%', borderColor: 'var(--glass-border)', margin: 0 }} />

            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                <h4 className="text-muted" style={{ fontSize: '0.85em', textTransform: 'uppercase', letterSpacing: '0.1em' }}>Environment</h4>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9em' }}>
                    <span className="text-muted">Temperature</span>
                    <span>25°C</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9em' }}>
                    <span className="text-muted">Humidity</span>
                    <span>80%</span>
                </div>
            </div>

            {/* Stats Panel Integration */}
            {stats && (
                <>
                    <hr style={{ width: '100%', borderColor: 'var(--glass-border)', margin: 0 }} />
                    <StatsPanel stats={stats} />
                </>
            )}
        </div>
    );
};

export default ControlPanel;
