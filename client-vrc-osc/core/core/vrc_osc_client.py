from pythonosc import udp_client

class VrcOscClient():
    def __init__(self, path: str) -> None:
        """Initialize client

        VRCのクライアントに接続するための準備
        https://docs.vrchat.com/v2022.1.1/docs/osc-overview

        :param path: target_path
        """
        self._client = udp_client.SimpleUDPClient('127.0.0.1', 9000)
        self._path = '/avatar/parameters/' + path

    def send_message(self, value) -> None:
        self._client.send_message(self._path, value)
