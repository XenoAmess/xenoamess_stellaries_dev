# 0.4.0正式素材审阅方案（PENDING）

## 目标与范围

2026-10-19主线程授权准备具体可审阅的发布素材方案：核对四条历史inline图片的公开HTTPS可达性与原字节；核对六槽图库并选取已完成RC6 Purifier真实截图供WS-06替换；整理最终上传、独立远端核验与tag顺序。只写草案／调查证据，不改VERSION、descriptor、正式CHANGELOG、正式description或图片manifest，不操作游戏UI、Steam客户端、发布、Git。Steam继续离线。

## 设计与验收标准

先读现有draft、图片manifest、0.3.1远端核验与1019发布入口。普通HTTPS GET只核公开图片，不登录Steam、不调用上传；记录请求URL、最终URL、HTTP状态、长度、SHA256与已有核验记录比较，网络失败如实保留，不推断可达。现有inline若已经是HTTPS，保留原immutable commit URL，不为“转换”改字符串。

通过原GPU图／OCR、原生SAV及receipt追溯RC6候选素材；优先选择真实单母星开局帧，明确实际日期。2201年图只能称首年后状态或母舰配置，不能称2200年1月1日新局。后置tutorial关闭、设计器结果及maintenance tooltip可分别佐证其明确范围，不外推同国Relic对照／成长实效。截图不裁改、不重绘；仅提出新文件名与原位替换WS-06的manifest草案，其它图库槽和四条inline保持可达。全部case与正式素材批准保持PENDING。

调查证据另存`docs/evidence/1019-requirements/release-media-review-v1.json`，只含实际网络结果、已存在源路径／SHA、日期与建议，不伪造完成状态。最终命令按现有代码确认参数、工作目录、own item 3815707212和只读上游3710613857，逐字节远端核验成功后才允许主线程创建并推送v0.4.0，最后恢复Steam离线。本线程不执行这些命令。

## 公开图片核验结果

四条inline本来就使用HTTPS，不需要改URL。2026-10-19实际对四个immutable GitHub raw URL及六个0.3.1图库Steam图片URL执行普通HTTPS GET，十张全部HTTP 200、最终URL仍HTTPS、图像解码成功、逐字节SHA与0.3.1核验记录一致。网络报告为[release-media-network-review-v1.json](evidence/1019-requirements/release-media-network-review-v1.json)，SHA `979e702ebbcc4bce91d22fdbb2f03220d1f61ef3025761e6b7af7ebcc63229d2`。此观察只证明当时图片字节可达；不证明工坊已更新或新版本已验收。没有启动Steam native API、登录或上传。

网页渲染器第一次访问首图发生timeout；独立原字节GET随后成功，此失败边界如实保留在网络报告中。最终prepare仍须重新GET，发布后的verify仍须验证真实工坊HTML中的四个img和渲染图字节，不能用本报告替代。

四条必须保持原样的URL仍固定于commit `62e273a504a817be3c4037340557c4f1e3e2e522`，相对路径／SHA如下：

| 图 | `eat_everything_origin/docs/evidence/1015-2026-10-15/`下路径 | SHA256 |
| --- | --- | --- |
| INLINE-1 | `v17-large-ui-runtime/large17-queen-report.jpg` | `50a4d3c4ea06dc31a68cb0d5dae7a8069056a7607b37cab040fb31b5c83fab0f` |
| INLINE-2 | `v17-large-ui-runtime/large17-source-actual-report.jpg` | `ecdb40300706d3ddbfcc3d3280d6de823bd07d568854baf93a66f81e24007f67` |
| INLINE-3 | `v13-shipyard-runtime/yard-v13-mother-model-details.jpg` | `e65954d93d95a7cb95f7644b642342baed7fe4dbed219431c34744391e98ff27` |
| INLINE-4 | `v17-large-ui-runtime/complete17-double-paid-ui.jpg` | `a4c719c68363c20696da87c7fdb4ace526231a6456144c640d595728428ccdff` |

description保留这四张历史图的年代／夹具说明，尤其母舰图不代表0.4新配置，双队列预置资源不代表开局赠品。封面WS-00及WS-01～05现有本地字节均与图片manifest匹配；首轮仅验证这些旧字节可达，10月20日逐图审阅后进一步建议WS-03～05也原位换图，见下文。WS-06当前旧图虽仍可达，但画有额外殖民地，必须换掉。任何替换都不清空图库。

## WS-06具体候选

