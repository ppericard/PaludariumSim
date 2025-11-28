import React, { useState } from 'react';
import SimulationCanvas from './components/SimulationCanvas';
import ControlPanel from './components/ControlPanel';
import { useSimulation } from './hooks/useSimulation';
import './App.css';

function App() {
  const [mode, setMode] = useState('Scientific'); // 'Zen' or 'Scientific'
  const { agents, isConnected, spawnAgent } = useSimulation();

  const handleSpawn = (type) => {
    console.log(`Spawn request: ${type}`);
    spawnAgent(type);
  };

  const toggleMode = () => {
    setMode(prev => prev === 'Scientific' ? 'Zen' : 'Scientific');
  };

  return (
    <div className="App" style={{ position: 'relative', width: '100vw', height: '100vh', overflow: 'hidden' }}>
      <SimulationCanvas agents={agents} isConnected={isConnected} />

      {/* Overlay UI */}
      <ControlPanel
        mode={mode}
        onSpawn={handleSpawn}
        onToggleMode={toggleMode}
      />

      {mode === 'Zen' && (
        <div style={{
          position: 'absolute',
          bottom: '20px',
          left: '50%',
          transform: 'translateX(-50%)',
          color: 'rgba(255, 255, 255, 0.5)',
          pointerEvents: 'none',
          fontStyle: 'italic'
        }}>
          Zen Mode - Enjoy the view
        </div>
      )}
    </div>
  );
}

export default App;
