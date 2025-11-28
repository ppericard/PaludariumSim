import React from 'react';
import { Stage, Container, Graphics } from '@pixi/react';

const Agent = ({ x, y, color, type, size }) => {
    const draw = React.useCallback((g) => {
        g.clear();
        g.beginFill(parseInt(color.replace('#', ''), 16));
        const radius = size ? size * 2 : 5; // Scale size for visibility
        if (type === 'plant') {
            g.drawRect(-radius, -radius * 2, radius * 2, radius * 2); // Simple plant shape
        } else {
            g.drawCircle(0, 0, radius);
        }
        g.endFill();
    }, [color, type, size]);

    return <Graphics draw={draw} x={x} y={y} />;
};

const SimulationCanvas = ({ agents, isConnected }) => {
    return (
        <div style={{ width: '100vw', height: '100vh', display: 'flex', flexDirection: 'column' }}>
            <div style={{ padding: '10px', background: '#333', color: '#fff' }}>
                Status: {isConnected ? 'Connected' : 'Disconnected'} | Agents: {agents.length}
            </div>
            <Stage width={800} height={600} options={{ backgroundColor: 0x1099bb }}>
                <Container>
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
                </Container>
            </Stage>
        </div>
    );
};

export default SimulationCanvas;
