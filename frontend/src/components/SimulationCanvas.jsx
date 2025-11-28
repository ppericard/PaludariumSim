import React, { useEffect, useState, useRef } from 'react';
import { Stage, Container, Sprite, Graphics } from '@pixi/react';
import * as PIXI from 'pixi.js';

const Agent = ({ x, y, color }) => {
    const draw = React.useCallback((g) => {
        g.clear();
        g.beginFill(color.replace('#', '0x'));
        g.drawCircle(0, 0, 5); // 5px radius
        g.endFill();
    }, [color]);

    return <Graphics draw={draw} x={x} y={y} />;
};

const SimulationCanvas = () => {
    const [agents, setAgents] = useState([]);
    const [isConnected, setIsConnected] = useState(false);
    const ws = useRef(null);

    useEffect(() => {
        ws.current = new WebSocket('ws://localhost:8000/ws');

        ws.current.onopen = () => {
            console.log('Connected to simulation server');
            setIsConnected(true);
        };

        ws.current.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.agents) {
                setAgents(data.agents);
            }
        };

        ws.current.onclose = () => {
            console.log('Disconnected from simulation server');
            setIsConnected(false);
        };

        return () => {
            if (ws.current) {
                ws.current.close();
            }
        };
    }, []);

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
                        />
                    ))}
                </Container>
            </Stage>
        </div>
    );
};

export default SimulationCanvas;