推荐原GPU帧：`C:/Users/1/AppData/Local/xenoamess_stellaries_dev/artifacts/1019-implementation/runs/20261019T150008Z/r6pu-verified-designer-result.jpg`。已实际查看原图：右侧只列一个EEP-Core，母舰实际部件／耐久／速度面板清楚，底部没有posttutorial-details那张额外的悬浮tooltip。虽然文件名含designer，它展示的是实际舰船部件详情，不能据文件名宣称已看见设计器供电余额。

| 项目 | 实际值／建议 |
| --- | --- |
| 原图SHA | `66e19e3869ba19c51436b0b1165ad9278fd316f44f23c40b7fe09b99c0bd6416` |
| 原图大小 | JPEG，1024×768，203506 bytes，低于上传工具1MB限制 |
| 原始OCR SHA | `55f288353bf0582458d2f6c47b5e35742cc1e3f797844a700bd2d6755d3a1709`；其image_sha256与原图完全一致 |
| 原图实际日期 | **2201.01.01**，不是2200.01.01 |
| 实际run／PID | `20261019T150008Z`／30812；RC6树`cc181c8a27ede295e9fcebeffc5e10bb75e9cd643edec1d194b928993ffab33a` |
| 建议新文件名 | `workshop/images/06-purifier-single-homeworld-0.4.0-2201.jpg`，只原字节复制，不覆盖旧文件名或裁改原图 |
| 建议caption | 种族洁癖单母星王庭与母舰实际装备（2201.01.01，首年经济观察后；C0，非成长展示）。 |
| 同日原生SAV | `docs/evidence/1019-rc6-economy/purifier/r6puyearui.sav`，SHA `79c49aaae6660f341c7f3e08751a415405e44c4d139d465367a8b07870b393b0`；audit与native-save receipt均已存在 |
| 原始F12动作 | 同目录`r6pu-verified-designer-result-f12.action.json`，物理scan code88，OCR记录fresh Steam F12 GPU backbuffer |

原生报告记录同日C0、六tier0；UI可见舰体93960、装甲显示44787、护盾167310、速度417、伤害6178.04，海军容量115/66。装甲显示是整数舍入，不能把44787写成SAV的精确最大值44787.6。海容超限真实保留，不将截图包装成无维护负担或无经营压力；也不把C0当成长效果样本。

其它候选已查看：`r6pu-initial.jpg`确为2200.01.01，但危机／首次接触弹窗遮挡主画面，不推荐；`r6pu-posttutorial-details.jpg`同为2201.01.01，可作备选，但底部tooltip遮挡；`r6pu-ship-maintenance-hover.jpg`同日清楚显示实际单舰维护10.07能量／2.88合金与原Mother维护优惠，适合作维护证据，遮挡面积较大，不作WS-06主图。不能由该维护图推导供电非负、同国Relic对照完成或成长/RNG通过。

调查期间localization线程完成了真实项目内归档：`docs/evidence/1019-rc6-purifier-mothership-ui-v1/`，index SHA `1af328168e120469fa168a7bdeb4f50621e8ff53303c99221dfbc3c21309f661`，verify SHA `cac86b4342f84dc7043920bd30031ccd381f8ac0eece3fe557241e6db77edf6a`。推荐原图／OCR／F12现在实际存在于该目录`raw/r6pu-verified-designer-result.*`，逐源字节与artifact一致；posttutorial-details和maintenance-hover也在同一raw归档。当前提案直接绑定这份已存在canonical，无需再复制GPU包或追加实机；2200年初的遮挡图仅作artifact比较，不冒称也包含在后置UI归档中。

正式采用时，`workshop/images-manifest.json`中WS-06的source可填写`../docs/evidence/1019-rc6-purifier-mothership-ui-v1/raw/r6pu-verified-designer-result.jpg`；新图及其同日SAV仍须实际挂入最终`purifier_startup`的screenshot／native_save evidence并经过该case审查。然后将原WS-06索引5原位REPLACE；单独采用WS-06时是KEEP×5／REPLACE×1，10月20日完整逐图方案则待另三张实际新图齐备后KEEP×2／REPLACE×4。新文件名可防止旧缓存与0.3.0全删重建故障，调用链应是现有`update_previews_in_place`的`UpdateItemPreviewFile`，不能用全删再Add方案。

首轮审阅提案[release-media-review-v1.json](evidence/1019-requirements/release-media-review-v1.json)原字节保留，其中`selection_approved=false`记录当时状态。**2026-10-20主线程已明确采用WS-06图66e19e…，例行素材选择已授权，不再等待选择批准。** 当前未完成的是最终case证据审查及整套正式媒体冻结，不能把这些范围与已确定的选图混淆。同日SAV与后置tutorial确认截图只按各自来源关联，不声称整份gamestate在这些UI动作前后逐字节一致。

