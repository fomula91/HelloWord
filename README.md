# 항해99 Chapter 1 - 팀별 미니 프로젝트(1조)

## PLAN

- 1일차 - 03.07(월) : 프로젝트 주제 선정, 템플릿 구성, 기초 설계
- 2일차 - 03.08(화) : 설계 확정, 역할 분담, 템플릿 및 기능 구현
- 3일차 - 03.09(수) : 전체 기능/디자인 구현 및 검토
- 4일차 - 03.10(목) : 서버 배포 후 코드 리뷰 및 리팩토링

## LOG

### 1일차 - 03.07(월)

- 기능 정의, 템플릿 구성, DB 스키마 및 API 설계
- S.A(Start Assignment) 작성 ([`S.A`](https://choewy.tistory.com/125))
- 테스트 버전 구현 ([`v1.0.0-test`](https://github.com/fomula91/HelloWord/tree/v1.0.0-test))
  - 템플릿 : 김형중, 하상우
  - API : 최원영, 홍승민
- 점검 및 코드 리뷰 진행

### 2일차 - 03.08(화)

- 세부 내용 설계 및 로직 확정
- 역할 분담

| 이름  | 역할                                                 |
|-----|----------------------------------------------------|
| 최원영 | - 로직 및 API 설계<br>- 단어 조회 페이지 구현<br>- 전체 기능 검토 및 통합 |
| 하상우 | - 회원가입, 로그인 페이지 구현<br>- 회원 인증 API 구현               |
| 홍승민 | - 단어 퀴즈 페이지 구현<br>- 단어 수정 및 삭제 API 구현<br>- 서버 배포   |
| 김형중 | - 단어 조회 API 구현<br>- 단어 등록 API 구현                            |

- JWT 사용자 인증, 인가 기능 구현
- 전체 템플릿 구현 완료
- 1차 코드 통합 ([`v1.0.2-first-merge`](https://github.com/fomula91/HelloWord/tree/v1.0.2-first-merge))
- 중간 점검 및 코드 리뷰 진행 

### 3일차 - 03.09(수)

- (작성 필요)

## NOTE

### Dependencies

- flask
- pymongo
- PyJWT
- configparser
- certifi

### Environment (`config.ini`)

```ini
[DB_CONFIG]
HOST = ${Mongo DB URI}

[FLASK_SECRET_KEY]
KEY = ${Secret Key}
```

### Issues (# 1)

pymongo 설치 후 bson과의 충돌 이슈 발생(파이썬 3.7 이상인 경우 bson 기능을 지원하는데, 이때 pymongo의 bson과 충돌 발생)

> bson과 pymongo를 지운 후 다시 pymongo를 설치하여 해결

```
$ pip uninstall bson
$ pip uninstall pymongo
$ pip install pymongo
```