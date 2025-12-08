const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const getHeaders = () => {
  const headers = {
    'Content-Type': 'application/json',
  };
  // @ts-ignore
  const token = localStorage.getItem('jwt_token');
  if (token) {
    // @ts-ignore
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
};

const handleResponse = async (response) => {
  if (response.status === 204) {
    return {}; // No content to parse
  }
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'API request failed');
  }
  return response.json();
};

const api = {
  get: async (endpoint) => {
    const response = await fetch(`${BASE_URL}${endpoint}`, {
      method: 'GET',
      headers: getHeaders(),
    });
    return handleResponse(response);
  },
  post: async (endpoint, data, options = {}) => {
    const response = await fetch(`${BASE_URL}${endpoint}`, {
      method: 'POST',
      headers: { ...getHeaders(), ...options.headers },
      body: data instanceof URLSearchParams ? data.toString() : JSON.stringify(data),
    });
    return handleResponse(response);
  },
  put: async (endpoint, data) => {
    const response = await fetch(`${BASE_URL}${endpoint}`, {
      method: 'PUT',
      headers: getHeaders(),
      body: JSON.stringify(data)
    });
    return handleResponse(response);
  },
  delete: async (endpoint) => {
    const response = await fetch(`${BASE_URL}${endpoint}`, {
      method: 'DELETE',
      headers: getHeaders()
    });
    return handleResponse(response);
  }
};

// --- Category Specific Functions ---
export const getCategories = () => {
  return api.get('/api/v1/categories/');
};

export const createCategory = (name: string, emoji?: string) => {
  return api.post('/api/v1/categories/', { name, emoji });
};

export const updateCategory = (id: string, name: string, emoji?: string) => {
  return api.put(`/api/v1/categories/${id}`, { name, emoji });
};

export const deleteCategory = (id: string) => {
  return api.delete(`/api/v1/categories/${id}`);
};

// --- Transaction Specific Functions ---
export const getTransactions = () => {
  return api.get('/api/v1/transactions/');
};

export const createTransaction = (transaction) => {
  return api.post('/api/v1/transactions/', transaction);
};

export const updateTransaction = (id, transaction) => {
  return api.put(`/api/v1/transactions/${id}`, transaction);
};

export const deleteTransaction = (id) => {
  return api.delete(`/api/v1/transactions/${id}`);
};

export const getSummary = () => {
  return api.get('/api/v1/dashboard/summary');
};

export const getChartData = () => {
  return api.get('/api/v1/dashboard/chart-data');
};

// --- Auth Specific Functions ---
export const registerUser = (email: string, password: string) => {
  return api.post('/api/v1/auth/signup', { email, password });
};

export const loginUser = (email: string, password: string) => {
  const formData = new URLSearchParams();
  formData.append('username', email);
  formData.append('password', password);
  return api.post('/api/v1/auth/login', formData, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  });
};

export const exportTransactions = async () => {
  const response = await fetch(`${BASE_URL}/api/v1/export/csv`, {
    method: 'GET',
    headers: getHeaders(),
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Export failed');
  }
  return response.blob();
};

export default api;
