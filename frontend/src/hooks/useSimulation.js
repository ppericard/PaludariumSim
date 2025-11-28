import { useState, useEffect, useRef, useCallback } from 'react';

export const useSimulation = () => {
    const [agents, setAgents] = useState([]);
    const [environment, setEnvironment] = useState(null);
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
            if (data.environment) {
                setEnvironment(data.environment);
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

    const spawnAgent = useCallback((type) => {
        if (ws.current && isConnected) {
            ws.current.send(JSON.stringify({ type: 'spawn', payload: { agent_type: type } }));
        }
    }, [isConnected]);

    return { agents, environment, isConnected, spawnAgent };
};
