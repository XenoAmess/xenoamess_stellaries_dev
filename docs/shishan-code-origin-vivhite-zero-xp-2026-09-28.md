# 白绮零经验复活与重载实机记录（2026-09-28）

## 目标与范围

补齐 `WH-03` 中领袖当前经验为零时的意外死亡、备份、付费复活及存档重载路径。使用正式 Mod、简体中文、Stellaris 4.5.1 单 Mod 隔离用户目录 `final_offline_20260928_0351`，Steam 离线。测试在同一暂停日 `2203.06.03` 进行；控制台仅触发原版 `kill_leader` 以调用正式死亡回调，没有绕过 Mod 的备份或复活事件。

## 过程与证据

1. 基线领袖 `16777287` 为 5 级传奇行政官，带白绮肖像、标记和专属特质；存档领袖块没有 `experience` 字段，即当前经验为零。国家拥有该领袖及白绮基础全国修正。
2. 在玩家国家作用域执行 `every_owned_leader={limit={has_leader_flag=shishan_code_vivhite} kill_leader={show_notification=no}}`。出现[备份事件](../assets/shishan-code-origin/evidence/vivhite-zero-xp-backup-event.jpg)。[待复活存档](../assets/shishan-code-origin/evidence/vivhite-zero-xp-pending.sav) SHA-256 为 `eb2f8d0b504b49a1c94db64c2d5cb90e068d9d3bd14c3c8128b7f44e0e9a1b26`；国家变量 `shishan_code_vivhite_backup_xp=0`，待复活标记存在，基础全国修正已移除，白绮不在玩家 `owned_leaders` 中。
3. 从游戏菜单重载待复活存档，首都“重启白绮”决议仍能打开[付费事件](../assets/shishan-code-origin/evidence/vivhite-zero-xp-reboot-after-reload.jpg)。选择复活后保存[已复活存档](../assets/shishan-code-origin/evidence/vivhite-zero-xp-revived.sav)，SHA-256 为 `8f2cdebaaf24f2af61120538b1d535b4cb009a027d13004f48be09faa8d6af4c`。
4. 两份存档同日库存精确对照：能量币 `2185.77415→1685.77415`，合金 `1124.15471→924.15471`；分别只扣 `500` 和 `200`。复活后待复活标记及备份变量消失，白绮基础全国修正恢复。玩家 `owned_leaders` 仅有新白绮 `167772174`；旧领袖 `16777287` 只留在死亡记录。新白绮仍是 5 级传奇行政官，保留白绮肖像、标记与专属特质，仍无 `experience` 字段，代表零经验保持。
5. 再从游戏菜单重载复活存档，首都决议变为“与白绮交谈”，不再显示重启入口。点击后出现[正常对话与人物图](../assets/shishan-code-origin/evidence/vivhite-zero-xp-dialogue-after-reload.jpg)。

## 结论与边界

零经验领袖的死亡备份、跨重载付费复活、精确扣费、等级与已有特质保留、唯一性以及复活后交谈路径均通过。本轮没有单独构造 `experience_gain_mult=0` 且**当前经验非零**的组合；先前 `1.26` 倍经验获取修正、当前经验 `317.52` 的路径已经实测通过，见[实机发现](shishan-code-origin-runtime-findings-2026-09-27.md)。
