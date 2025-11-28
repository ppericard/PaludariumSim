import React from 'react';
import { Application, extend } from '@pixi/react';
import { Container, Graphics } from 'pixi.js';

import { config } from '../config';

// Register PixiJS components
extend({ Container, Graphics });

const Agent = ({ x, y, color, type, size }) => {
    const draw = React.useCallback((g) => {
        g.clear();
        const colorInt = parseInt(color.replace('#', ''), 16);
        const radius = size ? size * 2 : 5; // Scale size for visibility
        if (type === 'plant') {
            g.rect(-radius, -radius * 2, radius * 2, radius * 2); // Simple plant shape
            g.fill(colorInt);
        } else {
            g.circle(0, 0, radius);
            g.fill(colorInt);
        }
    }, [color, type, size]);

    return <pixiGraphics draw={draw} x={x} y={y} />;
};

const Terrain = ({ grid, gridSize }) => {
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
};

const SimulationCanvas = ({ agents, environment, isConnected }) => {
    // Calculate overlay opacity: 1.0 light = 0 opacity, 0.0 light = 0.9 opacity
    const lightLevel = environment?.light_level ?? 1.0;
    const overlayOpacity = 0.9 * (1.0 - lightLevel);
    const terrainGrid = environment?.terrain;

    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', background: '#121212', flex: 1, height: '100vh' }}>
            <div style={{ padding: '10px', background: 'rgba(51, 51, 51, 0.8)', color: '#fff', width: `${config.CANVAS_WIDTH}px`, boxSizing: 'border-box', borderRadius: '8px 8px 0 0' }}>
                Status: {isConnected ? 'Connected' : 'Disconnected'} | Agents: {agents.length} | Light: {(lightLevel * 100).toFixed(0)}%
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
