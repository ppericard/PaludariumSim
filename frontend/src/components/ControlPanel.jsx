import React from 'react';
import StatsPanel from './StatsPanel';

const ControlPanel = ({ onSpawn, onToggleMode, mode, stats, environment, onSetSpeed, onSetLightMode, onSpawnBatch, onSaveState, onLoadState, selectedAgent, onCloseInspector, onReset }) => {
    const isZen = mode === 'Zen';
    const [saveName, setSaveName] = React.useState('save1');
    const [showDevTools, setShowDevTools] = React.useState(false);

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
            {/* Inspector Panel (Overlays top if active) */}
            {selectedAgent && (
                <div style={{
                    background: 'rgba(50, 50, 60, 0.9)',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    borderRadius: '8px',
                    padding: '15px',
                    marginBottom: '10px',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '8px'
                }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <h4 style={{ margin: 0, color: '#fff' }}>Inspector</h4>
                        <button onClick={onCloseInspector} style={{ background: 'none', border: 'none', color: '#aaa', cursor: 'pointer' }}>✕</button>
                    </div>

                    <div style={{ fontSize: '0.9em', color: '#ccc' }}>
                        <div><strong>ID:</strong> {selectedAgent.id.substring(0, 8)}...</div>
                        <div><strong>Type:</strong> {selectedAgent.type}</div>
                        {selectedAgent.state.species && <div><strong>Species:</strong> {selectedAgent.state.species}</div>}
                        {selectedAgent.state.habitat && <div><strong>Habitat:</strong> {selectedAgent.state.habitat}</div>}

                        {/* Components List */}
                        {selectedAgent.components && (
                            <div style={{ marginTop: '5px' }}>
                                <strong>Components:</strong>
                                <div style={{ fontSize: '0.85em', color: '#aaa', marginLeft: '5px' }}>
                                    {selectedAgent.components.join(', ')}
                                </div>
                            </div>
                        )}

                        <div style={{ marginTop: '5px' }}><strong>Position:</strong> ({selectedAgent.position.x.toFixed(0)}, {selectedAgent.position.y.toFixed(0)})</div>

                        {/* Dynamic Stats based on state keys */}
                        <div style={{ marginTop: '10px', display: 'flex', flexDirection: 'column', gap: '5px' }}>
                            {selectedAgent.state.energy !== undefined && (
                                <div>
                                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8em' }}>
                                        <span>Energy</span>
                                        <span>{selectedAgent.state.energy.toFixed(1)}%</span>
                                    </div>
                                    <div style={{ width: '100%', height: '4px', background: '#333', borderRadius: '2px' }}>
                                        <div style={{ width: `${Math.min(100, selectedAgent.state.energy)}%`, height: '100%', background: '#f1c40f', borderRadius: '2px' }} />
                                    </div>
                                </div>
                            )}
                            {selectedAgent.state.hunger !== undefined && (
                                <div>
                                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8em' }}>
                                        <span>Hunger</span>
                                        <span>{selectedAgent.state.hunger.toFixed(1)}%</span>
                                    </div>
                                    <div style={{ width: '100%', height: '4px', background: '#333', borderRadius: '2px' }}>
                                        <div style={{ width: `${Math.min(100, selectedAgent.state.hunger)}%`, height: '100%', background: '#e74c3c', borderRadius: '2px' }} />
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            )}

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
                    <span className="text-muted">Compute Time</span>
                    <span>{environment?.last_tick_duration ? environment.last_tick_duration.toFixed(2) : 0} ms</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9em' }}>
                    <span className="text-muted">Actual TPS</span>
                    <span>{environment?.actual_tps ? environment.actual_tps.toFixed(1) : 0} / {environment?.target_tps || 0}</span>
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
                        Fern
                    </button>
                    <button onClick={() => onSpawn('animal')} className="btn-premium btn-danger">
                        Frog
                    </button>
                    <button onClick={() => onSpawn('Fish')} className="btn-premium" style={{ background: '#3498db', borderColor: '#2980b9' }}>
                        Fish
                    </button>
                    <button onClick={() => onSpawn('Lizard')} className="btn-premium" style={{ background: '#8e44ad', borderColor: '#9b59b6' }}>
                        Lizard
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

                {/* Light Switch */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '5px', marginTop: '5px' }}>
                    <span className="text-muted" style={{ fontSize: '0.9em' }}>Light Mode</span>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '5px' }}>
                        <button
                            onClick={() => onSetLightMode('always_on')}
                            className={`btn-premium ${environment?.light_mode === 'always_on' ? 'active' : ''}`}
                            style={{
                                padding: '4px',
                                fontSize: '0.8em',
                                background: environment?.light_mode === 'always_on' ? 'rgba(255, 255, 255, 0.2)' : 'rgba(0, 0, 0, 0.2)'
                            }}
                        >
                            Always On
                        </button>
                        <button
                            onClick={() => onSetLightMode('cycle')}
                            className={`btn-premium ${environment?.light_mode === 'cycle' ? 'active' : ''}`}
                            style={{
                                padding: '4px',
                                fontSize: '0.8em',
                                background: environment?.light_mode === 'cycle' ? 'rgba(255, 255, 255, 0.2)' : 'rgba(0, 0, 0, 0.2)'
                            }}
                        >
                            Cycle
                        </button>
                    </div>
                </div>
            </div>

            {/* Stats Panel Integration */}
            {stats && (
                <>
                    <hr style={{ width: '100%', borderColor: 'var(--glass-border)', margin: 0 }} />
                    <StatsPanel stats={stats} />
                </>
            )}

            <hr style={{ width: '100%', borderColor: 'var(--glass-border)', margin: 0 }} />

            {/* Developer Tools */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                <div
                    onClick={() => setShowDevTools(!showDevTools)}
                    style={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        cursor: 'pointer',
                        color: 'rgba(255,255,255,0.5)',
                        fontSize: '0.85em',
                        textTransform: 'uppercase',
                        letterSpacing: '0.1em'
                    }}
                >
                    <span>Developer Tools</span>
                    <span>{showDevTools ? '▼' : '▶'}</span>
                </div>

                {showDevTools && (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginTop: '5px' }}>
                        {/* Batch Spawn */}
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
                            <span className="text-muted" style={{ fontSize: '0.8em' }}>Batch Spawn</span>
                            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '5px' }}>
                                <button onClick={() => onSpawnBatch('plant', 100)} className="btn-premium" style={{ fontSize: '0.75em', padding: '4px' }}>+100 Plants</button>
                                <button onClick={() => onSpawnBatch('animal', 100)} className="btn-premium" style={{ fontSize: '0.75em', padding: '4px' }}>+100 Animals</button>
                                <button onClick={() => onSpawnBatch('plant', 500)} className="btn-premium" style={{ fontSize: '0.75em', padding: '4px' }}>+500 Plants</button>
                                <button onClick={() => onSpawnBatch('animal', 500)} className="btn-premium" style={{ fontSize: '0.75em', padding: '4px' }}>+500 Animals</button>
                            </div>
                        </div>

                        {/* Save / Load */}
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
                            <span className="text-muted" style={{ fontSize: '0.8em' }}>State Management</span>
                            <input
                                type="text"
                                value={saveName}
                                onChange={(e) => setSaveName(e.target.value)}
                                style={{
                                    background: 'rgba(0,0,0,0.3)',
                                    border: '1px solid rgba(255,255,255,0.2)',
                                    color: 'white',
                                    padding: '4px',
                                    fontSize: '0.8em',
                                    width: '100%',
                                    boxSizing: 'border-box'
                                }}
                            />
                            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '5px' }}>
                                <button onClick={() => onSaveState(saveName)} className="btn-premium" style={{ fontSize: '0.75em', padding: '4px' }}>Save</button>
                                <button onClick={() => onLoadState(saveName)} className="btn-premium" style={{ fontSize: '0.75em', padding: '4px' }}>Load</button>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default ControlPanel;
