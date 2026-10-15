# main.py
import os
import webview

# ============================================================
# 版本号 —— 全项目唯一来源
#   改这里，窗口标题、主菜单页脚、开始游戏页、关于页、
#   控制台 info / status 的版本显示会全部跟着变，不用去改别的文件。
# ============================================================
APP_NAME    = "赌注 BETA"
APP_VERSION = "1.0"

import backend.state as _state        # noqa: E402  必须在 import api 之前
_state.APP_NAME    = APP_NAME
_state.APP_VERSION = APP_VERSION

from backend.api import API           # noqa: E402


def main():
    api = API()

    # pywebview 支持相对路径，会相对脚本所在目录解析
    html_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "ui", "index.html"
    )

    window = webview.create_window(
        title=f"🎲 {APP_NAME} · v{APP_VERSION}",
        url=html_path,
        js_api=api,
        width=1000,
        height=720,
        background_color="#0a0a0f",
        text_select=False,
        resizable=False,   # 想响应式就把这行删掉
    )
    api.attach_window(window)

    # 直接点窗口右上角关闭时，也要落盘
    def on_closing():
        api.save()

    try:
        window.events.closing += on_closing      # pywebview >= 3.x
    except AttributeError:
        pass

    webview.start(debug=False)   # 调试时改 True 可按 F12 开 DevTools


if __name__ == "__main__":
    main()
