# 항해99 Chapter 1 - 팀별 미니 프로젝트(1조)

## S.A(Starting Assignment)

- [https://choewy.tistory.com/125](https://choewy.tistory.com/125)

## 의존성 패키지

- flask
- pymongo
- PyJWT

## 이슈 사항

- pymongo 설치 후 bson 사용 시 에러 발생

> 파이썬 3.7 이상인 경우 bson 기능을 지원하는데, 이때 pymongo의 bson과 충돌 발생
> 따라서, bson과 pymongo를 지운 후 다시 pymongo를 설치하여 해결

```
$ pip uninstall bson
$ pip uninstall pymongo
$ pip install pymongo
```
