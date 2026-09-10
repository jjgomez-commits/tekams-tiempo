import { supabase } from '@/lib/supabase'
import { NextRequest, NextResponse } from 'next/server'

export async function GET() {
  try {
    const { data, error } = await supabase
      .from('time_entries')
      .select('*')

    if (error) throw error

    return NextResponse.json(data)
  } catch (error) {
    return NextResponse.json({ error: 'Error fetching entries' }, { status: 500 })
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { user_id, project_id, tool_id, week, hours } = body

    const { data, error } = await supabase
      .from('time_entries')
      .insert([
        {
          user_id,
          project_id,
          tool_id,
          week,
          hours
        }
      ])
      .select()

    if (error) throw error

    return NextResponse.json(data)
  } catch (error) {
    return NextResponse.json({ error: 'Error creating entry' }, { status: 500 })
  }
}
