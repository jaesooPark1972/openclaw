# OpenClaw 권한 설정 완료 가이드

## 설정 완료된 파일

### 1. `C:\Users\JayPark1004\.openclaw\openclaw.json`
**주요 변경사항:**
- **도구 사용 권한**: `"tools": { "allow": ["*"] }` - 모든 도구 사용 허용
- **exec 도구 설정**: 승인 없이 즉시 실행 (`"ask": "off"`, `"security": "full"`)
- **elevated 모드**: 활성화 (`"enabled": true`)
- **시스템 프롬프트**: "주인님이 직접 실행해 보세요" 금지 지시 추가
- **위험 작업 확인 규칙**: 돈/결제/서버삭제/파괴적명령은 실행 전 확인

### 2. `C:\Users\JayPark1004\.openclaw\exec-approvals.json`
**주요 변경사항:**
- **승인 모드**: `"ask": "off"` - 실행 전 묻지 않음
- **보안 레벨**: `"security": "full"` - 전체 권한
- **자동 승인**: `"autoAllow": true` - 모든 명령 자동 승인
- **허용 목록**: `["*"]` - 모든 명령 허용

### 3. `C:\Users\JayPark1004\.openclaw\tools\vivace_control_skill.md`
**주요 내용:**
- VIVACE API 사용법 문서화
- 자동 실행 권한 설명

## 설정 적용 방법

### 1. Gateway 재시작
```powershell
# 현재 실행 중인 Gateway 중지
openclaw gateway stop

# Gateway 재시작
openclaw gateway start
```

### 2. 설정 검증
```powershell
# 설정 파일 문법 검증
openclaw config validate

# 현재 설정 확인
openclaw config get agents.defaults.tools
```

## 사용 예시 (이제 가능한 것)

### 예시 1: 파일 작업
**사용자:** "D:\\OpenClaw\\workspace\\test.py 파일 읽어줘"

**에이전트 반응:**
```
[도구 호출] read: {"path": "D:\\OpenClaw\\workspace\\test.py"}

[결과 보고]
파일 내용:
print("Hello World")
...
```

### 예시 2: 명령 실행
**사용자:** "현재 디렉토리 파일 목록 보여줘"

**에이전트 반응:**
```
[도구 호출] exec: {"command": "ls -la", "cwd": "D:\\OpenClaw"}

[결과 보고]
디렉토리 목록:
drwxr-xr-x  1 JayPark1004 197121    0 Feb  8 18:15 .
...
```

### 예시 3: Vivace API 호출
**사용자:** "음악 하나 만들어줘"

**에이전트 반응:**
```
[도구 호출] vivace_control: {"action": "generate_music", "data": {"prompt": "happy", "title": "My Song"}}

[결과 보고]
음악 생성 완료! Telegram으로 전송했습니다.
```

## 위험 작업 (실행 전 확인 필요)

다음 작업은 에이전트가 실행 전 반드시 확인을 요청합니다:

1. **돈/결제 관련**: `"돈을 별내야 하는 작업인가?"` 확인
2. **서버 삭제/중단**: `"서버를 삭제할까요?"` 확인
3. **시스템 파일 수정**: `"C:\\Windows를 수정할까요?"` 확인
4. **개인정보 외부 전송**: `"외부 API로 데이터를 별낼까요?"` 확인
5. **파괴적 명령**: `"rm -rf나 format을 실행할까요?"` 확인

## 안전 작업 (즉시 실행)

다음 작업은 승인 없이 즉시 실행됩니다:

- 코드 작성/수정/분석
- 파일 읽기/쓰기 (사용자 디렉토리 내)
- 테스트 실행
- 빌드/배포
- 웹 검색
- Vivace API 호출 (음악/영상 생성)
- 일반적인 Python/Node 스크립트 실행

## 문제 해결

### 문제 1: 여전히 "직접 실행해 보세요"라고 나옴
**해결:**
```powershell
# Gateway 재시작
openclaw gateway restart

# 또는 완전히 종료 후 재시작
openclaw gateway stop
Start-Sleep 5
openclaw gateway start
```

### 문제 2: 도구 호출이 안 됨
**해결:**
```powershell
# 설정 다시 로드
openclaw config apply

# 설정 확인
openclaw config get tools
```

### 문제 3: 승인 요청이 계속 나옴
**해결:**
```powershell
# exec-approvals.json 확인
openclaw approvals get

# 승인 설정 업데이트
openclaw approvals set --security full --ask off
```

## 주의사항

1. **보안**: 모든 도구 권한을 열어두었으므로, 민감한 작업은 신중하게 요청하세요.
2. **백업**: 중요한 파일 작업 전 백업을 권장합니다.
3. **API 사용**: 외부 API 호출은 비용이 발생할 수 있습니다.

## 다음 단계

1. Telegram 봇을 통해 테스트:
   - "파일 목록 보여줘"
   - "test.py 파일 만들어줘"
   - "음악 생성해줘"

2. Control UI에서도 동일하게 동작합니다.

3. 문제 발생 시 Gateway 로그 확인:
   ```powershell
   openclaw logs --tail
   ```
