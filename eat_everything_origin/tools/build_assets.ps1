$ErrorActionPreference = 'Stop'
$taskRoot = Split-Path $PSScriptRoot -Parent
$taskRepo = Split-Path $taskRoot -Parent
$taskTexconv = Join-Path $taskRepo '_runtime/heart-of-devouring/tools/texconv.exe'
if ((Get-FileHash -LiteralPath $taskTexconv -Algorithm SHA256).Hash.ToLower() -ne 'dcfdec10244e02cf5037fba089c55fb7e1326b1c8181742d77d15fa5cb5eef06') { throw 'texconv fingerprint mismatch' }
Add-Type -AssemblyName System.Drawing
$taskIntermediate = Join-Path $taskRepo '_runtime/heart-of-devouring/asset-intermediates'
New-Item -ItemType Directory -Path $taskIntermediate -Force | Out-Null
$taskGenerated = Join-Path $taskRoot 'assets/queen-baiqi/generated'
$taskAssetMap = @(
    @('QBA-03-core-attempt-01/original.png','core',450,150,'gfx/event_pictures'),
    @('QBA-04-devouring-attempt-01/original.png','devouring',450,150,'gfx/event_pictures'),
    @('QBA-05-growth-attempt-01/original.png','growth',450,150,'gfx/event_pictures'),
    @('QBA-06-psionic-attempt-01/original.png','psionic',450,150,'gfx/event_pictures'),
    @('QBA-07-fleet-attempt-01/original.png','fleet',450,150,'gfx/event_pictures'),
    @('QBA-03-core-attempt-01/original.png','origin',220,115,'gfx/interface/icons/origins'),
    @('QBA-08-icon-attempt-01/original.png','heart',40,40,'gfx/interface/icons/origins'),
    @('QBA-01-layerize-03/layer-01.png','baiqi',512,640,'gfx/models/portraits/eep'),
    @('QBA-02-layerize-05/layer-01.png','baiqi_full',768,1152,'gfx/models/portraits/eep')
)
$taskManifest = @()
foreach ($taskEntry in $taskAssetMap) {
    $taskSource = Join-Path $taskGenerated $taskEntry[0]
    $taskImage = [System.Drawing.Image]::FromFile($taskSource)
    $taskW = [int]$taskEntry[2]; $taskH = [int]$taskEntry[3]
    $taskBitmap = New-Object System.Drawing.Bitmap($taskW,$taskH,[System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $taskGraphics = [System.Drawing.Graphics]::FromImage($taskBitmap)
    $taskGraphics.Clear([System.Drawing.Color]::Transparent)
    $taskGraphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $taskGraphics.CompositingMode = [System.Drawing.Drawing2D.CompositingMode]::SourceCopy
    if ($taskEntry[1] -like 'baiqi*') {
        $taskScale = [Math]::Min($taskW/$taskImage.Width,$taskH/$taskImage.Height)
        $taskRect = [System.Drawing.RectangleF]::new([single](($taskW-$taskImage.Width*$taskScale)/2),[single](($taskH-$taskImage.Height*$taskScale)/2),[single]($taskImage.Width*$taskScale),[single]($taskImage.Height*$taskScale))
        $taskGraphics.DrawImage($taskImage,$taskRect)
    } else {
        $taskScale = [Math]::Max($taskW/$taskImage.Width,$taskH/$taskImage.Height)
        $taskSrcW = $taskW/$taskScale; $taskSrcH = $taskH/$taskScale
        $taskCropY = if ($taskEntry[4] -eq 'gfx/event_pictures' -or $taskEntry[1] -eq 'origin') { 0 } else { ($taskImage.Height-$taskSrcH)/2 }
        $taskSrcRect = [System.Drawing.RectangleF]::new([single](($taskImage.Width-$taskSrcW)/2),[single]$taskCropY,[single]$taskSrcW,[single]$taskSrcH)
        $taskGraphics.DrawImage($taskImage,[System.Drawing.RectangleF]::new(0,0,$taskW,$taskH),$taskSrcRect,[System.Drawing.GraphicsUnit]::Pixel)
    }
    $taskPng = Join-Path $taskIntermediate ('eep_'+$taskEntry[1]+'.png')
    $taskBitmap.Save($taskPng,[System.Drawing.Imaging.ImageFormat]::Png)
    $taskGraphics.Dispose(); $taskBitmap.Dispose(); $taskImage.Dispose()
    $taskDestination = Join-Path (Join-Path $taskRoot 'mod') $taskEntry[4]
    New-Item -ItemType Directory -Path $taskDestination -Force | Out-Null
    $taskFormat = if (($taskW % 4 -eq 0) -and ($taskH % 4 -eq 0)) { 'BC3_UNORM' } else { 'B8G8R8A8_UNORM' }
    & $taskTexconv '-nologo' '-y' '-f' $taskFormat '-m' '1' '-o' $taskDestination $taskPng
    if ($LASTEXITCODE -ne 0) { throw "DDS conversion failed: $taskPng" }
    $taskDds = Join-Path $taskDestination ('eep_'+$taskEntry[1]+'.dds')
    $taskManifest += @{source=$taskEntry[0];source_sha256=(Get-FileHash $taskSource).Hash.ToLower();target=$taskDds.Substring($taskRoot.Length+1).Replace('\','/');sha256=(Get-FileHash $taskDds).Hash.ToLower();width=$taskW;height=$taskH}
}
$taskModifierDir = Join-Path $taskRoot 'mod/gfx/interface/icons/modifiers'
New-Item -ItemType Directory -Path $taskModifierDir -Force | Out-Null
foreach ($taskIconName in @('mod_situation_eep_devouring_max_progress_add','mod_situation_eep_devouring_max_progress_mult','eep_capacity')) {
    Copy-Item -LiteralPath (Join-Path $taskRoot 'mod/gfx/interface/icons/origins/eep_heart.dds') -Destination (Join-Path $taskModifierDir ($taskIconName+'.dds'))
}
$taskCover = [System.Drawing.Image]::FromFile((Join-Path $taskGenerated 'QBA-09-cover-attempt-01/original.png'))
$taskCoverBitmap = New-Object System.Drawing.Bitmap(512,512)
$taskG = [System.Drawing.Graphics]::FromImage($taskCoverBitmap)
$taskG.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$taskG.DrawImage($taskCover,0,0,512,512)
$taskCoverBitmap.Save((Join-Path $taskRoot 'mod/thumbnail.png'),[System.Drawing.Imaging.ImageFormat]::Png)
$taskG.Dispose();$taskCoverBitmap.Dispose();$taskCover.Dispose()
$taskManifest | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $taskRoot 'docs/evidence/asset-build.json') -Encoding UTF8
