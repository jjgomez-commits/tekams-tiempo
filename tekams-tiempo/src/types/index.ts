export interface TimeEntry {
  id: string
  user_id: string
  project_id: string
  tool_id: string
  week: string
  hours: number
  created_at: string
}

export interface User {
  id: string
  name: string
  email: string
  role: 'admin' | 'user'
  cost_per_hour: number
  created_at: string
}

export interface Project {
  id: string
  name: string
  created_at: string
}
