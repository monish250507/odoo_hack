import jsPDF from 'jspdf'
import * as XLSX from 'xlsx'

export function exportToCSV(data: Record<string, unknown>[], filename: string) {
  if (!data.length) return
  const headers = Object.keys(data[0])
  const rows = data.map((row) => headers.map((h) => String(row[h] ?? '')).join(','))
  const csv = [headers.join(','), ...rows].join('\n')
  const blob = new Blob([csv], { type: 'text/csv' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${filename}.csv`
  a.click()
  URL.revokeObjectURL(url)
}

export function exportToExcel(data: Record<string, unknown>[], filename: string) {
  const ws = XLSX.utils.json_to_sheet(data)
  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, ws, 'Data')
  XLSX.writeFile(wb, `${filename}.xlsx`)
}

export function exportToPDF(title: string, data: Record<string, unknown>[], filename: string) {
  const doc = new jsPDF()
  doc.setFontSize(18)
  doc.text(title, 14, 20)
  doc.setFontSize(11)

  const headers = Object.keys(data[0] || {})
  let y = 35

  // Header row
  headers.forEach((h, i) => {
    doc.text(h, 14 + i * 40, y)
  })
  y += 8

  // Data rows
  data.slice(0, 30).forEach((row) => {
    if (y > 270) { doc.addPage(); y = 20 }
    headers.forEach((h, i) => {
      doc.text(String(row[h] ?? ''), 14 + i * 40, y)
    })
    y += 7
  })

  doc.save(`${filename}.pdf`)
}
