# 0.4.0正式发布执行记录

最终状态（2026-10-20）：18组约定专项PASS_SCOPED，正式0.4.0已成功发布到
[自有工坊3815707212](https://steamcommunity.com/sharedfiles/filedetails/?id=3815707212)。
独立59文件、公开正文、Change Note、封面、六图库和四inline全部远端核验通过，
v0.4.0已推送；Steam实时及持久离线状态已恢复，本地exclude原字节恢复。
以下保留设计、冻结检查点、失败尝试与实际收尾的时间顺序。

执行期间实机发现原生通知漏翻译，实际采用rc.8修正：在RC7基础上只追加十语言
同一描述键与版本元数据。所有P脚本/组件/资源和原译文原字节保持。原冻结
publish_1019.py不改；通过publish_1020_localization.py执行严格来源补丁合同及
独立RC8中文通知/结算/重复/重载证明后再调用原门禁。下述最初“仅版本元数据”
范围由这一具体、有源码证书和负例测试的补充取代，不能作任意变更的豁免。

用户已要求验收完成后自行发布Steam更新。本记录约束最后执行阶段：

1. 完成RC7剩余四项与三个候选进程的完整停机日志审查；旧版EEP05仅作独立人口
   基线，不混入候选run。最终逐项审查后另建final-result，原PENDING历史保留。
2. 只把VERSION与descriptor的Mod版本改成正式0.4.0；其余被测59文件保持原字节。
   正式六类CHANGELOG在上传前建立；Change Note读取同一正式条目。
   冻结已有六槽媒体候选并更新玩家说明；旧四条inline图片保持。
3. 正式包再次执行open_kaishek、record-static和严格发布门禁。冻结输入提交推送
   后才上线Steam。目标仅3815707212，上游3710613857始终只读。
4. 上传后独立下载并逐文件验证，再验证公开说明、Change Note、六槽图库及四张
   inline原字节。提交推送真实回执后才创建、推送v0.4.0标签，最后恢复Steam离线。

工作树另有用户未提交的`evidence/1019-rc7-purifier-economy-worker-ui-v1/`目录。
它不加入本次提交，也不修改其内容。若全仓库clean门禁被该唯一无关目录阻挡，
可在`.git/info/exclude`临时加入其精确路径，让门禁检查本次任务全部已提交输入；
记录原文件字节，发布后原字节恢复，绝不使用广泛忽略或删除用户文件。

验收边界继续保留单人postload布局校正、旧mobile-starbase缓存、多人数值未实机、
v2固定微小伤害预算及原strict FAIL；非中文九语言只称静态校验通过。灭国后的
原版nomads.94告警已有原生war清理与源码支持，但内部FROM派发根因仍有限定，
在已知限制中明确。测试不推广为全政体、全部DLC或完整自然战役验收。

本页初建时仍未发布。各实际门禁、上传、远端验证、提交和标签结果随后追加。

## 正式冻结检查点

2026-10-20已完成18组限定共同审查及实际0.3.1同EEP05人口5300对照；final-result
为PASS_SCOPED、components IMPLEMENTED，138 true及合同要求保留的1 false。
独立RC8通知/结算/重复/重载与源码差异合同通过；原始FAIL和57份RC7停机日志保留。
正式VERSION/descriptor现为0.4.0，正式六类CHANGELOG已先建立。新工具对正式包
36/36 P、12DDS、132键×10静态通过，record-static完成；prepare为PASS_SCOPED，
59生产文件、四个公开inline原字节均匹配，封面加六图库原位冻结，历史/压力标题保留。
原publish_1019.py及独立检查器仍原字节；实际使用窄适配器调用原门禁。
远端v0.4.0标签查询当前为空；此处尚未上传，后续仍需实际远端验证后再打标签。

## 实际上传与公开页面限流

冻结提交`6c2b185a3`已推送后，窄适配器的正式preflight通过，Steam提交返回
`UPLOADED`，版本0.4.0、目标3815707212、submit_result=1、无需法律协议确认。
此次成功提交不得重复上传同一版本。独立Workshop下载完成，59个生产文件逐字节一致。
首轮公开changelog请求返回HTTP429；冷却后第二轮core-verification实际通过：
公开元数据、正式Change Note、封面、59个下载文件和六槽图库均准确。
后续简体中文公开正文HTML请求仍返回HTTP429，故此时整体远端校验尚未完成，不能打标签。

继续只读校验并遵守冷却；必要时仅为urllib设置与既有changelog请求相同的浏览器
User-Agent，再运行原verify流程。工具源码、比较条件、图片字节和发布输入均不变；
不得用缓存或手造回执代替实际公开页面响应。验收要求仍为原verify全部通过。

浏览器User-Agent单独重试仍429，响应无Retry-After。冷却后可尝试同一官方页面
等价的query参数顺序（同id、同l=schinese），仅改变HTTP传输地址的参数排序；
保留实际请求/响应URL、状态、正文hash及原验证入口，所有内容比较继续由原工具执行。

等价query顺序仍429；实际Steam客户端已成功打开同一更新后的工坊页面。
本机urllib默认经127.0.0.1代理，继续调查直连等传输差异，仅调整本次只读请求的
opener，不修改用户系统代理设置，不读取或公开登录凭据，不改变原验收比较条件。

直连超时；同一官方页面移除l参数，改用公开的`Steam_Language=schinese`语言偏好
cookie与`Accept-Language: zh-CN`后实际返回HTTP200（80998字节）。这不使用登录
凭据。接下来仅将原verify的这一条HTML请求转为同id的上述官方URL与中文偏好，
其余网络请求及全部原校验保持；保留实际HTTP响应状态/URL和最终正文hash。

全流程重试曾在封面CDN读流时发生ConnectionResetError，另一次在changelog的
l=english请求429，均未写整体PASS。对changelog同样只用其原语言的公开偏好cookie
替代l参数；同目标、同版本Change Note仍须原exact_change_note实际校验通过。

## 远端完整核验通过

实际重新执行原verify全流程成功：`PASS`，59个生产文件、公开元数据、正式
Change Note、封面及六槽图库完全一致，公开HTML中四张inline图片均实际显示且
下载原字节一致。`publication-0.4.0/workshop-verification.json`为正式成功回执；
`public-page.json`记录正文hash与四张实际渲染图片URL；`public-page-transport-v1.json`
记录两条官方HTML请求实际HTTP200的URL与公开语言偏好。没有使用登录凭据或缓存
代替响应，原发布工具源码与所有内容比较条件未改。

此前HTTP429、CDN读流重置、直连超时均属已保留的失败尝试，不是最终状态。
上传仅成功执行一次，未重复提交0.4.0。接下来先提交推送这些回执，再运行tag-check、
创建并推送正式v0.4.0标签，最后恢复Steam离线及本地exclude原字节。

## 标签与离线收尾

核验回执提交`f6e7968280b72b7cd744b9fe7304684bca4516e3`已推送，原tag-check
实际返回READY_TO_TAG；随后创建、推送v0.4.0，远端peeled提交与上述核验提交一致。
Steam菜单多次点击“进入离线模式”未生效，SDK仍BLoggedOn=true、持久偏好仍0，
因此尚不宣称已恢复。仓库10月15日建造UI调查已有同类菜单迟滞、正常重启后恢复的
实际经验。先核无游戏运行，关闭本任务启动的Paradox launcher，再正常关闭并重启
Steam客户端后重试菜单；不强杀客户端，不修改账号配置冒充实时离线。

首次正常重启完成，但菜单尝试后UI一度显示“离线模式”而新鲜SDK及持久配置仍为
在线/0；保留不一致，不能凭UI判通过。本机steamui.dll包含`-offlinemode`启动参数，
接下来正常关闭客户端后用该参数启动，逐项验证实时BLoggedOn=false和持久偏好1。
不修改快捷方式、系统代理、登录数据或客户端源码，不启用远程调试。

上述启动参数也未使持久偏好变1。修订最后一条诊断边界：允许仅本次启动临时
localhost CEF调试接口，以调用本机sp.js中菜单实际使用的
`SteamClient.User.GoOffline()`。只查询该函数是否存在并执行这一次模式切换，
不读取Auth、令牌或其它账号数据。完成后正常关闭该调试实例、以普通参数重新启动，
必须确认本地调试端口关闭及最终实时离线/持久偏好均通过；不改启动快捷方式。

该临时调试启动在执行前被自动审批拒绝，理由仅为`blocked by policy`，所以未执行，
未启用调试端口、未调用该接口。放弃此诊断方案；以普通参数恢复Steam，通过标准
Windows UI Automation/普通鼠标键盘继续操作原客户端，不申请绕过该拒绝。

## 最终完成与恢复结果

最终使用标准Win32鼠标消息，按实际WindowFromPoint命中的Chromium子窗口及
ScreenToClient坐标，操作原Steam菜单“进入离线模式”成功。实际子窗口坐标为
菜单按钮(35,13)、菜单项(64,82)，没有调用调试接口，没有改Steam账号数据。
先前普通物理点击未可靠触发操作；不能仅凭发送成功或“离线模式”UI文本判通过。
本次不把这一现象归因成已证实的Steam缺陷。

2026-10-20T00:17:41Z新鲜SDK成功初始化且BLoggedOn=false；持久配置的已清理
WantsOfflineMode值为["1"]；localhost:8080不可连接。全过程客户端正常退出/启动，
没有强杀，游戏在本阶段始终未运行；本任务启动的Paradox Launcher已正常关闭。
只保存已清理状态JSON，包含桌面/账号信息的截图留在仓库外，不提交。

正式标签v0.4.0远端对象为`02de5a51da075fb4e03047867d72255dbe1fa209`，
peeled提交为`f6e7968280b72b7cd744b9fe7304684bca4516e3`，与先推送的完整核验
回执提交一致。原tag-check结果READY_TO_TAG、验证报告SHA及远端refs已归档。

`.git/info/exclude`恢复后SHA256为
`6671fe83b7a07c8932ee89164d1f2793b2318058eb8b98dc5c06ee0a5a3b0ec1`，
与保存的原文件完全一致。恢复前核对临时版本SHA，避免覆盖并发用户修改。
唯一原用户未跟踪目录重新出现在git status中，其内容未被本任务修改、删除或提交。
项目README及两级知识库入口已同步实际0.4.0发布事实；原交接和历史PENDING保留。

正式回执均位于`docs/evidence/publication-0.4.0/`：

- `workshop-verification.json`、`public-page.json`及`public-page-transport-v1.json`：完整远端核验。
- `release-tag-v1.json`：原打标门禁与远端标签核对。
- `steam-offline-restoration-v1.json`：实时离线、持久偏好及调试端口关闭。
- `local-exclude-restoration-v1.json`：本地忽略文件原字节恢复。

open_kaishek修复提交d2a2627e3023310d96f1a2d1e63478f6a6ee7a57与其upstream一致，
工具仓库工作树干净。没有新增Paradox共通语法结论，因此本次无需改CK3知识库。
