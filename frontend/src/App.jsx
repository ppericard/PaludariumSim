import React, { useState } from 'react';
import SimulationCanvas from './components/SimulationCanvas';
import ControlPanel from './components/ControlPanel';
import { useSimulation } from './hooks/useSimulation';
import './App.css';

function App() {
  const [mode, setMode] = useState('Scientific'); // 'Zen' or 'Scientific'
  const { agents, environment, isConnected, spawnAgent } = useSimulation();

  const handleSpawn = (type) => {
    console.log(`Spawn request: ${type}`);
    spawnAgent(type);
  };

  const toggleMode = () => {
    setMode(prev => prev === 'Scientific' ? 'Zen' : 'Scientific');
  };

  return (
    <div className="App" style={{ display: 'flex', width: '100vw', height: '100vh', overflow: 'hidden' }}>
      <SimulationCanvas agents={agents} environment={environment} isConnected={isConnected} />

      {/* Main Control Panel (Sidebar) */}
      <ControlPanel
        mode={mode}
        onSpawn={handleSpawn}
        onToggleMode={toggleMode}
      />

      {/* Zen Mode Toggle (Always visible but subtle in Scientific mode) */}
      {mode === 'Zen' && (
        <button
          onClick={toggleMode}
          className="glass-panel btn-premium"
          style={{
            position: 'absolute',
            top: '20px',
            right: '20px',
            zIndex: 100,
            background: 'rgba(0,0,0,0.3)',
            color: 'rgba(255,255,255,0.7)'
          }}
        >
          Exit Zen Mode
        </button>
      )}

      {/* Zen Mode Indicator */}
      <div style={{
        position: 'absolute',
        bottom: '40px',
        left: '50%',
        transform: 'translateX(-50%)',
        color: 'rgba(255, 255, 255, 0.4)',
        pointerEvents: 'none',
        fontStyle: 'italic',
        opacity: mode === 'Zen' ? 1 : 0,
        transition: 'opacity 1s ease',
        letterSpacing: '0.1em',
        textTransform: 'uppercase',
        fontSize: '0.9em'
      }}>
        Zen Mode Active
      </div>
    </div>
  );
}

export default App;
