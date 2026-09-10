'use client'

import { useState, useEffect } from 'react'
import { supabase } from '@/lib/supabase'

const TOOLS = ['H00', 'H01', 'H05', 'H06', 'H09', 'H12', 'H15', 'H17']
const TOOL_NAMES: Record<string, string> = {
  'H00': 'PLAN DIRECTOR',
  'H01': 'PRESUPUESTO ANUAL',
  'H05': 'ARGUMENTARIO COMERCIAL',
  'H06': 'ASSESSMENT COMERCIAL',
  'H09': 'TEATRO DE VENTAS',
  'H12': 'PLAN DE VENTAS',
  'H15': 'SESIÓN CUSTOMER FOCUS',
  'H17': 'ESTRATEGIA DE MARKETING'
}

const PROJECTS = [
  { id: '01', name: '01. Tovar' },
  { id: '02', name: '02. HJO' },
  { id: '03', name: '03. NGS' },
  { id: '04', name: '04. Grupo GAM' }
]

const USERS = ['Jose', 'Antonio', 'JuanJo', 'Jon', 'Paula', 'Puri', 'Fran']
const ADMINS = ['Jose', 'Antonio', 'JuanJo', 'Jon']

export default function TimeMatrix() {
  const [viewType, setViewType] = useState<'projects' | 'weeks'>('projects')
  const [viewMode, setViewMode] = useState<'hours' | 'euros'>('hours')
  const [currentUser, setCurrentUser] = useState('Jose')
  const [selectedUser, setSelectedUser] = useState('')
  const [data, setData] = useState<Record<string, Record<string, Record<string, number>>>>({})
  const [loading, setLoading] = useState(true)

  const isAdmin = ADMINS.includes(currentUser)

  // Cargar datos de Supabase
  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const { data: entries, error } = await supabase
        .from('time_entries')
        .select('*')

      if (error) throw error

      // Procesar datos
      const processed: Record<string, Record<string, Record<string, number>>> = {}
      entries?.forEach((entry: any) => {
        if (!processed[entry.tool_id]) processed[entry.tool_id] = {}
        if (!processed[entry.tool_id][entry.project_id]) processed[entry.tool_id][entry.project_id] = 0
        processed[entry.tool_id][entry.project_id] += entry.hours || 0
      })

      setData(processed)
    } catch (error) {
      console.error('Error loading data:', error)
    } finally {
      setLoading(false)
    }
  }

  const renderMatrix = () => {
    if (viewType === 'projects') {
      return renderProjectsMatrix()
    } else {
      return renderWeeksMatrix()
    }
  }

  const renderProjectsMatrix = () => {
    const usersToShow = selectedUser && isAdmin ? [selectedUser] : [currentUser]

    return (
      <div className="overflow-x-auto border border-gray-300 rounded-lg">
        <table className="w-full border-collapse bg-white">
          <thead>
            <tr className="bg-blue-900 text-white font-semibold">
              <th className="border border-gray-300 px-4 py-2 text-left min-w-200px">Herramienta</th>
              <th className="border border-gray-300 px-4 py-2 text-center min-w-100px bg-green-900">Base</th>
              {PROJECTS.map(proj => (
                <th key={proj.id} className="border border-gray-300 px-4 py-2 text-center min-w-120px">
                  {proj.name}
                </th>
              ))}
              <th className="border border-gray-300 px-4 py-2 text-center min-w-120px bg-blue-800">TOTAL</th>
            </tr>
          </thead>
          <tbody>
            {TOOLS.map(tool => {
              let totalTool = 0
              const projTotals: Record<string, number> = {}

              PROJECTS.forEach(proj => {
                const val = data[tool]?.[proj.id] || 0
                projTotals[proj.id] = val
                totalTool += val
              })

              return (
                <tr key={tool} className="border-b border-gray-200">
                  <td className="border border-gray-300 px-4 py-2 bg-gray-50 font-medium">
                    {tool} - {TOOL_NAMES[tool]?.substring(0, 20)}
                  </td>
                  <td className="border border-gray-300 px-4 py-2 text-center bg-green-50 font-semibold">
                    {viewMode === 'hours' ? '12.5h' : '625€'}
                  </td>
                  {PROJECTS.map(proj => (
                    <td key={proj.id} className="border border-gray-300 px-4 py-2 text-center">
                      {viewMode === 'hours'
                        ? (projTotals[proj.id] || 0).toFixed(1) + 'h'
                        : ((projTotals[proj.id] || 0) * 50).toFixed(2) + '€'}
                    </td>
                  ))}
                  <td className="border border-gray-300 px-4 py-2 text-center bg-blue-100 font-semibold">
                    {viewMode === 'hours'
                      ? totalTool.toFixed(1) + 'h'
                      : (totalTool * 50).toFixed(2) + '€'}
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    )
  }

  const renderWeeksMatrix = () => {
    const weeks = ['W31', 'W32', 'W33', 'W34', 'W35']

    return (
      <div className="overflow-x-auto border border-gray-300 rounded-lg">
        <table className="w-full border-collapse bg-white">
          <thead>
            <tr className="bg-blue-900 text-white font-semibold">
              <th className="border border-gray-300 px-4 py-2 text-left min-w-200px">Herramienta</th>
              {weeks.map(week => (
                <th key={week} className="border border-gray-300 px-4 py-2 text-center min-w-100px">
                  {week}
                </th>
              ))}
              <th className="border border-gray-300 px-4 py-2 text-center min-w-120px bg-blue-800">TOTAL</th>
            </tr>
          </thead>
          <tbody>
            {TOOLS.map(tool => (
              <tr key={tool} className="border-b border-gray-200">
                <td className="border border-gray-300 px-4 py-2 bg-gray-50 font-medium">
                  {tool} - {TOOL_NAMES[tool]?.substring(0, 20)}
                </td>
                {weeks.map(week => (
                  <td key={week} className="border border-gray-300 px-4 py-2 text-center">
                    {viewMode === 'hours' ? (Math.random() * 10).toFixed(1) + 'h' : (Math.random() * 500).toFixed(2) + '€'}
                  </td>
                ))}
                <td className="border border-gray-300 px-4 py-2 text-center bg-blue-100 font-semibold">
                  {viewMode === 'hours' ? '50.0h' : '2500€'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto p-6">
      {/* Pestañas de vista */}
      <div className="flex gap-1 mb-6 border-b-2 border-gray-200">
        <button
          onClick={() => setViewType('projects')}
          className={`px-4 py-2 font-semibold ${
            viewType === 'projects'
              ? 'text-blue-900 border-b-2 border-blue-900'
              : 'text-gray-600'
          }`}
        >
          Por Proyectos
        </button>
        <button
          onClick={() => setViewType('weeks')}
          className={`px-4 py-2 font-semibold ${
            viewType === 'weeks'
              ? 'text-blue-900 border-b-2 border-blue-900'
              : 'text-gray-600'
          }`}
        >
          Por Semanas
        </button>
      </div>

      {/* Título y botones de vista */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">
          Resumen: Herramientas × {viewType === 'projects' ? 'Proyectos' : 'Semanas'}
        </h1>
        <div className="flex gap-2">
          <button
            onClick={() => setViewMode('hours')}
            className={`px-4 py-2 font-bold rounded ${
              viewMode === 'hours'
                ? 'bg-blue-900 text-white'
                : 'bg-gray-200 text-gray-800'
            }`}
          >
            Horas
          </button>
          <button
            onClick={() => setViewMode('euros')}
            className={`px-4 py-2 font-bold rounded ${
              viewMode === 'euros'
                ? 'bg-blue-900 text-white'
                : 'bg-gray-200 text-gray-800'
            }`}
          >
            Euros
          </button>
        </div>
      </div>

      {/* Filtros */}
      <div className="flex gap-4 mb-6 bg-gray-50 p-4 rounded-lg flex-wrap">
        {isAdmin && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Ver usuario</label>
            <select
              value={selectedUser}
              onChange={e => setSelectedUser(e.target.value)}
              className="border border-gray-300 rounded px-3 py-2 w-180px"
            >
              <option value="">-- Todos --</option>
              {USERS.map(user => (
                <option key={user} value={user}>{user}</option>
              ))}
            </select>
          </div>
        )}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Usuario actual</label>
          <div className="px-3 py-2 bg-white border border-gray-300 rounded">
            {currentUser}
          </div>
        </div>
      </div>

      {/* Matriz */}
      {loading ? (
        <div className="text-center py-8 text-gray-500">Cargando datos...</div>
      ) : (
        renderMatrix()
      )}
    </div>
  )
}
