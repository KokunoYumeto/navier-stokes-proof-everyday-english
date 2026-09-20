$ErrorActionPreference = 'Stop'

$evidenceDir = [System.IO.Path]::GetFullPath($PSScriptRoot)
$projectDir = [System.IO.Path]::GetFullPath((Join-Path $evidenceDir '..\..'))
$figureDir = Join-Path $projectDir 'everyday\illustrations'
$sourceDir = Join-Path $figureDir 'src'
$renderDir = Join-Path $evidenceDir 'rendered'
$stem = 'EE-ILL-P006-001-angular-momentum-flux-sign'

$tex = Join-Path $sourceDir "$stem.tex"
$buildScript = Join-Path $sourceDir 'build-EE-ILL-P006-001.ps1'
$pdf = Join-Path $figureDir "$stem.pdf"
$svg = Join-Path $figureDir "$stem.svg"
$pdfPng = Join-Path $renderDir 'EE-ILL-P006-001-pdf.png'
$svgPng = Join-Path $renderDir 'EE-ILL-P006-001-svg.png'
$svgAlignedPng = Join-Path $renderDir 'EE-ILL-P006-001-svg-aligned.png'
$ledger = Join-Path $evidenceDir 'ILLUSTRATIONS.jsonl'
$manuscript = Join-Path $projectDir 'everyday\sections\pp001-006.tex'

foreach ($path in @($tex, $buildScript, $pdf, $svg, $ledger, $manuscript)) {
  if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
    throw "Required illustration file is missing: $path"
  }
}

foreach ($tool in @('xmllint', 'pdfinfo', 'pdftotext', 'pdftoppm', 'magick')) {
  if (-not (Get-Command $tool -ErrorAction SilentlyContinue)) {
    throw "Required validation tool is unavailable: $tool"
  }
}

$texText = [System.IO.File]::ReadAllText($tex)
$requiredTex = @(
  'EXACT SIGN/PRODUCT DIAGRAM',
  'w_r=+a>0',
  'w_\theta=+b>0',
  'w_r=-a<0',
  'w_\theta=-b<0',
  'w_rw_\theta=(+a)(+b)=ab>0',
  'w_rw_\theta=(-a)(-b)=ab>0',
  'r\,w_rw_\theta=rab>0',
  'positive outward angular-momentum flux factor',
  'not pulse geometry',
  'carry no scale or geometric information'
)
foreach ($literal in $requiredTex) {
  if (-not $texText.Contains($literal)) {
    throw "Required exact label or relation is missing from the TeX source: $literal"
  }
}

function Get-Utf8TextSha256([string]$value) {
  $bytes = [System.Text.Encoding]::UTF8.GetBytes($value)
  return ([System.BitConverter]::ToString(
      [System.Security.Cryptography.SHA256]::HashData($bytes)
    )).Replace('-', '').ToLowerInvariant()
}

function Get-LineSpanSha256([string]$path, [int]$start, [int]$end) {
  $lines = [System.IO.File]::ReadAllLines($path)
  if ($start -lt 1 -or $end -lt $start -or $end -gt $lines.Count) {
    throw "Invalid recorded line span $start-$end for $path"
  }
  $span = ($lines[($start - 1)..($end - 1)] -join "`n") + "`n"
  return Get-Utf8TextSha256 $span
}

$ledgerLines = @(Get-Content -LiteralPath $ledger)
if ($ledgerLines.Count -ne 1) { throw 'The illustration ledger must contain exactly one JSON object line.' }
$record = $ledgerLines[0] | ConvertFrom-Json -Depth 100
if ($record.id -ne 'EE-ILL-P006-001') { throw 'The illustration ledger has the wrong stable ID.' }
if ($record.status -ne 'integrated') { throw 'The illustration ledger does not record integrated status.' }
if (-not $record.integration.manuscript_edited) { throw 'The integration receipt does not record the manuscript edit.' }

$integration = $record.integration.manuscript
if ($integration.path -ne 'everyday/sections/pp001-006.tex') {
  throw 'The integration receipt points to the wrong manuscript path.'
}
$manuscriptHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $manuscript).Hash.ToLowerInvariant()
if ($manuscriptHash -ne $integration.file_sha256) { throw 'The recorded manuscript hash is stale.' }

