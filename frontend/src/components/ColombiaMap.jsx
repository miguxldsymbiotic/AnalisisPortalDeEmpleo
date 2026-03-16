import { useEffect, useState } from 'react';
import {
    ComposableMap,
    Geographies,
    Geography,
    ZoomableGroup,
} from 'react-simple-maps';
import { api } from '../services/api';

// Colombia departamentos GeoJSON local
const COLOMBIA_GEO_URL = '/colombia.json';

// Normalización avanzada para matching de departamentos
function normalize(str) {
    if (!str) return '';
    return str
        .toUpperCase()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .replace(/\b(D\.C\.|DISTRITO CAPITAL|BOGOTA DC)\b/g, 'D.C.')
        .replace(/[^A-Z]/g, ' ')
        .replace(/\s+/g, ' ')
        .trim();
}

function getColor(count, max) {
    if (!count || !max) return '#1e293b';
    const ratio = count / max;
    if (ratio > 0.4) return '#1d4ed8'; // Blue intense
    if (ratio > 0.2) return '#3b82f6';
    if (ratio > 0.1) return '#60a5fa';
    if (ratio > 0.05) return '#93c5fd';
    if (ratio > 0.01) return '#bfdbfe';
    return '#334155';
}

export default function ColombiaMap() {
    const [territorial, setTerritorial] = useState([]);
    const [tooltip, setTooltip] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.getTerritorial()
            .then(data => setTerritorial(data))
            .catch(err => console.error('Error loading territorial data:', err))
            .finally(() => setLoading(false));
    }, []);

    const maxVacantes = territorial.length
        ? Math.max(...territorial.map(d => d.total_vacantes))
        : 1;

    // Mapa de datos por nombre normalizado
    const dataByDept = {};
    territorial.forEach(d => {
        dataByDept[normalize(d.departamento)] = d;
    });

    if (loading) {
        return (
            <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800 backdrop-blur-sm shadow-lg h-[600px] flex items-center justify-center">
                <div className="animate-pulse text-slate-400">Cargando mapa territorial...</div>
            </div>
        );
    }

    return (
        <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800 backdrop-blur-sm shadow-lg relative">
            <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                <span className="text-2xl">🗺️</span> Mapa Territorial — Concentración de Vacantes
            </h2>
            <p className="text-sm text-slate-400 mb-6">
                Concentración de la demanda laboral por departamento. Hover para ver detalles por región.
            </p>

            <div className="h-[550px] w-full relative bg-slate-950/20 rounded-xl overflow-hidden">
                <ComposableMap
                    projection="geoMercator"
                    projectionConfig={{
                        scale: 1900,
                        center: [-74, 4.5],
                    }}
                    style={{ width: '100%', height: '100%' }}
                >
                    <ZoomableGroup zoom={1} minZoom={1} maxZoom={8}>
                        <Geographies geography={COLOMBIA_GEO_URL}>
                            {({ geographies }) =>
                                geographies.map(geo => {
                                    // Try all common variants for property name
                                    const rawName = 
                                        geo.properties.NOMBRE_DPT || 
                                        geo.properties.DEPARTAMEN || 
                                        geo.properties.name || 
                                        geo.properties.DPTO_NOMBRE ||
                                        geo.properties.NOMBRE;
                                    
                                    const geoNameNorm = normalize(rawName);
                                    const deptData = dataByDept[geoNameNorm];

                                    return (
                                        <Geography
                                            key={geo.rsmKey}
                                            geography={geo}
                                            fill={getColor(deptData?.total_vacantes || 0, maxVacantes)}
                                            stroke="#0f172a"
                                            strokeWidth={0.5}
                                            style={{
                                                default: { outline: 'none', transition: 'all 250ms' },
                                                hover: {
                                                    fill: '#fbbf24',
                                                    outline: 'none',
                                                    cursor: 'pointer',
                                                },
                                                pressed: { outline: 'none' },
                                            }}
                                            onMouseEnter={() => {
                                                setTooltip({
                                                    name: rawName,
                                                    data: deptData,
                                                });
                                            }}
                                            onMouseLeave={() => setTooltip(null)}
                                        />
                                    );
                                })
                            }
                        </Geographies>
                    </ZoomableGroup>
                </ComposableMap>

                {/* TOOLTIP OVERLAY */}
                {tooltip && (
                    <div className="absolute top-4 right-4 p-5 bg-slate-900/95 border border-slate-700 rounded-xl backdrop-blur-md shadow-2xl min-w-[280px] z-50 animate-in fade-in zoom-in duration-200">
                        <h3 className="font-bold text-white text-lg mb-3 pb-2 border-b border-slate-700">
                            {tooltip.name}
                        </h3>
                        {tooltip.data ? (
                            <div className="space-y-2 text-sm">
                                <div className="flex justify-between items-center">
                                    <span className="text-slate-400">Total Vacantes:</span>
                                    <span className="text-blue-400 font-bold text-base">
                                        {tooltip.data.total_vacantes?.toLocaleString()}
                                    </span>
                                </div>
                                <div className="flex justify-between items-center">
                                    <span className="text-slate-400">Plazas Disponibles:</span>
                                    <span className="text-white font-mono">
                                        {tooltip.data.total_plazas?.toLocaleString()}
                                    </span>
                                </div>
                                <div className="pt-2">
                                    <span className="text-slate-500 text-xs block mb-1">SALARIO PREDOMINANTE</span>
                                    <span className="text-emerald-400 font-medium">
                                        {tooltip.data.salario_predominante}
                                    </span>
                                </div>
                                <div>
                                    <span className="text-slate-500 text-xs block mb-1">SECTOR PRINCIPAL</span>
                                    <span className="text-indigo-400 font-medium line-clamp-1">
                                        {tooltip.data.sector_top}
                                    </span>
                                </div>
                                <div className="grid grid-cols-2 gap-2 pt-3">
                                    <div className="bg-slate-800/50 p-2 rounded-lg text-center">
                                        <span className="text-[10px] text-slate-500 block">REMOTO</span>
                                        <span className="text-purple-400 font-bold">{tooltip.data.teletrabajo_pct}%</span>
                                    </div>
                                    <div className="bg-slate-800/50 p-2 rounded-lg text-center">
                                        <span className="text-[10px] text-slate-500 block">INCLUSIÓN</span>
                                        <span className="text-pink-400 font-bold">{tooltip.data.discapacidad_pct}%</span>
                                    </div>
                                </div>
                            </div>
                        ) : (
                            <div className="py-4 text-center">
                                <p className="text-slate-500 text-sm">No se encontraron vacantes activas en este departamento.</p>
                            </div>
                        )}
                    </div>
                )}
            </div>

            {/* LEGEND */}
            <div className="flex flex-col items-center gap-3 mt-8">
                <div className="flex items-center gap-2">
                    <span className="text-[10px] text-slate-500 uppercase tracking-wider">Menos</span>
                    <div className="flex h-2">
                        {['#334155', '#bfdbfe', '#93c5fd', '#60a5fa', '#3b82f6', '#1d4ed8'].map((c, i) => (
                            <div key={i} className="w-10 h-full first:rounded-l-full last:rounded-r-full" style={{ backgroundColor: c }} />
                        ))}
                    </div>
                    <span className="text-[10px] text-slate-500 uppercase tracking-wider">Más</span>
                </div>
                <p className="text-[10px] text-slate-500">Distribución porcentual de vacantes sobre el total nacional</p>
            </div>
        </div>
    );
}
