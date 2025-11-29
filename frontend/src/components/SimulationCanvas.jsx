import React from 'react';
import { Application, extend } from '@pixi/react';
import { Container, Graphics } from 'pixi.js';

import { config } from '../config';

// Register PixiJS components
extend({ Container, Graphics });

const Agent = ({ x, y, color, type, size, onClick, isSelected }) => {
    const draw = React.useCallback((g) => {
        g.clear();
        const colorInt = parseInt(color.replace('#', ''), 16);
        const radius = size ? size * 2 : 5; // Scale size for visibility

        if (isSelected) {
            g.lineStyle(2, 0xFFFFFF, 1); // White border for selection
        }

        if (type === 'plant') {
            g.rect(-radius, -radius * 2, radius * 2, radius * 2); // Simple plant shape
            g.fill(colorInt);
        } else {
            g.circle(0, 0, radius);
            g.fill(colorInt);
        }
    }, [color, type, size, isSelected]);

    return (
        <pixiGraphics
            draw={draw}
            x={x}
            y={y}
            interactive={true}
            pointerdown={onClick}
            cursor="pointer"
        />
    );
};

const Terrain = React.memo(({ grid, gridSize }) => {
    const draw = React.useCallback((g) => {
        g.clear();
        if (!grid) return;

        grid.forEach((row, y) => {
            row.forEach((cellType, x) => {
                const color = config.TERRAIN_COLORS[cellType] || 0x000000;
                g.rect(x * gridSize, y * gridSize, gridSize, gridSize);
                g.fill(color);
            });
        });
    }, [grid, gridSize]);

    return <pixiGraphics draw={draw} />;
});

const SimulationCanvas = ({ agents, environment, isConnected, onAgentSelect, onReset }) => {
    // Calculate overlay opacity: 1.0 light = 0 opacity, 0.0 light = 0.9 opacity
    const lightLevel = environment?.light_level ?? 1.0;
    const overlayOpacity = 0.9 * (1.0 - lightLevel);
    const terrainGrid = environment?.terrain;

    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', background: '#121212', flex: 1, height: '100vh' }}>
            <div style={{
                padding: '10px 20px',
                background: 'rgba(51, 51, 51, 0.8)',
                color: '#fff',
                width: `${config.CANVAS_WIDTH}px`,
                boxSizing: 'border-box',
                borderRadius: '8px 8px 0 0',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
            }}>
                {/* Title */}
                <h1 style={{ margin: 0, fontSize: '1em', letterSpacing: '1px', color: 'white' }}>PALUDARIUM <span style={{ opacity: 0.5 }}>SIM</span></h1>

                {/* Status */}
                <span style={{ fontSize: '0.9em', color: isConnected ? '#4caf50' : '#f44336' }}>
                    Status: {isConnected ? 'Connected' : 'Reconnecting...'} <span style={{ color: '#ccc' }}>| Agents: {agents.length} | Light: {(lightLevel * 100).toFixed(0)}%</span>
                </span>

                {/* Reset Button */}
                <button
                    onClick={onReset}
                    className="btn-premium btn-danger"
                    style={{ fontSize: '0.7em', padding: '4px 8px' }}
                >
                    Reset
                </button>
            </div>
            <div style={{ position: 'relative', width: config.CANVAS_WIDTH, height: config.CANVAS_HEIGHT }}>
                <Application width={config.CANVAS_WIDTH} height={config.CANVAS_HEIGHT} options={{ backgroundColor: 0x1099bb }}>
                    <pixiContainer>
                        {/* Terrain Layer */}
                        {terrainGrid && <Terrain grid={terrainGrid} gridSize={config.TERRAIN_GRID_SIZE} />}

                        {/* Agents Layer */}
                        {agents.map((agent) => (
                            <Agent
                                key={agent.id}
                                x={agent.position.x}
                                y={agent.position.y}
                                color={agent.state.color || '#ffffff'}
                                type={agent.type}
                                size={agent.state.size}
                                onClick={() => onAgentSelect(agent.id)}
                                isSelected={false} // TODO: Pass selected ID down if we want visual feedback
                            />
                        ))}
                    </pixiContainer>
                </Application>
                {/* Day/Night Overlay */}
                <div style={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    width: '100%',
                    height: '100%',
                    backgroundColor: '#000020', // Dark blue tint
                    opacity: overlayOpacity,
                    pointerEvents: 'none',
                    transition: 'opacity 0.5s ease'
                }} />
            </div>
        </div>
    );
};

export default SimulationCanvas;
