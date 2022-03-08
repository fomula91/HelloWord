# 항해99 Chapter 1 - 팀별 미니 프로젝트(1조)

## S.A(Starting Assignment)

- [https://choewy.tistory.com/125](https://choewy.tistory.com/125)

## 진행 상황

### 1일차 : 2022.03.07(월)

- 기능 정의, 템플릿 구성, DB 스키마 설계, SA 작성
- 각자 테스트 버전 구현(역할 분담, 추가 의견 반영 목적)
  - FE : 김형중, 하상우
  - BE : 최원영, 홍승민

### 2일차 : 2022.03.08(화)

- DB 스키마, API 설계, 기능 설계 완료
- 기능별 담당자 지정 및 개발 시작
- Repository 초기화

## 의존성 패키지

- flask
- pymongo
- PyJWT

## 이슈 사항

### pymongo 설치 후 bson과의 충돌 이슈 발생

파이썬 3.7 이상인 경우 bson 기능을 지원하는데, 이때 pymongo의 bson과 충돌 발생

(따라서, bson과 pymongo를 지운 후 다시 pymongo를 설치하여 해결)

```
$ pip uninstall bson
$ pip uninstall pymongo
$ pip install pymongo
```