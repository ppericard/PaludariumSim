import React, { useState } from 'react';
import SimulationCanvas from './components/SimulationCanvas';
import ControlPanel from './components/ControlPanel';
import { useSimulation } from './hooks/useSimulation';
import Logger from './utils/Logger';
import './App.css';

function App() {
  const [mode, setMode] = useState('Scientific'); // 'Zen' or 'Scientific'
  const [selectedAgentId, setSelectedAgentId] = useState(null);
  const { agents, environment, stats, isConnected, spawnAgent, setSpeed, setLightMode, spawnBatch, saveState, loadState, resetSimulation } = useSimulation();

  // Find the actual agent object from the current agents list
  const selectedAgent = React.useMemo(() => {
    if (!selectedAgentId) return null;
    return agents.find(a => a.id === selectedAgentId) || null;
  }, [agents, selectedAgentId]);

  const handleSpawn = (type) => {
    Logger.debug(`Spawn request: ${type}`);
    spawnAgent(type);
  };

  const toggleMode = () => {
    setMode(prev => prev === 'Scientific' ? 'Zen' : 'Scientific');
  };

  return (
    <div className="App" style={{ display: 'flex', width: '100vw', height: '100vh', overflow: 'hidden' }}>
      <SimulationCanvas
        agents={agents}
        environment={environment}
        isConnected={isConnected}
        onAgentSelect={setSelectedAgentId}
        onReset={resetSimulation}
      />

      {/* Main Control Panel (Sidebar) */}
      <ControlPanel
        mode={mode}
        onSpawn={handleSpawn}
        onToggleMode={toggleMode}
        stats={stats}
        environment={environment}
        onSetSpeed={setSpeed}
        onSetLightMode={setLightMode}
        onSpawnBatch={spawnBatch}
        onSaveState={saveState}
        onLoadState={loadState}
        selectedAgent={selectedAgent}
        onCloseInspector={() => setSelectedAgentId(null)}
        onReset={resetSimulation}
      />

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
