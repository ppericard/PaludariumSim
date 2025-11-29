import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { config } from '../config';

const StatsPanel = ({ stats }) => {
    const [fullData, setFullData] = useState([]);
    const [timeScale, setTimeScale] = useState('1m'); // '1m', '5m', 'all'

    useEffect(() => {
        // Fetch initial history
        fetch(`${config.API_URL}/history`)
            .then(res => res.json())
            .then(data => {
                if (Array.isArray(data)) {
                    setFullData(data);
                }
            })
            .catch(err => console.error("Failed to fetch history:", err));
    }, []);

    useEffect(() => {
        if (!stats) return;

        setFullData(prevData => {
            // Check for simulation reset (time went backwards)
            if (prevData.length > 0 && stats.time < prevData[prevData.length - 1].time) {
                return [stats];
            }

            // Check if this timestamp already exists to avoid duplicates
            // stats.time is in ticks.
            if (prevData.length > 0 && prevData[prevData.length - 1].time === stats.time) {
                return prevData;
            }
            // Keep only last 10000 points (approx 2.7 hours at 10 TPS)
            const newData = [...prevData, stats];
            if (newData.length > 10000) {
                return newData.slice(newData.length - 10000);
            }
            return newData;
        });
    }, [stats]);

    const getFilteredData = () => {
        if (timeScale === 'all') return fullData;

        // Convert ticks to approximate time for filtering
        // 10 ticks = 1 second.
        const lastTick = fullData.length > 0 ? fullData[fullData.length - 1].time : 0;
        const durationTicks = timeScale === '1m' ? 60 * 10 : 5 * 60 * 10;
        const cutoff = lastTick - durationTicks;

        return fullData.filter(d => d.time > cutoff);
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
                        <XAxis
                            dataKey="time"
                            type="number"
                            domain={['dataMin', 'dataMax']}
                            hide={true}
                        />
                        <YAxis stroke="rgba(255,255,255,0.3)" fontSize={10} width={30} />
                        <Tooltip
                            contentStyle={{ backgroundColor: '#222', border: '1px solid #444', fontSize: '12px' }}
                            itemStyle={{ fontSize: '12px' }}
                            labelStyle={{ display: 'none' }}
                        />
                        <Legend wrapperStyle={{ fontSize: '10px' }} />
                        {/* Dynamic Lines based on keys in the last data point (excluding 'time') */}
                        {getFilteredData().length > 0 && Object.keys(getFilteredData()[getFilteredData().length - 1])
                            .filter(key => key !== 'time')
                            .map((key, index) => {
                                // Generate a color based on index or key
                                const colors = ['#2ecc71', '#e74c3c', '#3498db', '#9b59b6', '#f1c40f', '#e67e22'];
                                const color = colors[index % colors.length];
                                return (
                                    <Line
                                        key={key}
                                        type="monotone"
                                        dataKey={key}
                                        stroke={color}
                                        dot={false}
                                        strokeWidth={2}
                                        isAnimationActive={false}
                                        name={key}
                                    />
                                );
                            })
                        }
                    </LineChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};

export default StatsPanel;
