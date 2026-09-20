[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$projectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$lockPath = Join-Path $projectRoot "everyday\epubcheck-lock.json"
$lock = Get-Content -Raw -LiteralPath $lockPath | ConvertFrom-Json
$dependencyRoot = [System.IO.Path]::GetFullPath((Join-Path $projectRoot "tmp\dependencies"))
$runtimeJar = [System.IO.Path]::GetFullPath((Join-Path $projectRoot $lock.runtime_jar))

if (-not $runtimeJar.StartsWith($dependencyRoot + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "The locked EPUBCheck runtime path is outside tmp/dependencies."
}

function Assert-Archive([string]$Path) {
    $item = Get-Item -LiteralPath $Path
    if ($item.Length -ne [int64]$lock.archive.bytes) {
        throw "The EPUBCheck archive byte length does not match the lock."
    }
    $observed = (Get-FileHash -Algorithm SHA256 -LiteralPath $Path).Hash.ToLowerInvariant()
    if ($observed -ne $lock.archive.sha256) {
        throw "The EPUBCheck archive SHA-256 does not match the lock."
    }
}

$java = Get-Command java -ErrorAction SilentlyContinue
if ($null -eq $java) {
    throw "Java is required to run EPUBCheck."
}

if (Test-Path -LiteralPath $runtimeJar -PathType Leaf) {
    $version = (& $java.Source -jar $runtimeJar --version 2>&1 | Out-String).Trim()
    if ($LASTEXITCODE -ne 0 -or $version -notmatch [regex]::Escape($lock.version)) {
        throw "The existing EPUBCheck runtime does not match the locked version."
    }
    [ordered]@{
        status = "ready"
        version = $version
        runtime_jar = $lock.runtime_jar
        runtime_jar_sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $runtimeJar).Hash.ToLowerInvariant()
    } | ConvertTo-Json
    exit 0
}

New-Item -ItemType Directory -Force -Path $dependencyRoot | Out-Null
$archivePath = Join-Path $dependencyRoot $lock.archive.name
if (-not (Test-Path -LiteralPath $archivePath -PathType Leaf)) {
    $downloadPath = Join-Path $dependencyRoot ($lock.archive.name + ".download-" + $PID)
    & curl.exe -L --fail --silent --show-error --output $downloadPath $lock.archive.url
    if ($LASTEXITCODE -ne 0) {
        throw "The EPUBCheck archive download failed."
    }
    Assert-Archive $downloadPath
    Move-Item -LiteralPath $downloadPath -Destination $archivePath
}
Assert-Archive $archivePath

$runtimeRoot = Split-Path -Parent (Split-Path -Parent $runtimeJar)
if (Test-Path -LiteralPath $runtimeRoot) {
    throw "The EPUBCheck runtime directory exists but the locked jar is missing."
}
New-Item -ItemType Directory -Path $runtimeRoot | Out-Null
Expand-Archive -LiteralPath $archivePath -DestinationPath $runtimeRoot
if (-not (Test-Path -LiteralPath $runtimeJar -PathType Leaf)) {
    throw "The locked EPUBCheck jar was not found after extraction."
}

$version = (& $java.Source -jar $runtimeJar --version 2>&1 | Out-String).Trim()
if ($LASTEXITCODE -ne 0 -or $version -notmatch [regex]::Escape($lock.version)) {
    throw "The extracted EPUBCheck runtime does not match the locked version."
}
[ordered]@{
    status = "installed"
    version = $version
    archive_sha256 = $lock.archive.sha256
    runtime_jar = $lock.runtime_jar
    runtime_jar_sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $runtimeJar).Hash.ToLowerInvariant()
} | ConvertTo-Json
