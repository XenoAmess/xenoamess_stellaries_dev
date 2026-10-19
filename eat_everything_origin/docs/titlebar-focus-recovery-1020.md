# 严格验证的Stellaris标题栏焦点恢复

## 目标与范围（实施前）

r7pu经济collector在m04后、m05点击前因SetForegroundWindow被Windows拒绝而停止，
CLEANUP_REQUIRED及原4月／receipt均保留。root已只读确认PID37300的游戏窗口
有效、可见、未最小化，cursor可读；当前前台为cmd。不能把焦点拒绝误报成需要
用户解锁，也不能绕过桌面锁定政策。本线程只修
`tools/runtime_single_homeworld.py:focus_current_window`、新增mock测试／本文／
旧source证据，不实际操作UI，不改其它工具、Mod、模型、发布gate或系统设置。

原source SHA为cb0d2d2469c47183eac3211148bbf6c9e51b263bc719c35bfb9981e18326ea34，
实施前原字节存入`docs/evidence/1020-titlebar-focus-recovery/old-tool/`并设置-text。
already-foreground与原original_focus成功路径保持原行为，只在原API激活被拒绝
的明确异常后考虑恢复，锁屏／无窗口／其它错误不回退。

## 设计与API依据

Microsoft说明[SetForegroundWindow](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setforegroundwindow)
受前台资格限制，即使满足列举条件仍可被拒绝；不能把一次调用当成功。
[SetWindowPos](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwindowpos)
的HWND_TOP仅改Z顺序，SWP_NOACTIVATE不激活，NOMOVE／NOSIZE不改位置／尺寸。
文档也提示抬前可能受资格约束，所以这一步本身不是保证成功的绕过机制：必须
在之后重新确认窗口和点击点实际归属，未满足就停止，不向遮挡窗口盲点。

