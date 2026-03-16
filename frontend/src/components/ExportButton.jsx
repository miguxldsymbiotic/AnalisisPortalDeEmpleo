import { useState } from 'react';
import { Download, FileSpreadsheet, FileText, ChevronDown, Loader2 } from 'lucide-react';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export default function ExportButton({ filters = {} }) {
    const [open, setOpen] = useState(false);
    const [loading, setLoading] = useState(false);

    const handleExport = async (formato) => {
        setLoading(true);
        setOpen(false);

        try {
            const params = new URLSearchParams();
            params.set('formato', formato);
            if (filters.departamento) params.set('departamento', filters.departamento);
            if (filters.sector) params.set('sector', filters.sector);
            if (filters.tipo_contrato) params.set('tipo_contrato', filters.tipo_contrato);
            if (filters.nivel_estudios) params.set('nivel_estudios', filters.nivel_estudios);

            const url = `${API_BASE_URL}/vacantes/exportar?${params.toString()}`;

            const res = await fetch(url);
            if (!res.ok) throw new Error('Error en la descarga');

            const blob = await res.blob();
            const downloadUrl = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = downloadUrl;
            a.download = formato === 'csv' ? 'vacantes_colombia.csv' : 'vacantes_colombia.xlsx';
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(downloadUrl);
        } catch (err) {
            console.error('Export error:', err);
            alert('Error al exportar. Intenta de nuevo.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="relative">
            <button
                onClick={() => setOpen(!open)}
                disabled={loading}
                className="flex items-center gap-2 px-4 py-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white rounded-xl font-medium text-sm shadow-lg hover:shadow-xl transition-all duration-300 disabled:opacity-50"
            >
                {loading ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                    <Download className="w-4 h-4" />
                )}
                Exportar datos
                <ChevronDown className={`w-4 h-4 transition-transform ${open ? 'rotate-180' : ''}`} />
            </button>

            {open && (
                <div className="absolute right-0 top-full mt-2 w-52 bg-slate-800 border border-slate-700 rounded-xl shadow-2xl z-50 overflow-hidden">
                    <button
                        onClick={() => handleExport('csv')}
                        className="flex items-center gap-3 w-full px-4 py-3 text-left text-sm text-slate-200 hover:bg-slate-700/50 transition-colors"
                    >
                        <FileText className="w-4 h-4 text-green-400" />
                        <div>
                            <p className="font-medium">CSV</p>
                            <p className="text-xs text-slate-400">Para análisis en cualquier herramienta</p>
                        </div>
                    </button>
                    <hr className="border-slate-700" />
                    <button
                        onClick={() => handleExport('xlsx')}
                        className="flex items-center gap-3 w-full px-4 py-3 text-left text-sm text-slate-200 hover:bg-slate-700/50 transition-colors"
                    >
                        <FileSpreadsheet className="w-4 h-4 text-blue-400" />
                        <div>
                            <p className="font-medium">Excel (XLSX)</p>
                            <p className="text-xs text-slate-400">Con formato y estilos</p>
                        </div>
                    </button>
                </div>
            )}
        </div>
    );
}
