import axios from "axios";

const api = axios.create({
  baseURL: "/api",
});

export default {
  getStats: () => api.get("/dashboard/stats"),
  getSeverityBreakdown: () => api.get("/dashboard/severity-breakdown"),
  getTopTechniques: (limit = 10) =>
    api.get(`/dashboard/top-techniques?limit=${limit}`),
  getAlertVolume: (days = 30) =>
    api.get(`/dashboard/alert-volume?days=${days}`),

  getAlerts: (params = {}) => api.get("/alerts/", { params }),
  getAlert: (id) => api.get(`/alerts/${id}`),
  createAlert: (data) => api.post("/alerts/", data),
  updateAlert: (id, data) => api.patch(`/alerts/${id}`, data),
  deleteAlert: (id) => api.delete(`/alerts/${id}`),

  enrichAlert: (alertId) => api.post(`/enrichment/${alertId}`),
  lookupIndicator: (indicator, indicatorType) =>
    api.post("/enrichment/lookup", {
      indicator,
      indicator_type: indicatorType,
    }),

  getMitreTactics: () => api.get("/mitre/tactics"),
  getMitreTechniques: () => api.get("/mitre/techniques"),
  getMitreCoverage: () => api.get("/mitre/coverage"),
};