fallback只对当前run实际PID且进程为stellaris.exe、唯一匹配PID可见有效窗口，
标题为Stellaris、非最小化且client1024x768的窗口。先确认cursor可读和前台不是
lockapp，取得真实nonclient标题栏坐标／状态；通过
[GetTitleBarInfo](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-gettitlebarinfo)
与[TITLEBARINFO](https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-titlebarinfo)
及[WM_NCHITTEST](https://learn.microsoft.com/en-us/windows/win32/inputdev/wm-nchittest)的
HTCAPTION验证可点击标题区域，排除不可用、不可见、offscreen、关闭／最小化／
最大化按钮、client viewport等区域。抬前后重获句柄、窗口几何、cursor和点击点
归属；[WindowFromPoint](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-windowfrompoint)
必须返回同一已授权窗口，hit-test必须仍为HTCAPTION。只物理单击该标题点，再
重获窗口并要求真实foreground正是该唯一游戏窗口；失败绝不返回成功。

不使用AttachThreadInput、前台锁设置／注册表、focus权限改写、消息模拟鼠标或
游戏viewport输入。恢复action使用独占文件记录原拒绝、PID／HWND、titlebar／
client几何、cursor、抬前flags、物理单击点与最终foreground／失败；不能覆盖旧
action。没有verified foreground时原调用者不会继续发命令。

## 验收标准

- mock覆盖already-foreground、原成功两路径无回退；错误异常／锁屏／wrong PID／
  非Stellaris进程或标题、多个窗口、失活／最小化／错误尺寸／读cursor失败拒绝。
- 标题栏缺失／不真实、按钮／client hit-test、遮挡点、抬前失败／过程句柄失效
  或几何变化均拒绝，不能先click后补查。
- 成功恢复只抬前且仅物理单击验证标题栏，核新foreground后返回句柄并记录action；
  点击后仍非前台则记录失败并raise。
- 源码差异只在focushelper范围，原文件其它函数／常量保持；定向mock测试通过。
- 本线程不执行实际恢复。root在封口后执行真实恢复、新prefix r7puc重新采全年；
  原r7pu失败分支不覆盖，不声明新年度或游戏功能PASS。

## 追加约束（实现中，先于追加实现）

root随后确认鼠标处于物理屏幕角落，`pyautogui.failSafeCheck()`真实抛出
`FailSafeException`。原`original_focus`若抛该异常，必须原样传播，不能进入恢复。
直接恢复入口、抬前前和物理点击前也必须显式执行相同急停检查；不禁用`FAILSAFE`，
不通过WinAPI或其它输入把鼠标移出角落。离线mock补充以上四个拒绝分支。root已
请求用户自行把鼠标移到屏幕中间，本线程不移动真实鼠标。

## 实施与离线检查结果

本机pywin32没有`win32gui.GetTitleBarInfo`包装，因此新增私有函数以ctypes绑定
原生API，显式设置64位安全的HWND／指针参数与`TITLEBARINFO.cbSize`，没有猜测
标题栏高度。标题栏必须位于真实窗口范围内且完全在client上方，其实际状态不能
不可用、不可见或offscreen。中心点两次验证为HTCAPTION；抬前之后必须仍属同一
WindowFromPoint与GA_ROOT。`WM_NCHITTEST`只向已验证的目标HWND发送，使用
[SendMessageTimeoutW](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-sendmessagetimeoutw)
及SMTO_ABORTIFHUNG／SMTO_ERRORONEXIT、2000毫秒超时；失败不视为caption。
这些消息仅查询位置，不模拟鼠标输入。

原`already-foreground`和`original_focus`成功路径保持。仅原调用抛出
`pywintypes.error`且`funcname`精确为SetForegroundWindow时执行恢复。新action
使用UUID文件名与独占`x`创建；失败也记录阶段、原错误、已取得的部分窗口状态和
失败原因。抬前使用HWND_TOP与NOMOVE／NOSIZE／NOACTIVATE（flags=19），随后
重新验证窗口和几何；只物理单击已验证的nonclient点，实际foreground核验成功
后才返回。系统窗口状态可在两次调用之间变化，代码提供紧邻操作的重复检查，
不宣称多次Win32调用具有系统级原子性。

2026-10-20 01:37（上海时间）离线定向mock：47项通过，运行1.879秒，进程退出码0。
测试不导入真实desktop harness，只提取生产源码的focus函数，以伪API和临时
目录执行；ctypes包装测试也替换WinDLL，未查询或操作真实桌面。它覆盖四个
急停分支、原两条成功路径、所有拒绝条件、抬前后的句柄／几何改变、遮挡点、
真实foreground未建立、原生查询超时、64位句柄、独占action碰撞及其它原节点
AST一致性。此结果只证明离线工具逻辑，不构成实机恢复或Mod验收通过。

- 原源码SHA：`cb0d2d2469c47183eac3211148bbf6c9e51b263bc719c35bfb9981e18326ea34`。
- 新源码SHA：`ce9e5de261f477ee23c52979ea5140c6881a414f5728d30af17d1c7f2ff7b2a3`。
- 测试源码SHA：`8d6e99432aee87f98e53235c046e62c3442994e48d1a4a55a6f381b4c705522f`。
- [原始测试输出](evidence/1020-titlebar-focus-recovery/mock-tests-v1.txt)及
  [带源码哈希的运行记录](evidence/1020-titlebar-focus-recovery/mock-tests-v1.json)。
- [逐字节改动范围检查](evidence/1020-titlebar-focus-recovery/source-scope-v1.json)：
  焦点函数块之前624字节、之后19177字节均与原文件完全相同；其它函数与常量
  未改。没有改Mod、其它工具、模型、发布gate、系统设置，也没有执行Git操作。

交还root后，待用户解除角落急停，才按既定范围做真实恢复和新r7puc全年采集。
此前失败r7pu不得改写成成功记录。

## 用户明确授权的鼠标恢复（2026-10-20 01:40，操作前）

用户回复“你自己移动啊”，明确要求 root 自行移开鼠标。该授权覆盖前文要求用户
自行移动的操作限制；生产工具与 47 项测试仍保持急停开启。root 仅执行一次
Windows SetCursorPos 将鼠标从屏幕角落移到物理屏幕中央，记录前后坐标及用户
授权来源，不点击、不关闭 FAILSAFE；随后重新执行 failSafeCheck，通过后才调用
既有焦点恢复、关闭遗留控制台／debug，再以新 r7puc 采集全年。此动作不会改写
原 r7pu 失败或构成任何 Mod 测试通过。

## 真实恢复证据封存范围（复制前）

root已报告实际恢复由原正常焦点路径完成。本次只读封存当前run
`20261019T164112Z`中`r7puc-user-authorized-cursor-reset.action.json`、
`r7puc-recover-console*`、`r7puc-recover-debug*`的原字节到独立子包；建立
逐文件SHA／大小清单与复制后验证。不得复制或改写r7puc经济记录、活动日志、
Mod、工具或原47项mock证据；不执行UI或Git。真实标题栏fallback未触发，不能
据正常路径恢复报告其已通过实机验证。此前r7pu失败保持原状。

## 真实恢复与原字节封存结果

2026-10-20 01:40（上海时间）root执行用户授权的鼠标操作。独立action实际记录
操作前坐标为`[567,569]`，此时已不在角落；屏幕`[2560,1440]`，目标和操作后
均为`[1280,720]`。`FAILSAFE`保持true，随后`failSafeCheck`通过。前文描述的是
操作计划，不能据此把实际操作前坐标改写成角落坐标，也不能称本次移鼠标绕过了
仍在触发的角落急停。

root报告`focus_current_window`返回HWND `98176084`，本次原正常路径成功。
源目录在封存时没有`focus-titlebar-recovery-*.action.json`，所以新增标题栏
fallback在此实际场景中**未执行**；原47项mock覆盖结果不变，其实机结果仍为
未覆盖。root随后关闭遗留console／debug，三张新鲜GPU画面及OCR均绑定PID
`37300`、标题Stellaris、client `1024x768`，采集时间为01:40:10至01:40:26。
最后画面仍为旧场景的2200.05.01暂停状态，普通通知弹窗可见；画面只证明恢复后
可继续按新方案操作，不能视作新r7puc年度经济或任何Mod功能通过。

[独立封存索引](evidence/1020-titlebar-focus-recovery/native-normal-path-v1/archive-index-v1.json)
含11份原字节payload，共644429字节，其中3张GPU图与3份OCR的图片SHA全部
闭合。每份复制前后源SHA稳定、目标与源逐字节相同；
[完整性核验](evidence/1020-titlebar-focus-recovery/native-normal-path-v1/archive-verification-v1.json)
的PASS仅指封存完整性。索引SHA为
`202c3243ff1a588bd2a4273a7dea4a6bbeb7bd15cf4d8619c9f2b411cacb3a15`，
核验SHA为`e01b39db433a4c66f4c19c4b3aa4db5230893d69bfb356422d7b4e9f1a4898fa`。

封存时再次核对原mock记录绑定的工具、测试及旧工具源码，其字节均未改变；未
重跑或改写原47项结果。本次没有触碰r7puc经济文件、活动日志、UI、Git或原r7pu
失败记录；新r7puc全年由root独立执行，结果须另行验收。
