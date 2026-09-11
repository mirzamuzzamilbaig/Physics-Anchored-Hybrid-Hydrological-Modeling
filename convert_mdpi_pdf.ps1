$word = New-Object -ComObject Word.Application
$word.Visible = $false
$wdFormatPDF = 17

$docxFiles = @(
    "paper_latex/Research_Article_Geosciences_Journal.docx",
    "Research_Article_MDPI_Geosciences.docx"
)

try {
    foreach ($file in $docxFiles) {
        $docxPath = Join-Path -Path $PWD -ChildPath $file
        $pdfPath = [System.IO.Path]::ChangeExtension($docxPath, ".pdf")
        
        if (Test-Path $docxPath) {
            Write-Host "Converting $file to PDF..."
            $doc = $word.Documents.Open($docxPath)
            $doc.SaveAs($pdfPath, $wdFormatPDF)
            $doc.Close()
            Write-Host "SUCCESS: Generated $pdfPath"
        }
    }
} catch {
    Write-Error $_
} finally {
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
}
