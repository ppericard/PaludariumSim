import { useState, useEffect, useRef, useCallback } from 'react';

export const useSimulation = () => {
    const [agents, setAgents] = useState([]);
    const [environment, setEnvironment] = useState(null);
    const [stats, setStats] = useState(null);
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
                if (data.environment.stats) {
                    setStats(data.environment.stats);
                }
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

    const setSpeed = useCallback((speed) => {
        if (ws.current && isConnected) {
            ws.current.send(JSON.stringify({ type: 'set_speed', payload: { speed: speed } }));
        }
    }, [isConnected]);

    const setLightMode = useCallback((mode) => {
        if (ws.current && isConnected) {
            ws.current.send(JSON.stringify({ type: 'set_light_mode', payload: { mode: mode } }));
        }
    }, [isConnected]);

    return { agents, environment, stats, isConnected, spawnAgent, setSpeed, setLightMode };
};