$manuscriptText = [System.IO.File]::ReadAllText($manuscript)
$segmentPattern = '(?s)\\begin\{EESegment\}\{EE-TGT-P006-001\}(?<body>.*?)\\end\{EESegment\}'
$segmentMatches = [System.Text.RegularExpressions.Regex]::Matches($manuscriptText, $segmentPattern)
if ($segmentMatches.Count -ne 1) { throw 'The integrated target segment must occur exactly once.' }
$segmentBody = $segmentMatches[0].Groups['body'].Value
if ((Get-Utf8TextSha256 $segmentBody) -ne $integration.segment_body_sha256) {
  throw 'The recorded integrated segment-body hash is stale.'
}
if ([System.Text.Encoding]::UTF8.GetByteCount($segmentBody) -ne $integration.segment_body_bytes) {
  throw 'The recorded integrated segment-body byte count is stale.'
}
if ((Get-LineSpanSha256 $manuscript $integration.segment_line_start $integration.segment_line_end) -ne
    $integration.segment_span_sha256) {
  throw 'The recorded integrated segment line-span hash is stale.'
}
if ((Get-LineSpanSha256 $manuscript $integration.figure_line_start $integration.figure_line_end) -ne
    $integration.figure_span_sha256) {
  throw 'The recorded integrated figure line-span hash is stale.'
}

$figurePattern = '(?s)\\begin\{figure\}\[htbp\](?<body>.*?)\\end\{figure\}'
$figureMatches = [System.Text.RegularExpressions.Regex]::Matches($segmentBody, $figurePattern)
if ($figureMatches.Count -ne 1) { throw 'The target segment must contain exactly one standard figure environment.' }
$figureText = $figureMatches[0].Value
$includeMatch = [System.Text.RegularExpressions.Regex]::Match(
  $figureText,
  '\\includegraphics\[width=\\linewidth\]\{(?<argument>[^}]+)\}'
)
if (-not $includeMatch.Success -or
    $includeMatch.Groups['argument'].Value -ne $integration.includegraphics_argument) {
  throw 'The integrated figure asset reference does not match the receipt.'
}
$captionLabelMatch = [System.Text.RegularExpressions.Regex]::Match(
  $figureText,
  '(?s)\\caption\{(?<caption>.*?)\}\s*\\label\{(?<label>[^}]+)\}'
)
if (-not $captionLabelMatch.Success) { throw 'The integrated caption and label could not be parsed.' }
$caption = [System.Text.RegularExpressions.Regex]::Replace(
  $captionLabelMatch.Groups['caption'].Value,
  '\s+',
  ' '
).Trim()
if ($caption -ne $integration.caption) { throw 'The integrated caption does not match the receipt.' }
if ($captionLabelMatch.Groups['label'].Value -ne $integration.label) {
  throw 'The integrated figure label does not match the receipt.'
}
if (([regex]::Matches($manuscriptText, [regex]::Escape("\label{$($integration.label)}"))).Count -ne 1) {
  throw 'The integrated figure label is not unique in the manuscript file.'
}
if (([regex]::Matches($manuscriptText, [regex]::Escape(
        "\includegraphics[width=\linewidth]{$($integration.includegraphics_argument)}"
      ))).Count -ne 1) {
  throw 'The integrated figure asset reference is not unique in the manuscript file.'
}
$resolvedAsset = Join-Path $projectDir $integration.asset_resolved_path
if ([System.IO.Path]::GetFullPath($resolvedAsset) -ne [System.IO.Path]::GetFullPath($pdf)) {
  throw 'The integrated asset path does not resolve to the validated PDF.'
}
if ((Get-FileHash -Algorithm SHA256 -LiteralPath $resolvedAsset).Hash.ToLowerInvariant() -ne
    $integration.asset_sha256) {
  throw 'The integrated PDF hash does not match the receipt.'
}

& xmllint --noout $svg
if ($LASTEXITCODE -ne 0) { throw 'SVG XML validation failed.' }

$svgText = [System.IO.File]::ReadAllText($svg)
foreach ($literal in @('role="img"', '<title id="ee-ill-title">', '<desc id="ee-ill-desc">')) {
  if (-not $svgText.Contains($literal)) {
    throw "SVG accessibility metadata is missing: $literal"
  }
}
if ($svgText -match '<image\b') {
  throw 'SVG contains a raster image element; the fallback must remain vector.'
}

