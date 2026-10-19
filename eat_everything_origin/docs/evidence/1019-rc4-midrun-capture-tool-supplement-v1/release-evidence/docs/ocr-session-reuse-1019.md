# 同进程OCR实例复用调查与验收

## 目标与范围

2026-10-19主线程要求缩短实机工具每帧OCR初始化及完整probe取证时间。本任务只优化测试工具`tools/runtime_single_homeworld.py`内的同进程OCR调用；只离线读取已经归档的简体中文截图，不操作桌面、不启动或停止游戏、不修改共享`runtime.py`／harness、生产Mod、冻结树、静态门禁或既有原始证据，不提交Git。

## 设计

先只读定位`runtime.py`的gpu_capture和single-homeworld的bounded_ocr调用链、RapidOCR实现及默认线程行为。若实例能安全串行复用，采用进程内惰性缓存；缓存按实际工厂身份隔离，初始化和推理互斥，避免同一session并发调用。保持图像输入、OCR参数、rows／boxes／scores、超时和调用者可见返回形状；若边界条件要求独立子进程或同实例无法保证结果一致，则不实施缓存并记录原因。共享harness的gpu_capture仅记录瓶颈，不修改。

新增离线比较证据只写新路径。使用至少三帧已归档简中截图，覆盖控制台／HUD与密集原生界面；每帧对比旧路径每次构造与复用实例的完整返回值，明确排除模型返回的耗时统计字段，文字／行序／坐标／置信度要求逐项精确相等。记录构造、推理和总耗时、截图字节SHA、工具／模型／环境版本及重复调用结果。不把OCR一致性报告作为任何Mod实机case通过证据。

## 验收标准

- 所有比较帧的新旧文字、行序、boxes与scores精确一致；任一不一致则不实施优化。
- 实测缓存热调用的总耗时低于相同帧的旧构造+推理；首帧冷启动成本单列，不夸大完整probe收益。
- 必要的定向测试覆盖同工厂复用、不同工厂隔离和并发互斥；初始化／推理失败继续明确抛错，不伪造空OCR成功。
- 不改共享runtime.py与任何既有归档；记录工具SHA变动。未来receipt绑定实际执行的新工具字节，旧receipt与旧报告继续绑定旧归档源，不能回填成新工具结果。

## 调查与结果

首轮只读发现：HEAD和工作区`runtime_single_homeworld.py`第37行已经有`@lru_cache(maxsize=1)`，当前没有该文件的未提交diff；因此正常导入single入口后的同进程调用已复用实例。本轮不添加第二份缓存。主线程明确限定仅三帧测量，并追加检查load_run／focus／capture是否每次重新核树或调用PowerShell。

可重复离线测量脚本保存为新证据`docs/evidence/1019-analysis/ocr-session-reuse-benchmark-v1.py`；它只AST提取当前bounded_ocr函数，在独立进程里对三个固定归档截图运行新建实例参照／当前缓存及一次热重复。不导入运行时入口或harness，不操作桌面。新结果写同目录新JSON，不覆盖已有材料；若结果不等则脚本返回非零。因为没有改执行工具，不新增模拟实现的单元测试。

## 追加授权：保持完整范围的截图枚举优化

三帧OCR均精确一致，现有session缓存已经生效；每帧热OCR仍约8秒。进一步只读测得load_run+process_record中位0.001281秒；截图全量glob+Path.stat每轮中位2.129577秒，15003项，gpu_capture前后各扫一次约4.26秒。load_run只读两个JSON，无树manifest／PowerShell。主线程据此授权修改共享测试入口`tools/runtime.py`的gpu_capture截图枚举，并暂停UI worker等待本任务封口；此前禁止改共享入口的范围现仅为该明确优化扩展。

设计：增加无UI的`screenshot_mtimes`助手，以`os.scandir`依次枚举每个profile的原固定`760/remote/281990/screenshots`叶目录，复用Windows DirEntry.stat缓存。仍覆盖完整profile集合及大小写不敏感的原`*.jpg`条目，不要求日期／新目录，不删除截图，不筛掉原glob会匹配的条目类型。不存在的根／叶目录返回空，目录枚举OSError按Path.glob行为忽略；已枚举条目的stat错误仍抛出。gpu_capture的before和fresh均调用同一助手，fresh仍要求每个path当前mtime大于before.get(path,0)，仍选择最大mtime，12秒deadline／0.1秒轮询／0.2秒落盘等待／明确失败不变。

