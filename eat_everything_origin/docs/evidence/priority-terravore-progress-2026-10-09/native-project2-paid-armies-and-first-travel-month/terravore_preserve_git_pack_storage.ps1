$ErrorActionPreference='Stop'
$repoRoot='D:\workspace\xenoamess_stellaries_dev'
$gitRoot=Join-Path $repoRoot '.git'
$source=(Resolve-Path -LiteralPath (Join-Path $gitRoot 'objects\pack')).Path
$storageRoot='C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\git-object-pack-storage-terravore-20261012'
$destination=Join-Path $storageRoot 'pack'
$original=Join-Path $storageRoot 'original'
$backup=Join-Path $gitRoot 'pack-source-preserved-terravore-20261012'
$runRoot='C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\20261009T044016Z'
if ($source -ne (Join-Path $gitRoot 'objects\pack')) { throw 'Unexpected source' }
foreach ($p in @($destination,$original)) { if (-not [IO.Path]::GetFullPath($p).StartsWith($storageRoot+'\')) { throw 'Outside storage root' }; if (Test-Path -LiteralPath $p) { throw 'Destination already exists' } }
if (-not [IO.Path]::GetFullPath($backup).StartsWith($gitRoot+'\') -or (Test-Path -LiteralPath $backup)) { throw 'Invalid backup path' }
$files=@(Get-ChildItem -LiteralPath $source -Force)
if ($files.Where({$_.PSIsContainer}).Count -gt 0) { throw 'Unexpected nested directory' }
$manifest=@($files | ForEach-Object { @{name=$_.Name;bytes=$_.Length;sha256=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLower()} })
New-Item -ItemType Directory -Path $destination,$original | Out-Null
$manifest | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $storageRoot 'source-manifest.json') -Encoding UTF8
foreach ($row in $manifest) { Copy-Item -LiteralPath (Join-Path $source $row.name) -Destination (Join-Path $destination $row.name); if ((Get-FileHash -LiteralPath (Join-Path $destination $row.name) -Algorithm SHA256).Hash.ToLower() -ne $row.sha256) { throw 'Copied SHA differs' } }
Write-Output 'COPY_ALL_BYTES_VERIFIED'
$active=@(Get-CimInstance Win32_Process | Where-Object { $_.Name -match '^git.*\.exe$' })
if ($active.Count -ne 0) { throw 'Active Git processes; original source unchanged' }
foreach ($row in $manifest) { if ((Get-FileHash -LiteralPath (Join-Path $source $row.name) -Algorithm SHA256).Hash.ToLower() -ne $row.sha256) { throw 'Source changed during copy' } }
if (@(Get-ChildItem -LiteralPath $source -Force).Count -ne $manifest.Count) { throw 'Source inventory changed' }
Move-Item -LiteralPath $source -Destination $backup
New-Item -ItemType Junction -Path $source -Target $destination | Out-Null
$link=Get-Item -LiteralPath $source -Force
if ($link.LinkType -ne 'Junction' -or $link.Target[0] -ne $destination) { throw 'Junction target mismatch' }
$stdout=Join-Path $runRoot 'git-pack-storage-connectivity-stdout.bin'
$stderr=Join-Path $runRoot 'git-pack-storage-connectivity-stderr.bin'
$proc=Start-Process -FilePath 'git.exe' -ArgumentList @('-c','gc.auto=0','-c','maintenance.auto=false','fsck','--connectivity-only','--no-dangling') -WorkingDirectory $repoRoot -RedirectStandardOutput $stdout -RedirectStandardError $stderr -WindowStyle Hidden -Wait -PassThru
if ($proc.ExitCode -ne 0) { throw 'Git connectivity failed; preserve backup, do not continue' }
$actualHead=(& git -c gc.auto=0 -c maintenance.auto=false rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0 -or $actualHead -ne 'eb1af11aea50dfbaced171de3002e64c5509ef26') { throw 'HEAD changed' }
Write-Output 'JUNCTION_GIT_CONNECTIVITY_PASS'
foreach ($row in $manifest) {
 $from=Join-Path $backup $row.name
 $to=Join-Path $original $row.name
 if (-not [IO.Path]::GetFullPath($from).StartsWith($backup+'\') -or -not [IO.Path]::GetFullPath($to).StartsWith($original+'\')) { throw 'File outside exact preserved roots' }
 Move-Item -LiteralPath $from -Destination $to -Force
 if ((Test-Path -LiteralPath $from) -or (Get-FileHash -LiteralPath $to -Algorithm SHA256).Hash.ToLower() -ne $row.sha256) { throw 'Original preservation mismatch' }
 if ((Get-FileHash -LiteralPath (Join-Path $source $row.name) -Algorithm SHA256).Hash.ToLower() -ne $row.sha256) { throw 'Live pack mismatch' }
}
if (@(Get-ChildItem -LiteralPath $backup -Force).Count -ne 0) { throw 'Original D backup not empty' }
$receipt=@{status='PASS_GIT_PACK_PRESERVED_TO_C';source=$source;junction_target=$destination;original_preserved=$original;empty_D_backup=$backup;files=$manifest.Count;bytes=($manifest | Measure-Object -Property bytes -Sum).Sum;git_connectivity_exit=$proc.ExitCode;head=$actualHead;free_D=(Get-PSDrive D).Free;free_C=(Get-PSDrive C).Free;manifest=$manifest}
$receipt | ConvertTo-Json -Depth 7 | Set-Content -LiteralPath (Join-Path $runRoot 'git-pack-storage-preserved-receipt.json') -Encoding UTF8
$receipt.Remove('manifest')
$receipt | ConvertTo-Json -Compress
