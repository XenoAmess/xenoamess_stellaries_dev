# 合成女王肖像 Mod 首次工坊发布计划

日期：2026-09-25。用户授权发布独立的“XenoAmess的合成女王美化”，并要求把实机截图上传为工坊图片资产、把完整 BBCode 说明纳入仓库。本轮首发版本为 `0.1.0`，Stellaris 应用 ID 为 `281990`，必须创建全新 Workshop 物品；上游 `3710613857` 及其他既有物品均为只读。

## 目标与实际范围

- 正式包只替换原版 10 个合成女王肖像键，共用一张 EvoLink 生成、带真实 Alpha 的静态 DDS。事件插画、对话背景、旗帜和图标尚未替换；描述和截图不得暗示已经替换。
- 使用现有简体中文实机验收截图制作工坊 JPEG，原始 PNG 保留在 `evidence/portrait-acceptance-rc2/`。发布副本放在 `workshop/media/`，并作为 Workshop 图片栏的附加预览逐张上传；BBCode 同时引用固定到已推送 Git 提交的 raw 图片 URL。
- 缩略图从已生成的透明人物图确定性合成，保存到 `mod/thumbnail.png`，描述符添加 `picture="thumbnail.png"`。美术主体与肖像定义不改动。
- `workshop/description.bbcode` 是工坊说明唯一真源；`workshop/change-note-v0.1.0.txt` 从同版本 changelog 提炼，以 `[v0.1.0]` 开头。说明必须写明《机械纪元》、Stellaris `4.4.*`、静态肖像和同文件 Mod 潜在冲突，以及当前验收边界。

## 已知验收边界与发布判断

`0.1.0-rc.2` 的 `open_kaishek` P 语言静态校验、透明通道和 R1/R3（人类玩家视角）/R5 简体中文实机检查通过，矩形画布边界已消失。R2 基础 `synth_queen` 缺少独立界面证据；R4 提前触发结局夹具虽然显示新人物，却有肖像选择器和领袖作用域错误，未证明自然结局。因此 **不得宣称整个 Mod 已通过全矩阵验收**。用户本轮明确要求公开发布，发布说明与 changelog 均须披露这些限制，后续继续补测。

## 操作顺序

1. 先完成本计划和验收标准，再修改版本、描述符、changelog 和发布图片。保持 `VERSION=descriptor.mod version=0.1.0`，并检查正式 changelog 包含新增、变更、修复、兼容范围、验收情况和已知限制。
2. `open_kaishek` 先验收生产 P 语言入口；复核 DDS 与源图哈希、描述符、图片尺寸和 JPEG 编码。新增缩略图后只需针对新增内容和发布包复核，既有运行时画面沿用 rc.2 同一 DDS 的证据。
3. 先提交并推送图片与正式包，取得不可变 Git SHA；将该 SHA 写入 BBCode 图片 URL，再提交并推送说明。逐个验证 URL 返回图片、BBCode 不超过 Steamworks 限制，并冻结上传目录的文件树与哈希。
4. 在已登录 Steam 客户端下使用 Steamworks UGC 首次 `CreateItem` 获取**新 ID**，调用 `StartItemUpdate` 设置标题、BBCode、内容目录、主预览图、三张附加预览、标签和公开可见性，再用同版本 Change Note `SubmitItemUpdate`。如首次创建返回需接受法律协议，停止公开步骤，交由用户亲自接受。
5. 读取匿名工坊详情核对 ID、应用、标题、说明、可见性、图片数量、更新时间与变更说明；从空缓存下载公开包，逐文件对比上传目录哈希，并确认没有更新上游物品。记录回执、URL、哈希及未验收项到 `docs` 与 `evidence`，提交并推送；最后推送唯一产品标签 `synthetic-queen-v0.1.0`。

## 完成标准

- 新公开物品 ID 存在且不是 `3710613857`；远端标题、BBCode、正式版本、内容文件和 Change Note 与仓库相符。
- 主缩略图和三张简体中文实机截图均在工坊图片栏可见，BBCode 中的固定 Git 图片链接均可读取。
- 所有上传包文件来自已提交的 `mod/`；不包含参考图、生成请求、测试日志、其他 Mod 或上游 `remote_file_id`。
- 发布记录诚实保留 R2/R4 未完成状态；本次不做灰风 Mod 并用测试。

