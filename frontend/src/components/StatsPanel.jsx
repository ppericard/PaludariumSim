import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const StatsPanel = ({ stats }) => {
    const [data, setData] = useState([]);

    useEffect(() => {
        if (!stats) return;

        setData(prevData => {
            const newData = [...prevData, { time: new Date().toLocaleTimeString(), ...stats }];
            // Keep last 60 data points (approx 1 minute at 1 update/sec if we throttle, or more)
            // Actually updates come at 10 ticks/sec (0.1s). That's too fast for the graph.
            // Let's limit graph updates or just keep a larger buffer but maybe slice it.
            // For now, let's keep 100 points.
            if (newData.length > 100) {
                return newData.slice(newData.length - 100);
            }
            return newData;
        });
    }, [stats]);

    if (!stats) return null;

    return (
        <div className="glass-panel" style={{
            position: 'absolute',
            bottom: '20px',
            right: '20px',
            width: '400px',
            height: '250px',
            padding: '15px',
            display: 'flex',
            flexDirection: 'column',
            gap: '10px'
        }}>
            <h4 style={{ margin: 0, fontSize: '0.9em', textTransform: 'uppercase', letterSpacing: '0.1em', color: 'rgba(255,255,255,0.7)' }}>
                Population Dynamics
            </h4>
            <div style={{ flex: 1, width: '100%', minHeight: 0 }}>
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={data}>
                        <XAxis dataKey="time" hide={true} />
                        <YAxis stroke="rgba(255,255,255,0.3)" fontSize={10} />
                        <Tooltip
                            contentStyle={{ backgroundColor: '#222', border: '1px solid #444', fontSize: '12px' }}
                            itemStyle={{ fontSize: '12px' }}
                        />
                        <Legend wrapperStyle={{ fontSize: '12px' }} />
                        <Line type="monotone" dataKey="plant" stroke="#2ecc71" dot={false} strokeWidth={2} />
                        <Line type="monotone" dataKey="animal" stroke="#e74c3c" dot={false} strokeWidth={2} />
                    </LineChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};

export default StatsPanel;
