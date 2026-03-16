import { useEffect, useState } from 'react';
import { api } from '../services/api';
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
    PieChart, Pie, Cell, Legend
} from 'recharts';
import { Briefcase, Building2, MapPin, MonitorPlay, Activity, Map, Heart, Scale, LayoutDashboard, TrendingUp } from 'lucide-react';
import ColombiaMap from './ColombiaMap';
import InclusionPanel from './InclusionPanel';
import GapAnalysis from './GapAnalysis';
import ExportButton from './ExportButton';
import TrendsSection from './TrendsSection';

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#14b8a6', '#f97316'];

const TABS = [
    { id: 'general', label: 'General', icon: LayoutDashboard },
    { id: 'territorial', label: 'Territorial', icon: Map },
    { id: 'trends', label: 'Tendencias', icon: TrendingUp },
    { id: 'inclusion', label: 'Inclusión', icon: Heart },
    { id: 'brechas', label: 'Brechas', icon: Scale },
];


export default function Dashboard() {
    const [stats, setStats] = useState(null);
    const [departments, setDepartments] = useState([]);
    const [sectors, setSectors] = useState([]);
    const [scraperStatus, setScraperStatus] = useState(null);
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState('general');

    const fetchData = async () => {
        try {
            const [resStats, resDepts, resSectors, resScraper] = await Promise.all([
                api.getStats(),
                api.getByDepartment(),
                api.getBySector(),
                api.getScraperStatus()
            ]);
            setStats(resStats);
            setDepartments(resDepts);
            setSectors(resSectors);
            setScraperStatus(resScraper);
        } catch (error) {
            console.error("Error fetching data:", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
        const interval = setInterval(fetchData, 3000);
        return () => clearInterval(interval);
    }, []);

    if (loading) return <div className="min-h-screen flex items-center justify-center bg-slate-900 text-white"><div className="animate-pulse text-2xl font-bold">Cargando datos...</div></div>;

    return (
        <div className="min-h-screen bg-slate-950 text-slate-200 p-6 md:p-10 font-sans">

            {/* HEADER */}
            <header className="mb-8 flex flex-col md:flex-row justify-between items-start md:items-center">
                <div>
                    <h1 className="text-4xl font-extrabold bg-gradient-to-r from-blue-400 to-indigo-500 bg-clip-text text-transparent mb-2">
                        Vacantes Colombia — BID Analytics
                    </h1>
                    <p className="text-slate-400">Dashboard analítico del mercado laboral para política pública</p>
                </div>

                <div className="mt-4 md:mt-0 flex items-center gap-4">
                    {/* EXPORT BUTTON */}
                    <ExportButton />

                    {/* SCRAPER STATUS */}
                    <div className="p-3 rounded-xl bg-slate-900/50 border border-slate-800 backdrop-blur-sm flex items-center gap-3">
                        <Activity className={`w-4 h-4 ${scraperStatus?.running ? 'text-green-400 animate-pulse' : 'text-slate-500'}`} />
                        <span className="text-sm font-medium">{scraperStatus?.running ? 'Scraper activo' : 'Inactivo'}</span>
                        <span className="text-xs text-slate-400 border-l border-slate-700 pl-3">
                            <span className="font-mono text-white">{(scraperStatus?.registros_nuevos || 0).toLocaleString()}</span> rec. nuevos
                        </span>
                    </div>
                </div>
            </header>

            {/* TAB NAVIGATION */}
            <nav className="flex gap-1 mb-8 p-1 bg-slate-900/50 border border-slate-800 rounded-xl w-fit">
                {TABS.map(tab => {
                    const Icon = tab.icon;
                    return (
                        <button
                            key={tab.id}
                            onClick={() => setActiveTab(tab.id)}
                            className={`flex items-center gap-2 px-4 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 ${
                                activeTab === tab.id
                                    ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/25'
                                    : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
                            }`}
                        >
                            <Icon className="w-4 h-4" />
                            {tab.label}
                        </button>
                    );
                })}
            </nav>

            {/* TAB CONTENT */}
            {activeTab === 'general' && (
                <>
                    {/* KPI CARDS */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 mb-10">
                        {[
                            { title: "Total Vacantes", value: stats?.total_vacantes?.toLocaleString(), icon: <Briefcase className="w-7 h-7 text-blue-400" />, color: "from-blue-500/20 to-blue-400/5" },
                            { title: "Total Plazas", value: stats?.total_plazas?.toLocaleString(), icon: <Building2 className="w-7 h-7 text-emerald-400" />, color: "from-emerald-500/20 to-emerald-400/5" },
                            { title: "Teletrabajo", value: `${stats?.teletrabajo_pct?.toFixed(1)}%`, icon: <MonitorPlay className="w-7 h-7 text-purple-400" />, color: "from-purple-500/20 to-purple-400/5" },
                            { title: "Discapacidad", value: `${stats?.discapacidad_pct?.toFixed(1)}%`, icon: <Heart className="w-7 h-7 text-pink-400" />, color: "from-pink-500/20 to-pink-400/5" },
                            { title: "Plaza Práctica", value: `${stats?.plaza_practica_pct?.toFixed(1) || 0}%`, icon: <Activity className="w-7 h-7 text-amber-400" />, color: "from-amber-500/20 to-amber-400/5" },
                        ].map((kpi, i) => (
                            <div key={i} className={`relative overflow-hidden p-5 rounded-2xl bg-gradient-to-br ${kpi.color} border border-slate-800/60 backdrop-blur-md shadow-xl hover:shadow-2xl hover:border-slate-700 transition-all duration-300 group`}>
                                <div className="flex justify-between items-start relative z-10">
                                    <div>
                                        <p className="text-slate-400 font-medium text-xs uppercase tracking-wider mb-1">{kpi.title}</p>
                                        <h3 className="text-3xl font-bold tracking-tight text-white group-hover:scale-105 transition-transform origin-left">{kpi.value}</h3>
                                    </div>
                                    <div className="p-2.5 bg-slate-900/50 rounded-xl border border-slate-700/50">
                                        {kpi.icon}
                                    </div>
                                </div>
                                <div className="absolute -bottom-10 -right-10 w-32 h-32 bg-white/5 blur-3xl rounded-full pointer-events-none"></div>
                            </div>
                        ))}
                    </div>

                    {/* CHARTS */}
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                        {/* BAR CHART: DEPARTMENTS */}
                        <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800 backdrop-blur-sm shadow-lg">
                            <h2 className="text-xl font-bold mb-6 flex items-center gap-2"><MapPin className="text-indigo-400" /> Top 10 Departamentos</h2>
                            <div className="h-[400px] w-full">
                                <ResponsiveContainer width="100%" height="100%">
                                    <BarChart data={departments} layout="vertical" margin={{ top: 0, right: 30, left: 40, bottom: 0 }}>
                                        <CartesianGrid strokeDasharray="3 3" stroke="#334155" horizontal={true} vertical={false} />
                                        <XAxis type="number" stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
                                        <YAxis dataKey="departamento" type="category" stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} width={100} />
                                        <Tooltip cursor={{ fill: '#1e293b' }} contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#fff' }} />
                                        <Bar dataKey="total" fill="#3b82f6" radius={[0, 4, 4, 0]}>
                                            {departments.map((entry, index) => (
                                                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                            ))}
                                        </Bar>
                                    </BarChart>
                                </ResponsiveContainer>
                            </div>
                        </div>

                        {/* PIE CHART: SECTORS */}
                        <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800 backdrop-blur-sm shadow-lg">
                            <h2 className="text-xl font-bold mb-6 flex items-center gap-2"><Building2 className="text-indigo-400" /> Top Sectores Económicos</h2>
                            <div className="h-[400px] w-full">
                                <ResponsiveContainer width="100%" height="100%">
                                    <PieChart>
                                        <Pie
                                            data={sectors}
                                            cx="50%"
                                            cy="50%"
                                            innerRadius={80}
                                            outerRadius={140}
                                            paddingAngle={5}
                                            dataKey="total"
                                            nameKey="sector"
                                            stroke="none"
                                        >
                                            {sectors.map((entry, index) => (
                                                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                            ))}
                                        </Pie>
                                        <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#fff' }} />
                                        <Legend verticalAlign="bottom" height={36} iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                                    </PieChart>
                                </ResponsiveContainer>
                            </div>
                        </div>
                    </div>
                </>
            )}

            {activeTab === 'territorial' && <ColombiaMap />}
            {activeTab === 'trends' && <TrendsSection />}
            {activeTab === 'inclusion' && <InclusionPanel />}
            {activeTab === 'brechas' && <GapAnalysis />}

        </div>
    );
}