## 上传工具设计与验收

`tools/publish_workshop.py` 默认只读预检，`--publish` 才执行一次新建与上传。预检强制版本、标题、文件白名单、已验收 DDS 哈希、BBCode 图片数量、图片体积以及 Git 干净工作树。工具只接受 Steamworks 为当前登录账号创建的新 ID，创建后立刻以原子写入保存回执；已有回执时拒绝再次创建，以防重试产生重复物品。法律协议标志为真时停止提交。上传返回结果、ID 与协议标志均须检查；随后仍以匿名远端读取和空缓存下载作为最终验收。静态验收先运行 Python 语法检查与只读预检；公开上传仅在这些检查通过后执行。

## 发布前实测记录

- 正式版肖像 DDS 的 SHA-256 仍为 `5225d045670268844f539ef1ec21eec094149efcaf796af1667d82145a4732d4`，与 rc.2 实机图一致。
- `open_kaishek` 的 `validate --profile stellaris-4.4.6` 对肖像定义返回 `VALIDATED`、语法和语义诊断均为 0；`parse` 对正式描述符返回 `PARSED`、0 diagnostics、`roundTrip=true`。
- 缩略图为 351×313 PNG、134,780 字节；三张 2560×1440 JPEG 分别为 317,805、322,378、320,956 字节。均来自已归档的 rc.2 简体中文实机 PNG，没有裁切或重绘。
- 图片及正式包已由提交 `68d672cbfa9a615e87e6183c8059be001f12b6c7` 推送到 `origin/main`。BBCode 为 2,437 UTF-8 字节，三张固定提交 raw URL 均返回 `200 image/jpeg`，内容 SHA-256 与仓库 JPEG 逐字节一致。

## 首次 Steamworks 连接检查

第一次 `--publish` 在 `CreateItem` 阶段返回无效句柄，没有生成物品 ID，也没有 `publish-state.json`。进一步读取 Steam 客户端日志发现该客户端自 2026-09-23 02:10 起处于 `Logged Off`；本机 Steam API 的 `BLoggedOn` 同样为 false。上传工具此前选用的过新 `SteamUtils011` 还导致 `GetAppID` 读数异常：安装的 DLL 内嵌 `SteamUtils009` 和 `SteamUser020`，实测 `SteamUtils009` 返回正确应用 ID `281990`。已将绑定改为 `SteamUtils009`、`SteamUser020` 和 Valve SDK 提供的 UGC v017，并在创建前显式检查登录和应用 ID。此阶段没有对上游或任何工坊物品提交更新。

2026-09-25 重启 Steam 客户端后，连接日志仍显示 `Logged Off`；本地账号设置 `RememberPassword=1`、`WantsOfflineMode=1`。根据 [Steam 官方离线模式说明](https://help.steampowered.com/en/faqs/view/0E18-319B-B2C8)，离线模式不提供需要网络连接的工坊功能。下一步只将该账号的离线模式意图改为在线，再正常重启客户端；原配置在 Steam 目录留备份，不进入仓库。

已正常关闭客户端、备份 `loginusers.vdf` 并只将该账号的 `WantsOfflineMode` 从 `1` 改为 `0`；重启后连接日志出现 `Logged On` 和登录响应 `OK`。Steam API 读回 `AppID=281990`、`BLoggedOn=true`。上传工具现在会在创建物品前验证这两个条件；待发布与远端核验完成后恢复原离线偏好。

在线后第二次创建仍返回无效句柄。调查游戏自带 `steam_api64.dll` 的导出跳转表：`CreateItem` 跳至虚表第 40 槽，`ReleaseQueryUGCRequest` 跳至第 18 槽，而当前公开 UGC v017 头文件对应第 41、19 槽，说明它不匹配此 DLL。切换只读探针到 `STEAMUGC_INTERFACE_VERSION016` 后，`GetNumSubscribedItems=21` 与客户端工坊日志一致，UGC 查询句柄可正常释放。根因是绑定了过新的 UGC 接口版本；工具须改用 v016 后再重试创建。两次失败均未生成物品 ID 或上传状态文件。
