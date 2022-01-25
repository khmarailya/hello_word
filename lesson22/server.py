"""
# https://developer.mozilla.org/ru/docs/Web/HTTP/Messages
# http://httpbin.org/#/HTTP_Methods
Пример:
    В строке браузера ввести
        http://127.0.0.1:5000
        http://127.0.0.1:5000/?status=404
        http://127.0.0.1:5000/?a=1&status=200&q=1
"""

import os
import re
import socket
from http import HTTPStatus
from typing import Iterator, Optional


class Server:
    HOST = ''
    PORT = 5000

    def __init__(self):
        self.remote_host: Optional[str] = None
        self.remote_port: Optional[int] = None
        self.connection: Optional[socket.socket] = None
        self.http_status: Optional[HTTPStatus] = None

        with open('line.html') as f:
            self.line_tmpl = f.read()

        with open('main.html') as f:
            self.body_tmpl = f.read()

    def format_line_tmpl(self, header, value) -> str:
        return self.line_tmpl.format(header=header, value=value)

    def format_body_tmpl(self, body) -> str:
        return self.body_tmpl.format(body=body)

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(f'starting on {self.HOST}:{self.PORT}, pid: {os.getpid()}')
            s.bind((self.HOST, self.PORT))
            s.listen(1)
            print(s)
            while True:
                print('waiting for a connection')
                self.connection, remote_address = s.accept()
                self.remote_host, self.remote_port = remote_address
                self.serve()

    def serve(self):
        with self.connection:
            try:
                print(self.connection)
                print(f'connection from {self.remote_host, self.remote_port}')

                data = self.connection.recv(4096)
                if not data:
                    print(f'no data from {self.remote_host, self.remote_port}')
                    return

                self.get_and_reply(data)
            except Exception as e:
                print(f'error: {e}')

    def parse(self, s: str) -> Iterator[str]:
        lines = (sss for sss in (ss.strip() for ss in s.split('\r\n')) if sss)
        r_type, r_line, r_version = next(lines).split(' ')
        yield self.format_line_tmpl('Request Method', r_type)
        yield self.format_line_tmpl('Request Source', (self.remote_host, self.remote_port))
        self.http_status = self.parse_status(r_line)
        yield self.format_line_tmpl('Request Status', f'{self.http_status.value} {self.http_status.name}')
        for line in lines:
            header_name, header_value = line.split(': ')
            yield self.format_line_tmpl(header_name, header_value)

    @classmethod
    def parse_status(cls, s: str) -> HTTPStatus:
        res = re.search('[?&]status=', s)
        if res is None:
            return HTTPStatus(200)

        s = s[res.span()[1]:]
        res = re.search('&', s)
        if res is not None:
            s = s[:res.span()[0]]

        try:
            return HTTPStatus(int(s))
        except ValueError:
            return HTTPStatus(200)

    def get_and_reply(self, recv_bytes: bytes):
        print('sending data back to the client')
        text = recv_bytes.decode('utf-8')
        print(f'Message received\n"{text}"')

        text = '\r\n'.join(self.parse(text))
        resp = '\r\n'.join([
            f'HTTP/1.1 {self.http_status.value} {self.http_status.name}',
            'Content-Type: text/html; charset=UTF-8',
            '\r\n',
            self.format_body_tmpl(text)
        ])
        sent_bytes = self.connection.send(resp.encode('utf-8'))
        print(f'{sent_bytes} bytes sent\n\n')


if __name__ == '__main__':
    Server().run()