## 2026-10-20采用与本地准备计划（实施前）

目标是把已经采用的WS-06变成可审阅本地素材，并只读查看WS-01～05是否会与0.4.0矛盾。先核当前正式manifest的真实相对目录，再将项目归档原图逐字节复制到`workshop/images/06-purifier-single-homeworld-0.4.0-2201.jpg`，已有目标时只接受完全相同字节，禁止覆盖不同文件。建立独立`docs/evidence/1019-requirements/images-manifest-0.4.0-proposed-20261020-v1.json`及`media-selection-20261020-v1.json`，不修改当前正式`workshop/images-manifest.json`的版本、状态或任何条目。

proposed明确写选择已授权、实际2201.01.01首年后、原图／OCR／SAV引用及候选树；顶层不得是FROZEN或已完成发布，不预填其它case通过。其余五槽逐图视觉审阅，若旧母舰配置、赠品殖民地或旧成长阈值会误导，给出替换槽及后续真实growth/report/reference图需求；同一图不得重复塞入两槽。四条历史inline URL及字节保持，图库替换继续原位，不删除历史原件。正式CHANGELOG最终使用实际发布日期，不能因任务前缀1019或今天10月20日预填未来发布日期。

验收标准：新WS-06本地文件与已封存源SHA66e19e…及203506长度完全一致、JPEG1024×768／OCR真实日期绑定成立；正式manifest前后SHA不变；proposed全部路径可解析或明确为尚未采样而无虚构路径；图片SHA唯一；其余五图的保留／替换依据落盘。仅资料与素材准备，不触碰Steam客户端、游戏UI、发布、生产源、版本或Git。

### 其它五槽逐图审阅

2026-10-20实际查看当前正式manifest选中的五张本地JPEG，没有依据目录中其它未入选图片猜测。以下为新的完整图库建议，取代首轮仅按远端字节可达给出的KEEP×5假设：

| 槽 | 原图可见内容 | 0.4.0建议及所需原件 |
| --- | --- | --- |
| WS-01 | 2297.06.01旧女王账簿，C76、容量余料0/4、人口余料0/6、D21；边境源星属于该后期画面，未标赠品。没有L／N成长阈值。 | 保留原槽／原字节，caption明确“1015历史王庭账簿与决议参考，非0.4成长报告”。0/4和0/6是容量／制造人口规则，不能误读为每级或每5级随机核心阈值。新成长信息由不同WS-05图展示。 |
| WS-02 | 2297.06.01旧源星战记，原生噬岩分支Q20／16/48有效月；未见旧母舰装备或“王座的贡品”。 | 保留原槽／原字节，caption明确“1015历史源星战记，非0.4巨像或本轮噬岩自然战役验收”。它没有认证新巨像／RNG；不为保留旧参考额外要求一轮实机。 |
| WS-03 | 2200.01.01旧母舰面板：舰体101460、甲24429、盾48370、速度294、旧核心／武器；右侧两殖民地含“王座的贡品”。 | **原位替换。** 等待主线程既定本轮同国同日native Relic参考舰实际面板，caption必须明确“原版参考舰／对照夹具，非生产Mother”；原生SAV／OCR／日期绑定齐备后才填source。与WS-06的生产C0面板形成清楚对照，不复用同一张图。 |
| WS-04 | 2200.05.02双队列本身是真实旧专项，但右侧两殖民地含“王座的贡品”，画面是旧蜂巢岗位／区划布局。 | **原位替换并改主题。** 使用主线程既定成长UI中的本轮高L Mother实际部件／属性面板；实际L／六tier及日期只从对应SAV／报告填写。无需为图库另跑两条建设队列，不借旧付费夹具冒称新局经济。此图须与WS-06 C0帧及WS-03参考舰不同。 |
| WS-05 | 2200.05.02旧危机夹具直接选中“王座的贡品”并将其绑定为核心，右侧两世界；旧报告没有六核心成长内容。 | **原位替换并改主题。** 使用主线程既定本轮新女王成长／六核心报告帧，显示真实C／L、下级阈值和六tier／待补奖励；同日原生SAV及无重复奖励证据按原矩阵审查。不能把这张未来report图同时放进WS-01或其它槽。 |

