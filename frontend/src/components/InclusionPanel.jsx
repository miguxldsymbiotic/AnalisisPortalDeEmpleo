import { useEffect, useState } from 'react';
import { api } from '../services/api';
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
    PieChart, Pie, Cell, Legend
} from 'recharts';
import { Heart, GraduationCap, Users, TrendingUp } from 'lucide-react';

const COLORS_DISC = ['#ec4899', '#f472b6', '#f9a8d4', '#fce7f3', '#be185d', '#9d174d', '#831843', '#500724', '#fda4af', '#fb7185'];
const COLORS_PLAZA = ['#8b5cf6', '#a78bfa', '#c4b5fd', '#ddd6fe', '#7c3aed', '#6d28d9', '#5b21b6', '#4c1d95', '#a5b4fc', '#818cf8'];

export default function InclusionPanel() {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.getInclusion()
            .then(d => setData(d))
            .catch(err => console.error('Error loading inclusion data:', err))
            .finally(() => setLoading(false));
    }, []);

    if (loading) {
        return (
            <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800 backdrop-blur-sm shadow-lg h-[400px] flex items-center justify-center">
                <div className="animate-pulse text-slate-400">Cargando datos de inclusión...</div>
            </div>
        );
    }

    if (!data) {
        return (
            <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800 text-slate-500">
                No hay datos de inclusión disponibles.
            </div>
        );
    }

    return (
        <div className="space-y-8">
            {/* KPI CARDS */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <KPICard
                    title="Total Vacantes"
                    value={data.total_vacantes?.toLocaleString()}
                    icon={<Users className="w-7 h-7 text-blue-400" />}
                    color="from-blue-500/20 to-blue-400/5"
                />
                <KPICard
                    title="Vacantes con Discapacidad"
                    value={data.discapacidad?.total?.toLocaleString()}
                    subtitle={`${data.discapacidad?.porcentaje}% del total`}
                    icon={<Heart className="w-7 h-7 text-pink-400" />}
                    color="from-pink-500/20 to-pink-400/5"
                />
                <KPICard
                    title="Plazas de Práctica"
                    value={data.plaza_practica?.total?.toLocaleString()}
                    subtitle={`${data.plaza_practica?.porcentaje}% del total`}
                    icon={<GraduationCap className="w-7 h-7 text-purple-400" />}
                    color="from-purple-500/20 to-purple-400/5"
                />
                <KPICard
                    title="Índice de Inclusión"
                    value={`${((data.discapacidad?.porcentaje || 0) + (data.plaza_practica?.porcentaje || 0)).toFixed(1)}%`}
                    subtitle="Disc. + Práctica combinado"
                    icon={<TrendingUp className="w-7 h-7 text-emerald-400" />}
                    color="from-emerald-500/20 to-emerald-400/5"
                />
            </div>

            {/* CHARTS */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* DISCAPACIDAD POR DEPARTAMENTO */}
                <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800 backdrop-blur-sm shadow-lg">
                    <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                        <Heart className="text-pink-400 w-5 h-5" />
                        Vacantes Inclusivas por Departamento
                    </h3>
                    <div className="h-[350px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={data.discapacidad?.por_departamento || []} layout="vertical"
                                margin={{ top: 0, right: 30, left: 20, bottom: 0 }}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#334155" horizontal vertical={false} />
                                <XAxis type="number" stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
                                <YAxis dataKey="departamento" type="category" stroke="#94a3b8" fontSize={11}
                                    tickLine={false} axisLine={false} width={120} />
                                <Tooltip cursor={{ fill: '#1e293b' }}
                                    contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#fff' }} />
                                <Bar dataKey="total" fill="#ec4899" radius={[0, 4, 4, 0]}>
                                    {(data.discapacidad?.por_departamento || []).map((_, i) => (
                                        <Cell key={i} fill={COLORS_DISC[i % COLORS_DISC.length]} />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* PLAZA PRÁCTICA POR DEPARTAMENTO */}
                <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800 backdrop-blur-sm shadow-lg">
                    <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                        <GraduationCap className="text-purple-400 w-5 h-5" />
                        Plazas de Práctica por Departamento
                    </h3>
                    <div className="h-[350px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={data.plaza_practica?.por_departamento || []} layout="vertical"
                                margin={{ top: 0, right: 30, left: 20, bottom: 0 }}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#334155" horizontal vertical={false} />
                                <XAxis type="number" stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
                                <YAxis dataKey="departamento" type="category" stroke="#94a3b8" fontSize={11}
                                    tickLine={false} axisLine={false} width={120} />
                                <Tooltip cursor={{ fill: '#1e293b' }}
                                    contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#fff' }} />
                                <Bar dataKey="total" fill="#8b5cf6" radius={[0, 4, 4, 0]}>
                                    {(data.plaza_practica?.por_departamento || []).map((_, i) => (
                                        <Cell key={i} fill={COLORS_PLAZA[i % COLORS_PLAZA.length]} />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* DISCAPACIDAD POR SECTOR */}
                <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800 backdrop-blur-sm shadow-lg">
                    <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                        <Heart className="text-pink-400 w-5 h-5" />
                        Inclusión por Sector Económico
                    </h3>
                    <div className="h-[350px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie data={data.discapacidad?.por_sector || []} cx="50%" cy="50%"
                                    innerRadius={70} outerRadius={130} paddingAngle={3}
                                    dataKey="total" nameKey="sector" stroke="none">
                                    {(data.discapacidad?.por_sector || []).map((_, i) => (
                                        <Cell key={i} fill={COLORS_DISC[i % COLORS_DISC.length]} />
                                    ))}
                                </Pie>
                                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#fff' }} />
                                <Legend verticalAlign="bottom" height={36} iconType="circle"
                                    wrapperStyle={{ fontSize: '11px' }} />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* PLAZA PRÁCTICA POR SECTOR */}
                <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800 backdrop-blur-sm shadow-lg">
                    <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                        <GraduationCap className="text-purple-400 w-5 h-5" />
                        Plazas de Práctica por Sector
                    </h3>
                    <div className="h-[350px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie data={data.plaza_practica?.por_sector || []} cx="50%" cy="50%"
                                    innerRadius={70} outerRadius={130} paddingAngle={3}
                                    dataKey="total" nameKey="sector" stroke="none">
                                    {(data.plaza_practica?.por_sector || []).map((_, i) => (
                                        <Cell key={i} fill={COLORS_PLAZA[i % COLORS_PLAZA.length]} />
                                    ))}
                                </Pie>
                                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#fff' }} />
                                <Legend verticalAlign="bottom" height={36} iconType="circle"
                                    wrapperStyle={{ fontSize: '11px' }} />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </div>
        </div>
    );
}

function KPICard({ title, value, subtitle, icon, color }) {
    return (
        <div className={`relative overflow-hidden p-6 rounded-2xl bg-gradient-to-br ${color} border border-slate-800/60 backdrop-blur-md shadow-xl hover:shadow-2xl hover:border-slate-700 transition-all duration-300 group`}>
            <div className="flex justify-between items-start relative z-10">
                <div>
                    <p className="text-slate-400 font-medium text-sm uppercase tracking-wider mb-2">{title}</p>
                    <h3 className="text-3xl font-bold tracking-tight text-white group-hover:scale-105 transition-transform origin-left">
                        {value}
                    </h3>
                    {subtitle && <p className="text-xs text-slate-500 mt-1">{subtitle}</p>}
                </div>
                <div className="p-3 bg-slate-900/50 rounded-xl border border-slate-700/50">
                    {icon}
                </div>
            </div>
            <div className="absolute -bottom-10 -right-10 w-32 h-32 bg-white/5 blur-3xl rounded-full pointer-events-none"></div>
        </div>
    );
}
