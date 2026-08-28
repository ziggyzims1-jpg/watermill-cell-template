// Local date as YYYY-MM-DD. Never toISOString().slice(0,10) — that is UTC,
// and after 7-8pm US time it names tomorrow. One definition, used everywhere,
// mirroring services/clock.py on the backend.
export function localDate(d = new Date()) {
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}-${m}-${day}`
}
