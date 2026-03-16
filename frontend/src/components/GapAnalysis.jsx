import { useEffect, useState } from 'react';
import { api } from '../services/api';
import {
    ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip,
    ResponsiveContainer, ZAxis, Cell
} from 'recharts';
import { Scale, Filter, AlertTriangle } from 'lucide-react';

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#14b8a6', '#f97316'];

// Assign numeric value to salary ranges for scatter plot
function salaryToNumeric(rango) {
    if (!rango) return 0;
    const r = rango.toUpperCase();
    if (r.includes('NO DEFINIDO') || r.includes('A CONVENIR')) return 1;
    if (r.includes('MENOS') || r.includes('< 1') || r.includes('MINIMO') || r.includes('SMMLV')) return 2;
    if (r.includes('1') && r.includes('2')) return 3;
    if (r.includes('2') && r.includes('4')) return 4;
    if (r.includes('4') && r.includes('6')) return 5;
    if (r.includes('6') && r.includes('8')) return 6;
    if (r.includes('8') || r.includes('MAS') || r.includes('MÁS') || r.includes('>')) return 7;
    return 1;
}

function educationToNumeric(nivel) {
    if (!nivel) return 0;
    const n = nivel.toUpperCase();
    if (n.includes('PRIMARIA')) return 1;
    if (n.includes('BACHILLER') || n.includes('SECUNDARIA')) return 2;
    if (n.includes('TEC') && !n.includes('TECNOLOGO') && !n.includes('TECNÓLOGO')) return 3;
    if (n.includes('TECNOLOGO') || n.includes('TECNÓLOGO')) return 4;
    if (n.includes('PROFESIONAL') || n.includes('UNIVERSIT')) return 5;
    if (n.includes('ESPECIALIZACION') || n.includes('ESPECIALIZACIÓN')) return 6;
    if (n.includes('MAESTRIA') || n.includes('MAESTRÍA') || n.includes('DOCTORADO')) return 7;
    return 2;
}

