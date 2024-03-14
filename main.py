import os
import shutil

def install_pre_commit_hook(repo_path):
    # 현재 스크립트와 동일한 디렉토리에 있는 pre-commit.py의 경로
    current_dir = os.path.dirname(os.path.realpath(__file__))
    pre_commit_script_path = os.path.join(current_dir, 'pre-commit.py')
    
    # 목표 Git hooks 디렉토리 경로
    git_hooks_path = os.path.join(repo_path, '.git', 'hooks')
    target_pre_commit_path = os.path.join(git_hooks_path, 'pre-commit')

    # pre-commit.py 파일을 .git/hooks 디렉토리로 복사
    if os.path.isfile(pre_commit_script_path):
        shutil.copy(pre_commit_script_path, target_pre_commit_path)
        print(f"'pre-commit.py'가 '{target_pre_commit_path}'로 복사되었습니다.")
    else:
        print("pre-commit.py 파일을 찾을 수 없습니다. 스크립트가 올바른 위치에 있는지 확인하세요.")
        return

    # 실행 권한 부여
    os.chmod(target_pre_commit_path, 0o775)
    print(f"'pre-commit' 스크립트에 실행 권한이 부여되었습니다.")

if __name__ == '__main__':
    repo_path = input("Git 저장소 경로를 입력하세요: ").strip()
    if os.path.exists(os.path.join(repo_path, '.git')):
        install_pre_commit_hook(repo_path)
    else:
        print("입력하신 경로에 .git 디렉토리가 존재하지 않습니다. 올바른 Git 저장소 경로인지 확인하세요.")
