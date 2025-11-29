import { useState, useEffect, useRef, useCallback } from 'react';
import Logger from '../utils/Logger';
import { config } from '../config';

/**
 * Custom hook to manage the simulation state and WebSocket connection.
 * 
 * @returns {Object} The simulation interface.
 * @returns {Array} return.agents - List of agents.
 * @returns {Object} return.environment - Environment state.
 * @returns {Object} return.stats - Simulation statistics.
 * @returns {boolean} return.isConnected - Connection status.
 * @returns {Function} return.spawnAgent - Function to spawn an agent: (type) => void.
 * @returns {Function} return.setSpeed - Function to set simulation speed: (speed) => void.
 * @returns {Function} return.setLightMode - Function to set light mode: (mode) => void.
 * @returns {Function} return.spawnBatch - Function to spawn a batch of agents: (type, count) => void.
 * @returns {Function} return.saveState - Function to save state: (filename) => void.
 * @returns {Function} return.loadState - Function to load state: (filename) => void.
 * @returns {Function} return.resetSimulation - Function to reset the simulation.
 */
export const useSimulation = () => {
    const [agents, setAgents] = useState([]);
    const [environment, setEnvironment] = useState(null);
    const [stats, setStats] = useState(null);
    const [isConnected, setIsConnected] = useState(false);

    const ws = useRef(null);
    const reconnectAttemptRef = useRef(0);
    const reconnectTimeoutRef = useRef(null);
    const isMountedRef = useRef(true);

    /**
     * Establishes the WebSocket connection.
     */
    const connect = useCallback(() => {
        if (ws.current?.readyState === WebSocket.OPEN) return;

        Logger.info(`Attempting to connect... (Attempt ${reconnectAttemptRef.current + 1})`);
        ws.current = new WebSocket(config.WS_URL || 'ws://localhost:8000/ws');

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

    /**
     * Spawns a single agent.
     * @param {string} type - The type of agent to spawn.
     */
    const spawnAgent = useCallback((type) => {
        if (ws.current && ws.current.readyState === WebSocket.OPEN) {
            ws.current.send(JSON.stringify({ type: 'spawn', payload: { agent_type: type } }));
        }
    }, []);

    /**
     * Sets the simulation speed.
     * @param {number} speed - The target TPS.
     */
    const setSpeed = useCallback((speed) => {
        if (ws.current && ws.current.readyState === WebSocket.OPEN) {
            ws.current.send(JSON.stringify({ type: 'set_speed', payload: { speed: speed } }));
        }
    }, []);

    /**
     * Sets the lighting mode.
     * @param {string} mode - 'cycle' or 'always_on'.
     */
    const setLightMode = useCallback((mode) => {
        if (ws.current && ws.current.readyState === WebSocket.OPEN) {
            ws.current.send(JSON.stringify({ type: 'set_light_mode', payload: { mode: mode } }));
        }
    }, []);

    /**
     * Spawns a batch of agents.
     * @param {string} type - Agent type.
     * @param {number} count - Number of agents.
     */
    const spawnBatch = useCallback((type, count) => {
        if (ws.current && ws.current.readyState === WebSocket.OPEN) {
            ws.current.send(JSON.stringify({ type: 'spawn_batch', payload: { type, count } }));
        }
    }, []);

    /**
     * Saves the current state to a file.
     * @param {string} filename - The filename.
     */
    const saveState = useCallback((filename) => {
        if (ws.current && ws.current.readyState === WebSocket.OPEN) {
            ws.current.send(JSON.stringify({ type: 'save_state', payload: { filename } }));
        }
    }, []);

    /**
     * Loads state from a file.
     * @param {string} filename - The filename.
     */
    const loadState = useCallback((filename) => {
        if (ws.current && ws.current.readyState === WebSocket.OPEN) {
            ws.current.send(JSON.stringify({ type: 'load_state', payload: { filename } }));
        }
    }, []);

    /**
     * Resets the simulation.
     */
    const resetSimulation = useCallback(() => {
        if (ws.current && ws.current.readyState === WebSocket.OPEN) {
            ws.current.send(JSON.stringify({ type: 'reset', payload: {} }));
        }
    }, []);

    return { agents, environment, stats, isConnected, spawnAgent, setSpeed, setLightMode, spawnBatch, saveState, loadState, resetSimulation };
};
