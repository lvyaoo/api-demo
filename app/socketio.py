from flask_socketio import Namespace, SocketIO


socketio = SocketIO()


class DefaultNamespace(Namespace):
    """SocketIO默认空间"""
    def on_connect(self) -> None:
        """connect事件"""
        pass

    def on_disconnect(self) -> None:
        """disconnect事件"""
        pass
