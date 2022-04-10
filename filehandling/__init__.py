# -*- coding: utf-8 -*-

import os
import json

from deepfolder import create


def readFile(path):
    """
      특정 경로에 있는 파일을 읽어 반환합니다.
      - path : string
    """
    f = open(path, 'r')
    data = f.read()
    f.close()
    return data


def create_tmp_path(path, tmp_path, filename):
    """
      임시 경로를 생성합니다. 통일성을 위해 별도함수로 분리했습니다.
      - path : string
      - tmp_path : string
      - filename : string
    """
    return tmp_path + "/" + path.replace("/", "_") + "_" + filename


def create_real_path(path, root_path, filename):
    """
      실제 파일 경로를 생성합니다. 통일성을 위해 별도함수로 분리했습니다.
      - path : string
      - tmp_path : string
      - filename : string
    """
    return root_path + "/" + path + "/" + filename


class File:
    def __init__(self, path, filename, root_path="./data", tmp_path="./tmp"):
        """
          파일을 삭제하거나 수정하거나 생성하거나 할 수 있도록 도와주는 도구입니다.
          - path : string, 단, 폴더 명으로 끝나야함
          - filename : string
          - root_path : string (optional), 단, 폴더 명으로 끝나야함
          - tmp_path : string (optional), 단, 폴더 명으로 끝나야함
        """
        if not create(root_path):
            raise Exception('폴더를 생성할 수 있는 구조가 아닙니다. (root) > ' + root_path)
        if not create(tmp_path):
            raise Exception('폴더를 생성할 수 있는 구조가 아닙니다. (tmp) > ' + tmp_path)
        if not create(root_path + "/" + path):
            raise Exception('폴더를 생성할 수 있는 구조가 아닙니다. (path) > ' +
                            root_path + "/" + path)

        self.__real_path = create_real_path(path, root_path, filename)
        self.__tmp_path = create_tmp_path(path, tmp_path, filename)
        self.__path = {
            'target': path,
            'tmp': tmp_path,
            'root': root_path,
        }

    def __remove(self, path):
        """
            주어진 파일을 제거합니다.
        """
        try:
            alive = os.path.exists(path)
            if alive:
                os.remove(path)
            return True
        except:
            return False

    def __write(self, data, mode, path):
        """
          파일에 문자열인 data를 mode에 따라 추가하거나 덮어쓰기하거나 생성합니다.
          - data : string
          - mode : 'a' 혹은 'w'
          - path : string 
        """
        if mode not in ['w', 'a']:
            return False

        alive_file = os.path.exists(path)

        if mode == "w" and alive_file:
            self.__remove(path)
        if mode == "a" and not alive_file:
            mode = "w"

        f = open(path, mode)
        f.write(data)
        f.close()
        return True

    def __get_file_info(self, mode):
        """
          mode에 따라 path, mode를 반환합니다.
          - mode : 'a' 혹은 'w'
        """
        alive_tmp_file = os.path.exists(self.__tmp_path)
        if alive_tmp_file is True and mode == "a":
            return self.__tmp_path, mode
        if mode == "w":
            if alive_tmp_file is True:
                self.clear()
            return self.__tmp_path, mode

        alive_real_file = os.path.exists(self.__real_path)

        if alive_real_file is True:
            self.__write(self.read(), 'w', self.__tmp_path)
        return self.__tmp_path, mode

    def read(self):
        """
          파일을 string 데이터로 가져옵니다.
          우선 임시폴더에 있는지 확인하고 없으면 real 폴더를 확인하고, 없으면 새로 생성합니다.
          path : string (optional)
        """
        # 임시 폴더에 파일이 존재를 확인하고 있으면 반환합니다.
        if os.path.isfile(self.__tmp_path):
            return readFile(self.__tmp_path)
        # real 폴더에 파일이 존재를 확인하고 있으면 반환합니다.
        if os.path.isfile(self.__real_path):
            return readFile(self.__real_path)

        # 파일이 존재하지 않으면 임시 폴더에 파일을 생성하고 재귀처리 합니다.
        f = open(self.__tmp_path, 'w')
        f.write("")
        f.close()

        return self.read()

    def read_json(self):
        """
          파일을 json 데이터로 가져옵니다. 단, 데이터가 json 포맷이 아닌 경우 {} 값을 반환합니다.
        """
        data = self.read()
        try:
            return json.loads(data)
        except:
            return {}

    def write(self, data, mode='w'):
        """
          파일에 문자열인 data를 mode에 따라 추가하거나 덮어쓰기하거나 생성합니다.
          - data : string
          - mode : 'a' 혹은 'w' (optional)
        """
        path, m = self.__get_file_info(mode)
        return self.__write(data, m, path)

    def write_json(self, data, mode='w'):
        """
          파일에 dict인 data를 mode에 따라 추가하거나 덮어쓰기하거나 생성합니다.
          - data : string
          - mode : 'a' 혹은 'w' (optional)
        """
        if isinstance(data, dict):
            return self.write(json.dumps(data, indent=2), mode)
        return False

    def overwrite(self, data):
        """
          파일에 문자열인 data를 덮어쓰기하거나 생성합니다.
          - data : string
        """
        return self.write_json(data, 'w')

    def overwrite_json(self, data):
        """
          파일에 dict인 data를 mode에 따라 덮어쓰기하거나 생성합니다.
          - data : string
        """
        return self.write(data, 'w')

    def appendwrite(self, data):
        """
          파일에 문자열인 data를 맨 하단에 추가하거나 생성합니다.
          - data : string
        """
        return self.write(data, 'a')

    def appendwrite_json(self, data):
        """
          파일에 dict인 data를 추가하거나 생성합니다.
          - data : string
        """
        next_data = self.read_json()
        next_data.update(data)
        return self.write_json(next_data, 'w')

    def clear(self):
        """
          임시 파일을 제거합니다.
        """
        if self.__remove(self.__tmp_path) is False:
            return False

    def remove(self):
        """
          파일을 제거합니다. (임시 파일/실제 파일 모두)
        """

        if self.clear() is False:
            return False
        if self.__remove(self.__real_path) is False:
            return False
        return True

    def removewrite_json(self, key):
        """
          파일에 문자열인 data를 key로 사용하고 있는 값을 제거합니다. 
          - key : string
        """
        next_data = self.read_json()
        next_data.pop(key, None)
        return self.write_json(next_data, 'w')

    def save(self):
        """
          임시 폴더에 저장된 파일을 원래 저장되어야할 폴더에 저장합니다.
        """
        if self.__write(self.read(), 'w', self.__real_path) is False:
            return False
        if self.clear() is False:
            return False
        return True

    def rename(self, to_filename):
        """
          파일의 이름을 변경합니다.
          - to_filename : string
        """

        # 이전 파일 정보를 가져옵니다.
        target = self.__path['target']
        root = self.__path['root']
        tmp = self.__path['tmp']

        # 파일을 이동할 경로를 생성합니다.
        next_tmp_path = create_tmp_path(target, tmp, to_filename)
        next_real_path = create_real_path(target, root, to_filename)

        # 같은 파일이면 False를 반환합니다.
        if next_tmp_path == next_real_path:
            return False

        # 이동할 경로에 파일이 존재하는지 확인합니다.
        alive_next_tmp = os.path.exists(next_tmp_path)
        alive_next_real = os.path.exists(next_real_path)

        # 이미 있는 파일이라면 False를 반환합니다.
        if alive_next_tmp or alive_next_real:
            return False

        # 현제 적용된 경로에 파일이 있는지 확인합니다.
        alive_now_tmp = os.path.exists(self.__tmp_path)
        alive_now_real = os.path.exists(self.__real_path)

        # 임시 파일이 생성된 상태라면, 데이터를 꺼내 변경된 경로로 저장합니다.
        if alive_now_tmp:
            tmp = readFile(self.__tmp_path)
            self.__write(tmp, 'w', next_tmp_path)

        # 실제 파일이 생성된 상태라면, 데이터를 꺼내 변경된 경로로 저장합니다.
        if alive_now_real:
            real = readFile(self.__real_path)
            self.__write(real, 'w', next_real_path)

        # 이전 파일을 삭제합니다.
        self.remove()

        # 새로운 파일 정보로 갱신합니다.
        self.__tmp_path = next_tmp_path
        self.__real_path = next_real_path

        return True


if __name__ == "__main__":
    from deepfolder import remove
    # 파일 생성 및 제거
    f = File("/", "test.xml", ".")
    print("처음 파일 열때, append로 write 시도 > " + str(f.appendwrite("test")))
    print("저장 시도 > " + str(f.save()))
    print("내용 > " + f.read())
    try:
        f.remove()
        print("삭제 > 성공")
    except:
        print("삭제 > 실패")
    # 기존 파일 추가
    f = File("/", "test.xml", ".")
    print("파일 생성 시도" + str(f.write("test")))
    print("저장 시도 > " + str(f.save()))
    print("내용 > " + f.read())
    print("파일 추가 시도" + str(f.appendwrite("test2")))
    print("저장 시도" + str(f.save()))
    print("내용 > " + f.read())

    # 기존 파일이름 변경 후 내용 추가하고 삭제
    print("이름 변경 시도" + str(f.rename("test2.xml")))
    print("내용 추가" + str(f.appendwrite("test3")))
    print("내용 > " + f.read())
    print("저장 시도" + str(f.save()))
    print("내용 > " + f.read())
    try:
        f.remove()
        print("삭제 > 성공")
    except:
        print("삭제 > 실패")
    remove("./tmp")
