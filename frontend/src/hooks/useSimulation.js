import { useState, useEffect, useRef, useCallback } from 'react';
import Logger from '../utils/Logger';

export const useSimulation = () => {
    const [agents, setAgents] = useState([]);
    const [environment, setEnvironment] = useState(null);
    const [stats, setStats] = useState(null);
    const [isConnected, setIsConnected] = useState(false);

    const ws = useRef(null);
    const reconnectAttemptRef = useRef(0);
    const reconnectTimeoutRef = useRef(null);
    const isMountedRef = useRef(true);

    const connect = useCallback(() => {
        if (ws.current?.readyState === WebSocket.OPEN) return;

        Logger.info(`Attempting to connect... (Attempt ${reconnectAttemptRef.current + 1})`);
        ws.current = new WebSocket('ws://localhost:8000/ws');

        ws.current.onopen = () => {
            if (!isMountedRef.current) return;
            Logger.info('Connected to simulation server');
            setIsConnected(true);
            reconnectAttemptRef.current = 0; // Reset attempts on success
        };

        ws.current.onmessage = (event) => {
            if (!isMountedRef.current) return;
            try {
                const data = JSON.parse(event.data);

                if (data.type === 'heartbeat') {
                    return;
                }

                if (data.agents) {
                    setAgents(data.agents);
                }
                if (data.environment) {
                    setEnvironment(data.environment);
                    if (data.environment.stats) {
                        setStats(data.environment.stats);
                    }
                }
            } catch (e) {
                Logger.error('Error parsing message:', e);
            }
        };

        ws.current.onclose = () => {
            if (!isMountedRef.current) return;
            Logger.warn('Disconnected from simulation server');
            setIsConnected(false);

            // Schedule reconnection
            const attempt = reconnectAttemptRef.current;
            const timeout = Math.min(1000 * Math.pow(2, attempt), 10000); // Max 10s
            Logger.info(`Reconnecting in ${timeout}ms...`);

            reconnectTimeoutRef.current = setTimeout(() => {
                if (isMountedRef.current) {
                    reconnectAttemptRef.current += 1;
                    connect();
                }
            }, timeout);
        };

        ws.current.onerror = (error) => {
            Logger.error('WebSocket error:', error);
            ws.current.close();
        };

    }, []);

    useEffect(() => {
        isMountedRef.current = true;
        connect();

        return () => {
            isMountedRef.current = false;
            if (ws.current) {
                ws.current.onclose = null; // Prevent reconnect on unmount
                ws.current.close();
            }
            if (reconnectTimeoutRef.current) {
                clearTimeout(reconnectTimeoutRef.current);
            }
        };
    }, [connect]);

    const spawnAgent = useCallback((type) => {
        if (ws.current && ws.current.readyState === WebSocket.OPEN) {
            ws.current.send(JSON.stringify({ type: 'spawn', payload: { agent_type: type } }));
        }
    }, []);

    const setSpeed = useCallback((speed) => {
        if (ws.current && ws.current.readyState === WebSocket.OPEN) {
            ws.current.send(JSON.stringify({ type: 'set_speed', payload: { speed: speed } }));
        }
    }, []);

    const setLightMode = useCallback((mode) => {
        if (ws.current && ws.current.readyState === WebSocket.OPEN) {
            ws.current.send(JSON.stringify({ type: 'set_light_mode', payload: { mode: mode } }));
        }
    }, []);

    const spawnBatch = useCallback((type, count) => {
        if (ws.current && ws.current.readyState === WebSocket.OPEN) {
            ws.current.send(JSON.stringify({ type: 'spawn_batch', payload: { type, count } }));
        }
    }, []);

    const saveState = useCallback((filename) => {
        if (ws.current && ws.current.readyState === WebSocket.OPEN) {
            ws.current.send(JSON.stringify({ type: 'save_state', payload: { filename } }));
        }
    }, []);

    const loadState = useCallback((filename) => {
        if (ws.current && ws.current.readyState === WebSocket.OPEN) {
            ws.current.send(JSON.stringify({ type: 'load_state', payload: { filename } }));
        }
    }, []);

    const resetSimulation = useCallback(() => {
        if (ws.current && ws.current.readyState === WebSocket.OPEN) {
            ws.current.send(JSON.stringify({ type: 'reset', payload: {} }));
        }
    }, []);

    return { agents, environment, stats, isConnected, spawnAgent, setSpeed, setLightMode, spawnBatch, saveState, loadState, resetSimulation };
};
