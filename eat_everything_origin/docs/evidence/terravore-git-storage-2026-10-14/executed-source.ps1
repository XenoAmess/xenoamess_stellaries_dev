$ErrorActionPreference = 'Stop'
$repoPath = [System.IO.Path]::GetFullPath('D:\workspace\xenoamess_stellaries_dev')
$gitRoot = [System.IO.Path]::GetFullPath((Join-Path $repoPath '.git'))
$objectRoot = [System.IO.Path]::GetFullPath((Join-Path $gitRoot 'objects'))
$storageRoot = [System.IO.Path]::GetFullPath('C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\git-loose-object-storage-terravore-20261014')
$mainRoot = Join-Path $storageRoot 'objects'
$originalRoot = Join-Path $storageRoot 'original'
$backupRoot = [System.IO.Path]::GetFullPath((Join-Path $gitRoot 'loose-original-terravore-20261014'))
$utf8 = New-Object System.Text.UTF8Encoding($false)
function Assert-InRoot([string]$path, [string]$root) {
    $absolute = [System.IO.Path]::GetFullPath($path)
    $boundary = [System.IO.Path]::GetFullPath($root).TrimEnd('\') + '\'
    if(-not $absolute.StartsWith($boundary, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw ('Path outside named root: ' + $absolute)
    }
    return $absolute
}
function Hash([string]$path) { return (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
function Require-NoGit { if(@(Get-Process -Name git -ErrorAction SilentlyContinue).Count -ne 0) { throw 'Active Git process; no migration allowed' } }
if((Test-Path -LiteralPath $storageRoot) -or (Test-Path -LiteralPath $backupRoot)) { throw 'Unique storage destination already exists' }
if(-not (Test-Path -LiteralPath (Join-Path $gitRoot 'HEAD'))) { throw 'Wrong repository Git root' }
Require-NoGit
$headBefore = (& git -C $repoPath rev-parse HEAD).Trim()
if($LASTEXITCODE -ne 0) { throw 'Cannot read Git HEAD' }
$indexBefore = Hash (Join-Path $gitRoot 'index')
$prefixes = @(Get-ChildItem -LiteralPath $objectRoot -Force -Directory | Where-Object { $_.Name -match '^[0-9a-f]{2}$' })
if($prefixes.Count -eq 0) { throw 'No loose directories found' }
$rows = @(
    foreach($dir in $prefixes) {
        Assert-InRoot $dir.FullName $objectRoot | Out-Null
        if($dir.Attributes -band [System.IO.FileAttributes]::ReparsePoint) { throw 'Existing loose prefix reparse point' }
        foreach($file in Get-ChildItem -LiteralPath $dir.FullName -Force) {
            if($file.PSIsContainer -or ($file.Attributes -band [System.IO.FileAttributes]::ReparsePoint)) { throw 'Unexpected nested loose object' }
            if($file.Name -notmatch '^[0-9a-f]{38}$') { throw 'Unexpected loose object filename' }
            [pscustomobject]@{prefix=$dir.Name;name=$file.Name;bytes=$file.Length;sha256=(Hash $file.FullName);source=$file.FullName}
        }
    }
)
$totalBytes = ($rows | Measure-Object -Property bytes -Sum).Sum
if((Get-PSDrive -Name C).Free -le ($totalBytes * 3 + 1000000000)) { throw 'Insufficient C space for verified copies' }
New-Item -ItemType Directory -Path $mainRoot -Force | Out-Null
New-Item -ItemType Directory -Path $originalRoot -Force | Out-Null
Copy-Item -LiteralPath $PSCommandPath -Destination (Join-Path $storageRoot 'executed-source.ps1')
$manifest = [pscustomobject]@{repo=$repoPath;git_root=$gitRoot;storage=$storageRoot;head_before=$headBefore;index_sha256_before=$indexBefore;files=$rows.Count;bytes=$totalBytes;manifest=$rows}
[System.IO.File]::WriteAllText((Join-Path $storageRoot 'source-manifest.json'), ($manifest | ConvertTo-Json -Depth 5), $utf8)
Write-Output ('MANIFEST ' + $rows.Count + ' files ' + $totalBytes + ' bytes')
foreach($dir in $prefixes) {
    New-Item -ItemType Directory -Path (Join-Path $mainRoot $dir.Name) | Out-Null
    New-Item -ItemType Directory -Path (Join-Path $originalRoot $dir.Name) | Out-Null
}
$copied = 0
foreach($row in $rows) {
    $target = Assert-InRoot (Join-Path (Join-Path $mainRoot $row.prefix) $row.name) $mainRoot
    Copy-Item -LiteralPath $row.source -Destination $target -Force
    if((Get-Item -LiteralPath $target -Force).Length -ne $row.bytes -or (Hash $target) -ne $row.sha256) { throw 'C first-copy verification failed' }
    $copied++
    if($copied % 2000 -eq 0) { Write-Output ('COPIED ' + $copied) }
}
Require-NoGit
if((Hash (Join-Path $gitRoot 'index')) -ne $indexBefore) { throw 'Index changed during copy' }
if((& git -C $repoPath rev-parse HEAD).Trim() -ne $headBefore) { throw 'HEAD changed during copy' }
New-Item -ItemType Directory -Path $backupRoot | Out-Null
foreach($dir in $prefixes) {
    $source = Assert-InRoot $dir.FullName $objectRoot
    $backup = Assert-InRoot (Join-Path $backupRoot $dir.Name) $backupRoot
    $target = Assert-InRoot (Join-Path $mainRoot $dir.Name) $mainRoot
    Move-Item -LiteralPath $source -Destination $backup
    New-Item -ItemType Junction -Path $source -Value $target | Out-Null
    $link = Get-Item -LiteralPath $source -Force
    if($link.LinkType -ne 'Junction' -or [System.IO.Path]::GetFullPath($link.Target[0]) -ne $target) { throw 'Prefix junction target differs' }
}
Write-Output 'PREFIX_JUNCTIONS_CREATED'
& git -C $repoPath -c gc.auto=0 -c maintenance.auto=false fsck --connectivity-only 1> (Join-Path $storageRoot 'fsck-stdout.txt') 2> (Join-Path $storageRoot 'fsck-stderr.txt')
$fsckExit = $LASTEXITCODE
if($fsckExit -ne 0) { throw ('Git connectivity failed: ' + $fsckExit) }
if((Hash (Join-Path $gitRoot 'index')) -ne $indexBefore -or (& git -C $repoPath rev-parse HEAD).Trim() -ne $headBefore) { throw 'HEAD or index changed' }
$moved = 0
foreach($row in $rows) {
    $source = Assert-InRoot (Join-Path (Join-Path $backupRoot $row.prefix) $row.name) $backupRoot
    $target = Assert-InRoot (Join-Path (Join-Path $originalRoot $row.prefix) $row.name) $originalRoot
    if((Get-Item -LiteralPath $source -Force).Length -ne $row.bytes -or (Hash $source) -ne $row.sha256) { throw 'Original changed before transfer' }
    Move-Item -LiteralPath $source -Destination $target -Force
    if((Get-Item -LiteralPath $target -Force).Length -ne $row.bytes -or (Hash $target) -ne $row.sha256) { throw 'Original C transfer failed' }
    $moved++
    if($moved % 2000 -eq 0) { Write-Output ('ORIGINAL_PRESERVED ' + $moved) }
}
$receipt = [pscustomobject]@{status='PASS_GIT_LOOSE_STORAGE_MIGRATION';files=$rows.Count;bytes=$totalBytes;head=$headBefore;index_sha256=$indexBefore;fsck_exit=$fsckExit;prefix_junctions=$prefixes.Count;source_manifest_sha256=(Hash (Join-Path $storageRoot 'source-manifest.json'));D_free=(Get-PSDrive -Name D).Free;C_free=(Get-PSDrive -Name C).Free;scope='Only current repository loose-object prefixes; C first-copy and original preserved; no recursive deletes, no game actions'}
[System.IO.File]::WriteAllText((Join-Path $storageRoot 'receipt.json'), ($receipt | ConvertTo-Json -Depth 3), $utf8)
Write-Output ($receipt | ConvertTo-Json -Compress)
