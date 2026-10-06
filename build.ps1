$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$dataRaw = Get-Content -Raw "data.json" -Encoding UTF8
$articles = $dataRaw | ConvertFrom-Json
$template = Get-Content -Raw "template.html" -Encoding UTF8

$indexList = "<ul class='article-list'>"

foreach ($article in $articles) {
    $slug = $article.slug
    $title = $article.title
    $desc = $article.description
    $content = $article.content

    # Build Article Page
    $articleHtml = $template.Replace("{{TITLE}}", "$title | AI Business Tools")
    $articleHtml = $articleHtml.Replace("{{CONTENT}}", $content)
    Set-Content -Path "$slug.html" -Value $articleHtml -Encoding UTF8

    Write-Host "Generado: $slug.html"

    # Add to index
    $indexList += "<li><a href='$slug.html'>$title</a><p>$desc</p></li>"
}

$indexList += "</ul>"

# Build Index Page
$indexHtml = $template.Replace("{{TITLE}}", "Blog Inicio | AI Business Tools")
$indexHtml = $indexHtml.Replace("{{CONTENT}}", "<h1>Últimos Artículos</h1><p>Descubre estrategias y herramientas para escalar negocios con Inteligencia Artificial.</p>$indexList")
Set-Content -Path "index.html" -Value $indexHtml -Encoding UTF8

Write-Host "Generado: index.html"
Write-Host "¡Sitio web construido con éxito! Todo listo para monetizar."
