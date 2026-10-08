# 吞噬之心 0.2.0 首次发布

2026-10-08 16:56:09（北京时间）成功创建并公开上传[新工坊物品3815707212](https://steamcommunity.com/sharedfiles/filedetails/?id=3815707212)。上传版本0.2.0，上传Git源c8aa64ff；未更新只读上游3710613857。正式CHANGELOG和Change Note已在上传前建立，全部五入口保持开放。

完整实机验收仅焦土蜂巢；首发推荐焦土蜂巢；其它路线开放但未完成完整实机验收。首发31项适用合同与最终生产包冒烟通过；EAT-05／08不适用，原始FAIL和共用受控检查边界保留。其它九语言静态校验通过，运行时不在范围内。

17:00远端最终核验通过：Steam DownloadItem原生回调形成独立安装目录，全41生产文件SHA与冻结包一致；公开标题／正文、整段[v0.2.0] Change Note、封面字节、六张图库的顺序／图说／字节全部一致。回执见[上传状态](evidence/publish-state.json)、[独立下载](evidence/workshop-download.json)、[远端核验](evidence/workshop-verification.json)。

失败记录：首次Steamworks初始化在客户端尚未完成连接时返回未登录，尚未创建物品；恢复实际登录后才上传成功。远端第一次Change Note检查因Steam把换行渲染成br而误报，未重新上传成功版本。按先文档后实现规则修正段落解析，10项正反例和实际原始页面精确整段比较通过，再执行完整远端核验；证据见[HTML校验](evidence/publication-0.2.0/change-note-rendering-check.json)。该发布工具修复不改41个生产文件。

17:01Steam实际界面恢复“离线模式”，继续离线测试。发布回执提交推送后创建并推送v0.2.0标签，标签只在远端通过后产生。用户要求发布后继续测试与修复，首发不是总任务结束。

17:04发布回执与HTML校验修复提交e52c5f76已推送main；远端核验通过后创建的注解标签v0.2.0已推送（标签对象8676b6af，指向e52c5f76）。Steam离线、工作区干净后继续下一轮对照。