$pdfInfo = (& pdfinfo $pdf | Out-String)
if ($pdfInfo -notmatch '(?m)^Pages:\s+1\s*$') { throw 'PDF does not have exactly one page.' }
if ($pdfInfo -notmatch '(?m)^Encrypted:\s+no\s*$') { throw 'PDF encryption state is not acceptable.' }
if ($pdfInfo -notmatch '(?m)^JavaScript:\s+no\s*$') { throw 'PDF unexpectedly contains JavaScript.' }

$pdfText = (& pdftotext -layout $pdf - | Out-String)
foreach ($literal in @(
  'EXACT SIGN/PRODUCT DIAGRAM',
  'Case A: outward + surplus',
  'Case B: inward + deficit',
  'positive outward angular-momentum flux factor',
  'Scope and limit.'
)) {
  if (-not $pdfText.Contains($literal)) {
    throw "Required PDF text is missing after extraction: $literal"
  }
}

New-Item -ItemType Directory -Path $renderDir -Force | Out-Null
& pdftoppm -png -r 200 -singlefile $pdf (Join-Path $renderDir 'EE-ILL-P006-001-pdf')
if ($LASTEXITCODE -ne 0) { throw 'PDF rendering failed.' }
& magick -background white -density 200 $svg -strip -define 'png:exclude-chunks=date,time' $svgPng
if ($LASTEXITCODE -ne 0) { throw 'SVG rendering failed.' }

$pdfDimensions = (& magick identify -format '%wx%h' $pdfPng).Trim()
$svgDimensions = (& magick identify -format '%wx%h' $svgPng).Trim()
if ($pdfDimensions -ne '1260x788') { throw "Unexpected PDF render dimensions: $pdfDimensions" }
if ($svgDimensions -ne '1260x787') { throw "Unexpected SVG render dimensions: $svgDimensions" }

& magick $svgPng -background white -gravity north -extent 1260x788 -strip `
    -define 'png:exclude-chunks=date,time' $svgAlignedPng
if ($LASTEXITCODE -ne 0) { throw 'SVG alignment render failed.' }

$savedPreference = $ErrorActionPreference
$ErrorActionPreference = 'Continue'
$metricText = (& magick compare -metric RMSE $pdfPng $svgAlignedPng 'null:' 2>&1 | Out-String).Trim()
$metricExit = $LASTEXITCODE
$ErrorActionPreference = $savedPreference
if ($metricExit -notin @(0, 1)) { throw "Image comparison failed: $metricText" }
if ($metricText -notmatch '\((?<normalized>[0-9.]+)\)') {
  throw "Could not parse normalized RMSE: $metricText"
}
$normalizedRmse = [double]$Matches['normalized']
if ($normalizedRmse -gt 0.07) {
  throw "PDF and SVG renders differ beyond the accepted antialiasing tolerance: $normalizedRmse"
}

$hashes = @{}
foreach ($path in @($tex, $buildScript, $pdf, $svg, $pdfPng, $svgPng)) {
  $hashes[[System.IO.Path]::GetFileName($path)] = (Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash.ToLowerInvariant()
}

[ordered]@{
  illustration_id = 'EE-ILL-P006-001'
  status = 'pass'
  checks = [ordered]@{
    required_exact_labels_and_relations = 'pass'
    svg_xml = 'pass'
    svg_accessibility_metadata = 'pass'
    svg_vector_only = 'pass'
    pdf_page_count = 1
    pdf_encrypted = $false
    pdf_javascript = $false
    pdf_text_extraction = 'pass'
    pdf_render_dimensions = $pdfDimensions
    svg_render_dimensions = $svgDimensions
    pdf_svg_normalized_rmse = $normalizedRmse
    pdf_svg_rmse_threshold = 0.07
    ledger_status = $record.status
    manuscript_hash = 'pass'
    integrated_target_id = $integration.target_id
    integrated_segment_body_hash = 'pass'
    integrated_segment_line_span_hash = 'pass'
    integrated_figure_line_span_hash = 'pass'
    integrated_figure_environment = 'pass'
    integrated_asset_reference = 'pass'
    integrated_caption = 'pass'
    integrated_label = 'pass'
    integrated_label_unique = 'pass'
  }
  sha256 = $hashes
} | ConvertTo-Json -Depth 6
