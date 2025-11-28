import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const StatsPanel = ({ stats }) => {
    const [fullData, setFullData] = useState([]);
    const [timeScale, setTimeScale] = useState('1m'); // '1m', '5m', 'all'

    useEffect(() => {
        if (!stats) return;

        setFullData(prevData => {
            const now = new Date();
            const newDataPoint = {
                time: now.toLocaleTimeString(),
                timestamp: now.getTime(),
                ...stats
            };
            return [...prevData, newDataPoint];
        });
    }, [stats]);

    const getFilteredData = () => {
        if (timeScale === 'all') return fullData;

        const now = new Date().getTime();
        const duration = timeScale === '1m' ? 60 * 1000 : 5 * 60 * 1000;
        const cutoff = now - duration;

        return fullData.filter(d => d.timestamp > cutoff);
    };

    if (!stats) return null;

    return (
        <div style={{
            width: '100%',
            height: '200px',
            display: 'flex',
            flexDirection: 'column',
            gap: '10px',
            marginTop: 'auto' // Push to bottom if in flex container
        }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h4 style={{ margin: 0, fontSize: '0.85em', textTransform: 'uppercase', letterSpacing: '0.1em', color: 'rgba(255,255,255,0.7)' }}>
                    Population
                </h4>
                <select
                    value={timeScale}
                    onChange={(e) => setTimeScale(e.target.value)}
                    style={{
                        background: 'rgba(0,0,0,0.3)',
                        border: '1px solid rgba(255,255,255,0.2)',
                        color: 'white',
                        fontSize: '0.8em',
                        padding: '2px 5px',
                        borderRadius: '4px',
                        outline: 'none'
                    }}
                >
                    <option value="1m">Last 1m</option>
                    <option value="5m">Last 5m</option>
                    <option value="all">All Time</option>
                </select>
            </div>
            <div style={{ flex: 1, width: '100%', minHeight: 0 }}>
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={getFilteredData()}>
                        <XAxis dataKey="time" hide={true} />
                        <YAxis stroke="rgba(255,255,255,0.3)" fontSize={10} width={30} />
                        <Tooltip
                            contentStyle={{ backgroundColor: '#222', border: '1px solid #444', fontSize: '12px' }}
                            itemStyle={{ fontSize: '12px' }}
                            labelStyle={{ display: 'none' }}
                        />
                        <Legend wrapperStyle={{ fontSize: '10px' }} />
                        <Line type="monotone" dataKey="plant" stroke="#2ecc71" dot={false} strokeWidth={2} isAnimationActive={false} />
                        <Line type="monotone" dataKey="animal" stroke="#e74c3c" dot={false} strokeWidth={2} isAnimationActive={false} />
                    </LineChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};

export default StatsPanel;
