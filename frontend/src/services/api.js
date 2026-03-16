const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export const api = {
    // ─── Estadísticas existentes ────────────────────────────────────
    getStats: async () => {
        const res = await fetch(`${API_BASE_URL}/estadisticas/resumen`);
        if (!res.ok) throw new Error("Network response was not ok");
        return res.json();
    },
    getByDepartment: async () => {
        const res = await fetch(`${API_BASE_URL}/estadisticas/por-departamento`);
        if (!res.ok) throw new Error("Network response was not ok");
        return res.json();
    },
    getBySector: async () => {
        const res = await fetch(`${API_BASE_URL}/estadisticas/por-sector`);
        if (!res.ok) throw new Error("Network response was not ok");
        return res.json();
    },
    getSalaries: async () => {
        const res = await fetch(`${API_BASE_URL}/estadisticas/salarios`);
        if (!res.ok) throw new Error("Network response was not ok");
        return res.json();
    },

    // ─── Scraper ────────────────────────────────────────────────────
    getScraperStatus: async () => {
        const res = await fetch(`${API_BASE_URL}/scraper/estado`);
        if (!res.ok) throw new Error("Network response was not ok");
        return res.json();
    },
    startScraper: async () => {
        const res = await fetch(`${API_BASE_URL}/scraper/iniciar`, { method: 'POST' });
        if (!res.ok) throw new Error("Network response was not ok");
        return res.json();
    },

    // ─── Nuevos endpoints BID ───────────────────────────────────────
    getTerritorial: async () => {
        const res = await fetch(`${API_BASE_URL}/estadisticas/territorial`);
        if (!res.ok) throw new Error("Network response was not ok");
        return res.json();
    },
    getInclusion: async () => {
        const res = await fetch(`${API_BASE_URL}/estadisticas/inclusion`);
        if (!res.ok) throw new Error("Network response was not ok");
        return res.json();
    },
    getBrechas: async (sector) => {
        const params = new URLSearchParams();
        if (sector) params.set('sector', sector);
        const url = `${API_BASE_URL}/estadisticas/brechas${params.toString() ? '?' + params.toString() : ''}`;
        const res = await fetch(url);
        if (!res.ok) throw new Error("Network response was not ok");
        return res.json();
    },
    getTendencias: async () => {
        const res = await fetch(`${API_BASE_URL}/estadisticas/tendencias`);
        if (!res.ok) throw new Error("Network response was not ok");
        return res.json();
    },


    // ─── Exportación ────────────────────────────────────────────────
    exportData: async (filters = {}, formato = 'csv') => {
        const params = new URLSearchParams({ formato });
        Object.entries(filters).forEach(([k, v]) => {
            if (v) params.set(k, v);
        });
        const url = `${API_BASE_URL}/vacantes/exportar?${params.toString()}`;
        const res = await fetch(url);
        if (!res.ok) throw new Error("Network response was not ok");
        return res.blob();
    },
};
