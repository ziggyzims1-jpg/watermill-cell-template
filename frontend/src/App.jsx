import { useEffect, useState } from 'react'

export default function App() {
  const [health, setHealth] = useState(null)

  useEffect(() => {
    fetch('/api/health')
      .then((r) => r.json())
      .then(setHealth)
      .catch(() => setHealth({ status: 'unreachable' }))
  }, [])

  return (
    <div className="shell">
      <header className="shell-header">
        {/* Brand slot: replace with the client's logo from assets/branding/ */}
        <span className="brand">Cell Template</span>
      </header>
      <main className="shell-main">
        <p>
          Backend: {health ? health.status : 'checking…'}
        </p>
      </main>
    </div>
  )
}
