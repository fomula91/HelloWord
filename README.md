# 항해99 Chapter 1 - 팀별 미니 프로젝트(1조)

## Tags

- [`S.A(Start Assignment)`](https://choewy.tistory.com/125)
- [`v1.0.0-test`](https://github.com/fomula91/HelloWord/tree/v1.0.0-test)
- [`v1.0.2-first-merge`](https://github.com/fomula91/HelloWord/tree/v1.0.2-first-merge)
- [`v1.0.3-complete`](https://github.com/fomula91/HelloWord/tree/v1.0.3-complete)
- [`v1.0.4-refectory`](https://github.com/fomula91/HelloWord/tree/v1.0.4-refectory)

## Plan

- 1일차 - 03.07(월) : 프로젝트 주제 선정, 템플릿 구성, 기초 설계
- 2일차 - 03.08(화) : 설계 확정, 역할 분담, 템플릿 및 기능 구현
- 3일차 - 03.09(수) : 전체 기능/디자인 구현 및 검토
- 4일차 - 03.10(목) : 서버 배포 후 코드 리뷰 및 리팩토링

## Role
         
### 최원영

- 로직 및 API 설계
- 단어 조회 페이지 구현
- 전체 기능 검토 및 통합
- Repo 관리

### 하상우

- 회원가입, 로그인 페이지 구현
- 회원 인증 API 구현

### 홍승민

- 단어 퀴즈 페이지 구현
- 단어 수정 및 삭제 API 구현
- 서버 배포 및 관리

### 김형중

- 단어 조회 API 구현
- 단어 등록 API 구현

## Log

### Day #1 - 2022.03.07

- 주제 선정 및 기능 정의
- 템플릿 구성, DB 스키마 및 API 설계
- S.A(Start Assignment) 작성
- 테스트 버전 구현 (템플릿 : 김형중, 하상우 / API : 최원영, 홍승민)
- 점검 및 코드 리뷰 진행

### Day #2 - 2022.03.08

- 세부 내용 설계 및 로직 확정
- 역할 분담
- JWT 사용자 인증, 인가 기능 구현
- 전체 템플릿 구현 완료 

### Day #3 - 2022.03.09

- 중간 점검 및 코드 리뷰 진행
- 전체 기능 구현 완료
- 코드 병합

## Note

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

### Issues #1

pymongo 설치 후 bson과의 충돌 이슈 발생(파이썬 3.7 이상인 경우 bson 기능을 지원하는데, 이때 pymongo의 bson과 충돌 발생)

> bson과 pymongo를 지운 후 다시 pymongo를 설치하여 해결

```
$ pip uninstall bson
$ pip uninstall pymongo
$ pip install pymongo
```