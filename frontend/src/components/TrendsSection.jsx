import { useEffect, useState } from 'react';
import { api } from '../services/api';
import {
    AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts';
import { TrendingUp, Calendar, MonitorPlay } from 'lucide-react';

export default function TrendsSection() {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.getTendencias()
            .then(d => setData(d))
            .catch(err => console.error('Error loading trends:', err))
            .finally(() => setLoading(false));
    }, []);

    if (loading) {
        return (
            <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800 backdrop-blur-sm shadow-lg h-[400px] flex items-center justify-center">
                <div className="animate-pulse text-slate-400">Cargando serie de tiempo...</div>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800 backdrop-blur-sm shadow-lg">
                <div className="flex justify-between items-start mb-8">
                    <div>
                        <h2 className="text-xl font-bold flex items-center gap-2">
                            <TrendingUp className="text-blue-400 w-5 h-5" />
                            Evolución del Mercado Laboral
                        </h2>
                        <p className="text-sm text-slate-400 mt-1">
                            Volumen semanal de nuevas vacantes publicadas.
                        </p>
                    </div>
                    <div className="flex items-center gap-2 text-xs text-slate-500 bg-slate-800/50 px-3 py-1.5 rounded-full border border-slate-700">
                        <Calendar className="w-3 h-3" />
                        Últimos 6 meses
                    </div>
                </div>

                <div className="h-[450px] w-full">
                    <ResponsiveContainer width="100%" height="100%">
                        <AreaChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                            <defs>
                                <linearGradient id="colorTotal" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                                </linearGradient>
                                <linearGradient id="colorTele" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3}/>
                                    <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0}/>
                                </linearGradient>
                            </defs>
                            <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
                            <XAxis 
                                dataKey="fecha" 
                                stroke="#94a3b8" 
                                fontSize={11} 
                                tickLine={false} 
                                axisLine={false}
                                tickFormatter={(val) => `Sem ${val.split('-')[1]}`}
                            />
                            <YAxis 
                                stroke="#94a3b8" 
                                fontSize={11} 
                                tickLine={false} 
                                axisLine={false}
                                tickFormatter={(val) => val.toLocaleString()}
                            />
                            <Tooltip 
                                contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', color: '#fff' }}
                                itemStyle={{ fontSize: '12px' }}
                            />
                            <Area 
                                type="monotone" 
                                dataKey="total" 
                                name="Nuevas Vacantes"
                                stroke="#3b82f6" 
                                strokeWidth={3}
                                fillOpacity={1} 
                                fill="url(#colorTotal)" 
                            />
                            <Area 
                                type="monotone" 
                                dataKey="teletrabajo" 
                                name="Teletrabajo"
                                stroke="#8b5cf6" 
                                strokeWidth={2}
                                fillOpacity={1} 
                                fill="url(#colorTele)" 
                                strokeDasharray="5 5"
                            />
                        </AreaChart>
                    </ResponsiveContainer>
                </div>
                
                <div className="mt-6 flex justify-center gap-8 border-t border-slate-800/50 pt-6">
                    <div className="flex items-center gap-2">
                        <div className="w-3 h-3 rounded-full bg-blue-500 shadow-[0_0_8px_rgba(59,130,246,0.5)]"></div>
                        <span className="text-xs text-slate-300">Total Vacantes</span>
                    </div>
                    <div className="flex items-center gap-2">
                        <div className="w-3 h-3 rounded-full bg-purple-500 shadow-[0_0_8px_rgba(139,92,246,0.5)]"></div>
                        <span className="text-xs text-slate-300">Teletrabajo / Remoto</span>
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="p-5 rounded-2xl bg-slate-900/40 border border-slate-800 flex items-center gap-4">
                    <div className="p-3 bg-blue-500/10 rounded-xl">
                        <TrendingUp className="text-blue-400 w-6 h-6" />
                    </div>
                    <div>
                        <p className="text-xs text-slate-500 uppercase font-bold tracking-wider">Crecimiento Semanal</p>
                        <p className="text-lg font-bold text-white">
                            {data.length >= 2 ? (
                                ((data[data.length-1].total - data[data.length-2].total) / (data[data.length-2].total || 1) * 100).toFixed(1) + '%'
                            ) : 'N/A'}
                        </p>
                    </div>
                </div>
                <div className="p-5 rounded-2xl bg-slate-900/40 border border-slate-800 flex items-center gap-4">
                    <div className="p-3 bg-purple-500/10 rounded-xl">
                        <MonitorPlay className="text-purple-400 w-6 h-6" />
                    </div>
                    <div>
                        <p className="text-xs text-slate-500 uppercase font-bold tracking-wider">Adopción Remoto</p>
                        <p className="text-lg font-bold text-white">
                            {data.length > 0 ? (
                                (data[data.length-1].teletrabajo / (data[data.length-1].total || 1) * 100).toFixed(1) + '%'
                            ) : 'N/A'}
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}