验收：先在全部现有截图上逐path／mtime精确比较原glob+stat与scandir，再给两者相同次数耗时对照；若有外部写入导致集合变化则不宣告等价。新增必要单元测试使用临时截图树／fake clock，覆盖多profile、大小写后缀、非固定叶／非jpg排除、既有同名文件mtime增加、新文件、无新截图超时，确认实际gpu_capture调用链仍拒绝无新文件。测试通过后报告新runtime.py字节SHA；旧归档和旧receipt不修改，新执行receipt必须保存本次实际工具源字节。

## 实际结果与使用边界

已实施且只修改`runtime.py`的枚举助手和两处调用，未改OCR／截图输入／等待／失败合同。定向测试6项通过（0.297秒），定向diff空白检查通过。初版测试使用同名文件mtime只增加1ns，在Windows文件时间表示下未形成可观察增量，已将合成fixture改为1ms；没有改实际mtime比较。测试覆盖原glob会包含的`.jpg`目录条目、大小写后缀、多profile及固定路径边界，实际gpu_capture在fake F12下接受新文件／同名更新、按最大mtime选新文件，拒绝相同或更旧mtime并达到12秒超时；没有实际F12／鼠标／游戏操作。

- [三帧OCR完整比较](evidence/1019-analysis/ocr-session-reuse-benchmark-v1.json)，SHA `8b4b3cdf48dab252459f657d0ab5c8d68b5c52de4a275975e76b477960142698`：原生母舰详情、控制台、保存窗口三个归档简中图，新建参照与现有缓存的未舍入boxes／txts／scores和最终rows全部精确一致；首帧热重复也一致。构造中位0.609780秒，缓存命中工厂约1.6～2.2微秒，热OCR推理7.577～8.272秒。该缓存本来已存在，本任务没有新增缓存提速。
- [JSON与旧截图扫描只读计时](evidence/1019-analysis/ocr-capture-readonly-cost-v1.json)，SHA `a3fe665689b6fa5fd48636475a582995c3daf16e9b02620c19f7b555834234d2`：load_run＋process_record中位0.001281秒；源码调用清单保留，无树校验或PowerShell。focus_current_window仅查询Win32前台／窗口集合，前台正确时直接返回，未调用focus本身做实测。
- [全量截图枚举新旧对照](evidence/1019-analysis/ocr-screenshot-scan-benchmark-v1.json)，SHA `ca471a1ee5d2a4026af3a3ea4814179b1e1b42369d08e39d6fc5a1b10ae7dbaa`：15003条完整path／mtime连续三轮逐项完全一致，三轮集合SHA也稳定；旧glob＋stat中位2.127782秒，scandir中位0.192123秒，约11.08倍。每帧两次扫描离线估计节省3.871318秒；未实测完整probe或新一次实机capture总耗时。

可重复比较脚本分别为同目录`ocr-session-reuse-benchmark-v1.py`与`ocr-screenshot-scan-benchmark-v1.py`，默认拒绝覆盖已存在结果。复测应在新证据路径运行，保留原报告不变。环境为Python3.14.7、RapidOCR3.9.2／ONNX Runtime1.29.0／NumPy2.5.2／Pillow12.3.0；三个模型未下载或修改，当前已安装模型SHA为det `090f04abcd9d9a7498bc4ebf677e4cb9bdce1fe4197ddb7e529f1ef44e1ff94f`、cls `e47acedf663230f8863ff1ab0e64dd2d82b838fceb5957146dab185a89d6215c`、rec `6f327246b50388f3c176ae304bd95767ea6dc0c9ae92153ef8cbe210b3c14884`，config SHA `06623941e188461a0bc263fe16175cb5e5f6f6b01f4387e546d3a741569fc021`。三个帧比较为串行；RapidOCR有可变参数状态，不能由本报告推断并发推理安全，本任务没有引入并发推理或改现有缓存。

新`runtime.py`原始SHA为`84b7fdda9489392f5abab5fc71c9bd61bcc5933185a02f7c6c479d703b155ffc`；旧工具为`91b831241440a04ffa55d7226c7e2eb158907ebdc62054a906ff51e9f5e77adf`。`runtime_single_homeworld.py`未改，SHA仍`cb0d2d2469c47183eac3211148bbf6c9e51b263bc719c35bfb9981e18326ea34`。新worker应归档／绑定本次新工具字节，旧receipt、旧执行器源副本和旧Mod报告不得更新SHA或倒填为新工具；OCR比较报告记录的是改枚举前的共享工具SHA，随后枚举报告记录新SHA，两份证据按实际执行时间保持原样。本轮未改任何生产文件／冻结树／gate／已封版progress／历史原生证据或验收状态，未进行Git操作。
