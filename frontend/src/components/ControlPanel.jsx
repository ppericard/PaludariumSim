import React from 'react';

const ControlPanel = ({ onSpawn, onToggleMode, mode }) => {
    return (
        <div style={{
            position: 'absolute',
            top: '10px',
            right: '10px',
            background: 'rgba(0, 0, 0, 0.7)',
            padding: '20px',
            borderRadius: '8px',
            color: 'white',
            display: 'flex',
            flexDirection: 'column',
            gap: '10px',
            width: '200px'
        }}>
            <h3>Control Panel</h3>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span>Mode: {mode}</span>
                <button onClick={onToggleMode} style={{ padding: '5px 10px', cursor: 'pointer' }}>
                    Switch
                </button>
            </div>

            {mode === 'Scientific' && (
                <>
                    <hr style={{ width: '100%', borderColor: '#555' }} />
                    <h4>Spawn Agents</h4>
                    <button onClick={() => onSpawn('plant')} style={{ padding: '8px', cursor: 'pointer', background: '#2ecc71', border: 'none', color: 'white', borderRadius: '4px' }}>
                        Add Plant
                    </button>
                    <button onClick={() => onSpawn('animal')} style={{ padding: '8px', cursor: 'pointer', background: '#e74c3c', border: 'none', color: 'white', borderRadius: '4px' }}>
                        Add Animal
                    </button>

                    <hr style={{ width: '100%', borderColor: '#555' }} />
                    <h4>Environment</h4>
                    <div style={{ fontSize: '0.9em' }}>
                        <div>Temp: 25°C</div>
                        <div>Humidity: 80%</div>
                    </div>
                </>
            )}
        </div>
    );
};

export default ControlPanel;
