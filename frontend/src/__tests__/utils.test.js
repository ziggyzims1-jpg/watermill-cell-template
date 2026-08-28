import { describe, it, expect } from 'vitest'
import { localDate } from '../utils.js'

describe('localDate', () => {
  it('formats in local time, not UTC', () => {
    // 23:30 local on Jan 5. In UTC (TZ pinned to America/New_York in the
    // vite config) this instant is already Jan 6 — the exact bug the helper
    // exists to prevent.
    const d = new Date(2026, 0, 5, 23, 30)
    expect(localDate(d)).toBe('2026-01-05')
  })

  it('zero-pads month and day', () => {
    expect(localDate(new Date(2026, 2, 4))).toBe('2026-03-04')
  })
})
