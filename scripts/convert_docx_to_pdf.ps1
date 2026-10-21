$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open('C:\Projects\QFlow\QFLOW_PROJECT_REPORT.docx')
    $pages = $doc.ComputeStatistics(2)
    Write-Host "Total Word Pages: $pages"
    $doc.SaveAs([ref]'C:\Projects\QFlow\QFLOW_PROJECT_REPORT.pdf', [ref]17)
    $doc.Close([ref]$false)
} finally {
    $word.Quit()
}
