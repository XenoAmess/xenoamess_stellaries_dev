$ErrorActionPreference = 'Stop'
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$utf8Evidence = [System.Text.UTF8Encoding]::new($false)
$workspaceEvidence = 'D:\workspace\xenoamess_stellaries_dev'
$sourceEvidence = 'D:\workspace\xenoamess_stellaries_dev\_runtime\heart-of-devouring\runs\20261009T044016Z'
$backupEvidence = 'D:\workspace\xenoamess_stellaries_dev\_runtime\heart-of-devouring\runs\20261009T044016Z.storage-migration-backup'
$physicalEvidence = 'C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\20261009T044016Z'
$parentEvidence = Split-Path -Parent $physicalEvidence
$verifyEvidence = Join-Path $PSScriptRoot 'verify_active_evidence_storage_v1.py'
$receiptEvidence = Join-Path $parentEvidence '20261009T044016Z-storage-migration-result.json'
$preEvidence = Join-Path $parentEvidence '20261009T044016Z-storage-copy-before-junction.json'
$postEvidence = Join-Path $parentEvidence '20261009T044016Z-storage-copy-after-junction.json'
$phaseEvidence = 'preflight'
$freeBeforeEvidence = (Get-PSDrive -Name D).Free
try {
    if ((Get-Location).Path -ne $workspaceEvidence) { throw 'Unexpected working directory.' }
    $sourceItemEvidence = Get-Item -LiteralPath $sourceEvidence -Force
    if ($sourceItemEvidence.FullName -ne $sourceEvidence -or
        ($sourceItemEvidence.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0 -or
        -not $sourceItemEvidence.PSIsContainer) { throw 'Source must be the exact ordinary workspace run directory.' }
    if (-not $sourceEvidence.StartsWith($workspaceEvidence + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Source outside workspace.' }
    if ([IO.Path]::GetFullPath($backupEvidence) -ne $sourceEvidence + '.storage-migration-backup' -or
        (Split-Path -Parent $backupEvidence) -ne (Split-Path -Parent $sourceEvidence)) { throw 'Unexpected backup path.' }
    if ([IO.Path]::GetFullPath($physicalEvidence) -ne $physicalEvidence) { throw 'Unexpected physical target.' }
    foreach ($pathEvidence in @($physicalEvidence, $backupEvidence, $receiptEvidence, $preEvidence, $postEvidence)) {
        if (Test-Path -LiteralPath $pathEvidence) { throw "Target already exists: $pathEvidence" }
    }
    if ((Get-PSDrive -Name C).Free -lt 5GB) { throw 'C drive has insufficient space.' }
    $processesEvidence = Get-CimInstance Win32_Process | Where-Object {
        $_.Name -match '^python' -and $_.CommandLine -like '*20261009T044016Z*'
    }
    if ($processesEvidence) { throw 'An active run helper is still running.' }
    foreach ($fileEvidence in @($PSCommandPath, $verifyEvidence)) {
        $copiedEvidence = Join-Path $sourceEvidence (Split-Path -Leaf $fileEvidence)
        if (Test-Path -LiteralPath $copiedEvidence) { throw 'Migration source receipt already exists.' }
        Copy-Item -LiteralPath $fileEvidence -Destination $copiedEvidence -ErrorAction Stop
    }
    New-Item -ItemType Directory -Path $parentEvidence -Force | Out-Null
    $phaseEvidence = 'copy'
    & robocopy.exe $sourceEvidence $physicalEvidence /E /COPY:DAT /DCOPY:DAT /R:1 /W:1 /NFL /NDL /NP /NJH /NJS
    $copyExitEvidence = $LASTEXITCODE
    if ($copyExitEvidence -gt 7) { throw "Robocopy failed: $copyExitEvidence" }
    $phaseEvidence = 'verify_copy'
    & python -X utf8 $verifyEvidence $sourceEvidence $physicalEvidence $preEvidence
    if ($LASTEXITCODE -ne 0) { throw 'Full raw-byte copy verification failed; source retained.' }
    $phaseEvidence = 'create_junction'
    # Check both final absolute paths again immediately before the only move.
    if ((Get-Item -LiteralPath $sourceEvidence).FullName -ne $sourceEvidence -or
        (Test-Path -LiteralPath $backupEvidence)) { throw 'Move precondition changed.' }
    Move-Item -LiteralPath $sourceEvidence -Destination $backupEvidence -ErrorAction Stop
    New-Item -ItemType Junction -Path $sourceEvidence -Value $physicalEvidence -ErrorAction Stop | Out-Null
    $phaseEvidence = 'verify_junction'
    if ((Get-Item -LiteralPath $sourceEvidence -Force).LinkType -ne 'Junction') { throw 'Expected a junction.' }
    & python -X utf8 $verifyEvidence $backupEvidence $sourceEvidence $postEvidence
    if ($LASTEXITCODE -ne 0) { throw 'Full junction verification failed; both copies retained.' }
    $phaseEvidence = 'release_verified_duplicate'
    $backupItemEvidence = Get-Item -LiteralPath $backupEvidence -Force
    if ($backupItemEvidence.FullName -ne $backupEvidence -or
        ($backupItemEvidence.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0 -or
        -not $backupEvidence.StartsWith($workspaceEvidence + '\', [StringComparison]::OrdinalIgnoreCase)) {
        throw 'Backup deletion target is not the exact verified ordinary workspace directory.'
    }
    Remove-Item -LiteralPath $backupEvidence -Recurse -Force -ErrorAction Stop
    if (Test-Path -LiteralPath $backupEvidence) { throw 'Verified duplicate was not fully removed.' }
    $phaseEvidence = 'complete'
    $resultEvidence = [ordered]@{
        status = 'PASS_ACTIVE_EVIDENCE_PHYSICAL_STORAGE_RELOCATION'
        checked_at_utc = [DateTime]::UtcNow.ToString('o')
        logical_path = $sourceEvidence
        physical_path = $physicalEvidence
        robocopy_exit_code = $copyExitEvidence
        before_copy_full_SHA_verification = $preEvidence
        after_junction_full_SHA_verification = $postEvidence
        d_free_before = $freeBeforeEvidence
        d_free_after = (Get-PSDrive -Name D).Free
        scope = 'All evidence retained; original logical path unchanged. No Mod, game or acceptance changes.'
    }
    [IO.File]::WriteAllText($receiptEvidence, ($resultEvidence | ConvertTo-Json -Depth 6), $utf8Evidence)
    foreach ($fileEvidence in @($preEvidence, $postEvidence, $receiptEvidence)) {
        Copy-Item -LiteralPath $fileEvidence -Destination (Join-Path $sourceEvidence (Split-Path -Leaf $fileEvidence)) -ErrorAction Stop
    }
    $resultEvidence | ConvertTo-Json -Depth 6
} catch {
    if (-not (Test-Path -LiteralPath $sourceEvidence) -and (Test-Path -LiteralPath $backupEvidence)) {
        $restoreItemEvidence = Get-Item -LiteralPath $backupEvidence -Force
        if ($restoreItemEvidence.FullName -eq $backupEvidence -and
            ($restoreItemEvidence.Attributes -band [IO.FileAttributes]::ReparsePoint) -eq 0) {
            Move-Item -LiteralPath $backupEvidence -Destination $sourceEvidence -ErrorAction Stop
        }
    }
    if (Test-Path -LiteralPath $parentEvidence) {
        $failureEvidence = [ordered]@{status='STOPPED_STORAGE_RELOCATION'; phase=$phaseEvidence; reason=$_.Exception.Message; evidence_retained=$true}
        [IO.File]::WriteAllText($receiptEvidence, ($failureEvidence | ConvertTo-Json), $utf8Evidence)
    }
    throw
}
