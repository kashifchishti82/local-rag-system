import { useAuth } from '@/contexts/AuthContext'
import { redirect } from 'next/navigation'
import SystemMetrics from '@/components/features/SystemMetrics'
import AdminSettings from '@/components/features/AdminSettings'
import HealthMonitor from '@/components/features/HealthMonitor'

export default function AdminPage() {
  const { user } = useAuth()

  // Redirect if not admin
  if (user?.role !== 'admin') {
    redirect('/')
  }

  return (
    <main className="flex flex-col gap-6">
      <h1 className="text-4xl font-bold mb-8">Admin Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <SystemMetrics />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <AdminSettings />
        <HealthMonitor />
      </div>
    </main>
  )
}