这三张新原件尚未产生／交付时，proposed对应条目不填写虚构file、source、SHA、run或日期，明确`PENDING_NATIVE_SOURCE`。它们来自已经安排的reference、grown Mother、growth report三种不同既定UI证据，不新增实机case，不要求重跑已完成经济。WS-06素材已选定，WS-03～05是实际来源未齐，不是等待再次例行选图授权。四条immutable inline仍保留上述历史图片及历史说明，即便它们不再占据新图库槽，也不能删除其URL／字节。

主线程随后已明确采用这三槽的修订方向，且说明本轮Machine成长采样结束后将从既定UI取得report／Mother面板，Relic参考由后续既定C0功能分支取得。这里只记录来源计划，不预填未来run、日期、C／L／tier或任何PASS；三图到齐后应新建proposed v2保留本v1原字节。

### 本地准备完成事实

已按正式manifest中WS-06的实际`file`解析素材目录，确认是本项目`workshop/images/`，不是仓库另一个Mod或上传内容目录。已创建[06-purifier-single-homeworld-0.4.0-2201.jpg](../workshop/images/06-purifier-single-homeworld-0.4.0-2201.jpg)，逐字节等于已采用原图：SHA `66e19e3869ba19c51436b0b1165ad9278fd316f44f23c40b7fe09b99c0bd6416`、203506 bytes、JPEG1024×768。原始源、旧WS-06文件和其它旧图片均未覆盖或删除。

独立[proposed manifest v1](evidence/1019-requirements/images-manifest-0.4.0-proposed-20261020-v1.json) SHA `d9da8833b555993be905d84740236f368eae60a3a8ee461eabc056226687469c`。其目标版本0.4.0仅在独立草案中表达；status为PROPOSED、final_release_selection=false，WS-06 selection_approved=true且为LOCAL_READY_PENDING_CASE_REVIEW；WS-03～05无虚构file／source／SHA／日期／run。WS-01／02在草案中标注历史，正式manifest版本0.3.1／FROZEN以及原条目完全未改。

独立[选择与复制回执](evidence/1019-requirements/media-selection-20261020-v1.json) SHA `00d4556050635706d8788d20010c322d260fc7276b5e7c7c4b5889f0bd98b6f3`，记录明确授权、实际源／目标／OCR／SAV、三槽来源缺项和10项只读材料检查。正式manifest前后SHA均为`3f3e2759c8fdb73758d5c80fca3c60a57ddba15faee7085ce0fec383c1323f6d`；七个现正式图片字节仍与原manifest一致，四条inline URL／指纹保持，所有当前可用active图SHA互异。只完成素材准备，不将任何运行时case或正式发布状态晋级。执行了只读diff空白检查，没有执行Git写操作／提交／推送。

## 最短正式发布路径（仅供主线程最终执行）

1. **先完成证据审查。** 所有未完成RC6开局／三经济分支操作约束／母舰同国Relic与实际jump／成长与真实随机核心／巨像守卫／普通拆解／迁移／重启／重复初始化及最后日志仍按矩阵处理。各18组完整且范围明确后，才由主线程建立`docs/evidence/1019-requirements/final-result.json`并执行`check-runtime`。迁移v2保留`damage_preserved=false`及明确v2合同，不能抹掉v1 FAIL。当前图片网络PASS、Purifier受限报告及源码证书不能代替这些实机缺项。
2. **正式化与本地冻结。** 在候选生产脚本／图片／翻译全部冻结后，只将`eat_everything_origin/VERSION`及`mod/descriptor.mod`版本元数据改为0.4.0；`supported_version`不冒充Mod版本。建立实际日期的正式六类CHANGELOG，再从同条目生成`[v0.4.0]`note。按最终真实范围更新description与七ID图片manifest，保留v2舍入、旧mobilebase与多人未验限制。PENDING不能自动删成“全部通过”。重新跑正式包静态工具，接着record-static和prepare；prepare不登录Steam，但会GET四张公开图。**本步骤当前仍PENDING，本文没有执行。**
3. **上传checkpoint。** 主线程只提交／推送正式冻结输入及本地证据到当前跟踪分支；工作区干净且HEAD等于upstream后执行preflight。检查输出version=0.4.0、own ID=3815707212、图库6槽、四inline完全一致。3710613857始终只读。此时Steam仍离线。
4. **最后才短暂上线Steam并上传一次。** 只有步骤1～3通过，才由主线程将Steam切在线并执行publish。上传只能固定own item；成功0.4.0不得重传。若提交结果未知，先核对远端／回执，不能盲目重试；确定未形成远端更新的失败重试才可沿用版本。
5. **独立下载与公开核验。** download通过真实DownloadItem回调取得独立安装目录；verify必须使用回执目录，不能传本地生产mod。核包中每个文件／元数据、正式description、同条Change Note、6张图库顺序／文件名／字节及4个正文img渲染／字节。任何失败都不得打tag。
6. **核验checkpoint后再tag，最后恢复离线。** 主线程提交并推送真实publish/download/verification/public-page等回执，工作区干净后跑tag-check。仅返回READY_TO_TAG才创建并推送新`v0.4.0`标签；不强推已有标签。最终恢复Steam离线并记录实际结果，异常停止发布路径时同样恢复离线。

