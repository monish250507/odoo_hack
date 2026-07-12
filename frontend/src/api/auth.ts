import apiClient from './client'

export interface LoginPayload { email: string; password: string }
export interface RegisterPayload { email: string; password: string; full_name: string }
export interface AuthResponse { access_token: string; refresh_token: string; token_type: string; user: UserProfile }
export interface UserProfile { id: string; email: string; full_name: string; role: string; department_id?: string; points: number }

export const authApi = {
  login: (payload: LoginPayload) =>
    apiClient.post<AuthResponse>('/api/v1/auth/login', payload).then(r => r.data),
  register: (payload: RegisterPayload) =>
    apiClient.post<AuthResponse>('/api/v1/auth/register', payload).then(r => r.data),
  me: () =>
    apiClient.get<UserProfile>('/api/v1/auth/me').then(r => r.data),
  logout: () =>
    apiClient.post('/api/v1/auth/logout').then(r => r.data),
}
