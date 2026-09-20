param(
  [switch]$KeepBuildFiles
)

$ErrorActionPreference = 'Stop'
$scriptDir = [System.IO.Path]::GetFullPath($PSScriptRoot)
$figureDir = [System.IO.Path]::GetFullPath((Join-Path $scriptDir '..'))
$buildRoot = [System.IO.Path]::GetFullPath((Join-Path $scriptDir '.build'))
$pdfBuild = [System.IO.Path]::GetFullPath((Join-Path $buildRoot 'pdf'))
$svgBuild = [System.IO.Path]::GetFullPath((Join-Path $buildRoot 'svg'))

if (-not $buildRoot.StartsWith($scriptDir, [System.StringComparison]::OrdinalIgnoreCase)) {
  throw "Build directory escaped the illustration source directory: $buildRoot"
}

$stem = 'EE-ILL-P006-001-angular-momentum-flux-sign'
$source = Join-Path $scriptDir "$stem.tex"
$pdfOutput = Join-Path $figureDir "$stem.pdf"
$svgOutput = Join-Path $figureDir "$stem.svg"

foreach ($tool in @('pdflatex', 'latex', 'dvisvgm')) {
  if (-not (Get-Command $tool -ErrorAction SilentlyContinue)) {
    throw "Required tool is unavailable: $tool"
  }
}

New-Item -ItemType Directory -Path $pdfBuild -Force | Out-Null
New-Item -ItemType Directory -Path $svgBuild -Force | Out-Null

$oldEpoch = $env:SOURCE_DATE_EPOCH
$env:SOURCE_DATE_EPOCH = '1789855200'
try {
  & pdflatex -interaction=nonstopmode -halt-on-error -file-line-error `
      -output-directory="$pdfBuild" "$source"
  if ($LASTEXITCODE -ne 0) { throw "pdflatex failed with exit code $LASTEXITCODE" }

  $builtPdf = Join-Path $pdfBuild "$stem.pdf"
  Copy-Item -LiteralPath $builtPdf -Destination $pdfOutput -Force

  & latex -interaction=nonstopmode -halt-on-error -file-line-error `
      -output-directory="$svgBuild" "$source"
  if ($LASTEXITCODE -ne 0) { throw "latex failed with exit code $LASTEXITCODE" }

  $builtDvi = Join-Path $svgBuild "$stem.dvi"
  & dvisvgm --exact-bbox --no-fonts --precision=5 `
      --output="$svgOutput" "$builtDvi"
  if ($LASTEXITCODE -ne 0) { throw "dvisvgm failed with exit code $LASTEXITCODE" }

  $svg = [System.IO.File]::ReadAllText($svgOutput)
  $svg = [System.Text.RegularExpressions.Regex]::Replace(
    $svg,
    '<svg\s+',
    '<svg role="img" aria-labelledby="ee-ill-title ee-ill-desc" ',
    1
  )
  $metadata = @'
<title id="ee-ill-title">Same product, same outward angular-momentum flux</title>
<desc id="ee-ill-desc">Exact sign and product diagram at one fixed cylindrical radius greater than zero. In Case A, the pulse radial component is positive and points away from the axis, while the azimuthal component is a positive surplus. Their product is positive. In Case B, the radial component is negative and points toward the axis, while the azimuthal component is a negative deficit. The product of the two negative components is again positive. Multiplying either product by the positive radius keeps the outward angular-momentum flux factor positive. The arrows show signs and basis directions only; they do not show pulse geometry, paths, profiles, magnitudes, or the full solution.</desc>
'@
  $svg = [System.Text.RegularExpressions.Regex]::Replace(
    $svg,
    '(<svg[^>]*>)',
    "`$1`r`n$metadata",
    1
  )
  [System.IO.File]::WriteAllText(
    $svgOutput,
    $svg,
    [System.Text.UTF8Encoding]::new($false)
  )
}
finally {
  $env:SOURCE_DATE_EPOCH = $oldEpoch
}

if (-not $KeepBuildFiles) {
  $knownSuffixes = @('.aux', '.log', '.dvi')
  foreach ($dir in @($pdfBuild, $svgBuild)) {
    foreach ($suffix in $knownSuffixes) {
      $candidate = Join-Path $dir "$stem$suffix"
      if (Test-Path -LiteralPath $candidate) {
        Remove-Item -LiteralPath $candidate -Force
      }
    }
  }
}

Get-FileHash -Algorithm SHA256 -LiteralPath $source, $pdfOutput, $svgOutput |
  Select-Object Path, Hash
