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
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', background: '#121212', flex: 1, height: '100vh' }}>
            <div style={{ padding: '10px', background: 'rgba(51, 51, 51, 0.8)', color: '#fff', width: '1000px', boxSizing: 'border-box', borderRadius: '8px 8px 0 0' }}>
                Status: {isConnected ? 'Connected' : 'Disconnected'} | Agents: {agents.length}
            </div>
            <Application width={1000} height={800} options={{ backgroundColor: 0x1099bb }}>
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
