const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/v1'

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: { ...(options.body instanceof FormData ? {} : { 'Content-Type': 'application/json' }), ...(options.headers || {}) }
  })
  if (response.status === 204) return null
  const payload = await response.json().catch(() => ({}))
  if (!response.ok) throw new Error(payload.detail || 'No fue posible completar la solicitud')
  return payload
}

export const api = {
  login: (email, password) => {
    const body = new URLSearchParams({ username: email, password })
    return request('/auth/login', { method: 'POST', body, headers: { 'Content-Type': 'application/x-www-form-urlencoded' } })
  },
  register: (data) => request('/auth/registro', { method: 'POST', body: JSON.stringify(data) }),
  me: (token) => request('/auth/me', { headers: { Authorization: `Bearer ${token}` } }),
  getBook: (token, id) => request(`/libros/${id}`, { headers: { Authorization: `Bearer ${token}` } }),
  createBook: (token, data) => request('/libros', { method: 'POST', body: JSON.stringify(data), headers: { Authorization: `Bearer ${token}` } }),
  uploadCover: (token, id, file) => {
    const form = new FormData(); form.append('archivo', file)
    return request(`/libros/${id}/portada`, { method: 'POST', body: form, headers: { Authorization: `Bearer ${token}` } })
  },
  logout: (token) => request('/auth/logout', { method: 'POST', body: JSON.stringify({ refresh_token: token }) })
}