export default function GapAnalysis() {
    const [data, setData] = useState(null);
    const [sector, setSector] = useState('');
    const [loading, setLoading] = useState(true);

    const fetchBrechas = (sectorFilter) => {
        setLoading(true);
        api.getBrechas(sectorFilter || undefined)
            .then(d => setData(d))
            .catch(err => console.error('Error loading gap data:', err))
            .finally(() => setLoading(false));
    };

    useEffect(() => {
        fetchBrechas('');
    }, []);

    const handleSectorChange = (e) => {
        const val = e.target.value;
        setSector(val);
        fetchBrechas(val);
    };

    if (loading && !data) {
        return (
            <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800 backdrop-blur-sm shadow-lg h-[400px] flex items-center justify-center">
                <div className="animate-pulse text-slate-400">Cargando análisis de brechas...</div>
            </div>
        );
    }

    // Prepare scatter data
    const scatterData = (data?.brechas || []).map((b, i) => ({
        x: salaryToNumeric(b.rango_salarial),
        y: b.experiencia_promedio_meses,
        z: b.total_vacantes,
        sector: b.sector,
        nivel_estudios: b.nivel_estudios,
        rango_salarial: b.rango_salarial,
        total_plazas: b.total_plazas,
        colorIdx: i,
    }));

    return (
        <div className="space-y-8">
            {/* HEADER + FILTER */}
            <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800 backdrop-blur-sm shadow-lg">
                <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
                    <div>
                        <h2 className="text-xl font-bold flex items-center gap-2">
                            <Scale className="text-amber-400 w-5 h-5" />
                            Análisis de Brechas Oferta-Demanda
                        </h2>
                        <p className="text-sm text-slate-400 mt-1">
                            Cruce de nivel educativo × rango salarial × experiencia requerida por sector.
                            Identifica vacantes desalineadas.
                        </p>
                    </div>
                    <div className="flex items-center gap-2">
                        <Filter className="text-slate-400 w-4 h-4" />
                        <select
                            value={sector}
                            onChange={handleSectorChange}
                            className="bg-slate-800 border border-slate-700 text-white rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                        >
                            <option value="">Todos los sectores</option>
                            {(data?.sectores_disponibles || []).map(s => (
                                <option key={s} value={s}>{s}</option>
                            ))}
                        </select>
                    </div>
                </div>

                {/* SCATTER CHART */}
                <div className="h-[450px] w-full">
                    <ResponsiveContainer width="100%" height="100%">
                        <ScatterChart margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                            <XAxis
                                type="number"
                                dataKey="x"
                                name="Salario"
                                domain={[0, 8]}
                                ticks={[1, 2, 3, 4, 5, 6, 7]}
                                tickFormatter={(v) => {
                                    const labels = ['', 'N/D', '<1 SMMLV', '1-2 SMMLV', '2-4 SMMLV', '4-6 SMMLV', '6-8 SMMLV', '>8 SMMLV'];
                                    return labels[v] || '';
                                }}
                                stroke="#94a3b8"
                                fontSize={10}
                                angle={-25}
                                textAnchor="end"
                            />
                            <YAxis
                                type="number"
                                dataKey="y"
                                name="Experiencia (meses)"
                                stroke="#94a3b8"
                                fontSize={12}
                                label={{
                                    value: 'Experiencia (meses)',
                                    angle: -90,
                                    position: 'insideLeft',
                                    style: { fill: '#94a3b8', fontSize: 12 },
                                }}
                            />
                            <ZAxis
                                type="number"
                                dataKey="z"
                                range={[50, 800]}
                                name="Vacantes"
                            />
                            <Tooltip
                                cursor={{ strokeDasharray: '3 3' }}
                                content={({ payload }) => {
                                    if (!payload || !payload.length) return null;
                                    const d = payload[0].payload;
                                    return (
                                        <div className="bg-slate-800/95 border border-slate-700 rounded-lg p-3 text-sm shadow-xl">
                                            <p className="font-bold text-white mb-1">{d.sector}</p>
                                            <p className="text-slate-300">Estudios: <span className="text-blue-400">{d.nivel_estudios}</span></p>
                                            <p className="text-slate-300">Salario: <span className="text-emerald-400">{d.rango_salarial}</span></p>
                                            <p className="text-slate-300">Experiencia: <span className="text-amber-400">{d.y} meses</span></p>
                                            <p className="text-slate-300">Vacantes: <span className="text-white font-bold">{d.z}</span></p>
                                            <p className="text-slate-300">Plazas: <span className="text-white">{d.total_plazas}</span></p>
                                        </div>
                                    );
                                }}
                            />
                            <Scatter data={scatterData} shape="circle">
                                {scatterData.map((entry, index) => (
                                    <Cell
                                        key={index}
                                        fill={COLORS[index % COLORS.length]}
                                        fillOpacity={0.7}
                                    />
                                ))}
                            </Scatter>
                        </ScatterChart>
                    </ResponsiveContainer>
                </div>
            </div>

            {/* TABLE: Top brechas */}
            <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800 backdrop-blur-sm shadow-lg overflow-x-auto">
                <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                    <AlertTriangle className="text-amber-400 w-5 h-5" />
                    Detalle de Brechas {sector && `— ${sector}`}
                </h3>
                <table className="w-full text-sm text-left">
                    <thead>
                        <tr className="text-slate-400 border-b border-slate-700">
                            <th className="py-3 px-2 font-medium">Sector</th>
                            <th className="py-3 px-2 font-medium">Nivel Estudios</th>
                            <th className="py-3 px-2 font-medium">Rango Salarial</th>
                            <th className="py-3 px-2 font-medium text-right">Exp. Prom. (meses)</th>
                            <th className="py-3 px-2 font-medium text-right">Vacantes</th>
                            <th className="py-3 px-2 font-medium text-right">Plazas</th>
                        </tr>
                    </thead>
                    <tbody>
                        {(data?.brechas || []).slice(0, 20).map((b, i) => (
                            <tr key={i} className="border-b border-slate-800/50 hover:bg-slate-800/30 transition-colors">
                                <td className="py-2 px-2 text-white">{b.sector}</td>
                                <td className="py-2 px-2 text-blue-400">{b.nivel_estudios}</td>
                                <td className="py-2 px-2 text-emerald-400">{b.rango_salarial}</td>
                                <td className="py-2 px-2 text-right text-amber-400 font-mono">{b.experiencia_promedio_meses}</td>
                                <td className="py-2 px-2 text-right text-white font-mono font-bold">{b.total_vacantes}</td>
                                <td className="py-2 px-2 text-right text-slate-300 font-mono">{b.total_plazas}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                {(data?.brechas || []).length === 0 && (
                    <p className="text-slate-500 text-center py-8">
                        No hay datos de brechas con los filtros actuales.
                    </p>
                )}
            </div>
        </div>
    );
}
