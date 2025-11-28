import React from 'react';
import { Application, extend } from '@pixi/react';
import { Container, Graphics } from 'pixi.js';

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

const SimulationCanvas = ({ agents, isConnected }) => {
    return (
        <div style={{ width: '100vw', height: '100vh', display: 'flex', flexDirection: 'column' }}>
            <div style={{ padding: '10px', background: '#333', color: '#fff' }}>
                Status: {isConnected ? 'Connected' : 'Disconnected'} | Agents: {agents.length}
            </div>
            <Application width={800} height={600} options={{ backgroundColor: 0x1099bb }}>
                <pixiContainer>
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
        </div>
    );
};

export default SimulationCanvas;