以下命令从`D:/workspace/xenoamess_stellaries_dev`执行；是供最终阶段复核的准确入口，**不是现在执行的授权或完成记录**：

```powershell
# 阶段1：只读最终candidate矩阵；当前PENDING不得跳过
python eat_everything_origin/tools/publish_1019.py check-runtime

# 阶段2：仅在正式元数据及完整条目已写、所有验收通过后
python D:/workspace/open_kaishek/tools/accept_stellaris_mod.py --mod D:/workspace/xenoamess_stellaries_dev/eat_everything_origin/mod --game C:/SteamLibrary/steamapps/common/Stellaris --version-file D:/workspace/xenoamess_stellaries_dev/eat_everything_origin/VERSION --expected-exe-sha256 400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83 --report D:/workspace/xenoamess_stellaries_dev/eat_everything_origin/docs/evidence/publication-0.4.0/open-kaishek.json
python eat_everything_origin/tools/publish_1019.py record-static
python eat_everything_origin/tools/publish_1019.py prepare

# 主线程提交／推送正式冻结输入后，仍离线
python eat_everything_origin/tools/publish_1019.py preflight

# 主线程最后切Steam在线；只能更新3815707212
python eat_everything_origin/tools/publish_1019.py publish
python eat_everything_origin/tools/publish_1019.py download --timeout 600
$releasedWorkshopDirectory = (Get-Content -Raw eat_everything_origin/docs/evidence/publication-0.4.0/workshop-download.json | ConvertFrom-Json).folder
python eat_everything_origin/tools/publish_1019.py verify --download "$releasedWorkshopDirectory"

# 主线程提交／推送真实核验回执后；仍不得以空白或伪造回执替代
python eat_everything_origin/tools/publish_1019.py tag-check
git tag -a v0.4.0 -m "Eat Everything Origin 0.4.0"
git push origin refs/tags/v0.4.0
# 主线程恢复Steam离线，记录最终离线状态
```

`publish_1019`是唯一适配入口，不能直接运行仍为0.3.1默认值的`publish_update.py`。preflight要求完整工作区干净／已push；tag-check再次要求真实核验回执已提交／已push，因而上传checkpoint和核验checkpoint是两个不同的提交时点。`verify`本身不创建tag。metadata-only比对仍只允许descriptor版本变化；任何生产源变化都必须另冻候选、补适用验收，不能借正式化流程改脚本。

## 本轮验证与交付边界

只读运行现有`workshop_images.local_images(ROOT, "0.3.1")`，当前封面及六图库共七源全部成立；对推荐帧另核JPEG格式／尺寸、1MB上限、OCR字节绑定／真实日期、无debug或eep-key泄漏、同日SAV/audit绑定及新目标文件名未占用，材料层八项检查均成立。独立复核新后置UI归档85文件／5077506字节及45条canonical引用，全部与其索引SHA／长度一致。没有修改该归档任何文件。

审阅提案[release-media-review-v1.json](evidence/1019-requirements/release-media-review-v1.json)最终SHA为`02dbd2848a8f3ec60e671ef55d2c4a96db9feaa93499d0cbfb2ebff54a401715`，仍为`PENDING_MATERIAL_REVIEW_NOT_RELEASE_ACCEPTANCE`；正式图片manifest、正式preflight、远端新版本验证等仍false，源图在项目内这一事实则已按新归档如实更新。网络报告仍保留独立SHA，不因新增本地归档而重写。

再次核对notes draft：六类条目与`[v0.4.0]`note正文完全对应，description建议仍5232 UTF-8字节、BBCode配对完整、四URL及顺序与0.3.1记录完全相同。只更新其媒体现况和本文交叉引用，未把任何待验收玩法改为已通过。未改发布工具／测试／生产源／VERSION／descriptor／正式CHANGELOG／正式description／正式图库manifest，未操作游戏UI／Steam客户端／Git。因仅为文档与只读调查，没有新增或重复运行软件单元测试。
